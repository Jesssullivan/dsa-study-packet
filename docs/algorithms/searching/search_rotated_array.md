---
title: Search Rotated Array
---

# Search Rotated Array

## Problem

An array sorted in ascending order was rotated at some pivot.
Given a target value, return its index or -1. All values are
distinct.

## Approach

Modified binary search. At each step, determine which half is
sorted (compare nums[lo] to nums[mid]). Then check whether the
target lies within the sorted half to decide which side to search.

## When to Use

Invariant-based binary search — array is sorted but shifted/rotated.
Identify which half is sorted, then decide which side to search.
Keywords: "rotated sorted array", "shifted sequence", "cyclic order".

## Complexity

| | |
|---|---|
| **Time** | `O(log n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.searching.search_rotated_array
        options:
          show_source: true

=== "Tests"

    ```python title="tests/searching/test_search_rotated_array.py"
    --8<-- "tests/searching/test_search_rotated_array.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge searching search_rotated_array`

        Then implement the functions to make all tests pass.
        Use `just study searching` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.searching.search_rotated_array
            options:
              show_source: true
