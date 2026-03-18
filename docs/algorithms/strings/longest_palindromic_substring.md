---
title: Longest Palindromic Substring
---

# Longest Palindromic Substring

## Problem

Given a string, return the longest substring that is a palindrome.

## Approach

Expand around center for each position. Try both odd-length (single
center) and even-length (two-char center) expansions. Track the best
start and length.

## When to Use

Substring search with symmetry constraint. Related to Manacher's
algorithm for O(n).

## Complexity

| | |
|---|---|
| **Time** | `O(n²)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.strings.longest_palindromic_substring
        options:
          show_source: true

=== "Tests"

    ```python title="tests/strings/test_longest_palindromic_substring.py"
    --8<-- "tests/strings/test_longest_palindromic_substring.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge strings longest_palindromic_substring`

        Then implement the functions to make all tests pass.
        Use `just study strings` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.strings.longest_palindromic_substring
            options:
              show_source: true
