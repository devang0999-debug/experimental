"""A minimal LRU cache built on OrderedDict, with hit/miss stats."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Hashable, Iterator


class LRUCache:
    """Fixed-capacity least-recently-used cache.

    Accessing or setting a key marks it most-recently-used. When the cache is
    full, the least-recently-used entry is evicted on insert.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._store: "OrderedDict[Hashable, Any]" = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self._store:
            self._store.move_to_end(key)
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return default

    def put(self, key: Hashable, value: Any) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self.capacity:
            self._store.popitem(last=False)  # drop least-recently-used

    def __contains__(self, key: Hashable) -> bool:
        return key in self._store

    def __len__(self) -> int:
        return len(self._store)

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._store)

    def stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "size": len(self._store)}


if __name__ == "__main__":
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")          # 'a' is now most-recently-used
    cache.put("c", 3)       # evicts 'b'
    print("b in cache:", "b" in cache)
    print("keys:", list(cache))
    print("stats:", cache.stats())
