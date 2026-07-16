"""Sieve of Eratosthenes: all primes up to n.

Problem:
    Given a non-negative integer n, return every prime number less than or
    equal to n, in increasing order.

Approach:
    Whiteboard form (sieve_of_eratosthenes): allocate a boolean array of size
    n + 1, mark 0 and 1 as not prime, then for each candidate p starting at 2,
    if p is still marked prime, strike every multiple of p starting at p*p
    (smaller multiples of p already got struck by a smaller prime factor).
    Collect the indices still marked prime. Pythonic form (sieve_slices):
    same invariant, but each strike pass is a single slice assignment
    (``sieve[p * p :: p]``) instead of a nested loop, and the surviving
    indices are collected with a list comprehension over ``enumerate``.

When to use:
    Precomputing all primes up to n for many repeated queries (primality
    checks, factorization prep, counting primes / pi(n)). Contrast with
    per-number trial division, which costs O(sqrt(n)) *per query*. The sieve
    amortizes that cost across every number up to n in one pass.

Complexity:
    Time:  O(n log log n)
    Space: O(n)
"""

from math import isqrt


def sieve_of_eratosthenes(n: int) -> list[int]:
    """Return every prime <= n, in increasing order.

    >>> sieve_of_eratosthenes(10)
    [2, 3, 5, 7]
    >>> sieve_of_eratosthenes(1)
    []
    """
    if n < 2:
        return []

    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0  # 0 and 1 are not prime by definition

    for p in range(2, isqrt(n) + 1):  # beyond sqrt(n), no unstruck composite remains
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):  # below p*p already struck
                is_prime[multiple] = 0

    return [i for i, prime in enumerate(is_prime) if prime]


# Pythonic slice-assignment and comprehension form
def sieve_slices(n: int) -> list[int]:
    """Return every prime <= n via strided slice assignment.

    >>> sieve_slices(10)
    [2, 3, 5, 7]
    >>> sieve_slices(1)
    []
    """
    if n < 2:
        return []

    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0

    for p in range(2, isqrt(n) + 1):
        if is_prime[p]:
            start = p * p
            # bytes(span) must be exactly as long as the strided slice it replaces
            span = len(range(start, n + 1, p))
            is_prime[start::p] = bytes(span)

    return [i for i, prime in enumerate(is_prime) if prime]
