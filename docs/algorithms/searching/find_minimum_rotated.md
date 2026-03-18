---
title: Find Minimum Rotated
---

# Find Minimum Rotated

## Problem

Given a rotated sorted array of unique elements, find the minimum
element.

## Approach

Binary search variant. If nums[mid] > nums[hi], the minimum is in
the right half; otherwise it is in the left half (including mid).
Converge until lo == hi.

## When to Use

Pivot finding in a rotated sorted array — "find rotation point",
"minimum in rotated". Compare mid vs right boundary to decide
which half contains the pivot. See also: search_rotated_array.

## Complexity

| | |
|---|---|
| **Time** | `O(log n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.searching.find_minimum_rotated
        options:
          show_source: true

=== "Tests"

    ```python title="tests/searching/test_find_minimum_rotated.py"
    --8<-- "tests/searching/test_find_minimum_rotated.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge searching find_minimum_rotated`

        Then implement the functions to make all tests pass.
        Use `just study searching` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.searching.find_minimum_rotated
            options:
              show_source: true
