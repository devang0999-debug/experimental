"""A thread-safe token-bucket rate limiter."""

from __future__ import annotations

import threading
import time


class TokenBucket:
    """Classic token-bucket limiter.

    ``capacity`` tokens are available at most; the bucket refills at
    ``refill_rate`` tokens per second. Call :meth:`acquire` to consume tokens.
    """

    def __init__(self, capacity: float, refill_rate: float) -> None:
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive")
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._tokens = float(capacity)
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last
        self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
        self._last = now

    def acquire(self, tokens: float = 1.0, block: bool = True) -> bool:
        """Consume ``tokens``. If ``block`` is True, wait until available."""
        if tokens > self.capacity:
            raise ValueError("requested tokens exceed bucket capacity")
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
                if not block:
                    return False
                missing = tokens - self._tokens
                wait = missing / self.refill_rate
            time.sleep(wait)


if __name__ == "__main__":
    bucket = TokenBucket(capacity=5, refill_rate=2)
    start = time.monotonic()
    for i in range(10):
        bucket.acquire()
        print(f"request {i:2d} at {time.monotonic() - start:5.2f}s")
