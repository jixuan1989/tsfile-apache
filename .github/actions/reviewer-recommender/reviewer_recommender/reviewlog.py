# SPDX-License-Identifier: Apache-2.0
"""GitHub-side signals: merged-PR review history, reviewer workload, and
git-author -> GitHub-login identity resolution.

All GitHub access goes through the `gh` CLI (pre-installed on Action runners).

Conventions:
  * every login-keyed dict produced here uses lowercase logins;
  * a PR author's own reviews on their own PR never count. On GitHub a review
    in state COMMENTED is how authors reply inline, so they are replies, not
    reviews;
  * automation accounts never count as reviewers. GitHub classifies the
    account itself (`__typename` / `type` = "Bot"), which is what is used when
    the API says so; the name heuristic in `Config.is_bot` is the fallback.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import time
from collections import defaultdict
from dataclasses import dataclass, field

from .config import Config
from .history import AuthorHistory, ModuleSignal, parse_time
from .modules import ModuleMap

REVIEW_STATES = ("APPROVED", "CHANGES_REQUESTED", "COMMENTED")
NON_HUMAN = ("Bot", "Mannequin")   # account types that are not people

_PR_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: MERGED, first: 50, after: $cursor,
                 orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { endCursor hasNextPage }
      nodes {
        number
        title
        createdAt
        updatedAt
        changedFiles
        author { login __typename }
        files(first: 100) { nodes { path } }
        reviews(first: 100) {
          nodes { author { login __typename } state submittedAt }
        }
      }
    }
  }
}
"""

# `gh` prints "<message> (HTTP 422)" on stderr when the API rejects a request.
_STATUS_RE = re.compile(r"\(HTTP\s+(\d{3})\)")
_DECODER = json.JSONDecoder()


class GhError(RuntimeError):
    """`gh` failed for good. `status` is the HTTP status parsed from stderr
    (None when the CLI failed before/without an HTTP answer)."""

    def __init__(self, args: list[str], stderr: str, status: int | None = None) -> None:
        # Keep the invocation for diagnosis but never more than the first three
        # words: the tail can carry request payloads.
        self.cmd = "gh " + " ".join(args[:3])
        self.stderr = (stderr or "").strip()
        self.status = status
        first = self.stderr.splitlines()[0] if self.stderr else "exit without error message"
        super().__init__(f"{self.cmd} failed: {first[:300]}")


def gh_api(args: list[str], retries: int = 3, cwd: str | None = None) -> str:
    """Run `gh <args>` and return stdout.

    Transient failures (network, 5xx, 408/429, rate limits) are retried with
    backoff. Any other 4xx fails immediately: retrying a 403 or a 422 can only
    produce the same answer, so the caller must see it.
    """
    gh = os.environ.get("GH_BIN", "gh")
    err, status = "", None
    for attempt in range(max(1, retries)):
        try:
            proc = subprocess.run(  # noqa: S603 - fixed argv, `gh` from PATH
                [gh, *args], capture_output=True, text=True,
                encoding="utf-8", errors="replace", cwd=cwd,
            )
        except FileNotFoundError:
            raise GhError(args, f"`{gh}` not found on PATH") from None
        if proc.returncode == 0:
            return proc.stdout
        err, status = proc.stderr, _http_status(proc.stderr)
        if not _retryable(err, status):
            break
        if attempt < retries - 1:
            time.sleep(2 * (attempt + 1))
    raise GhError(args, err, status)


def is_transient(err: GhError) -> bool:
    """Whether `gh_api` retries a request that failed this way (the answer
    never arrived, or GitHub said "later"), as opposed to an answer GitHub will
    give again."""
    return _retryable(err.stderr, err.status)


def _http_status(stderr: str) -> int | None:
    m = _STATUS_RE.search(stderr)
    return int(m.group(1)) if m else None


def _retryable(stderr: str, status: int | None) -> bool:
    low = stderr.lower()
    if "usage:" in low or "unknown flag" in low or "unknown command" in low:
        return False  # bad invocation
    if status is None:
        return True  # network error / EOF / timeout
    if status >= 500 or status in (408, 429):
        return True
    if status == 403 and "rate limit" in low:
        return True  # abuse / secondary rate limit
    return False


