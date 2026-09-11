"""Tiny scratch script: Fibonacci sequence up to n terms."""


def fib(n: int) -> list[int]:
    seq: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


if __name__ == "__main__":
    print(fib(15))
