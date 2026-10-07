"""Iterate any iterable in fixed-size chunks, lazily."""

from __future__ import annotations

from itertools import islice
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield lists of up to ``size`` items from ``iterable``.

    Works on any iterable (including unbounded generators) without materializing
    the whole input. The final chunk may be shorter than ``size``.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            return
        yield batch


if __name__ == "__main__":
    for group in chunked(range(10), 3):
        print(group)
