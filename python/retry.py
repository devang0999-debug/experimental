"""A small retry decorator with exponential backoff."""

from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(
    tries: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry the wrapped callable up to ``tries`` times.

    The wait between attempts starts at ``delay`` seconds and is multiplied by
    ``backoff`` after each failure. The last exception is re-raised if every
    attempt fails.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            wait = delay
            for attempt in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == tries:
                        raise
                    print(f"[retry] {func.__name__} failed ({exc!r}); "
                          f"attempt {attempt}/{tries}, sleeping {wait:.2f}s")
                    time.sleep(wait)
                    wait *= backoff
            raise RuntimeError("unreachable")

        return wrapper

    return decorator


if __name__ == "__main__":
    state = {"n": 0}

    @retry(tries=4, delay=0.1)
    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("not ready yet")
        return "ok"

    print(flaky())
