# SPDX-License-Identifier: Apache-2.0
"""GitHub Action entrypoint: recommend reviewers for one pull request.

Environment (set by the composite action, see action.yml):
  GITHUB_REPOSITORY   owner/name of the base repository
  PR_NUMBER           number of the pull request
  GITHUB_TOKEN        token with pull-requests: write
  TOP_N, WINDOW_DAYS  optional overrides
  REQUEST_REVIEWERS   "false" -> comment only (default: also request reviewers)
  DRY_RUN             "true"  -> print everything, write nothing

The pull request is looked up through the API by its number, so the action
fits any trigger whose workflow can pass one (`pull_request_target` takes it
from the event, `workflow_run` finds it first). Only the base side is read from
disk (the PR's base commit on `pull_request_target`, the default branch on
`workflow_run`) and pull request data is treated as data, so code from the PR
is never run. Drafts are left alone: they get their recommendation when they
are marked ready for review.

When the branch on disk is not the one the PR targets — a PR against a release
branch, under `workflow_run` — the comment says so: the modules and the history
are then those of the branch on disk.

The pull request is read as it is when the action runs, not as it was when the
run started: one whose job waited behind another finds it closed, and leaves
it alone. It is read a second time right before the first write, as reading
the files and scoring them takes a while: closed or a draft again by then, it
is left alone; with a new head, the files of that head are read instead.

Modes:
  dry-run                  print the comment and who would be requested
  request-reviewers=false  post (or update in place) the comment only
  default                  comment + one review request per recommended reviewer

Reviewers are requested *before* the comment is rendered, and the comment
reports what actually happened; it never claims a request that failed. Each
reviewer is asked once per pull request, and no more than `top-n` are asked
in all: who is on the list of the pull request already, who has reviewed it,
and who this action asked before are passed over. Whom it asked before is
read from the action's own comment (RECORD).

The comment is the action's own or it is not touched. With GITHUB_TOKEN every
workflow of a repository writes as the same account, and that account may
edit and delete anybody's comment; so a comment counts as this action's when
GitHub says the token wrote it, it starts with our title and it ends with
RECORD — and nothing else is ever edited or deleted.

A comment that cannot be posted is an error (exit 1) rather than a warning: a
run that silently posts nothing looks like a run that worked. Nor does one
job leave two: an edit that may or may not have landed is not followed by a
new comment, and a POST whose answer was lost is looked for before it is
repeated.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import os
import re
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config, UNASSIGNED
from .deps import build_dep_graph
from .history import collect_history, head_commit, parse_time
from .modules import build_module_map
from .reviewlog import (
    GhError,
    build_identity_index,
    fetch_merged_prs,
    fetch_pending_reviews,
    gh_api,
    gh_json,
    is_bot_account,
    is_transient,
    merge_identities,
    pr_files,
    review_signals,
    submitted_reviewers,
    unresolved_authors,
)
from .score import Candidate, recommend

MARKER = "## 🤖 Suggested reviewers"
# The title the comment carried before 2026-11-26, when it was written in
# Chinese. Such a comment carries no record (RECORD_HEAD), so it is not known
# to be this action's and is left alone.
OLD_MARKERS = ("## 🤖 Reviewer 推荐",)
HISTORY_PRS = 100   # most recent merged PRs used as the review corpus
READS = 3           # how often the files of a pull request are read at most: it can get a new head while they are read

# The last line of the comment. GitHub does not show it. It is what tells the
# comment of this action from any other, and it keeps what no API keeps: whom
# the action requested on the pull request. A review request leaves the pull
# request when the review is submitted, and the request would be made again.
RECORD_HEAD = "<!-- pr-reviewer-recommender requested:"
RECORD_TAIL = " -->"
RECORD_LINE = re.compile(re.escape(RECORD_HEAD) + r"(?: [A-Za-z0-9_-]+(?:,[A-Za-z0-9_-]+)*)?" + re.escape(RECORD_TAIL))


@dataclass
class Requests:
    """What was (or, in dry-run, would be) done about review requests."""
    enabled: bool
    dry_run: bool
    requested: list[str] = field(default_factory=list)     # asked on this run
    already: list[str] = field(default_factory=list)       # were on the PR already
    reviewed: list[str] = field(default_factory=list)      # reviewed this PR already
    asked_before: list[str] = field(default_factory=list)  # among the top of this run, and asked on an earlier run
    capped: list[str] = field(default_factory=list)        # left out: top-n were asked in all
    failed: list[tuple[str, str]] = field(default_factory=list)   # (login, reason)
    budget: int = 0        # how many reviewers this action asks on the pull request in all
    record: list[str] = field(default_factory=list)        # whom this action asked on it in all, this run done


def main() -> int:
    slug = os.environ.get("GITHUB_REPOSITORY", "").strip()
    raw_number = os.environ.get("PR_NUMBER", "")
    pr_number = raw_number.strip()
    # ASCII digits and no leading zero: what a pull request number looks like.
    # Not isdecimal(), which also takes other scripts' digits — the Arabic-Indic
    # zero passes a check for "0" and int() turns it into pull request 0. The
    # length also keeps int() from raising further on (it has a limit on the
    # digits it converts).
    if "/" not in slug:
        print("error: GITHUB_REPOSITORY (owner/name) must be set", file=sys.stderr)
        return 2
    if raw_number == "":
        print("error: PR_NUMBER must be set: the number of the pull request", file=sys.stderr)
        return 2
    if not re.fullmatch(r"[1-9][0-9]{0,11}", pr_number):
        # Said here, before anything is read: a 404 further on would point at the token.
        print(f"error: PR_NUMBER must be the number of a pull request, not {raw_number!r}", file=sys.stderr)
        return 2
    owner, name = slug.split("/", 1)
    try:
        cfg = Config(top_n=_env_int("TOP_N", 3), window_days=_env_int("WINDOW_DAYS", 365))
        if cfg.window_days <= 0:
            raise ValueError("WINDOW_DAYS must be positive")
        dry_run = _env_flag("DRY_RUN")
        request = _env_flag("REQUEST_REVIEWERS", default=True)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    try:
        return _run(owner, name, int(pr_number), cfg, dry_run, request)
    except GhError as e:
        print(f"error: {e}", file=sys.stderr)
        if hint := _hint(e):
            print(f"hint: {hint}", file=sys.stderr)
        return 1


def _run(owner: str, name: str, pr_number: int, cfg: Config, dry_run: bool, request: bool) -> int:
    workspace = Path(os.environ.get("GITHUB_WORKSPACE") or os.getcwd()).resolve()
    pr = _pr_info(owner, name, pr_number)
    if why := _why_not(pr, owner, name, pr_number):
        print(why)
        return 0
    author = pr["author"]
    if author and is_bot_account({"login": author, "type": pr["authorType"]}, cfg):
        print(f"PR #{pr_number}: opened by a bot (@{author}), nothing to recommend")
        return 0
    ref = parse_time(pr["createdAt"])

    mmap = build_module_map(workspace)
    since = (ref - dt.timedelta(days=cfg.window_days)).isoformat()
    base = head_commit(workspace)
    raw = collect_history(workspace, mmap, cfg, ref, before=pr["createdAt"])
    # Identities come from the commits reachable from `base`. Asked without a
    # ref, the API lists the default branch: another history when the PR
    # targets another branch, and its authors then count as unlinked.
    ident = build_identity_index(owner, name, since, until=pr["createdAt"], ref=base)
    history = merge_identities(raw, ident)
    kept = sum(h.total_commits for h in history.values())
    dropped = unresolved_authors(raw, ident, cfg)
    print(
        f"history: {kept} commits by {len(history)} accounts in the last {cfg.window_days} days; "
        f"{len(dropped)} git author(s) without a linked GitHub account dropped"
        + (f" ({', '.join(dropped[:8])}{'…' if len(dropped) > 8 else ''})" if dropped else "")
        + f"; identity scan: {ident.commits_scanned} commits"
        + (" (scan limit reached)" if ident.truncated else "")
        + (f", {ident.ambiguous} ambiguous" if ident.ambiguous else "")
    )

    rsig = review_signals(fetch_merged_prs(owner, name, max_prs=HISTORY_PRS), mmap, cfg, ref)
    # What this PR is waiting on does not count against the people requested on
    # it, or a re-run would demote them and request other people on top.
    pending = fetch_pending_reviews(owner, name, skip=pr_number)
    dep_adj = build_dep_graph(workspace, mmap).adj
    # What a new head of the pull request does not change: who reviewed it
    # already, and what this action asked on it before. Both are read before
    # anything is written — should the comments not be readable, nothing is.
    reviewed = submitted_reviewers(owner, name, pr_number)
    earlier = _our_comments(owner, name, pr_number)
    asked_before: list[str] = []
    for c in earlier:
        asked_before += [login for login in c.requested if login not in asked_before]

    for attempt in range(READS):
        files = pr_files(owner, name, pr_number)
        if not files:
            print(f"PR #{pr_number}: no changed files, nothing to recommend")
            return 0
        modules = cfg.touched_modules(mmap.of(f) for f in files)
        print(f"PR #{pr_number} by @{author or '?'}: {len(files)} files -> {', '.join(modules)}")
        if pr["changedFiles"] > len(files):
            print(f"note: GitHub lists {pr['changedFiles']} changed files; the API returned {len(files)}")
        cands = recommend(modules, history, rsig, cfg, ref, pr_author=author or None,
                          dep_adj=dep_adj, pending=pending)
        if not cands:
            print("no candidate survived filtering; nothing to post")
            return 0
        top = cands[: cfg.effective_top_n()]
        # The pull request as it is now, after its files were read and scored.
        # The head is what was scored: a push in the meantime means reviewers
        # would be asked for files that are no longer the pull request's, and a
        # notification cannot be taken back. The run of the new head recommends.
        now = _pr_info(owner, name, pr_number)
        if why := _why_not(now, owner, name, pr_number):
            print(why)
            return 0
        pushed = now["head"] != pr["head"]           # other files may be the pull request's now
        retargeted = now["baseRef"] != pr["baseRef"]  # against another branch: another diff
        if not pushed and not retargeted:
            break
        if attempt == READS - 1:
            print(f"PR #{pr_number}: its head or its base changed {READS - 1} times while it was being "
                  "read; nothing written. The run started by the last of these changes recommends")
            return 0
        if pushed:
            print(f"note: PR #{pr_number} got a new head while it was being read ({pr['head'][:12]} -> "
                  f"{now['head'][:12]}): reading that one instead")
        else:
            print(f"note: PR #{pr_number} was made to target {now['baseRef']} instead of {pr['baseRef']} "
                  "while it was being read: reading it again")
        pr = now

    # The branch whose commit is on disk, and the one the PR targets. They differ
    # for a PR against another branch under `workflow_run`, where the default
    # branch is the only one the workflow may check out: the modules are then
    # found in a tree that may be laid out differently.
    read = os.environ.get("BASE_REF", "").strip()
    other = now["baseRef"] if read and now["baseRef"] != read else ""
    if other:
        print(f"note: the pull request targets {other} and {read} is what is on disk: "
              "the modules and the history are those of the latter")
    outcome = _request_reviewers(owner, name, pr_number, top, now, reviewed, asked_before, request, dry_run,
                                 budget=cfg.effective_top_n())
    body = _render(top, modules, cfg, outcome, ident, read_from=(read, other) if other else None)
    print(f"--- comment ---\n{body}\n---------------")
    if dry_run:
        print("dry-run: nothing was posted and no reviewer was requested")
        return 0
    _post_comment(owner, name, pr_number, body, earlier)
    return 0


# ---------- inputs ----------

def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{name}={raw!r} is not an integer") from None


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    if raw in ("true", "1", "yes"):
        return True
    if raw in ("false", "0", "no"):
        return False
    raise ValueError(f"{name}={raw!r}: expected true or false")


def _hint(err: GhError) -> str:
    low = err.stderr.lower()
    if err.status == 403 and "rate limit" in low:
        return "GitHub rate limit reached; re-run the job later."
    if err.status in (403, 404):
        # No way is pointed at a token from a secret: on `pull_request` a PR
        # from a fork has no right to see one, and giving it one would hand
        # the write token to a workflow the PR can change.
        return (
            "the token was not allowed to do this. On PRs opened from a fork, GITHUB_TOKEN is "
            "read-only while the workflow runs on `pull_request`: run the action on "
            "`pull_request_target` instead, or on `workflow_run` where the owner of the "
            "repository does not allow that (README, \"Usage as a GitHub Action\"). "
            "Otherwise check the token has pull-requests: write."
        )
    return ""


# ---------- pull request ----------

def _pr_info(owner: str, name: str, pr_number: int) -> dict:
    """state, author, createdAt, draft, changedFiles, the branch targeted, its
    head commit and the reviewers requested."""
    data = gh_json([
        "api", f"repos/{owner}/{name}/pulls/{pr_number}", "--jq",
        "{state: .state, author: .user.login, authorType: .user.type, createdAt: .created_at,"
        " draft: .draft, changedFiles: .changed_files, baseRef: .base.ref, head: .head.sha,"
        " reviewers: [.requested_reviewers[]?.login]}",
    ])
    head = (data.get("head") or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        # Without the head commit, the pull request as it was scored could not
        # be told from the one it is when written to.
        raise GhError(["api", f"repos/{owner}/{name}/pulls/{pr_number}"],
                      f"the head commit of pull request {pr_number} came back as {head!r}, not a commit SHA")
    reviewers = {r.lower() for r in data.get("reviewers") or [] if r}
    return {
        "state": (data.get("state") or "").strip().lower(),
        "author": (data.get("author") or "").lower(),
        "authorType": data.get("authorType"),
        "createdAt": data["createdAt"],
        "draft": bool(data.get("draft")),
        "changedFiles": data.get("changedFiles") or 0,
        "baseRef": (data.get("baseRef") or "").strip(),
        "head": head,
        "reviewers": reviewers,
    }


def _why_not(pr: dict, owner: str, name: str, pr_number: int) -> str:
    """Why nothing is done for the pull request as it is, if anything: the line
    to print. Empty when it is to be recommended for."""
    if pr["state"] not in ("open", "closed"):
        # Not an answer to go on. Taken for closed it would skip the
        # recommendation without a word; taken for open it would write.
        raise GhError(["api", f"repos/{owner}/{name}/pulls/{pr_number}"],
                      f"the state of pull request {pr_number} came back as {pr['state']!r}, not open or closed")
    if pr["state"] != "open":
        # Read as it is now, not as it was when the run started: under
        # workflow_run the job of a run can wait a long time for its turn.
        return f"PR #{pr_number}: not open any more (GitHub says {pr['state']}), nothing to recommend"
    if pr["draft"]:
        return f"PR #{pr_number}: a draft, nothing to recommend until it is marked ready for review"
    return ""


def _request_reviewers(
    owner: str, name: str, pr_number: int, top: list[Candidate], pr: dict,
    reviewed: set[str], asked_before: list[str], enabled: bool, dry_run: bool, budget: int,
) -> Requests:
    """Ask each of `top` in turn, passing over whoever:

    * is on the list of the pull request already, whoever put them there;
    * has submitted a review on it — GitHub takes a reviewer off that list when
      they do, so the list alone would have them asked again on the next push;
    * this action asked on an earlier run, even if the request has since been
      removed;
    * would take the number this action asked on the pull request past
      `budget`: one notification each, and so many in all.

    `pr` is the pull request as read last, so that the list is the current one.
    """
    out = Requests(enabled=enabled, dry_run=dry_run, budget=budget, record=list(asked_before))
    if not enabled:
        return out
    asked = set(asked_before)
    for c in top:
        login = c.key.lower()
        if login in pr["reviewers"]:
            out.already.append(login)
        elif login in reviewed:
            out.reviewed.append(login)
        elif login in asked:
            out.asked_before.append(login)
        elif len(asked) >= budget:
            out.capped.append(login)
        elif dry_run:
            out.requested.append(login)
        else:
            try:
                # One request per reviewer, and `reviewers[]` so that gh sends an
                # array. `-f reviewers=a,b` sends the string "a,b", which the API
                # rejects with 422 "... is not an array". Asking one at a time
                # keeps a single non-requestable reviewer from voiding the rest.
                gh_api([
                    "api", "-X", "POST",
                    f"repos/{owner}/{name}/pulls/{pr_number}/requested_reviewers",
                    "-f", f"reviewers[]={login}",
                ])
                out.requested.append(login)
                out.record.append(login)   # asked, as far as is known: a failure is not one
            except GhError as e:
                out.failed.append((login, _reason(e)))
    return out


_STATUS_AT_END = re.compile(r"\s*\(HTTP (\d{3})\)\s*$")


def _reason(err: GhError) -> str:
    """The API's own first sentence with its status, e.g. 'Reviews may only be
    requested from collaborators. (HTTP 422)'."""
    lines = err.stderr.splitlines()
    line = lines[0].strip() if lines else ""
    if line.lower().startswith("gh: "):
        line = line[4:]
    status = ""
    if m := _STATUS_AT_END.search(line):
        status, line = f" (HTTP {m.group(1)})", line[: m.start()]
    line = " ".join(line.split())
    if ". " in line:  # GitHub appends an explanation; the first sentence says it
        line = line.split(". ", 1)[0] + "."
    elif len(line) > 120:
        line = line[:120].rstrip() + "…"
    return f"{line}{status}".strip() or (f"HTTP {err.status}" if err.status else "gh failed")


