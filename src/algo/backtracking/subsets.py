"""Subsets — generate all subsets of a set.

Problem:
    Given an integer array of unique elements, return all possible
    subsets (the power set). The solution must not contain duplicate
    subsets.

Approach:
    subsets: backtracking. At each index, decide to include or exclude
    the element. Append a snapshot of the current path at every node.
    subsets_bitmask is the iterative alternate: every integer from 0 to
    2^n - 1 encodes one inclusion/exclusion choice per bit.

When to use:
    Power set / feature combinations — "generate all subsets", "all
    combinations of features", "enumerate configurations". Include/exclude
    decision at each element. Also: feature selection, test coverage sets.

Complexity:
    Time:  O(n * 2^n)
    Space: O(n)  (excluding output; recursion depth is n)
"""

from collections.abc import Sequence


def subsets(nums: Sequence[int]) -> list[list[int]]:
    """Return all subsets of *nums*.

    >>> sorted(subsets([1, 2, 3]), key=len)
    [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    """
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        # snapshot copy -- path is reused and mutated across the whole walk
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            # i + 1 (not i): each element is used at most once per subset,
            # unlike combination_sum's unlimited-reuse variant
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


# --- iterative alternate: bitmask enumeration over 2^n choices ---
def subsets_bitmask(nums: Sequence[int]) -> list[list[int]]:
    """Return all subsets of *nums* by enumerating bitmasks.

    >>> sorted(subsets_bitmask([1, 2, 3]), key=len)
    [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    """
    n = len(nums)
    return [[nums[i] for i in range(n) if mask & (1 << i)] for mask in range(1 << n)]
