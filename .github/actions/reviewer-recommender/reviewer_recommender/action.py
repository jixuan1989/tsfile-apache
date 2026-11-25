# SPDX-License-Identifier: Apache-2.0
"""GitHub Action entrypoint: recommend reviewers for one pull request.

Environment (set by the composite action, see action.yml):
  GITHUB_REPOSITORY   owner/name of the base repository
  PR_NUMBER           number of the pull request
  GITHUB_TOKEN        token with pull-requests: write
  TOP_N, WINDOW_DAYS  optional overrides
  REQUEST_REVIEWERS   "false" -> comment only (default: also request reviewers)
  DRY_RUN             "true"  -> print everything, write nothing

Only the base-branch checkout is read from disk and pull request data is
treated as data, so the action is safe on `pull_request_target` (code from the
PR is never run).

Modes:
  dry-run                  print the comment and who would be requested
  request-reviewers=false  post (or update in place) the comment only
  default                  comment + one review request per recommended reviewer

Reviewers are requested *before* the comment is rendered, and the comment
reports what actually happened; it never claims a request that failed. A
comment that cannot be posted is an error (exit 1) rather than a warning: a
run that silently posts nothing looks like a run that worked.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config, UNASSIGNED
from .deps import build_dep_graph
from .history import collect_history, parse_time
from .modules import build_module_map
from .reviewlog import (
    GhError,
    build_identity_index,
    fetch_merged_prs,
    fetch_pending_reviews,
    gh_api,
    gh_json,
    gh_json_values,
    is_bot_account,
    merge_identities,
    pr_files,
    review_signals,
    unresolved_authors,
)
from .score import Candidate, recommend

MARKER = "## 🤖 Reviewer 推荐"
HISTORY_PRS = 100   # most recent merged PRs used as the review corpus


@dataclass
class Requests:
    """What was (or, in dry-run, would be) done about review requests."""
    enabled: bool
    dry_run: bool
    requested: list[str] = field(default_factory=list)
    already: list[str] = field(default_factory=list)     # were on the PR already
    failed: list[tuple[str, str]] = field(default_factory=list)   # (login, reason)


def main() -> int:
    slug = os.environ.get("GITHUB_REPOSITORY", "").strip()
    pr_number = os.environ.get("PR_NUMBER", "").strip()
    if "/" not in slug or not pr_number.isdigit():
        print("error: GITHUB_REPOSITORY (owner/name) and PR_NUMBER must be set", file=sys.stderr)
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
    author = pr["author"]
    if author and is_bot_account({"login": author, "type": pr["authorType"]}, cfg):
        print(f"PR #{pr_number}: opened by a bot (@{author}), nothing to recommend")
        return 0
    ref = parse_time(pr["createdAt"])

    files = pr_files(owner, name, pr_number)
    if not files:
        print(f"PR #{pr_number}: no changed files, nothing to recommend")
        return 0
    mmap = build_module_map(workspace)
    modules = cfg.touched_modules(mmap.of(f) for f in files)
    print(f"PR #{pr_number} by @{author or '?'}: {len(files)} files -> {', '.join(modules)}")
    if pr["changedFiles"] > len(files):
        print(f"note: GitHub lists {pr['changedFiles']} changed files; the API returned {len(files)}")

    since = (ref - dt.timedelta(days=cfg.window_days)).isoformat()
    ident = build_identity_index(owner, name, since, until=pr["createdAt"])
    raw = collect_history(workspace, mmap, cfg, ref, before=pr["createdAt"])
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
    pending = fetch_pending_reviews(owner, name)
    dep_adj = build_dep_graph(workspace, mmap).adj
    cands = recommend(modules, history, rsig, cfg, ref, pr_author=author or None,
                      dep_adj=dep_adj, pending=pending)
    if not cands:
        print("no candidate survived filtering; nothing to post")
        return 0

    top = cands[: cfg.effective_top_n()]
    outcome = _request_reviewers(owner, name, pr_number, top, pr["reviewers"], request, dry_run)
    body = _render(top, modules, cfg, outcome, ident)
    print(f"--- comment ---\n{body}\n---------------")
    if dry_run:
        print("dry-run: nothing was posted and no reviewer was requested")
        return 0
    _post_comment(owner, name, pr_number, body)
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
        return (
            "the token was not allowed to do this. On PRs opened from a fork, GITHUB_TOKEN is "
            "read-only while the workflow runs on `pull_request`: trigger it on "
            "`pull_request_target` instead, or pass a PAT / GitHub App token (README, "
            "\"Pull requests from forks\"). Otherwise check the token has pull-requests: write."
        )
    return ""


# ---------- pull request ----------

def _pr_info(owner: str, name: str, pr_number: int) -> dict:
    """author, createdAt, changedFiles and the reviewers already requested."""
    data = gh_json([
        "api", f"repos/{owner}/{name}/pulls/{pr_number}", "--jq",
        "{author: .user.login, authorType: .user.type, createdAt: .created_at,"
        " changedFiles: .changed_files, reviewers: [.requested_reviewers[]?.login]}",
    ])
    reviewers = {r.lower() for r in data.get("reviewers") or [] if r}
    return {
        "author": (data.get("author") or "").lower(),
        "authorType": data.get("authorType"),
        "createdAt": data["createdAt"],
        "changedFiles": data.get("changedFiles") or 0,
        "reviewers": reviewers,
    }


def _request_reviewers(
    owner: str, name: str, pr_number: int, top: list[Candidate],
    already: set[str], enabled: bool, dry_run: bool,
) -> Requests:
    out = Requests(enabled=enabled, dry_run=dry_run)
    if not enabled:
        return out
    for c in top:
        login = c.key.lower()
        if login in already:
            out.already.append(login)
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

def _token_login() -> str | None:
    """Account behind the token, when the token may read it. GITHUB_TOKEN may
    refuse (`403`); the caller then falls back to matching by bot author."""
    try:
        login = gh_api(["api", "user", "--jq", ".login"], retries=1).strip()
    except GhError:
        return None
    return login.lower() or None


def _existing_comment_id(owner: str, name: str, pr_number: int, me: str | None) -> int | None:
    """Id of the recommendation comment posted earlier, if any.

    "Ours" = starts with our marker and authored by the token's own account.
    When that account is unknown, any bot account counts: comments written with
    GITHUB_TOKEN belong to `github-actions[bot]`, a GitHub App writes as
    `<app>[bot]`.
    """
    rows = gh_json_values([
        "api", "--paginate", f"repos/{owner}/{name}/issues/{pr_number}/comments",
        "--jq", f".[] | select(.body | startswith({json.dumps(MARKER, ensure_ascii=False)}))"
                " | {id, login: .user.login}",
    ])
    mine = None
    for c in rows:
        login = (c.get("login") or "").lower()
        if not login:
            continue
        # `me[bot]` too: should the API ever let an installation token read
        # `/user`, its comments are still authored as "<app>[bot]".
        ours = login in (me, f"{me}[bot]") if me is not None else login.endswith("[bot]")
        if ours:
            mine = c["id"]     # keep the most recent one
    return mine


def _post_comment(owner: str, name: str, pr_number: int, body: str) -> None:
    """Create the recommendation comment, or edit ours in place (re-runs and
    force-pushes do not pile up comments)."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(body)
        path = f.name
    try:
        prior = _existing_comment_id(owner, name, pr_number, _token_login())
        if prior:
            gh_api(["api", "-X", "PATCH", f"repos/{owner}/{name}/issues/comments/{prior}",
                    "-F", f"body=@{path}"])
            print(f"updated recommendation comment {prior} in place")
        else:
            gh_api(["api", "-X", "POST", f"repos/{owner}/{name}/issues/{pr_number}/comments",
                    "-F", f"body=@{path}"])
            print("posted recommendation comment")
    finally:
        with contextlib.suppress(OSError):
            os.unlink(path)


