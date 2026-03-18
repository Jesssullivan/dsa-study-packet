---
title: Quickselect
---

# Quickselect

## Problem

Given an unsorted array and integer k, return the kth smallest
element (1-indexed).

## Approach

Lomuto partition scheme. Pick a pivot, partition the array so
elements less than the pivot come before it. If the pivot lands
at position k-1 we are done; otherwise recurse on the correct
half. Randomized pivot for expected O(n).

## When to Use

Selection without full sort — "kth smallest/largest", "median",
"top K" when you don't need sorted output. O(n) average vs
O(n log n) for full sort. See also: heaps/kth_largest for streaming.

## Complexity

| | |
|---|---|
| **Time** | `O(n) average, O(n^2) worst case` |
| **Space** | `O(1)  (in-place partitioning)` |

## Implementation

=== "Solution"

    ::: algo.sorting.quickselect
        options:
          show_source: true

=== "Tests"

    ```python title="tests/sorting/test_quickselect.py"
    --8<-- "tests/sorting/test_quickselect.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge sorting quickselect`

        Then implement the functions to make all tests pass.
        Use `just study sorting` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.sorting.quickselect
            options:
              show_source: true
