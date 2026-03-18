---
title: Two Sum
---

# Two Sum

## Problem

Given an array of integers and a target, return the indices of the
two numbers that add up to the target. Each input has exactly one
solution and you may not use the same element twice.

## Approach

Single-pass hash map. For each element, compute the complement
(target - current). If the complement is already in the map, return
both indices. Otherwise store current value -> index.

## When to Use

Any problem asking "find pair with property X" — hash map for O(1) lookups.
Also: complement problems, two-number sum/difference/product.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.arrays.two_sum
        options:
          show_source: true

=== "Tests"

    ```python title="tests/arrays/test_two_sum.py"
    --8<-- "tests/arrays/test_two_sum.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge arrays two_sum`

        Then implement the functions to make all tests pass.
        Use `just study arrays` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.arrays.two_sum
            options:
              show_source: true
