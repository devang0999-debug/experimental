"""Flatten arbitrarily nested iterables into a single stream."""

from __future__ import annotations

from typing import Any, Iterable, Iterator

# Types that should be yielded whole rather than descended into.
_ATOMIC = (str, bytes, bytearray)


def flatten(nested: Iterable[Any]) -> Iterator[Any]:
    """Yield leaf items from ``nested``, descending into nested iterables.

    Strings and bytes are treated as atomic leaves (not iterated character by
    character). Depth is bounded only by the input, using an explicit stack so
    deep nesting will not overflow the call stack.
    """
    stack: list[Iterator[Any]] = [iter(nested)]
    while stack:
        try:
            item = next(stack[-1])
        except StopIteration:
            stack.pop()
            continue
        if isinstance(item, _ATOMIC):
            yield item
        elif isinstance(item, Iterable):
            stack.append(iter(item))
        else:
            yield item


if __name__ == "__main__":
    data = [1, [2, 3, [4, [5]]], "ab", (6, 7)]
    print(list(flatten(data)))
