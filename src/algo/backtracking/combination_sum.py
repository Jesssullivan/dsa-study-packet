"""Combination Sum — find combinations that sum to target.

Problem:
    Given an array of distinct positive integers (candidates) and a
    target integer, return all unique combinations where the chosen
    numbers sum to target. The same number may be used unlimited times.

Approach:
    Sort candidates, then backtrack. Start from the current index
    (not 0) to avoid duplicate combinations. Prune when the candidate
    exceeds the remaining target.

When to use:
    Partition into target — "all combinations summing to T", "coin change
    enumerate", "ways to split a budget". Unlimited reuse variant; start
    from current index to avoid duplicate combos. See also: dp/coin_change.

Complexity:
    Time:  O(2^target)  (bounded by target / min(candidates))
    Space: O(target / min(candidates))  (recursion depth)
"""

from collections.abc import Sequence


def combination_sum(candidates: Sequence[int], target: int) -> list[list[int]]:
    """Return all combinations of *candidates* that sum to *target*.

    >>> combination_sum([2, 3, 6, 7], 7)
    [[2, 2, 3], [7]]
    """
    result: list[list[int]] = []
    sorted_cands = sorted(candidates)

    def backtrack(start: int, path: list[int], remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(sorted_cands)):
            c = sorted_cands[i]
            if c > remaining:
                break
            path.append(c)
            backtrack(i, path, remaining - c)
            path.pop()

    backtrack(0, [], target)
    return result
