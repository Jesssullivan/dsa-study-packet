"""Merge Sort Inversions — count inversions using merge sort.

Problem:
    Count the number of inversions in an array. An inversion is a pair
    (i, j) where i < j but nums[i] > nums[j].

Approach:
    Modified merge sort. During the merge step, when an element from
    the right half is placed before elements remaining in the left
    half, those left-half elements all form inversions with it.

When to use:
    Counting disorder in sequences — "number of inversions", "how far
    from sorted", "Kendall tau distance". Modified merge sort counts
    cross-half inversions during the merge step. Also: rank correlation.

Complexity:
    Time:  O(n log n)
    Space: O(n)
"""

from collections.abc import Sequence


def count_inversions(nums: Sequence[int]) -> int:
    """Return the number of inversions in *nums*.

    >>> count_inversions([2, 4, 1, 3, 5])
    3
    >>> count_inversions([5, 4, 3, 2, 1])
    10
    """
    if len(nums) <= 1:
        return 0

    arr = list(nums)
    _, count = _merge_sort(arr, 0, len(arr) - 1)
    return count


def _merge_sort(arr: list[int], lo: int, hi: int) -> tuple[list[int], int]:
    if lo >= hi:
        return arr, 0

    mid = (lo + hi) // 2
    _, left_inv = _merge_sort(arr, lo, mid)
    _, right_inv = _merge_sort(arr, mid + 1, hi)
    split_inv = _merge(arr, lo, mid, hi)

    return arr, left_inv + right_inv + split_inv


def _merge(arr: list[int], lo: int, mid: int, hi: int) -> int:
    left = arr[lo : mid + 1]
    right = arr[mid + 1 : hi + 1]

    inversions = 0
    i = j = 0
    k = lo

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            inversions += len(left) - i
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return inversions