# ---------- comment ----------

# GraphQL and not REST: only GraphQL says for each comment whether the token's
# own account wrote it (`viewerDidAuthor`).
_COMMENTS_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      comments(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes { databaseId body viewerDidAuthor }
      }
    }
  }
}
"""


@dataclass(frozen=True)
class Comment:
    """A comment of this action on the pull request."""
    id: int
    body: str
    requested: tuple[str, ...]   # whom the action had asked for when it wrote it


def _recorded(body: str) -> tuple[str, ...] | None:
    """The logins in the record at the end of a comment, lowercase. None for a
    comment that has no such record: it is not known to be this action's."""
    last = (body or "").rstrip("\r\n").rsplit("\n", 1)[-1].rstrip("\r")
    if not RECORD_LINE.fullmatch(last):
        return None
    listed = last[len(RECORD_HEAD): -len(RECORD_TAIL)].strip()
    return tuple(listed.lower().split(",")) if listed else ()


def _record_line(logins) -> str:
    listed = ",".join(logins)
    return RECORD_HEAD + (f" {listed}" if listed else "") + RECORD_TAIL


def _our_comments(owner: str, name: str, pr_number: int) -> list[Comment]:
    """The comments of this action on the pull request, oldest first.

    Ours is a comment that GitHub says the account behind the token wrote
    (`viewerDidAuthor`), that starts with our title, and that ends with the
    record line. Who wrote it is not enough: with GITHUB_TOKEN every workflow
    of the repository writes as one account, and it is allowed to edit and
    delete the comments of everybody else. So a comment under our title that
    has no record — one of an earlier version of this action, or one of another
    workflow that writes under the same title — is left alone, and said so.
    """
    out, cursor = [], None
    while True:
        args = ["api", "graphql", "-f", f"query={_COMMENTS_QUERY}",
                "-f", f"owner={owner}", "-f", f"name={name}", "-F", f"number={pr_number}"]
        if cursor:
            args += ["-f", f"after={cursor}"]
        comments = gh_json(args)["data"]["repository"]["pullRequest"]["comments"]
        for node in comments["nodes"]:
            if not isinstance(node.get("viewerDidAuthor"), bool):
                # Without that answer every comment would pass for somebody
                # else's, and each run would post one more.
                raise GhError(args, f"the answer on the comments of pull request {pr_number} "
                                    "has no viewerDidAuthor")
            body = node.get("body") or ""
            if not node["viewerDidAuthor"] or not body.startswith((MARKER, *OLD_MARKERS)):
                continue
            recorded = _recorded(body)
            if recorded is not None and body.startswith(MARKER):
                out.append(Comment(int(node["databaseId"]), body, recorded))
            else:
                print(f"note: comment {node['databaseId']} is under the title of this action but has "
                      "no record of this action in it: left alone")
        if not comments["pageInfo"]["hasNextPage"]:
            return out
        cursor = comments["pageInfo"]["endCursor"]


