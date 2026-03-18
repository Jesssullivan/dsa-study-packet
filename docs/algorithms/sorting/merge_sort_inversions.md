---
title: Merge Sort Inversions
---

# Merge Sort Inversions

## Problem

Count the number of inversions in an array. An inversion is a pair
(i, j) where i < j but nums[i] > nums[j].

## Approach

Modified merge sort. During the merge step, when an element from
the right half is placed before elements remaining in the left
half, those left-half elements all form inversions with it.

## When to Use

Counting disorder in sequences — "number of inversions", "how far
from sorted", "Kendall tau distance". Modified merge sort counts
cross-half inversions during the merge step. Also: rank correlation.

## Complexity

| | |
|---|---|
| **Time** | `O(n log n)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.sorting.merge_sort_inversions
        options:
          show_source: true

=== "Tests"

    ```python title="tests/sorting/test_merge_sort_inversions.py"
    --8<-- "tests/sorting/test_merge_sort_inversions.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge sorting merge_sort_inversions`

        Then implement the functions to make all tests pass.
        Use `just study sorting` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.sorting.merge_sort_inversions
            options:
              show_source: true
