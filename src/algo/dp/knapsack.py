"""0/1 Knapsack — maximize value within weight capacity.

Problem:
    Given n items, each with a weight and value, and a knapsack with
    a weight capacity W, choose items to maximize total value without
    exceeding capacity. Each item can be taken at most once.

Approach:
    Classic DP. Include both the 2D tabulation (for clarity) and the
    space-optimized 1D version (iterate capacity backwards to avoid
    reusing items in the same row).

When to use:
    Resource allocation with constraints — "maximize value under weight
    limit", "subset sum", "budget allocation". 0/1 variant for items
    used at most once. Aviation: cargo loading optimization, fuel vs
    payload tradeoff.

Complexity:
    Time:  O(n * W)
    Space: O(n * W) for 2D, O(W) for 1D
"""

from collections.abc import Sequence


def knapsack_2d(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> int:
    """Return the maximum value achievable using 2D DP table.

    >>> knapsack_2d([1, 3, 4, 5], [1, 4, 5, 7], 7)
    9
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    return dp[n][capacity]


def knapsack(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> int:
    """Return the maximum value achievable using 1D space optimization.

    >>> knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
    9
    """
    dp = [0] * (capacity + 1)

    for w, v in zip(weights, values, strict=True):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)

    return dp[capacity]
