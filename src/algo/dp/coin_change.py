"""Coin Change — minimum coins to make amount.

Problem:
    Given an array of coin denominations and a target amount, return the
    fewest number of coins needed to make that amount. Return -1 if it
    cannot be made.

Approach:
    Bottom-up DP. dp[a] holds the minimum coins for amount a.
    For each amount from 1..target, try every coin and take the min.

When to use:
    Classic "minimum cost to reach target" DP. Any problem where you choose
    from a set of options to reach a goal with minimum steps/cost.
    Variations: unbounded knapsack, minimum operations.

Complexity:
    Time:  O(amount * len(coins))
    Space: O(amount)
"""

from collections.abc import Sequence


def coin_change(coins: Sequence[int], amount: int) -> int:
    """Return the minimum number of coins to make *amount*, or -1.

    >>> coin_change([1, 5, 10, 25], 30)
    2
    >>> coin_change([2], 3)
    -1
    """
    if amount < 0:
        return -1
    if amount == 0:
        return 0

    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)

    return dp[amount] if dp[amount] <= amount else -1
