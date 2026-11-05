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
"""git-log based authorship signals per module.

Identity: "Name <email>" (login resolution happens in API/action mode).
"""
from __future__ import annotations

import datetime as dt
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config
from .modules import ModuleMap

SEP = "\x1f"


@dataclass
class ModuleSignal:
    commits: int = 0
    weight: float = 0.0
    last: dt.datetime | None = None

    def add(self, when: dt.datetime, cfg: Config, ref: dt.datetime) -> None:
        self.commits += 1
        self.weight += cfg.decay(when, ref)
        if self.last is None or when > self.last:
            self.last = when


@dataclass
class AuthorHistory:
    modules: dict[str, ModuleSignal] = field(default_factory=dict)
    last_active: dt.datetime | None = None
    total_commits: int = 0


def git_log(repo: Path, since: str, before: str | None = None) -> list[tuple[str, dt.datetime, list[str]]]:
    """[(author, date, [files])] in chronological reach of git log."""
    args = [
        "git", "-C", str(repo), "log", f"--since={since}",
        "--no-merges", "--name-only", f"--format=%an{SEP}%ae{SEP}%aI",
    ]
    if before:
        args.append(f"--before={before}")
    proc = subprocess.run(args, capture_output=True, text=True, check=True)
    out: list[tuple[str, dt.datetime, list[str]]] = []
    author: str | None = None
    when: dt.datetime | None = None
    files: list[str] = []
    for line in proc.stdout.splitlines():
        if SEP in line:
            if author and when:
                out.append((author, when, files))
            name, email, iso = (p.strip() for p in line.split(SEP))
            author, files = f"{name} <{email}>", []
            try:
                when = dt.datetime.fromisoformat(iso)
            except ValueError:
                when = None
        elif line.strip() and author:
            files.append(line.strip())
    if author and when:
        out.append((author, when, files))
    return out


def collect_events(
    repo: Path, mmap: ModuleMap, since: str, before: str | None = None
) -> list[tuple[str, dt.datetime, set[str]]]:
    """Raw (author, when, modules) events — parameter-independent, for tuning reuse."""
    return [
        (author, when, {mmap.of(f) for f in files})
        for author, when, files in git_log(repo, since, before)
    ]


def materialize(
    events: list[tuple[str, dt.datetime, set[str]]], cfg: Config, ref: dt.datetime
) -> dict[str, AuthorHistory]:
    history: dict[str, AuthorHistory] = {}
    for author, when, mods in events:
        h = history.setdefault(author, AuthorHistory())
        h.total_commits += 1
        if h.last_active is None or when > h.last_active:
            h.last_active = when
        for m in mods:
            h.modules.setdefault(m, ModuleSignal()).add(when, cfg, ref)
    return history


def collect_history(
    repo: Path,
    mmap: ModuleMap,
    cfg: Config,
    ref: dt.datetime,
    since_days: int | None = None,
    before: str | None = None,
) -> dict[str, AuthorHistory]:
    """git log -> per-author per-module decayed commit signals."""
    days = since_days or cfg.window_days
    since = (ref - dt.timedelta(days=days)).isoformat()
    return materialize(collect_events(repo, mmap, since, before), cfg, ref)
