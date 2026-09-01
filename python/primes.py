"""Tiny scratch script: primes under a limit via a simple sieve."""


def primes_under(limit: int) -> list[int]:
    sieve = [True] * limit
    sieve[0:2] = [False, False] if limit > 1 else sieve[0:2]
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


if __name__ == "__main__":
    print(primes_under(50))
