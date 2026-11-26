# SPDX-License-Identifier: Apache-2.0
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
    dep_score: float = 0.0
    seams: list[str] = field(default_factory=list)   # "m↔n" 依赖接缝
    pending: int = 0                                  # 挂起的 review 请求数
    module_detail: dict[str, tuple[int, float, int, float]] = field(default_factory=dict)
    # module -> (commits, commit_w, reviews, review_w)
    last_active: dt.datetime | None = None

    @property
    def key(self) -> str:
        return self.name.split(" <")[0].strip()

    @property
    def evidence_count(self) -> int:
        """Commit+review count across touched modules (excludes (root)) — size-invariant
        confidence signal, immune to score inflation from seam/coupling bonuses."""
        return sum(
            nc + nr
            for m, (nc, _cw, nr, _rw) in self.module_detail.items()
            if m != "(root)"
        )


def recommend(
    modules: list[str],
    history: dict[str, AuthorHistory],
    reviews: dict[tuple[str, str], tuple[int, float]] | None,
    cfg: Config,
    ref: dt.datetime,
    pr_author: str | None = None,
    dep_adj: dict[str, set[str]] | None = None,
    pending: dict[str, int] | None = None,
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
    # Iterate in a fixed order: set order differs from one process to the next
    # (hash randomisation), and the comment must be the same on every run.
    order = sorted(modules_s)

    for name, h in history.items():
        if cfg.is_bot(name):
            continue
        if pr_key and _author_key(name) == pr_key:
            continue
        if h.last_active and (ref - h.last_active).days > cfg.inactive_days:
            continue

        c = Candidate(name=name, last_active=h.last_active)
        touched_all = True
        for m in order:
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
        # v2: dependency-seam bonus — history on both sides of a module boundary
        if dep_adj:
            for m in order:
                hm = h.modules.get(m)
                if not hm:
                    continue
                for nb in sorted(dep_adj.get(m, ())):
                    if nb in modules_s:
                        continue
                    hn = h.modules.get(nb)
                    if hn:
                        c.dep_score += cfg.dep_weight * min(hm.weight, hn.weight)
                        c.seams.append(f"{m}↔{nb}")
        # v2: workload balance — penalize per pending review request, cap out
        p = (pending or {}).get(_author_key(name), 0)
        if p >= cfg.max_pending:
            continue
        c.pending = p
        c.score = (c.commit_score + c.review_score + c.coupling + c.dep_score) * (
            cfg.workload_factor ** p
        )
        out.append(c)

    out.sort(key=lambda c: (-c.score, -c.commit_score, c.key))
    return out


def format_table(cands: list[Candidate], modules: list[str], cfg) -> str:
    top_n = cfg.effective_top_n()
    lines = [f"模块: {', '.join(sorted(modules))}"]
    if cands and cfg.is_low_confidence(cands[0].evidence_count):
        lines += ["⚠️ 该区域历史信号稀疏，推荐置信度低，建议结合团队实际分工判断。"]
    lines += ["", "Reviewer | 分数 | 依据", "---|---|---"]
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
        if c.seams:
            why += " · " + "、".join(c.seams[:2]) + " 接缝"
        if c.pending:
            why += f" · 待审 {c.pending}"
        lines.append(f"{c.key} | {c.score:.1f} | {why}")
    return "\n".join(lines)
