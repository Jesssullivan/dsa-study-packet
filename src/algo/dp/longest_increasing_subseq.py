"""Longest Increasing Subsequence — length of LIS.

Problem:
    Given an integer array, return the length of the longest strictly
    increasing subsequence.

Approach:
    length_of_lis: patience sorting with binary search. Maintain a list
    of "tails" where tails[i] is the smallest tail element for an
    increasing subsequence of length i+1. For each number, use
    bisect_left to find its position and either extend or replace.
    length_of_lis_dp is the classic O(n^2) DP alternate: dp[i] is the
    LIS length ending at i, built by scanning all earlier elements.

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
        # bisect_left (not bisect_right) enforces *strictly* increasing:
        # an equal value replaces rather than extends a run
        pos = bisect.bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)
        else:
            tails[pos] = n
    return len(tails)


# --- O(n^2) DP table alternate (explicit pairwise comparisons) ---
def length_of_lis_dp(nums: Sequence[int]) -> int:
    """Return the length of the longest strictly increasing subsequence.

    >>> length_of_lis_dp([10, 9, 2, 5, 3, 7, 101, 18])
    4
    >>> length_of_lis_dp([0, 1, 0, 3, 2, 3])
    4
    """
    if not nums:
        return 0

    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
