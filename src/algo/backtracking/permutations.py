"""Permutations — generate all permutations of a list.

Problem:
    Given an array of distinct integers, return all possible
    permutations in any order.

Approach:
    permutations: backtracking with a visited set. At each position,
    try every unused element, mark it used, recurse, then unmark.
    permutations_itertools is the stdlib alternate using
    itertools.permutations.

When to use:
    All orderings — "generate all permutations", "all arrangements",
    brute-force over orderings for small n. Building block for
    next-permutation and ranking/unranking algorithms.

Complexity:
    Time:  O(n * n!)
    Space: O(n)  (recursion depth + visited set)
"""

import itertools
from collections.abc import Sequence


def permutations(nums: Sequence[int]) -> list[list[int]]:
    """Return all permutations of *nums*.

    >>> sorted(permutations([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    result: list[list[int]] = []
    used = [False] * len(nums)

    def backtrack(path: list[int]) -> None:
        if len(path) == len(nums):
            # snapshot copy -- path keeps mutating after this append,
            # so appending path itself would alias every stored result
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


# --- stdlib alternate: itertools.permutations ---
def permutations_itertools(nums: Sequence[int]) -> list[list[int]]:
    """Return all permutations of *nums* using itertools.permutations.

    >>> sorted(permutations_itertools([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    return [list(p) for p in itertools.permutations(nums)]
