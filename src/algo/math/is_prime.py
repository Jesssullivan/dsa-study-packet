"""Check whether one integer is prime.

Problem:
    Given an integer n, return whether n is prime. A prime is an integer greater
    than 1 with no positive divisors other than 1 and itself.

Approach:
    Reject values below 2 and small composite factors first. Then try possible
    factors through sqrt(n), checking only numbers of the form 6k - 1 and
    6k + 1. This answers one primality query without building a table of every
    prime up to n.

When to use:
    Checking one or a few individual values. Use a sieve instead when many
    queries share the same upper bound or when every prime up to n is needed.

Complexity:
    Time:  O(sqrt(n))
    Space: O(1)
"""


def is_prime(n: int) -> bool:
    """Return whether *n* is prime.

    >>> is_prime(29)
    True
    >>> is_prime(1)
    False
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    factor = 5
    while factor * factor <= n:
        if n % factor == 0 or n % (factor + 2) == 0:
            return False
        factor += 6
    return True
