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
"""GitHub review history + identity resolution (login <-> git author).

All GitHub access goes through the `gh` CLI (present on Action runners).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import time
from collections import defaultdict

from .config import Config
from .modules import ModuleMap

_PR_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: MERGED, first: 50, after: $cursor,
                 orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { endCursor hasNextPage }
      nodes {
        number
        title
        createdAt
        author { login }
        files(first: 100) { nodes { path } }
        reviews(first: 100) {
          nodes { author { login } state submittedAt }
        }
      }
    }
  }
}
"""


def gh_api(args: list[str], retries: int = 3, cwd: str | None = None) -> str:
    gh = os.environ.get("GH_BIN", "gh")
    last_err = ""
    for attempt in range(retries):
        proc = subprocess.run([gh, *args], capture_output=True, text=True, cwd=cwd)
        if proc.returncode == 0:
            return proc.stdout
        last_err = proc.stderr[:300]
        time.sleep(2 * (attempt + 1))  # transient network / rate-limit backoff
    raise RuntimeError(f"gh {' '.join(args[:2])} failed: {last_err}")


def fetch_merged_prs(owner: str, name: str, max_prs: int = 100) -> list[dict]:
    """Most recent merged PRs: number, createdAt, author, files, reviews."""
    out: list[dict] = []
    cursor: str | None = None
    while len(out) < max_prs:
        args = ["api", "graphql", "-f", f"query={_PR_QUERY}", "-f", f"owner={owner}", "-f", f"name={name}"]
        if cursor:
            args += ["-f", f"cursor={cursor}"]
        raw = gh_api(args)
        data = json.loads(raw)["data"]["repository"]["pullRequests"]
        out.extend(data["nodes"])
        if not data["pageInfo"]["hasNextPage"] or not data["nodes"]:
            break
        cursor = data["pageInfo"]["endCursor"]
    return out[:max_prs]


def review_signals(
    prs: list[dict], mmap: ModuleMap, cfg: Config, ref: dt.datetime
) -> dict[tuple[str, str], tuple[int, float]]:
    """(reviewer_login, module) -> (count, decayed weight), only APPROVED/CHANGES_REQUESTED/COMMENTED count."""
    sig: dict[tuple[str, str], tuple[int, float]] = {}
    acc: dict[tuple[str, str], list[float]] = defaultdict(list)
    for pr in prs:
        if pr["createdAt"] >= ref.isoformat():
            continue  # only history before the reference point (no leakage)
        created = dt.datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
        modules = {mmap.of(f["path"]) for f in pr["files"]["nodes"]}
        for rv in pr["reviews"]["nodes"]:
            login = (rv["author"] or {}).get("login")
            if not login or cfg.is_bot(login):
                continue
            if rv["state"] not in ("APPROVED", "CHANGES_REQUESTED", "COMMENTED"):
                continue
            when = dt.datetime.fromisoformat(rv["submittedAt"].replace("Z", "+00:00"))
            if when > ref:
                continue
            w = cfg.decay(when, ref)
            for m in modules:
                acc[(login.lower(), m)].append(w)
    for k, ws in acc.items():
        sig[k] = (len(ws), sum(ws))
    return sig


def build_identity_map(owner: str, name: str, commits_to_scan: int = 500) -> dict[str, str]:
    """git email/name -> github login, resolved via the commits API (server-side email match)."""
    email_map: dict[str, str] = {}
    name_map: dict[str, str] = {}
    page = 1
    scanned = 0
    while scanned < commits_to_scan and page <= 10:
        raw = gh_api([
            "api", "-X", "GET", f"repos/{owner}/{name}/commits",
            "-f", "per_page=100", "-f", f"page={page}",
        ])
        batch = json.loads(raw)
        if not batch:
            break
        for c in batch:
            login = (c.get("author") or {}).get("login")
            info = c.get("commit", {}).get("author", {}) or {}
            email, gname = info.get("email", ""), info.get("name", "")
            if login:
                if email:
                    email_map[email.lower()] = login
                if gname:
                    name_map[gname.strip().lower()] = login
        scanned += len(batch)
        page += 1
    return {"email": email_map, "name": name_map}


def canonical_identities(history, identity: dict) -> dict[str, str]:
    """Map each 'Name <email>' history key -> login (or best-effort name)."""
    out: dict[str, str] = {}
    emap, nmap = identity["email"], identity["name"]
    for who in history:
        name, _, email = who.rpartition(" <")
        email = email.rstrip(">").lower()
        login = emap.get(email) or nmap.get(name.strip().lower())
        out[who] = login or name.strip()
    return out