def _post_comment(owner: str, name: str, pr_number: int, body: str, earlier: list[Comment]) -> None:
    """Create the recommendation comment, or edit ours in place (re-runs and
    force-pushes do not pile up comments). `earlier` are the comments of this
    action on the pull request as listed before anything was written, oldest
    first. Should there be more than one — two runs that overlapped can each
    have posted one — the newest is edited and the others are taken out. No
    other comment is edited or deleted."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(body)
        path = f.name
    try:
        if not earlier:
            _create_comment(owner, name, pr_number, path, body)
            return
        newest = earlier[-1]
        try:
            # Repeated by gh_api when the answer is lost, which changes nothing:
            # an edit sets the text.
            gh_api(["api", "-X", "PATCH", f"repos/{owner}/{name}/issues/comments/{newest.id}",
                    "-F", f"body=@{path}"])
        except GhError as e:
            if e.status != 404:
                # Whether the edit landed is not known. A new comment would
                # make it two if it did; the next run edits this one instead.
                raise
            print(f"note: recommendation comment {newest.id} is gone since it was listed; posting a new one")
            _create_comment(owner, name, pr_number, path, body)
            return
        print(f"updated recommendation comment {newest.id} in place")
        for old in earlier[:-1]:
            _take_out(owner, name, old.id)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(path)


def _create_comment(owner: str, name: str, pr_number: int, path: str, body: str, attempts: int = 3) -> int:
    """POST the comment from the file at `path`; its id.

    A POST is not repeated blind: GitHub may have created the comment and only
    the answer got lost, and a second one would leave two. So after every
    failure that leaves it open whether it landed — the answer never arrived,
    or GitHub said "later", on the last attempt as well — the comments are
    listed again, and one of this action's with exactly this body is taken as
    the comment of this run. A refusal is an answer: it is not looked into and
    not repeated.
    """
    endpoint = f"repos/{owner}/{name}/issues/{pr_number}/comments"
    out = None
    for attempt in range(attempts):
        try:
            out = gh_json(["api", "-X", "POST", endpoint, "-F", f"body=@{path}"], retries=1)
            break
        except GhError as e:
            if not is_transient(e):
                raise
            try:
                landed = [c.id for c in _our_comments(owner, name, pr_number) if c.body == body]
            except GhError as listing:
                # Not known whether it landed: sent again, it might be two.
                print(f"error: could not list the comments to tell whether the last try landed "
                      f"({_reason(listing)})", file=sys.stderr)
                raise e from None
            if landed:
                print(f"posted recommendation comment {landed[-1]} (the answer to the request was lost)")
                return landed[-1]
            if attempt == attempts - 1:
                raise
            time.sleep(2 * (attempt + 1))
    print(f"posted recommendation comment {out['id']}")
    return int(out["id"])


def _take_out(owner: str, name: str, comment_id: int) -> None:
    """Delete a recommendation comment an overlapping run left behind. A
    failure to is reported, not fatal: the comment of this run is already up."""
    try:
        gh_api(["api", "-X", "DELETE", f"repos/{owner}/{name}/issues/comments/{comment_id}"])
    except GhError as e:
        if e.status == 404:
            # Gone by the second of two tries, or taken out by a run that overlapped.
            print(f"recommendation comment {comment_id} was gone already")
        else:
            print(f"warning: could not take out recommendation comment {comment_id}: {_reason(e)}")
        return
    print(f"took out recommendation comment {comment_id}, left behind by an earlier run")


# ---------- rendering ----------

def _render(
    cands: list[Candidate], modules: list[str], cfg: Config, outcome: Requests, ident=None,
    read_from: tuple[str, str] | None = None,
) -> str:
    """`read_from`: (the branch whose commit was on disk, the branch the PR
    targets) when they differ."""
    show = ident.display if ident else (lambda login: login)
    named = [m for m in modules if m != UNASSIGNED]
    lines = [MARKER, "", _modules_line(named), ""]
    if read_from:
        # What is on disk is the tree the modules are found in and the history
        # the reviewers are read from. The merged PRs the review records come
        # from, and the reviews waiting everywhere, are read through the API
        # and belong to the repository, whatever branch they went into.
        lines += [f"> ℹ️ Based on `{read_from[0]}`, not on `{read_from[1]}`, the branch this PR targets: "
                  f"the modules and the commit history are those of `{read_from[0]}`. "
                  "The review records are those of the whole repository.", ""]
    if cfg.is_low_confidence(cands[0].evidence_count):
        # `(root)` is not counted as evidence, so for a PR outside every module
        # the count is 0 by construction: say what is actually the matter.
        why = (f"the top candidate has only {cands[0].evidence_count} commits and reviews in "
               "the modules this PR touches" if named else
               "this PR touches no module, so there is no module history to go by")
        lines += [f"> ⚠️ **Low confidence**: {why}. Treat the list as a starting point.", ""]
    lines += ["| Reviewer | Score | Why |", "|---|---|---|"]
    for c in cands:
        lines.append(f"| @{show(c.key)} | {c.score:.1f} | {_why(c)} |")
    # What became of the review requests stays out of the fold: it is the part
    # the reader may have to act on.
    lines += ["", *_footer(outcome, show)]
    if lines[-1] == "":
        lines.pop()
    lines += [
        "",
        "<details><summary>How the score is computed</summary>",
        "",
        "Commits and reviews in the modules this PR touches, each weighted by a "
        f"{cfg.halflife_days:.0f}-day half-life. A PR that touches several modules adds a "
        "bonus for people with history in every one of them, and for people with history "
        "on both sides of a dependency between a touched module and its neighbours. "
        "People with several reviews waiting rank lower.",
        "</details>",
        # Not shown by GitHub: what tells the next run whom this action asked.
        "",
        _record_line(outcome.record),
    ]
    return "\n".join(lines)


def _count(n: int, noun: str) -> str:
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _join(items) -> str:
    """'a', 'a and b', 'a, b and c'."""
    items = list(items)
    return ", ".join(items[:-1]) + " and " + items[-1] if len(items) > 1 else items[0]


def _modules_line(named: list[str]) -> str:
    """`named`: the modules the PR touches, without `(root)`."""
    if not named:
        return "This PR touches no module: its files are outside every module found in the repository."
    return f"This PR touches {_join(f'`{m}`' for m in named)}."


def _why(c: Candidate) -> str:
    bits = []
    for m, (nc, _cw, nr, _rw) in sorted(
        c.module_detail.items(), key=lambda kv: -(kv[1][1] + kv[1][3])
    ):
        parts = [_count(n, noun) for n, noun in ((nc, "commit"), (nr, "review")) if n]
        if parts:
            bits.append(f"`{m}` " + ", ".join(parts))
    why = " · ".join(bits) or "-"
    if c.coupling > 0:
        why += " · **history in every touched module**"
    if c.seams:
        why += " · on both sides of " + _join(f"`{s}`" for s in c.seams[:2])
    if c.pending:
        why += f" · {_count(c.pending, 'review')} pending"
    return why


def _footer(outcome: Requests, show) -> list[str]:
    at = lambda logins: _join(f"@{show(x)}" for x in logins)  # noqa: E731
    if not outcome.enabled:
        return ["No review was requested (`request-reviewers: false`)."]
    parts = []
    if outcome.requested:
        parts.append(("Would request reviews from" if outcome.dry_run else "Reviews requested from")
                     + f" {at(outcome.requested)}.")
    if outcome.already:
        parts.append(f"Already requested: {at(outcome.already)}.")
    if outcome.reviewed:
        parts.append(f"Already reviewed: {at(outcome.reviewed)}.")
    if outcome.asked_before:
        parts.append(f"Asked before on this pull request, and not asked again: {at(outcome.asked_before)}.")
    if outcome.capped:
        parts.append(f"Not asked, as this action asks at most {outcome.budget} reviewers per pull request: "
                     f"{at(outcome.capped)}.")
    if outcome.failed:   # a dry run makes no requests, so none can fail in it
        by_reason: dict[str, list[str]] = {}   # one sentence per distinct reason
        for login, reason in outcome.failed:
            by_reason.setdefault(reason, []).append(login)
        for reason, logins in by_reason.items():
            parts.append(f"Could not request a review from {at(logins)} ({reason}); "
                         f"add {at(logins)} in the Reviewers box.")
    return [" ".join(parts)] if parts else []


if __name__ == "__main__":
    raise SystemExit(main())
