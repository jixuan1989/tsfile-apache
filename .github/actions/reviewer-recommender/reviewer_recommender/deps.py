# SPDX-License-Identifier: Apache-2.0
"""Maven reactor dependency graph -> module adjacency.

Parses each module's pom.xml coordinates (groupId:artifactId) and its
<dependencies>; edges are kept only between modules of the same reactor
(i.e. directories known to the ModuleMap). Adjacency is bidirectional:
a seam is relevant in both directions (I depend on you / you depend on me).
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .modules import ModuleMap


@dataclass(frozen=True)
class DepGraph:
    adj: dict[str, set[str]] = field(default_factory=dict)

    def neighbors(self, module: str) -> set[str]:
        return self.adj.get(module, set())


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _pom_root(pom: Path) -> ET.Element | None:
    try:
        return ET.parse(pom).getroot()
    except (ET.ParseError, OSError):
        return None


def _coordinates(pom: Path) -> tuple[str | None, str | None]:
    """(groupId, artifactId) of the pom's own project (groupId may come from <parent>)."""
    root = _pom_root(pom)
    if root is None:
        return None, None
    group: str | None = None
    parent_group = None
    artifact = None
    for el in root:  # direct children only
        t = _local(el.tag)
        if t == "groupId" and el.text:
            group = el.text.strip()
        elif t == "artifactId" and el.text:
            artifact = el.text.strip()
        elif t == "parent":
            for sub in el:
                if _local(sub.tag) == "groupId" and sub.text:
                    parent_group = sub.text.strip()
    return (group or parent_group), artifact


def _dependencies(pom: Path) -> list[tuple[str, str]]:
    root = _pom_root(pom)
    if root is None:
        return []
    deps: list[tuple[str, str]] = []
    for el in root.iter():
        if _local(el.tag) != "dependencies":
            continue
        for dep in el:
            if _local(dep.tag) != "dependency":
                continue
            g = a = None
            for sub in dep:
                t = _local(sub.tag)
                if t == "groupId" and sub.text:
                    g = sub.text.strip()
                elif t == "artifactId" and sub.text:
                    a = sub.text.strip()
            if g and a:
                deps.append((g, a))
    return deps


def build_dep_graph(root: Path, mmap: ModuleMap) -> DepGraph:
    coords: dict[tuple[str, str], str] = {}
    module_poms: dict[str, Path] = {}
    root = root.resolve()
    for m in mmap.modules:
        pom = root / m / "pom.xml"
        if not pom.is_file():
            continue
        g, a = _coordinates(pom)
        if g and a:
            coords.setdefault((g, a), m)
            module_poms[m] = pom

    adj: dict[str, set[str]] = defaultdict(set)
    for m, pom in module_poms.items():
        for g, a in _dependencies(pom):
            n = coords.get((g, a))
            if n and n != m:
                adj[m].add(n)
                adj[n].add(m)
    return DepGraph(dict(adj))
