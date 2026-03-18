"""Single Number — find the element appearing once (others twice).

Problem:
    Given a non-empty array where every element appears twice except
    for one, find that single element.

Approach:
    XOR all elements. Since a ^ a = 0 and a ^ 0 = a, all pairs
    cancel out, leaving only the single element.

When to use:
    XOR uniqueness — "find the element appearing once while others appear
    twice". XOR cancels pairs: a ^ a = 0. Extends to "two unique numbers"
    by splitting on a differing bit. Keywords: "unique", "missing", "duplicate".

Complexity:
    Time:  O(n)
    Space: O(1)
"""

from collections.abc import Sequence


def single_number(nums: Sequence[int]) -> int:
    """Return the element that appears exactly once.

    >>> single_number([4, 1, 2, 1, 2])
    4
    >>> single_number([1])
    1
    """
    result = 0
    for n in nums:
        result ^= n
    return result
