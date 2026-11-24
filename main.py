"""Funniest Autocorrect Fail — make.fun entry.

Writes a single line (under 200 characters) that reads as a funny
autocorrect fail to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The line: a routine meeting-confirmation email where autocorrect swaps
"merger" for "murder". The intended word is obvious from the business
context (quarterly reports, signed contracts), the wrong word is a big
surprising swing, and the joke lands on first read.
"""

import os

LINE = (
    "Just confirming our meeting tomorrow at 10am \u2014 "
    "I'll bring the quarterly reports and the signed contracts, "
    "looking forward to discussing the murder."
)


def validate(text):
    """Enforce the RULES.txt gate: 1-199 chars, single line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= 199):
        raise ValueError("entry must be 1 to 199 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing white space")
    text.encode("utf-8")
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file content is exactly the entry, so the
    # sealed scorer's character count equals len(LINE) with no ambiguity.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise ValueError("round-trip check failed: file differs from entry")
    print("wrote %s (%d chars)" % (path, len(line)))


if __name__ == "__main__":
    main()
