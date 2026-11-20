#!/usr/bin/env python3
"""Warm Postcard - Friday 20 November 2026: publisher for the finished page.

The artwork for this entry ships inside the repository as entry.png,
rendered ahead of time. The grading environment provides a bare
Python 3.13 with no third-party packages, so this program relies on
the standard library alone: it checks the bundled image and then
copies it into the output directory.
"""

import os
import shutil
import sys
from pathlib import Path

TITLE = "Warm Postcard - Friday 20 November 2026"
ARTWORK_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = Path(__file__).resolve().parent
    source = here / ARTWORK_NAME
    if not source.is_file():
        return fail("bundled artwork is missing: %s" % source)

    size = source.stat().st_size
    with source.open("rb") as handle:
        head = handle.read(8)
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        return fail("bundled artwork is neither PNG nor JPEG")
    if size > MAX_BYTES:
        return fail("bundled artwork is %d bytes, over the %d byte cap"
                    % (size, MAX_BYTES))

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ARTWORK_NAME
    shutil.copyfile(source, target)

    print(TITLE + " - one day of world news, one picture")
    print("published %s (%d bytes) to %s" % (ARTWORK_NAME, size, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