# ---------- rendering ----------

def _render(
    cands: list[Candidate], modules: list[str], cfg: Config, outcome: Requests, ident=None
) -> str:
    show = ident.display if ident else (lambda login: login)
    lines = [
        MARKER,
        "",
        f"本 PR 涉及模块：`{'`, `'.join(m for m in modules if m != UNASSIGNED) or UNASSIGNED}`",
        "",
    ]
    if cfg.is_low_confidence(cands[0].evidence_count):
        lines += [
            "> ⚠️ **低置信度**：该区域历史信号稀疏（最佳候选在该模块仅 "
            f"{cands[0].evidence_count} 次 commit/review 记录），推荐仅供参考，"
            "建议结合团队实际分工判断。",
            "",
        ]
    lines += ["| Reviewer | 分数 | 依据 |", "|---|---|---|"]
    for c in cands:
        lines.append(f"| @{show(c.key)} | {c.score:.1f} | {_why(c)} |")
    # What became of the review requests stays out of the fold: it is the part
    # the reader may have to act on.
    lines += ["", *_footer(outcome, show)]
    if lines[-1] == "":
        lines.pop()
    lines += [
        "",
        "<details><summary>评分依据（可折叠）</summary>",
        "",
        "信号 = 该模块内的 commit 历史 + 历史 review 记录（均按时间半衰期 "
        f"{cfg.halflife_days:.0f} 天衰减加权）；",
        "跨模块 PR 对在所有涉及模块均有贡献者额外加分。",
        "</details>",
    ]
    return "\n".join(lines)


