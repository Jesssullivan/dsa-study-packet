---
title: Edit Distance
---

# Edit Distance

## Problem

Given two strings, return the minimum number of single-character
operations (insert, delete, replace) to convert word1 into word2.

## Approach

2D DP where dp[i][j] is the edit distance between the first i
characters of word1 and the first j characters of word2.
Space-optimized to a single row since each cell only depends on
the current and previous row.

## When to Use

String similarity / diff algorithms — "minimum edits", "Levenshtein
distance", spell checking, DNA sequence alignment. Foundation for
fuzzy matching and diff tools. See also: longest_common_subseq.

## Complexity

| | |
|---|---|
| **Time** | `O(m * n)` |
| **Space** | `O(n)  (space-optimized)` |

## Implementation

=== "Solution"

    ::: algo.dp.edit_distance
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_edit_distance.py"
    --8<-- "tests/dp/test_edit_distance.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp edit_distance`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.edit_distance
            options:
              show_source: true
