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
"""Local CLI: recommend reviewers for a file list against a local clone.

Usage:
  python -m reviewer_recommender.cli --repo /path/to/repo --files a.java,b.cc
  python -m reviewer_recommender.cli --repo . --files @files.txt --top 5 --json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .config import Config
from .history import collect_history
from .modules import build_module_map
from .score import format_table, recommend


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Module-aware reviewer recommendation (git-history mode)")
    ap.add_argument("--repo", required=True, type=Path, help="path to a local git clone")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--files", help="comma-separated file paths (relative to repo root)")
    g.add_argument("--files-from", type=Path, help="file containing one path per line")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--window-days", type=int, default=None)
    ap.add_argument("--halflife", type=float, default=180.0)
    ap.add_argument("--exclude-author", default=None, help="PR author to exclude")
    ap.add_argument("--before", default=None, help="ISO date: evaluate with only data before it (backtest)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.files:
        files = [f.strip() for f in args.files.split(",") if f.strip()]
    else:
        files = [ln.strip() for ln in args.files_from.read_text().splitlines() if ln.strip() and not ln.startswith("#")]

    repo = args.repo.resolve()
    if not (repo / ".git").exists():
        print(f"error: {repo} is not a git repository", file=sys.stderr)
        return 2

    cfg = Config(halflife_days=args.halflife, top_n=args.top)
    if args.window_days:
        cfg = Config(halflife_days=args.halflife, top_n=args.top, window_days=args.window_days)

    if args.before:
        ref = dt.datetime.fromisoformat(args.before)
        if ref.tzinfo is None:
            ref = ref.replace(tzinfo=dt.timezone.utc)
    else:
        ref = dt.datetime.now(tz=dt.timezone.utc)
    mmap = build_module_map(repo)
    mod_of = {f: mmap.of(f) for f in files}
    modules = cfg.touched_modules(mod_of.values())

    history = collect_history(repo, mmap, cfg, ref, before=args.before)
    cands = recommend(modules, history, None, cfg, ref, pr_author=args.exclude_author)

    if args.json:
        payload = {
            "modules": modules,
            "file_map": mod_of,
            "candidates": [
                {
                    "name": c.key,
                    "score": round(c.score, 3),
                    "commit": round(c.commit_score, 3),
                    "review": 0.0,
                    "coupling": round(c.coupling, 3),
                    "detail": c.module_detail and {
                        m: {"commits": v[0], "review": v[2]} for m, v in c.module_detail.items()
                    },
                }
                for c in cands[: args.top]
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_table(cands, modules, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
