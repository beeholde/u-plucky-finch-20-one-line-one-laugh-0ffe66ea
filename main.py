"""Produce the one-line entry for the laugh bounty.

The deliverable is a single sentence stored as UTF-8 bytes in
``entry.txt``.  This module keeps the sentence in one place,
sanity-checks it against the bounty limits, and writes it out
without appending anything extra.
"""

import sys
from pathlib import Path

ENTRY_TEXT = (
    "I returned a library book fourteen years late, "
    "and the librarian whispered, \"We've been waiting.\""
)

DEFAULT_OUTPUT_DIR = Path("/output")
ENTRY_FILENAME = "entry.txt"
LOWER_LIMIT = 1
UPPER_LIMIT = 200


def validate_sentence(sentence):
    """Return the sentence unchanged, or raise if it breaks a rule."""
    if not isinstance(sentence, str):
        raise TypeError("the entry has to be a string")
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("the entry has to fit on one line")
    if sentence.strip() == "":
        raise ValueError("the entry cannot be blank")
    length = len(sentence)
    if length < LOWER_LIMIT or length > UPPER_LIMIT:
        raise ValueError("entry length %d is outside the allowed range" % length)
    sentence.encode("utf-8")
    return sentence


def resolve_output_dir(argv):
    """Use the first CLI argument as the output folder when given."""
    if len(argv) > 1:
        return Path(argv[1])
    return DEFAULT_OUTPUT_DIR


def emit_entry(output_dir):
    """Persist the checked sentence and report the destination plus size."""
    payload = validate_sentence(ENTRY_TEXT).encode("utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / ENTRY_FILENAME
    destination.write_bytes(payload)
    return destination, len(payload)


def run(argv=None):
    arguments = sys.argv if argv is None else argv
    try:
        destination, byte_count = emit_entry(resolve_output_dir(arguments))
    except (TypeError, ValueError) as error:
        print("entry rejected: %s" % error, file=sys.stderr)
        return 1
    print("entry written: %s (%d bytes)" % (destination, byte_count))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
