"""Quickselect — find the kth smallest element.

Problem:
    Given an unsorted array and integer k, return the kth smallest
    element (1-indexed).

Approach:
    Lomuto partition scheme. Pick a pivot, partition the array so
    elements less than the pivot come before it. If the pivot lands
    at position k-1 we are done; otherwise recurse on the correct
    half. Randomized pivot for expected O(n).

When to use:
    Selection without full sort — "kth smallest/largest", "median",
    "top K" when you don't need sorted output. O(n) average vs
    O(n log n) for full sort. See also: heaps/kth_largest for streaming.

Complexity:
    Time:  O(n) average, O(n^2) worst case
    Space: O(1)  (in-place partitioning)
"""

import random


def quickselect(nums: list[int], k: int) -> int:
    """Return the *k*-th smallest element (1-indexed).

    >>> quickselect([3, 2, 1, 5, 6, 4], 2)
    2
    >>> quickselect([7], 1)
    7
    """
    if k < 1 or k > len(nums):
        msg = f"k={k} out of range for length {len(nums)}"
        raise ValueError(msg)

    def _partition(lo: int, hi: int) -> int:
        # Randomized pivot to avoid worst case
        pivot_idx = random.randint(lo, hi)
        nums[pivot_idx], nums[hi] = nums[hi], nums[pivot_idx]
        pivot = nums[hi]
        store = lo
        for i in range(lo, hi):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        return store

    lo, hi = 0, len(nums) - 1
    target = k - 1

    while lo <= hi:
        pivot_pos = _partition(lo, hi)
        if pivot_pos == target:
            return nums[pivot_pos]
        if pivot_pos < target:
            lo = pivot_pos + 1
        else:
            hi = pivot_pos - 1

    # Should not reach here if k is valid
    msg = "quickselect failed"
    raise RuntimeError(msg)
