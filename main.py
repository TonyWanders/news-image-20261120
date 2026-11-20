"""make.fun entry: Sum up 20 November's world news in one image.

Simplest program: copy the image this repo holds (entry.png)
to /output/entry.png.

Deterministic: the same input bytes are copied every run, so
both runs write identical bytes. No network, no randomness,
no timestamps, no external files.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

SRC = Path(__file__).resolve().parent / "entry.png"
DEFAULT_DEST = Path("/output/entry.png")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    dest = Path(argv[0]) if argv else Path(os.environ.get("OUTPUT_PATH", DEFAULT_DEST))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, dest)
    # Verify the copy is byte-identical to the source, so a truncated
    # or partial write is caught instead of silently submitted.
    if _sha256(SRC) != _sha256(dest):
        print(f"ERROR: copied file does not match {SRC}", file=sys.stderr)
        return 1
    print(f"Wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
