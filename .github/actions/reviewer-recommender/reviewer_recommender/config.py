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
"""Scoring configuration."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

BOT_PATTERNS = ("[bot]", "bot", "github-actions", "dependabot", "renovate", "codecov", "semantic-release", "copilot")
UNASSIGNED = "(root)"


@dataclass(frozen=True)
class Config:
    halflife_days: float = 180.0
    commit_weight: float = 1.0        # λc
    review_weight: float = 1.5        # λr
    coupling_weight: float = 0.5      # λx
    root_weight: float = 0.2          # (root)/infra 路径信号降权
    window_days: int = 365            # 信号采集窗口
    inactive_days: int = 365          # 超过该天数无动作则排除
    top_n: int = 3
    bot_patterns: tuple[str, ...] = field(default_factory=lambda: BOT_PATTERNS)

    def touched_modules(self, modules) -> list[str]:
        """Scoring view of a module set: infra/(root) excluded unless it is all there is."""
        real = [m for m in set(modules) if m != UNASSIGNED]
        return sorted(real) if real else [UNASSIGNED]

    def decay(self, when: dt.datetime, ref: dt.datetime) -> float:
        """Exponential time-decay weight, halflife `halflife_days`."""
        age_days = max((ref - when).total_seconds() / 86400.0, 0.0)
        return 0.5 ** (age_days / self.halflife_days)

    def is_bot(self, identity: str) -> bool:
        low = identity.lower()
        return any(p in low for p in self.bot_patterns)
