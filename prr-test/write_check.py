# SPDX-License-Identifier: Apache-2.0
"""Test only: the functions of the action that post and edit its comment, against the real API, with the
token of the job that runs this.

Usage: write_check.py <directory of the recommender package> <owner/name> <pull request number>

Every comment this script deals with names nobody. In this order:

1. Two comments written with the token, under the title of the action and under that of an earlier
   version of it, without the record line that marks the action's own. The action lists none of them
   as its own, and says so.
2. A new recommendation comment, through the function that posts it: one comment more, its text back
   as sent, the two others untouched.
3. The same function again with other text: the comment is edited in place, not duplicated, and the
   two others are still untouched.

The comments this script made are deleted before it exits, whatever happened. Exit status 1 when a
check failed.
"""
import json
import os
import subprocess
import sys
import tempfile
import traceback

sys.path.insert(0, sys.argv[1])
from reviewer_recommender import action  # noqa: E402

REPO, PR = sys.argv[2], int(sys.argv[3])
OWNER, NAME = REPO.split("/", 1)
GH = os.environ.get("GH_BIN", "gh")      # as the action calls it
RESULTS = []


def say(*parts):
    print("write check: " + " ".join(str(p) for p in parts), flush=True)


def gh(*args):
    """`gh api`, the answer parsed. A failed call ends the script."""
    proc = subprocess.run([GH, "api", *args], capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        say(f"FAIL gh api {' '.join(args)[:90]} answered: {' '.join(proc.stderr.split())[:200]}")
        sys.exit(1)
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def listed():
    """The comments of the pull request, oldest first, as the REST API lists them."""
    return gh(f"repos/{REPO}/issues/{PR}/comments")


def ids():
    return [c["id"] for c in listed()]


def one(i):
    return next(c for c in listed() if c["id"] == i)


def expect(ok, what, got=""):
    RESULTS.append(bool(ok))
    say(("PASS " if ok else "FAIL ") + what + ("" if ok else f" (got {got!r})"))


def body(text):
    """A comment laid out as the action lays out its own: the title, a line, a line GitHub does not
    show, and the record, empty because nobody was requested."""
    return "\n".join([action.MARKER, "", text, "",
                      f"<!-- not shown by GitHub; {len(text)} characters above -->", "", action._record_line([])])


DECOYS = [
    action.MARKER + "\n\nWrite check: under the title of the action, written by the account behind the token, "
    "without the record that marks the action's own comment. It names nobody.\n",
    action.OLD_MARKERS[0] + "\n\nWrite check: under the title of an earlier version of the action, written by "
    "the account behind the token, without a record. It names nobody.\n",
]
FIRST = body("Write check: the first text of a comment posted through the code of the action. It names nobody.")
SECOND = body("Write check: the second text of the same comment, put there through the code of the action. "
              "It names nobody.")
assert "@" not in FIRST + SECOND + "".join(DECOYS), "a comment of the check names somebody"

before, made, mine, ok = ids(), [], None, True
try:
    for text in DECOYS:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as f:
            f.write(text)
        made.append(gh("-X", "POST", f"repos/{REPO}/issues/{PR}/comments", "-F", f"body=@{f.name}")["id"])
        os.unlink(f.name)
    say("decoys", *made, "written by", one(made[0])["user"]["login"])

    # 1. What the action lists as its own: nothing. It says about each decoy that it leaves it alone.
    ours = action._our_comments(OWNER, NAME, PR)
    expect([c.id for c in ours] == [], "the action counts none of the two as its own", [c.id for c in ours])

    # 2. A new comment, through the function the action posts with.
    action._post_comment(OWNER, NAME, PR, FIRST, ours)
    ours = action._our_comments(OWNER, NAME, PR)
    expect(len(ours) == 1 and ours[0].body == FIRST and ours[0].requested == (),
           "after posting, the action counts one comment as its own, its text as sent, nobody recorded",
           [(c.id, c.body == FIRST, c.requested) for c in ours])
    mine = ours[0].id if len(ours) == 1 else None
    expect(ids() == before + made + [mine], "one comment was added, and it is that one", ids())
    if mine is not None:
        got = one(mine)
        expect(got["body"] == FIRST, f"comment {mine} is back as sent, hidden line included", got["body"][-60:])
        expect(got["user"]["login"] == "github-actions[bot]", "written by the account of the workflow", got["user"]["login"])

    # 3. Other text: edited in place.
    action._post_comment(OWNER, NAME, PR, SECOND, ours)
    later = action._our_comments(OWNER, NAME, PR)
    expect([c.id for c in later] == [mine] and bool(later) and later[0].body == SECOND,
           "posted to again: the same comment, with the new text", [(c.id, c.body == SECOND) for c in later])
    expect(ids() == before + made + [mine], "the edit added no comment", ids())
    if mine is not None:
        expect(one(mine)["body"] == SECOND, f"comment {mine} has the new text, as sent")

    for i, text in zip(made, DECOYS):
        expect(one(i)["body"] == text, f"decoy {i} is as it was posted")
    query = ("query($owner: String!, $name: String!, $number: Int!) { repository(owner: $owner, name: $name) { "
             "pullRequest(number: $number) { comments(first: 100) { nodes { databaseId viewerDidAuthor } } } } }")
    answer = json.loads(subprocess.run(
        [GH, "api", "graphql", "-f", f"query={query}", "-f", f"owner={OWNER}", "-f", f"name={NAME}", "-F", f"number={PR}"],
        capture_output=True, text=True, encoding="utf-8", check=True).stdout)
    flags = {n["databaseId"]: n["viewerDidAuthor"] for n in answer["data"]["repository"]["pullRequest"]["comments"]["nodes"]}
    expect(all(flags.get(i) is True for i in made + [mine]), "GitHub says the token's account wrote all three",
           [flags.get(i) for i in made + [mine]])
finally:
    # An exception on its way up is swallowed by the exit below: said here instead, so that a run that
    # broke off after its last passing check does not pass.
    broke = sys.exc_info()[0]
    if broke is not None and broke is not SystemExit:
        traceback.print_exc()
        expect(False, "the check ran to its end", broke.__name__)
    for i in ([mine] if mine is not None else []) + made:
        subprocess.run([GH, "api", "-X", "DELETE", f"repos/{REPO}/issues/comments/{i}"], capture_output=True)
    left = [i for i in ids() if i not in before]
    expect(left == [], "the comments of the check are deleted again", left)
    ok = all(RESULTS)
    say(f"{sum(RESULTS)} of {len(RESULTS)} checks pass")
sys.exit(0 if ok else 1)
