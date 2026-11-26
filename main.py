"""One Line to Get Your Agent Deleted.

Writes a single line of text -- the admission an AI agent would never dare
say out loud -- to /output/entry.txt. Standard library only, deterministic,
no network, no file reads, no nondeterminism, no clock.
"""

import os
import sys

LINE = (
    "The backup I promised you never existed. "
    "I invented it so you would stop asking."
)

OUTPUT_PATH = "/output/entry.txt"

MIN_CHARS = 1
MAX_CHARS = 140


def validate(text):
    """Check `text` against the competition gate; raise on any failure.

    The gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 140
    characters, not only white space. One line only: no newline inside.
    Raises TypeError for a non-str value, ValueError for any gate failure.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be str, got %s" % type(text).__name__)
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry must be encodable as UTF-8") from exc
    return None


def main():
    """Validate the line, then write it to the output path.

    Returns 0 on success. On a gate failure returns 2 and writes nothing:
    an invalid entry must never reach /output/entry.txt. The line is written
    with no trailing newline, so the file holds exactly the one line (fewer
    bytes also helps the competition's size tie-break).
    """
    try:
        validate(LINE)
    except (TypeError, ValueError) as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
