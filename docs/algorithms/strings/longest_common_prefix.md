---
title: Longest Common Prefix
---

# Longest Common Prefix

## Problem

Given a list of strings, return the longest common prefix shared
by all of them.

## Approach

Vertical scanning: compare character-by-character across all strings.
Use the first string as reference; stop when any string differs or
is exhausted.

## When to Use

Autocomplete, trie-based search, file path commonality. Simple but
frequently asked.

## Complexity

| | |
|---|---|
| **Time** | `O(S) where S = sum of all string lengths` |
| **Space** | `O(1) — only stores the prefix end index` |

## Implementation

=== "Solution"

    ::: algo.strings.longest_common_prefix
        options:
          show_source: true

=== "Tests"

    ```python title="tests/strings/test_longest_common_prefix.py"
    --8<-- "tests/strings/test_longest_common_prefix.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge strings longest_common_prefix`

        Then implement the functions to make all tests pass.
        Use `just study strings` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.strings.longest_common_prefix
            options:
              show_source: true
