# SPDX-License-Identifier: Apache-2.0
"""Thin wrapper so the composite action can run one file without PYTHONPATH setup."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("GITHUB_WORKSPACE", os.getcwd())

from reviewer_recommender.action import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
