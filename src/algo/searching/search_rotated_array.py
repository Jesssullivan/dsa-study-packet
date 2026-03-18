"""Search in rotated sorted array.

Problem:
    An array sorted in ascending order was rotated at some pivot.
    Given a target value, return its index or -1. All values are
    distinct.

Approach:
    Modified binary search. At each step, determine which half is
    sorted (compare nums[lo] to nums[mid]). Then check whether the
    target lies within the sorted half to decide which side to search.

When to use:
    Invariant-based binary search — array is sorted but shifted/rotated.
    Identify which half is sorted, then decide which side to search.
    Keywords: "rotated sorted array", "shifted sequence", "cyclic order".

Complexity:
    Time:  O(log n)
    Space: O(1)
"""

from collections.abc import Sequence


def search_rotated(nums: Sequence[int], target: int) -> int:
    """Return the index of *target* in a rotated sorted array, or -1.

    >>> search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
    4
    >>> search_rotated([4, 5, 6, 7, 0, 1, 2], 3)
    -1
    >>> search_rotated([1], 1)
    0
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1
