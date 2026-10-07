"""Levenshtein edit distance between two strings."""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Return the minimum single-character edits to turn ``a`` into ``b``.

    Edits are insertion, deletion, and substitution. Uses two rolling rows,
    so memory is O(min(len(a), len(b))).
    """
    if len(a) < len(b):
        a, b = b, a  # ensure b is the shorter string
    if not b:
        return len(a)

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            substitute = previous[j - 1] + (ca != cb)
            current.append(min(insert, delete, substitute))
        previous = current
    return previous[-1]


if __name__ == "__main__":
    for x, y in [("kitten", "sitting"), ("flaw", "lawn"), ("abc", "abc")]:
        print(f"{x!r} -> {y!r}: {levenshtein(x, y)}")
