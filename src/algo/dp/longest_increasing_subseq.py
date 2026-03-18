"""Longest Increasing Subsequence — length of LIS.

Problem:
    Given an integer array, return the length of the longest strictly
    increasing subsequence.

Approach:
    Patience sorting with binary search. Maintain a list of "tails"
    where tails[i] is the smallest tail element for an increasing
    subsequence of length i+1. For each number, use bisect_left to
    find its position and either extend or replace.

When to use:
    Patience sorting / longest chain — "longest increasing subsequence",
    "longest chain of pairs", "box stacking". Binary search on tails
    array for O(n log n). Also: longest non-decreasing, envelope nesting.

Complexity:
    Time:  O(n log n)
    Space: O(n)
"""

import bisect
from collections.abc import Sequence


def length_of_lis(nums: Sequence[int]) -> int:
    """Return the length of the longest strictly increasing subsequence.

    >>> length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
    4
    >>> length_of_lis([0, 1, 0, 3, 2, 3])
    4
    """
    if not nums:
        return 0

    tails: list[int] = []
    for n in nums:
        pos = bisect.bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)
        else:
            tails[pos] = n
    return len(tails)
