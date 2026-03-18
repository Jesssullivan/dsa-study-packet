---
title: Longest Increasing Subseq
---

# Longest Increasing Subseq

## Problem

Given an integer array, return the length of the longest strictly
increasing subsequence.

## Approach

Patience sorting with binary search. Maintain a list of "tails"
where tails[i] is the smallest tail element for an increasing
subsequence of length i+1. For each number, use bisect_left to
find its position and either extend or replace.

## When to Use

Patience sorting / longest chain — "longest increasing subsequence",
"longest chain of pairs", "box stacking". Binary search on tails
array for O(n log n). Also: longest non-decreasing, envelope nesting.

## Complexity

| | |
|---|---|
| **Time** | `O(n log n)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.dp.longest_increasing_subseq
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_longest_increasing_subseq.py"
    --8<-- "tests/dp/test_longest_increasing_subseq.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp longest_increasing_subseq`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.longest_increasing_subseq
            options:
              show_source: true
