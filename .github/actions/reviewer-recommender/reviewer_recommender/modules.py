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
"""Repository module discovery and file -> module mapping.

Resolution order (generic, no hard-coded repo layout):
  1. Maven <module> entries from pom.xml files (recursive, depth <= 2)
  2. Directories containing a build marker (go.mod, CMakeLists.txt, ...) at depth <= 2
  3. Fallback: top-level directories
A file maps to the longest-matching module directory prefix.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

POM = "pom.xml"
BUILD_MARKERS = (
    "go.mod", "CMakeLists.txt", "pyproject.toml", "setup.py",
    "package.json", "Cargo.toml", "build.gradle", "Makefile",
)
SKIP_DIRS = (".git", ".github", "target", "node_modules", "build", "out", "dist")


@dataclass(frozen=True)
class ModuleMap:
    modules: tuple[str, ...]  # repo-relative posix dirs, longest first

    def of(self, path: str) -> str:
        """Return the module a file belongs to ('(root)' if none matches)."""
        for m in self.modules:
            if path == m or path.startswith(m + "/"):
                return m
        return "(root)"

    def of_many(self, paths) -> dict[str, list[str]]:
        """module -> files"""
        out: dict[str, list[str]] = {}
        for p in paths:
            out.setdefault(self.of(p), []).append(p)
        return out


def _pom_modules(pom: Path) -> list[str]:
    try:
        root = ET.parse(pom).getroot()
    except (ET.ParseError, OSError):
        return []
    mods = []
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]  # strip xml namespace
        text = (el.text or "").strip()
        if tag == "module" and text and "${" not in text:
            mods.append(text)
    return mods


def _poms_upto(root: Path, max_depth: int = 2) -> list[Path]:
    """pom.xml files in dirs up to `max_depth` below root (root pom = depth 0)."""
    out: list[Path] = []
    root = root.resolve()

    def walk(d: Path, depth: int) -> None:
        pom = d / POM
        if pom.is_file():
            out.append(pom)
        if depth >= max_depth:
            return
        try:
            entries = sorted(d.iterdir())
        except OSError:
            return
        for e in entries:
            if e.is_dir() and not e.name.startswith(SKIP_DIRS):
                walk(e, depth + 1)

    walk(root, 0)
    return out


def _dir_ok(d: Path) -> bool:
    return d.is_dir() and not d.name.startswith(SKIP_DIRS)


def build_module_map(root: Path) -> ModuleMap:
    root = root.resolve()
    mods: set[str] = set()

    # 1. Maven modules
    for pom in _poms_upto(root):
        base = pom.parent
        for m in _pom_modules(pom):
            target = (base / m).resolve()
            try:
                rel = target.relative_to(root).as_posix()
            except ValueError:
                continue  # outside repo (../ etc.)
            if rel != "." and _dir_ok(target):
                mods.add(rel)

    # 2. Build-marker directories (depth 1 and 2)
    for d in list(root.glob("*")) + list(root.glob("*/*")):
        if _dir_ok(d) and any((d / mk).is_file() for mk in BUILD_MARKERS):
            try:
                rel = d.relative_to(root).as_posix()
            except ValueError:
                continue
            if rel not in ("", "."):
                mods.add(rel)

    # 3. Fallback: top-level dirs
    if not mods:
        mods = {p.name for p in root.glob("*") if _dir_ok(p)}

    return ModuleMap(tuple(sorted(mods, key=lambda m: (-m.count("/"), -len(m)))))
