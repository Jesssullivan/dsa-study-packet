---
title: Longest Common Subseq
---

# Longest Common Subseq

## Problem

Given two strings, return the length of their longest common
subsequence. A subsequence is a sequence derived by deleting some
(or no) characters without changing the relative order.

## Approach

2D DP. If characters match, extend the diagonal; otherwise take
the max of skipping one character from either string.
Space-optimized to a single row.

## When to Use

Diff / alignment — "longest common subsequence", "diff two files",
DNA sequence alignment. Foundation for unified-diff algorithms.
See also: edit_distance for minimum-cost transformation.

## Complexity

| | |
|---|---|
| **Time** | `O(m * n)` |
| **Space** | `O(min(m, n))` |

## Implementation

=== "Solution"

    ::: algo.dp.longest_common_subseq
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_longest_common_subseq.py"
    --8<-- "tests/dp/test_longest_common_subseq.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp longest_common_subseq`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.longest_common_subseq
            options:
              show_source: true
