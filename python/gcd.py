"""Tiny scratch script: greatest common divisor via Euclid's algorithm."""


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    print(gcd(48, 18))
    print(gcd(1071, 462))
