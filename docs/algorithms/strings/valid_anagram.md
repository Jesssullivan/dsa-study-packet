---
title: Valid Anagram
---

# Valid Anagram

## Problem

Given two strings, determine if one is an anagram of the other
(same characters, same frequencies, different order allowed).

## Approach

Counter comparison — count character frequencies for both strings
and check equality.

## When to Use

Equivalence class membership — same chars different order. Group
anagrams builds on this. Also: frequency matching, permutation
checking.

## Complexity

| | |
|---|---|
| **Time** | `O(n) with Counter, O(n log n) with sort` |
| **Space** | `O(1) — bounded by alphabet size (26 for lowercase English)` |

## Implementation

=== "Solution"

    ::: algo.strings.valid_anagram
        options:
          show_source: true

=== "Tests"

    ```python title="tests/strings/test_valid_anagram.py"
    --8<-- "tests/strings/test_valid_anagram.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge strings valid_anagram`

        Then implement the functions to make all tests pass.
        Use `just study strings` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.strings.valid_anagram
            options:
              show_source: true
