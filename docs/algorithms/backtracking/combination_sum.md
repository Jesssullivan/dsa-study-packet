---
title: Combination Sum
---

# Combination Sum

## Problem

Given an array of distinct positive integers (candidates) and a
target integer, return all unique combinations where the chosen
numbers sum to target. The same number may be used unlimited times.

## Approach

Sort candidates, then backtrack. Start from the current index
(not 0) to avoid duplicate combinations. Prune when the candidate
exceeds the remaining target.

## When to Use

Partition into target — "all combinations summing to T", "coin change
enumerate", "ways to split a budget". Unlimited reuse variant; start
from current index to avoid duplicate combos. See also: dp/coin_change.

## Complexity

| | |
|---|---|
| **Time** | `O(2^target)  (bounded by target / min(candidates))` |
| **Space** | `O(target / min(candidates))  (recursion depth)` |

## Implementation

=== "Solution"

    ::: algo.backtracking.combination_sum
        options:
          show_source: true

=== "Tests"

    ```python title="tests/backtracking/test_combination_sum.py"
    --8<-- "tests/backtracking/test_combination_sum.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge backtracking combination_sum`

        Then implement the functions to make all tests pass.
        Use `just study backtracking` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.backtracking.combination_sum
            options:
              show_source: true
