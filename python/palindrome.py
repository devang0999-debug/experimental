"""Tiny scratch script: palindrome check, ignoring case and spaces."""


def is_palindrome(text: str) -> bool:
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    for s in ("racecar", "hello", "A man a plan a canal Panama"):
        print(f"{s!r}: {is_palindrome(s)}")
