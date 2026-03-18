"""Binary search.

Problem:
    Given a sorted array of integers and a target value, return the
    index of the target if found, otherwise return -1.

Approach:
    Both iterative and recursive implementations. Maintain lo/hi
    bounds; compute mid = lo + (hi - lo) // 2 to avoid overflow.

When to use:
    Sorted array lookup or any monotonic predicate search — "find target",
    "first/last occurrence", "search insert position". Foundation for
    bisect-based optimizations. Aviation: altitude/waypoint lookup tables.

Complexity:
    Time:  O(log n)
    Space: O(1) iterative, O(log n) recursive (call stack)
"""

from collections.abc import Sequence


def binary_search(nums: Sequence[int], target: int) -> int:
    """Return the index of *target* in sorted *nums*, or -1 if absent.

    >>> binary_search([1, 3, 5, 7, 9], 5)
    2
    >>> binary_search([1, 3, 5, 7, 9], 4)
    -1
    >>> binary_search([], 1)
    -1
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def binary_search_recursive(nums: Sequence[int], target: int) -> int:
    """Recursive binary search returning index or -1.

    >>> binary_search_recursive([2, 4, 6, 8, 10], 8)
    3
    >>> binary_search_recursive([2, 4, 6, 8, 10], 5)
    -1
    """

    def _helper(lo: int, hi: int) -> int:
        if lo > hi:
            return -1
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return _helper(mid + 1, hi)
        return _helper(lo, mid - 1)

    return _helper(0, len(nums) - 1)
