"""Streaming moving average over a fixed-size sliding window."""

from __future__ import annotations

from collections import deque
from typing import Iterable, Iterator


class MovingAverage:
    """Maintain the mean of the last ``window`` values in O(1) per update."""

    def __init__(self, window: int) -> None:
        if window <= 0:
            raise ValueError("window must be positive")
        self.window = window
        self._values: "deque[float]" = deque(maxlen=window)
        self._total = 0.0

    def add(self, value: float) -> float:
        """Add ``value`` and return the current window average."""
        if len(self._values) == self.window:
            self._total -= self._values[0]  # value about to be evicted
        self._values.append(value)
        self._total += value
        return self._total / len(self._values)

    @property
    def value(self) -> float:
        if not self._values:
            raise ValueError("no values yet")
        return self._total / len(self._values)


def rolling_mean(data: Iterable[float], window: int) -> Iterator[float]:
    """Yield the moving average after each value in ``data``."""
    avg = MovingAverage(window)
    for x in data:
        yield avg.add(x)


if __name__ == "__main__":
    print(list(rolling_mean([1, 2, 3, 4, 5, 6], window=3)))
