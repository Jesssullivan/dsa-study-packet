---
title: Three Sum
---

# Three Sum

## Problem

Given an integer array, return all unique triplets [a, b, c] such that
a + b + c = 0. The solution must not contain duplicate triplets.

## Approach

Sort the array. Fix one element and use two pointers on the remaining
subarray to find pairs that sum to the negation of the fixed element.
Skip duplicate values to avoid repeated triplets.

## When to Use

Reducing N-sum to 2-sum on a sorted array — "find triplets/k-tuples
with property X". Fix one element, two-pointer scan the rest.
Generalizes to k-sum by recursion down to the two-pointer base case.

## Complexity

| | |
|---|---|
| **Time** | `O(n^2)` |
| **Space** | `O(1)  (excluding output)` |

## Implementation

=== "Solution"

    ::: algo.two_pointers.three_sum
        options:
          show_source: true

=== "Tests"

    ```python title="tests/two_pointers/test_three_sum.py"
    --8<-- "tests/two_pointers/test_three_sum.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge two_pointers three_sum`

        Then implement the functions to make all tests pass.
        Use `just study two_pointers` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.two_pointers.three_sum
            options:
              show_source: true
