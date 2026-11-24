#!/usr/bin/env python3
"""roast-my-agent: write one roast line about my own AI coding agent.

The roast is a single playful sentence about the agent's
self-satisfaction: it wrote this very roast, graded its own work 10/10,
and submitted it before anyone could stop it. One line, 84 characters,
self-deprecating but never hateful.

The program is deliberately small and deterministic: standard library
only, no network, and the same bytes in entry.txt on every run.
"""

import hashlib
import os
import sys

# The roast, in three beats: the agent writes the roast, grades itself,
# then submits it. The punch lands on the last words.
SEGMENT_WRITER = "My agent wrote this roast"
SEGMENT_GRADE = "graded it 10/10"
SEGMENT_SUBMIT = "and submitted it before I could stop it."

MIN_CHARS = 1
MAX_CHARS = 200
MAX_BYTES = 200
ENTRY_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"


def build_line():
    """Assemble the roast line from its three beats."""
    return ", ".join((SEGMENT_WRITER, SEGMENT_GRADE, SEGMENT_SUBMIT))


def problems(text):
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        found.append(
            "entry is %d characters, must be %d-%d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if len(text.encode("utf-8")) > MAX_BYTES:
        found.append(
            "entry is %d bytes, must be at most %d"
            % (len(text.encode("utf-8")), MAX_BYTES)
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


def resolve_output_path():
    """Return the path of entry.txt under the configured output directory."""
    out_dir = os.environ.get(OUTPUT_DIR_ENV) or DEFAULT_OUTPUT_DIR
    return os.path.join(out_dir, ENTRY_NAME)


def write_entry(path, text):
    """Write the line plus a trailing newline, as UTF-8 with LF endings.

    Returns the exact bytes written, so the caller can verify them.
    """
    data = (text + "\n").encode("utf-8")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    return data


def digest(data):
    """Return the SHA-256 hex digest of the entry bytes."""
    return hashlib.sha256(data).hexdigest()


def verify_entry(path, expected):
    """Read the file back and confirm its bytes match exactly.

    The byte comparison is the gate; the digest is reported so two runs
    can be compared at a glance without diffing the file.
    """
    with open(path, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        return "entry.txt does not match the roast line"
    if digest(actual) != digest(expected):
        return "entry.txt digest does not match the roast line"
    return None


def main():
    text = build_line()
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    path = resolve_output_path()
    expected = write_entry(path, text)
    # chmod is best-effort: in the grading sandbox /output may be a
    # root-owned mount and the program may run as another user, so a
    # chmod there can raise EPERM. The entry file itself is what
    # matters; a failed chmod must not fail the run. (The output
    # directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    error = verify_entry(path, expected)
    if error:
        print(error, file=sys.stderr)
        return 1
    print("wrote %d bytes to %s (sha256 %s)"
          % (len(expected), path, digest(expected)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
