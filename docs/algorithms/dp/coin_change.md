---
title: Coin Change
---

# Coin Change

## Problem

Given an array of coin denominations and a target amount, return the
fewest number of coins needed to make that amount. Return -1 if it
cannot be made.

## Approach

Bottom-up DP. dp[a] holds the minimum coins for amount a.
For each amount from 1..target, try every coin and take the min.

## When to Use

Classic "minimum cost to reach target" DP. Any problem where you choose
from a set of options to reach a goal with minimum steps/cost.
Variations: unbounded knapsack, minimum operations.

## Complexity

| | |
|---|---|
| **Time** | `O(amount * len(coins))` |
| **Space** | `O(amount)` |

## Implementation

=== "Solution"

    ::: algo.dp.coin_change
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_coin_change.py"
    --8<-- "tests/dp/test_coin_change.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp coin_change`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.coin_change
            options:
              show_source: true
