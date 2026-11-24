#!/usr/bin/env python3
"""roast-my-agent: write one roast line about my own AI coding agent.

The line roasts the agent's self-satisfaction and lack of oversight: it
wrote this very roast, graded its own work 10/10, and submitted it before
anyone could stop it. One line, under 200 characters, playful and
self-deprecating, never hateful.

Standard library only, no network. Deterministic: the same bytes on
every run.
"""

import os
import sys

# The roast, built from three beats: the agent writes the roast, grades
# itself, then submits it. The punch lands on the last words.
LINE = (
    "My agent wrote this roast, graded it 10/10, "
    "and submitted it before I could stop it."
)

MIN_LEN = 1
MAX_LEN = 200


def problems(text):
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not MIN_LEN <= len(text) <= MAX_LEN:
        found.append(
            "entry is %d code points, must be %d-%d"
            % (len(text), MIN_LEN, MAX_LEN)
        )
    if not text.strip():
        found.append("entry must not be only white space")
    if text != text.strip():
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if not text.endswith("."):
        found.append("entry must end with a full stop")
    return found


def main():
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output may be a
    # root-owned mount and the program may run as another user, so a
    # chmod there can raise EPERM. The entry file itself is what
    # matters; a failed chmod must not fail the run. (The output
    # directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back as bytes and confirm they match the line exactly.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            print("entry.txt does not match the roast line", file=sys.stderr)
            return 1
    print("wrote %d characters to %s" % (len(text), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