def _json_values(text: str, args: list[str]) -> list:
    """Parse every JSON value in `text`: one document, one value per line
    (`--paginate --jq`), or several concatenated documents."""
    out, i, n = [], 0, len(text)
    try:
        while i < n:
            while i < n and text[i] in " \t\r\n":
                i += 1
            if i >= n:
                break
            value, i = _DECODER.raw_decode(text, i)
            out.append(value)
    except json.JSONDecodeError:
        raise GhError(args, f"unexpected non-JSON output: {text[:200]!r}") from None
    return out


def gh_json(args: list[str], retries: int = 3, cwd: str | None = None) -> object:
    """Run gh and parse stdout as a single JSON document."""
    text = gh_api(args, retries=retries, cwd=cwd)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise GhError(args, f"unexpected non-JSON output: {text[:200]!r}") from None


def gh_json_values(args: list[str], retries: int = 3, cwd: str | None = None) -> list:
    """Run gh and parse stdout as a stream of JSON values
    (the output shape of `gh api --paginate <path> --jq '.[] | {...}'`)."""
    return _json_values(gh_api(args, retries=retries, cwd=cwd), args)


# ---------- merged PRs ----------

def pr_files(owner: str, name: str, pr_number: int | str) -> list[str]:
    """Complete file list of a pull request (the first 100 are cheap; big PRs
    are paged through with REST)."""
    rows = gh_json_values([
        "api", "--paginate", f"repos/{owner}/{name}/pulls/{pr_number}/files",
        "--jq", ".[] | {filename}",
    ])
    return [r["filename"] for r in rows]


def fetch_merged_prs(
    owner: str,
    name: str,
    max_prs: int = 100,
    updated_before: dt.datetime | None = None,
    max_pages: int = 20,
) -> list[dict]:
    """Most recently updated merged PRs (newest first): number, createdAt,
    updatedAt, author, the complete file list (`files.nodes[].path`) and reviews.

    `updated_before` freezes the sample at a point in time so that a backtest
    run later still sees the same PRs.
    """
    out: list[dict] = []
    cursor: str | None = None
    for _ in range(max_pages):
        args = ["api", "graphql", "-f", f"query={_PR_QUERY}",
                "-f", f"owner={owner}", "-f", f"name={name}"]
        if cursor:
            args += ["-f", f"cursor={cursor}"]
        data = gh_json(args)["data"]["repository"]["pullRequests"]
        nodes = data["nodes"]
        if updated_before is not None:
            # Newest first, so only the front of the list is cut off; paging
            # goes on until `max_prs` PRs older than the cutoff are collected.
            nodes = [n for n in nodes if parse_time(n["updatedAt"]) < updated_before]
        out.extend(nodes)
        if not data["pageInfo"]["hasNextPage"] or len(out) >= max_prs:
            break
        cursor = data["pageInfo"]["endCursor"]
    out = out[:max_prs]
    for pr in out:
        seen = len(pr["files"]["nodes"])
        if pr.get("changedFiles", seen) > seen:  # GraphQL caps `files` at 100
            pr["files"]["nodes"] = [{"path": p} for p in pr_files(owner, name, pr["number"])]
    return out


# ---------- reviews ----------

def pr_author(pr: dict) -> str:
    """Lowercase login of the PR author ('' when unknown)."""
    return ((pr.get("author") or {}).get("login") or "").lower()


def is_bot_account(node: dict | None, cfg: Config) -> bool:
    """Whether an account node (`{"login", "__typename"}` from GraphQL or
    `{"login", "type"}` from REST) is automation. A missing or accountless
    node counts as one: it names nobody who could be requested."""
    if not node or node.get("__typename") in NON_HUMAN or node.get("type") in NON_HUMAN:
        return True
    login = (node.get("login") or "").strip().lower()
    return not login or cfg.is_bot(login)


def reviewers_of(pr: dict, cfg: Config) -> set[str]:
    """Distinct humans (lowercase logins) who reviewed `pr`, the PR author
    excluded."""
    author = pr_author(pr)
    out = set()
    for rv in (pr.get("reviews") or {}).get("nodes") or []:
        login = ((rv.get("author") or {}).get("login") or "").lower()
        if rv.get("state") not in REVIEW_STATES or is_bot_account(rv.get("author"), cfg):
            continue
        if login != author:
            out.add(login)
    return out


