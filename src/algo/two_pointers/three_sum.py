"""3Sum — find all unique triplets that sum to zero.

Problem:
    Given an integer array, return all unique triplets [a, b, c] such that
    a + b + c = 0. The solution must not contain duplicate triplets.

Approach:
    Sort the array. Fix one element and use two pointers on the remaining
    subarray to find pairs that sum to the negation of the fixed element.
    Skip duplicate values to avoid repeated triplets.

When to use:
    Reducing N-sum to 2-sum on a sorted array — "find triplets/k-tuples
    with property X". Fix one element, two-pointer scan the rest.
    Generalizes to k-sum by recursion down to the two-pointer base case.

Complexity:
    Time:  O(n^2)
    Space: O(1)  (excluding output)
"""

from collections.abc import Sequence


def three_sum(nums: Sequence[int]) -> list[list[int]]:
    """Return all unique triplets in *nums* that sum to zero.

    >>> three_sum([-1, 0, 1, 2, -1, -4])
    [[-1, -1, 2], [-1, 0, 1]]
    """
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    result: list[list[int]] = []

    for i in range(n - 2):
        # Skip duplicate fixed element
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue

        lo, hi = i + 1, n - 1
        while lo < hi:
            total = sorted_nums[i] + sorted_nums[lo] + sorted_nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([sorted_nums[i], sorted_nums[lo], sorted_nums[hi]])
                lo += 1
                # Skip duplicate left pointer
                while lo < hi and sorted_nums[lo] == sorted_nums[lo - 1]:
                    lo += 1

    return result
