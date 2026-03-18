---
title: Valid Palindrome
---

# Valid Palindrome

## Problem

Given a string, determine if it is a palindrome considering only
alphanumeric characters and ignoring case.

## Approach

Two pointers from both ends. Skip non-alphanumeric characters.
Compare lowercase characters at each pointer position.

## When to Use

String validity checks, symmetry problems. Foundation for palindrome
family (longest palindromic substring, palindrome partitioning).

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.strings.valid_palindrome
        options:
          show_source: true

=== "Tests"

    ```python title="tests/strings/test_valid_palindrome.py"
    --8<-- "tests/strings/test_valid_palindrome.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge strings valid_palindrome`

        Then implement the functions to make all tests pass.
        Use `just study strings` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.strings.valid_palindrome
            options:
              show_source: true