def review_events(
    prs: list[dict], mmap: ModuleMap, cfg: Config, ref: dt.datetime
) -> list[tuple[str, str, dt.datetime]]:
    """(reviewer, module, when) events usable at time `ref` — parameter-free,
    so tuning can re-decay them for every configuration."""
    evs: list[tuple[str, str, dt.datetime]] = []
    for pr in prs:
        if parse_time(pr["createdAt"]) >= ref:
            continue  # no leakage: only PRs that already existed count
        author = pr_author(pr)
        modules = cfg.touched_modules(mmap.of(f["path"]) for f in pr["files"]["nodes"])
        for rv in pr["reviews"]["nodes"]:
            if rv["state"] not in REVIEW_STATES or is_bot_account(rv.get("author"), cfg):
                continue
            login = (rv["author"]["login"] or "").lower()
            if login == author:
                continue
            when = parse_time(rv["submittedAt"])
            if when > ref:
                continue
            for m in modules:
                evs.append((login, m, when))
    return evs


def decayed_counts(
    events: list[tuple[str, str, dt.datetime]], cfg: Config, ref: dt.datetime
) -> dict[tuple[str, str], tuple[int, float]]:
    """[(actor, module, when)] -> {(actor, module): (count, decayed weight)}."""
    acc: dict[tuple[str, str], list[float]] = defaultdict(list)
    for actor, m, when in events:
        acc[(actor, m)].append(cfg.decay(when, ref))
    return {k: (len(ws), sum(ws)) for k, ws in acc.items()}


def review_signals(
    prs: list[dict], mmap: ModuleMap, cfg: Config, ref: dt.datetime
) -> dict[tuple[str, str], tuple[int, float]]:
    """(reviewer_login, module) -> (count, decayed weight)."""
    return decayed_counts(review_events(prs, mmap, cfg, ref), cfg, ref)


def fetch_pending_reviews(owner: str, name: str, skip: int | None = None) -> dict[str, int]:
    """login -> number of open PRs currently waiting on their review (workload signal).

    `skip` leaves one pull request out. Run for PR X, the reviews X itself is
    waiting on must not count against the people requested on it: on a re-run
    they would rank lower, and other people be requested on top of them."""
    pending: dict[str, int] = defaultdict(int)
    page = 1
    while page <= 10:  # hard cap: 1000 open PRs
        batch = gh_json(["api", f"repos/{owner}/{name}/pulls?state=open&per_page=100&page={page}"])
        if not isinstance(batch, list) or not batch:
            break
        for pr in batch:
            if pr.get("number") == skip:
                continue
            for rv in pr.get("requested_reviewers") or []:
                login = (rv or {}).get("login")
                if login:
                    pending[login.lower()] += 1
        if len(batch) < 100:
            break
        page += 1
    return dict(pending)


# A review once given: it may have been dismissed since, by a new commit or by
# hand, but the reviewer has seen the pull request and was told of it.
SUBMITTED = (*REVIEW_STATES, "DISMISSED")


def submitted_reviewers(owner: str, name: str, pr_number: int | str) -> set[str]:
    """Lowercase logins of everyone who has submitted a review on the pull
    request, in any state. A review still being written (PENDING) is not one.

    GitHub takes a reviewer off the list of requested reviewers as soon as they
    submit: going by that list alone, the next push would request them again.
    """
    rows = gh_json_values([
        "api", "--paginate", f"repos/{owner}/{name}/pulls/{pr_number}/reviews",
        "--jq", ".[] | {login: .user.login, state}",
    ])
    return {(r.get("login") or "").lower() for r in rows if r.get("state") in SUBMITTED}


# ---------- identity: git author -> GitHub login ----------

