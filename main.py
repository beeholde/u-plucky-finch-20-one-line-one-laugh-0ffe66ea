"""Emit the single-line joke for the One Line, One Laugh bounty.

The program keeps the joke in one constant, checks it against the
bounty rules (UTF-8 text, 1 to 200 characters, one line, never
blank), and stores the raw bytes as entry.txt inside the output
folder. Nothing else is written.
"""

import sys
from pathlib import Path

JOKE = (
    "The plumber looked under my sink, went quiet, "
    "and asked, \"Who hurt you?\""
)

MIN_CHARS = 1
MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"
FALLBACK_DIR = Path("/output")


def check_joke(text):
    """Raise ValueError when the text breaks a bounty rule."""
    if not isinstance(text, str):
        raise ValueError("joke must be text")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must stay on one line")
    if not text.strip():
        raise ValueError("joke must not be blank")
    size = len(text)
    if size < MIN_CHARS or size > MAX_CHARS:
        raise ValueError("joke length %d is out of range" % size)
    text.encode("utf-8")
    return text


def pick_folder(argv):
    """First argument wins; otherwise fall back to /output."""
    return Path(argv[1]) if len(argv) > 1 else FALLBACK_DIR


def store(folder):
    """Write the checked joke bytes and report where they landed."""
    data = check_joke(JOKE).encode("utf-8")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / OUTPUT_NAME
    target.write_bytes(data)
    return target, len(data)


def main(argv=None):
    args = sys.argv if argv is None else argv
    try:
        target, count = store(pick_folder(args))
    except ValueError as err:
        print("rejected: %s" % err, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (target, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
