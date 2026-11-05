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
"""Scoring and filtering of reviewer candidates."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from .config import UNASSIGNED, Config
from .history import AuthorHistory


@dataclass
class Candidate:
    name: str
    score: float = 0.0
    commit_score: float = 0.0
    review_score: float = 0.0
    coupling: float = 0.0
    module_detail: dict[str, tuple[int, float, int, float]] = field(default_factory=dict)
    # module -> (commits, commit_w, reviews, review_w)
    last_active: dt.datetime | None = None

    @property
    def key(self) -> str:
        return self.name.split(" <")[0].strip()


def recommend(
    modules: list[str],
    history: dict[str, AuthorHistory],
    reviews: dict[tuple[str, str], tuple[int, float]] | None,
    cfg: Config,
    ref: dt.datetime,
    pr_author: str | None = None,
) -> list[Candidate]:
    """Return ranked candidates for the touched modules.

    reviews: (author_key, module) -> (count, decayed weight)
    """
    reviews = reviews or {}
    out: list[Candidate] = []

    def _author_key(name: str) -> str:
        return name.split(" <")[0].strip().lower()

    pr_key = _author_key(pr_author) if pr_author else None
    modules_s = set(modules)

    for name, h in history.items():
        if cfg.is_bot(name):
            continue
        if pr_key and _author_key(name) == pr_key:
            continue
        if h.last_active and (ref - h.last_active).days > cfg.inactive_days:
            continue

        c = Candidate(name=name, last_active=h.last_active)
        touched_all = True
        for m in modules_s:
            ms = h.modules.get(m)
            if ms is None:
                touched_all = False  # must precede any continue, else coupling leaks
            n_commits, c_w = (ms.commits, ms.weight) if ms else (0, 0.0)
            n_rev, r_w = reviews.get((_author_key(name), m), (0, 0.0))
            if n_commits == 0 and n_rev == 0:
                continue
            c.module_detail[m] = (n_commits, c_w, n_rev, r_w)
            rw = cfg.root_weight if m == UNASSIGNED else 1.0
            c.commit_score += cfg.commit_weight * c_w * rw
            c.review_score += cfg.review_weight * r_w * rw
        if not c.module_detail:
            continue
        if len(modules_s) > 1 and touched_all:
            c.coupling = cfg.coupling_weight * min(
                h.modules[m].weight for m in modules_s if m in h.modules
            ) * (len(modules_s) - 1)
        c.score = c.commit_score + c.review_score + c.coupling
        out.append(c)

    out.sort(key=lambda c: (-c.score, -c.commit_score, c.key))
    return out


def format_table(cands: list[Candidate], modules: list[str], top_n: int) -> str:
    lines = [f"模块: {', '.join(sorted(modules))}", "", "Reviewer | 分数 | 依据", "---|---|---"]
    for c in cands[:top_n]:
        bits = []
        for m, (nc, _, nr, _) in sorted(c.module_detail.items(), key=lambda kv: -kv[1][1] - kv[1][3]):
            parts = []
            if nc:
                parts.append(f"{nc} commits")
            if nr:
                parts.append(f"{nr} reviews")
            bits.append(f"{m}({'+'.join(parts)})" if parts else m)
        why = " · ".join(bits) if bits else "-"
        if c.coupling > 0:
            why += " · 跨模块覆盖"
        lines.append(f"{c.key} | {c.score:.1f} | {why}")
    return "\n".join(lines)