@dataclass
class IdentityIndex:
    """git author email -> GitHub login.

    Resolved through the commits API: GitHub matches the commit email to the
    account server-side, so it also works for private (`noreply`) addresses and
    for one person committing under several names.
    """
    email_to_login: dict[str, str] = field(default_factory=dict)  # email(lower) -> login(lowercase)
    login_case: dict[str, str] = field(default_factory=dict)      # login(lowercase) -> casing GitHub shows
    commits_scanned: int = 0
    truncated: bool = False   # a scan limit stopped us while commits remained
    ambiguous: int = 0        # commits whose email maps to a second login

    def resolve(self, who: str) -> str | None:
        """'Name <email>' -> lowercase login, or None when the email belongs to
        no (scanned) GitHub account."""
        _, _, email = who.rpartition("<")
        return self.email_to_login.get(email.rstrip(">").strip().lower())

    def display(self, login: str) -> str:
        """Lowercase login -> the casing the account actually uses."""
        return self.login_case.get(login.lower(), login)


def build_identity_index(
    owner: str,
    name: str,
    since: str,
    until: str | None = None,
    max_commits: int = 3000,
    cfg: Config | None = None,
    ref: str | None = None,
) -> IdentityIndex:
    """Index the emails of commits committed in `[since, until]` (ISO-8601; pass
    the signal window so that every author who can appear in `git log` is
    covered). The commits are those reachable from `ref`: pass the commit whose
    history was read from git. Without it the API lists the default branch,
    which is another history when the pull request targets another branch.
    At most `max_commits` commits are read, newest first; `truncated` tells when
    the window holds more. Automation accounts are left out."""
    cfg = cfg or Config()
    idx = IdentityIndex()
    page = 1
    while idx.commits_scanned < max_commits:
        args = [
            "api", "-X", "GET", f"repos/{owner}/{name}/commits",
            "-f", "per_page=100", "-f", f"since={since}", "-f", f"page={page}",
        ]
        if until:
            args += ["-f", f"until={until}"]
        if ref:
            args += ["-f", f"sha={ref}"]
        batch = gh_json(args)
        if not isinstance(batch, list) or not batch:
            return idx
        full_page = len(batch) == 100
        for c in batch[: max_commits - idx.commits_scanned]:
            idx.commits_scanned += 1
            if is_bot_account(c.get("author"), cfg):
                continue  # automation: nothing to request a review from
            login = ((c.get("author") or {}).get("login") or "").strip()
            info = (c.get("commit") or {}).get("author") or {}
            email = (info.get("email") or "").strip().lower()
            if not login or not email:
                continue  # e.g. a web-flow merge commit authored as "GitHub"
            known = idx.email_to_login.get(email)
            if known is None:
                idx.email_to_login[email] = login.lower()
                idx.login_case.setdefault(login.lower(), login)
            elif known != login.lower():
                idx.ambiguous += 1
        if not full_page:
            return idx
        page += 1
    idx.truncated = True
    return idx


def merge_authors(history: dict[str, AuthorHistory], key_of) -> dict[str, AuthorHistory]:
    """Re-key history by `key_of(who)`, summing entries that land on the same
    key (one person, several git identities). Entries whose key is None are
    dropped."""
    out: dict[str, AuthorHistory] = {}
    for who, h in history.items():
        key = key_of(who)
        if key is None:
            continue
        tgt = out.setdefault(key, AuthorHistory())
        tgt.total_commits += h.total_commits
        if h.last_active and (tgt.last_active is None or h.last_active > tgt.last_active):
            tgt.last_active = h.last_active
        for m, ms in h.modules.items():
            t = tgt.modules.setdefault(m, ModuleSignal())
            t.commits += ms.commits
            t.weight += ms.weight
            if ms.last and (t.last is None or ms.last > t.last):
                t.last = ms.last
    return out


def merge_identities(
    history: dict[str, AuthorHistory], index: IdentityIndex
) -> dict[str, AuthorHistory]:
    """'Name <email>' keyed history -> lowercase-login keyed history.

    Unresolved authors are dropped instead of being kept under their git name.
    A name is not an account: it cannot be requested as a reviewer or
    @-mentioned, and kept as a candidate it would also slip past the
    PR-author filter (the filter compares logins).
    """
    return merge_authors(history, index.resolve)


def unresolved_authors(
    history: dict[str, AuthorHistory], index: IdentityIndex, cfg: Config | None = None
) -> list[str]:
    """History keys whose email is not linked to a GitHub account (for diagnostics).
    Automation is left out: it has no account to link by design."""
    cfg = cfg or Config()
    return sorted(who for who in history if index.resolve(who) is None and not cfg.is_bot(who))
