"""Entry for One Line, One Laugh: write a single funny line.

The whole entry is one sentence. The program checks the sentence
against the gate (UTF-8 text, 1 to 200 characters, one line, not
only whitespace) and then writes it to /output/entry.txt exactly
as written here, with no trailing newline added.
"""

import sys
from pathlib import Path

LINE = (
    "I returned a library book fourteen years late, "
    "and the librarian whispered, \"We've been waiting.\""
)

OUTPUT_PATH = Path("/output/entry.txt")
MIN_CHARS = 1
MAX_CHARS = 200


def check_line(text):
    """Raise ValueError unless text passes every gate rule."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError("entry length out of range: %d" % len(text))
    text.encode("utf-8")
    return text


def write_entry(text, path=OUTPUT_PATH):
    """Write the checked line to the output file as raw UTF-8 bytes."""
    data = check_line(text).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def main():
    try:
        size = write_entry(LINE)
    except ValueError as problem:
        print("invalid entry: %s" % problem, file=sys.stderr)
        return 1
    print("wrote %d bytes to %s" % (size, OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
