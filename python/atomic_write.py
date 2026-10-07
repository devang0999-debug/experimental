"""Write a file atomically: write to a temp file, then rename into place."""

from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from typing import Iterator, TextIO


@contextmanager
def atomic_write(path: str, encoding: str = "utf-8") -> Iterator[TextIO]:
    """Context manager yielding a writable handle to a temp file.

    On clean exit the temp file is flushed, fsync'd, and atomically renamed to
    ``path`` (same directory, so the rename stays on one filesystem). If the
    block raises, the temp file is removed and ``path`` is left untouched.
    """
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            yield handle
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)  # atomic on POSIX and Windows
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    target = "atomic_demo.txt"
    with atomic_write(target) as f:
        f.write("committed only if this block finishes\n")
    with open(target, encoding="utf-8") as f:
        print(f.read(), end="")
    os.unlink(target)
