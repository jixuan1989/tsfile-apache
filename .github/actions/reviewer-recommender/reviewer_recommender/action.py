#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""GitHub Action entrypoint.

Env contract (from composite action):
  GITHUB_REPOSITORY   owner/name
  PR_NUMBER           the pull request number
  GITHUB_TOKEN        token with pull-requests:write
  TOP_N / DRY_RUN / WINDOW_DAYS   optional overrides

The repo workspace is expected to be checked out with full history.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
from pathlib import Path

from .config import Config, UNASSIGNED
from .history import collect_history
from .modules import build_module_map
from .reviewlog import (
    build_identity_map,
    canonical_identities,
    fetch_merged_prs,
    gh_api,
    review_signals,
)
from .score import recommend

GITHUB_API = "https://api.github.com"


def main() -> int:
    repo_slug = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    if not repo_slug or not pr_number:
        print("error: GITHUB_REPOSITORY / PR_NUMBER env not set", file=sys.stderr)
        return 2
    owner, name = repo_slug.split("/", 1)
    cfg = Config(
        top_n=int(os.environ.get("TOP_N", "3")),
        window_days=int(os.environ.get("WINDOW_DAYS", "365")),
    )
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    workspace = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    pr = _pr_json(owner, name, pr_number)
    files = [f["path"] for f in pr["files"]]
    pr_author = (pr["author"] or {}).get("login")
    ref = dt.datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))

    mmap = build_module_map(workspace)
    modules = cfg.touched_modules(mmap.of(f) for f in files)

    print(f"PR #{pr_number} [{pr['title'][:50]}] modules: {modules}")
    raw_hist = collect_history(workspace, mmap, cfg, ref, before=pr["createdAt"])
    ident = build_identity_map(owner, name, commits_to_scan=800)
    history = {k.lower(): v for k, v in _canonical(raw_hist, ident).items()}
    rsig = review_signals(fetch_merged_prs(owner, name, max_prs=100), mmap, cfg, ref)
    cands = recommend(modules, history, rsig, cfg, ref, pr_author=pr_author)

    if not cands:
        print("no candidates survived filtering; skip comment")
        return 0

    body = _render(cands, modules, cfg, pr_number)
    print(body, "\n")

    if dry_run:
        print("(dry-run: no comment, no review request)")
        return 0

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        path = f.name
    prior = _existing_comment_id(owner, name, pr_number, str(workspace))
    if prior:
        gh_api(["api", "-X", "PATCH", f"repos/{owner}/{name}/issues/comments/{prior}",
                "-F", f"body=@{path}"], cwd=str(workspace))
        print(f"updated existing recommendation comment {prior}")
    else:
        gh_api(["pr", "comment", pr_number, "--body-file", path], cwd=str(workspace))

    reviewers = [c for c in (c.key for c in cands[: cfg.top_n])]
    if reviewers:
        try:
            gh_api([
                "api", "-X", "POST",
                f"repos/{owner}/{name}/pulls/{pr_number}/requested_reviewers",
                "-f", f"reviewers={','.join(reviewers)}",
            ])
            print(f"requested reviewers: {reviewers}")
        except RuntimeError as e:
            # e.g. reviewers are not collaborators of this fork — non-fatal
            print(f"warning: could not request reviewers ({e}); comment still posted")
    return 0


def _pr_json(owner: str, name: str, pr_number: str) -> dict:
    raw = gh_api([
        "pr", "view", pr_number, "--repo", f"{owner}/{name}",
        "--json", "files,author,createdAt,title,number",
    ])
    return json.loads(raw)


def _existing_comment_id(owner: str, name: str, pr_number: str, cwd: str) -> int | None:
    """Id of our own recommendation comment, if the PR already has one (edit-in-place)."""
    raw = gh_api(["api", f"repos/{owner}/{name}/issues/{pr_number}/comments"], cwd=cwd)
    for c in json.loads(raw):
        author = str((c.get("user") or {}).get("login", ""))
        if author.startswith("github-actions") and c.get("body", "").startswith("## 🤖 Reviewer 推荐"):
            return c["id"]
    return None


def _canonical(history, ident):
    from .history import AuthorHistory  # local import to avoid cycle at module load

    out: dict[str, AuthorHistory] = {}
    who_map = canonical_identities(history, ident)
    for who, h in history.items():
        tgt = out.setdefault(who_map[who], AuthorHistory())
        tgt.total_commits += h.total_commits
        if h.last_active and (tgt.last_active is None or h.last_active > tgt.last_active):
            tgt.last_active = h.last_active
        for m, ms in h.modules.items():
            t = tgt.modules.setdefault(m, type(ms)())
            t.commits += ms.commits
            t.weight += ms.weight
            if ms.last and (t.last is None or ms.last > t.last):
                t.last = ms.last
    return out


def _render(cands, modules, cfg, pr_number) -> str:
    lines = [
        "## 🤖 Reviewer 推荐",
        "",
        f"本 PR 涉及模块：`{'`, `'.join(m for m in modules if m != UNASSIGNED) or UNASSIGNED}`",
        "",
        "| Reviewer | 分数 | 依据 |",
        "|---|---|---|",
    ]
    for c in cands[: cfg.top_n]:
        bits = []
        for m, (nc, _cw, nr, _rw) in sorted(
            c.module_detail.items(), key=lambda kv: -(kv[1][1] + kv[1][3])
        ):
            parts = []
            if nc:
                parts.append(f"{nc} commits")
            if nr:
                parts.append(f"{nr} reviews")
            if parts:
                bits.append(f"`{m}` " + "+".join(parts))
        why = " · ".join(bits) or "-"
        if c.coupling > 0:
            why += " · **跨模块覆盖**"
        lines.append(f"| @{c.key} | {c.score:.1f} | {why} |")
    lines += [
        "",
        "<details><summary>评分依据（可折叠）</summary>",
        "",
        "信号 = 该模块内的 commit 历史 + 历史 review 记录（均按时间半衰期 180 天衰减加权）；",
        "跨模块 PR 对在所有涉及模块均有贡献者额外加分。自动请求了上表 reviewer。",
        "</details>",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
