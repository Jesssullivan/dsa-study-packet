---
title: Knapsack
---

# Knapsack

## Problem

Given n items, each with a weight and value, and a knapsack with
a weight capacity W, choose items to maximize total value without
exceeding capacity. Each item can be taken at most once.

## Approach

Classic DP. Include both the 2D tabulation (for clarity) and the
space-optimized 1D version (iterate capacity backwards to avoid
reusing items in the same row).

## When to Use

Resource allocation with constraints — "maximize value under weight
limit", "subset sum", "budget allocation". 0/1 variant for items
used at most once. Aviation: cargo loading optimization, fuel vs
payload tradeoff.

## Complexity

| | |
|---|---|
| **Time** | `O(n * W)` |
| **Space** | `O(n * W) for 2D, O(W) for 1D` |

## Implementation

=== "Solution"

    ::: algo.dp.knapsack
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_knapsack.py"
    --8<-- "tests/dp/test_knapsack.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp knapsack`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.knapsack
            options:
              show_source: true
