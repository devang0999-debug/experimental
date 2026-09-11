"""Tiny scratch script: word frequency count."""

from collections import Counter


def word_count(text: str) -> dict[str, int]:
    words = [w.strip(".,!?;:").lower() for w in text.split()]
    return dict(Counter(w for w in words if w))


if __name__ == "__main__":
    sample = "the quick brown fox the lazy dog the fox"
    for word, count in word_count(sample).items():
        print(f"{word}: {count}")
