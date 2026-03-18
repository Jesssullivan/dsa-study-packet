"""Two Sum — find two indices whose values sum to target.

Problem:
    Given an array of integers and a target, return the indices of the
    two numbers that add up to the target. Each input has exactly one
    solution and you may not use the same element twice.

Approach:
    Single-pass hash map. For each element, compute the complement
    (target - current). If the complement is already in the map, return
    both indices. Otherwise store current value -> index.

When to use:
    Any problem asking "find pair with property X" — hash map for O(1) lookups.
    Also: complement problems, two-number sum/difference/product.

Complexity:
    Time:  O(n)
    Space: O(n)
"""

from collections.abc import Sequence


def two_sum(nums: Sequence[int], target: int) -> tuple[int, int]:
    """Return indices of two elements that sum to *target*.

    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)
    """
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i

    msg = "no two elements sum to target"
    raise ValueError(msg)
