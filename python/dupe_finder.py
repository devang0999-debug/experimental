"""Find duplicate files under a directory by content hash."""

from __future__ import annotations

import argparse
import hashlib
import os
from collections import defaultdict


def file_hash(path: str, chunk_size: int = 65536) -> str:
    """Return the SHA-256 hex digest of a file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(root: str) -> dict[str, list[str]]:
    """Map each hash to the list of files sharing it (size prefilter first)."""
    by_size: dict[int, list[str]] = defaultdict(list)
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            try:
                by_size[os.path.getsize(path)].append(path)
            except OSError:
                continue

    by_hash: dict[str, list[str]] = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue  # unique size cannot be a duplicate
        for path in paths:
            try:
                by_hash[file_hash(path)].append(path)
            except OSError:
                continue

    return {h: p for h, p in by_hash.items() if len(p) > 1}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="directory to scan")
    args = parser.parse_args()

    dupes = find_duplicates(args.root)
    if not dupes:
        print("No duplicates found.")
        return
    for digest, paths in dupes.items():
        print(f"\n{digest[:12]}  ({len(paths)} copies)")
        for path in paths:
            print(f"  {path}")


if __name__ == "__main__":
    main()
