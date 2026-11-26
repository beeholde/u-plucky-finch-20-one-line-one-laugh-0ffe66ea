"""Deliver the single competition line as a plain text file.

Running this module writes one short joke into the chosen output
folder under the name entry.txt. The bytes on disk are exactly the
joke encoded as UTF-8, with no extra newline appended.
"""

import sys
from pathlib import Path

# The joke is kept in two pieces so the spoken punchline stays
# visually separate from the scene that sets it up.
LINE = (
    "The plumber looked under my sink, went quiet, and asked, "
    '"Who hurt you?"'
)

MIN_LENGTH = 1
MAX_LENGTH = 200


def validate(text):
    """Reject text that breaks the one-line competition rules."""
    if not isinstance(text, str):
        raise ValueError("the line must be a string")
    if "\n" in text or "\r" in text:
        raise ValueError("the line must fit on a single line")
    if not text.strip():
        raise ValueError("the line must not be blank")
    length = len(text)
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError("line length %d is outside the allowed range" % length)
    text.encode("utf-8")
    return text

FILE_NAME = "entry.txt"
DEFAULT_FOLDER = Path("/output")


def output_folder(arguments):
    """Return the folder given on the command line, else /output."""
    if len(arguments) > 1:
        return Path(arguments[1])
    return DEFAULT_FOLDER


def save_line(folder, text):
    """Validate text, then store it as UTF-8 bytes in the folder."""
    checked = validate(text)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / FILE_NAME
    payload = checked.encode("utf-8")
    path.write_bytes(payload)
    return path, len(payload)


def main(arguments=None):
    """Entry point: save the line and report the result."""
    args = sys.argv if arguments is None else arguments
    path, size = save_line(output_folder(args), LINE)
    print("saved %s (%d bytes)" % (path, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