def _count(n: int, noun: str) -> str:
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _why(c: Candidate) -> str:
    bits = []
    for m, (nc, _cw, nr, _rw) in sorted(
        c.module_detail.items(), key=lambda kv: -(kv[1][1] + kv[1][3])
    ):
        parts = []
        if nc:
            parts.append(_count(nc, "commit"))
        if nr:
            parts.append(_count(nr, "review"))
        if parts:
            bits.append(f"`{m}` " + "+".join(parts))
    why = " · ".join(bits) or "-"
    if c.coupling > 0:
        why += " · **跨模块覆盖**"
    if c.seams:
        why += " · " + "、".join(f"`{s}`" for s in c.seams[:2]) + " 接缝"
    if c.pending:
        why += f" · 待审 {c.pending}"
    return why


def _footer(outcome: Requests, show) -> list[str]:
    at = lambda logins: "、".join(f"@{show(x)}" for x in logins)  # noqa: E731
    if not outcome.enabled:
        return ["未自动请求 reviewer（`request-reviewers: false`，仅评论）。"]
    if outcome.dry_run:
        parts = [f"实际运行时会请求 {at(outcome.requested)} 进行 review"] if outcome.requested else []
        if outcome.already:
            parts.append(f"{at(outcome.already)} 已在 review 请求列表中")
        return ["；".join(parts) + "。"] if parts else []
    parts = []
    if outcome.requested:
        parts.append(f"已自动请求 {at(outcome.requested)} 进行 review")
    if outcome.already:
        parts.append(f"{at(outcome.already)} 已在 review 请求列表中，未重复请求")
    if outcome.failed:
        by_reason: dict[str, list[str]] = {}   # one sentence per distinct reason
        for login, reason in outcome.failed:
            by_reason.setdefault(reason, []).append(login)
        failed = "；".join(
            f"未能请求 {at(logins)} 进行 review（{reason}）" for reason, logins in by_reason.items()
        )
        parts.append(f"{failed}，可在 Reviewers 栏手动添加")
    if not parts:
        return []
    return ["；".join(parts) + "。"]


if __name__ == "__main__":
    raise SystemExit(main())
