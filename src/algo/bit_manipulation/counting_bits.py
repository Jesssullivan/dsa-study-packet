"""Counting Bits — count 1-bits for all numbers 0..n.

Problem:
    Given an integer n, return an array of length n+1 where the i-th
    element is the number of 1-bits in the binary representation of i.

Approach:
    DP recurrence: dp[i] = dp[i >> 1] + (i & 1).
    The number of set bits in i equals the bits in i//2 plus whether
    the least significant bit is set. Alternate counting_bits_listcomp
    gets the same answer with bin(i).count("1").

When to use:
    DP on binary representation — "count set bits for 0..n", "Hamming
    weight table". Recurrence dp[i] = dp[i>>1] + (i&1) builds on
    previously computed values. Also: popcount lookup tables.

Complexity:
    Time:  O(n)
    Space: O(n)
"""


def counting_bits(n: int) -> list[int]:
    """Return a list of bit counts for 0..n.

    >>> counting_bits(5)
    [0, 1, 1, 2, 1, 2]
    >>> counting_bits(0)
    [0]
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)  # bits(i) = bits(i//2) + i's own last bit
    return dp


# --- comprehension alternate: bin().count("1") per value (stdlib, O(n * bit-width)) ---
def counting_bits_listcomp(n: int) -> list[int]:
    """Return bit counts for 0..n using bin().count("1") (stdlib).

    >>> counting_bits_listcomp(5)
    [0, 1, 1, 2, 1, 2]
    >>> counting_bits_listcomp(0)
    [0]
    """
    return [bin(i).count("1") for i in range(n + 1)]
