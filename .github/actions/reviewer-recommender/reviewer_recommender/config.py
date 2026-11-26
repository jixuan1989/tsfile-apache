# SPDX-License-Identifier: Apache-2.0
"""Scoring configuration."""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field

# Bot detection works on words, not substrings: a login is a bot when one of its
# words (split on anything that is not a letter or digit) is a bot word, or when
# the whole login is a bot account. GitHub Apps are always "<app>[bot]". A bare
# substring test would also catch people whose handle merely contains "bot".
BOT_WORDS = ("bot", "codecov", "copilot", "dependabot", "renovate")
# Accounts whose name gives nothing away.
BOT_ACCOUNTS = ("github-actions", "semantic-release", "github-advanced-security")
UNASSIGNED = "(root)"


@dataclass(frozen=True)
class Config:
    halflife_days: float = 180.0
    commit_weight: float = 1.0        # λc
    review_weight: float = 2.5        # λr：唯一明显影响命中率的参数（2026-11-05 调参，2026-11-25 复核，DESIGN.md §8）
    coupling_weight: float = 0.5      # λx
    dep_weight: float = 0.3           # λd：依赖接缝加成（v2）
    workload_factor: float = 0.75     # 每个挂起 review 请求对总分的乘数（v2）
    max_pending: int = 6              # 挂起请求达到该数则排除（v2）
    low_confidence_min_evidence: int = 5  # top 候选触及模块证据数(commit+review)低于此 → 低置信（v2.1）
    root_weight: float = 0.2          # (root)/infra 路径信号降权
    window_days: int = 365            # 信号采集窗口
    inactive_days: int = 365          # 超过该天数无动作则排除
    top_n: int = 3
    bot_words: tuple[str, ...] = field(default_factory=lambda: BOT_WORDS)
    bot_accounts: tuple[str, ...] = field(default_factory=lambda: BOT_ACCOUNTS)

    def touched_modules(self, modules) -> list[str]:
        """Scoring view of a module set: infra/(root) excluded unless it is all there is."""
        real = [m for m in set(modules) if m != UNASSIGNED]
        return sorted(real) if real else [UNASSIGNED]

    def effective_top_n(self, requested: int | None = None) -> int:
        """Recommend at least 2 reviewers — single-name lists leave no backup (社区反馈 2026-11-05)."""
        n = requested if requested is not None else self.top_n
        return max(2, n)

    def is_low_confidence(self, evidence_count: int) -> bool:
        """Cold-module heuristic: evidence = commit+review count of the top candidate
        across touched modules. Count-based (not score-based) so it is invariant to
        repo size, decay window and bonus weights (seam/coupling can inflate scores)."""
        return evidence_count < self.low_confidence_min_evidence

    def decay(self, when: dt.datetime, ref: dt.datetime) -> float:
        """Exponential time-decay weight, halflife `halflife_days`."""
        age_days = max((ref - when).total_seconds() / 86400.0, 0.0)
        return 0.5 ** (age_days / self.halflife_days)

    def is_bot(self, identity: str) -> bool:
        """True for automation accounts. Accepts a login or a git identity
        ("Name <email>" — only the name part is looked at)."""
        login = identity.split(" <", 1)[0].strip().lower()
        if login in self.bot_accounts:
            return True
        return any(w in _words(login) for w in self.bot_words)


def _words(login: str) -> set[str]:
    return {w for w in re.split(r"[^a-z0-9]+", login) if w}
