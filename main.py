#!/usr/bin/env python3
"""Entry program for news-image-20261125.

Copies the pre-drawn front page (entry.png, built by gen_image.py in this
repository) to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, no
network, deterministic: the same bytes are written on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    sys.exit(main())
