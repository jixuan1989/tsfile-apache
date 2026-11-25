# SPDX-License-Identifier: Apache-2.0
"""Local CLI: recommend reviewers for a file list against a local clone.

Uses git history only (no review signals, no login resolution), so candidates
appear under their git author name.

Usage:
  python -m reviewer_recommender.cli --repo /path/to/repo --files a.java,b.cc
  python -m reviewer_recommender.cli --repo . --files-from files.txt --top 5 --json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .config import Config
from .deps import build_dep_graph
from .history import collect_history
from .modules import build_module_map
from .score import format_table, recommend


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # keep CJK names readable on any locale
    ap = argparse.ArgumentParser(description="Module-aware reviewer recommendation (git-history mode)")
    ap.add_argument("--repo", required=True, type=Path, help="path to a local git clone")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--files", help="comma-separated file paths (relative to repo root)")
    g.add_argument("--files-from", type=Path, help="file containing one path per line (# starts a comment)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--window-days", type=int, default=365)
    ap.add_argument("--halflife", type=float, default=180.0)
    ap.add_argument("--exclude-author", default=None,
                    help="git author name to leave out (as printed by git log, before ' <email>')")
    ap.add_argument("--before", default=None, help="ISO date: evaluate with only data before it (backtest)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.files:
        files = [f.strip() for f in args.files.split(",") if f.strip()]
    else:
        lines = args.files_from.read_text(encoding="utf-8").splitlines()
        files = [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]

    repo = args.repo.resolve()
    if not (repo / ".git").exists():
        print(f"error: {repo} is not a git repository", file=sys.stderr)
        return 2

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
    dep_adj = build_dep_graph(repo, mmap).adj
    cands = recommend(modules, history, None, cfg, ref, pr_author=args.exclude_author, dep_adj=dep_adj)

    if args.json:
        top_n = cfg.effective_top_n()
        payload = {
            "modules": modules,
            "top_n": top_n,
            "low_confidence": bool(cands and cfg.is_low_confidence(cands[0].evidence_count)),
            "file_map": mod_of,
            "candidates": [
                {
                    "name": c.key,
                    "score": round(c.score, 3),
                    "commit": round(c.commit_score, 3),
                    "review": round(c.review_score, 3),
                    "coupling": round(c.coupling, 3),
                    "seam": round(c.dep_score, 3),
                    "pending": c.pending,
                    "last_active": c.last_active.isoformat() if c.last_active else None,
                    "detail": c.module_detail and {
                        m: {"commits": v[0], "review": v[2]} for m, v in c.module_detail.items()
                    },
                }
                for c in cands[:top_n]
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_table(cands, modules, cfg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
