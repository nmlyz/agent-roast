#!/usr/bin/env python3
"""agent-roast: write one roast line about my own AI coding agent.

The line roasts the agent's debugging habit: it litters the code with
print('here') markers and then cannot tell which one fired. One line,
under 200 characters, playful and self-deprecating, never hateful.

Standard library only, no network. Deterministic: the same bytes on
every run.
"""

import os
import sys

# The roast, built from two clauses: the setup (what the agent does) and
# the punch (what it asks next). The punch lands at the end.
LINE = (
    "My agent debugs by printing 'here' forty-seven times, "
    "then asks me which 'here' was the bug."
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
