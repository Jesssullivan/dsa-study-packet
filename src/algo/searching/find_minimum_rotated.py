"""Find minimum in rotated sorted array.

Problem:
    Given a rotated sorted array of unique elements, find the minimum
    element.

Approach:
    Binary search variant. If nums[mid] > nums[hi], the minimum is in
    the right half; otherwise it is in the left half (including mid).
    Converge until lo == hi.

When to use:
    Pivot finding in a rotated sorted array — "find rotation point",
    "minimum in rotated". Compare mid vs right boundary to decide
    which half contains the pivot. See also: search_rotated_array.

Complexity:
    Time:  O(log n)
    Space: O(1)
"""

from collections.abc import Sequence


def find_min(nums: Sequence[int]) -> int:
    """Return the minimum element in a rotated sorted array.

    >>> find_min([3, 4, 5, 1, 2])
    1
    >>> find_min([4, 5, 6, 7, 0, 1, 2])
    0
    >>> find_min([1])
    1
    """
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1  # min is in the right half
        else:
            hi = mid  # mid could be the min

    return nums[lo]
