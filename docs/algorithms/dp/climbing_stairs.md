---
title: Climbing Stairs
---

# Climbing Stairs

## Problem

You are climbing a staircase with n steps. Each time you can climb
1 or 2 steps. Return the number of distinct ways to reach the top.

## Approach

Fibonacci variant. The number of ways to reach step i equals the
sum of ways to reach step i-1 (take 1 step) and step i-2 (take 2
steps). Use two rolling variables instead of an array.

## When to Use

Counting paths / Fibonacci family — "how many ways to reach step N",
"count distinct paths with step choices". Rolling-variable DP when
each state depends on a fixed number of previous states.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.dp.climbing_stairs
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_climbing_stairs.py"
    --8<-- "tests/dp/test_climbing_stairs.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp climbing_stairs`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.climbing_stairs
            options:
              show_source: true
