#!/usr/bin/env python3
"""news-image-20261125 entry program: publish the day's front page.

The finished page (entry.png, drawn at build time by gen_image.py)
sits next to this file. Running the program places a copy of it at
entry.png inside the directory named by the MAKEFUN_OUTPUT_DIR
environment variable, falling back to /output when that is unset.
The bytes are moved unchanged, so both grading runs produce exactly
the page that was drawn. Standard library only; nothing is fetched.
"""

import os
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "entry.png"


def publish() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(PAGE.read_bytes())
    return target


if __name__ == "__main__":
    print("published", publish())
