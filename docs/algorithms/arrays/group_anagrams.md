---
title: Group Anagrams
---

# Group Anagrams

## Problem

Given a list of strings, group the anagrams together. An anagram is a
word formed by rearranging the letters of another.

## Approach

Use the sorted characters of each string as a hash key.
All anagrams produce the same sorted tuple, so they land in the
same bucket in a defaultdict.

## When to Use

Grouping items by equivalence class — anagrams, isomorphic strings, etc.
Keywords: "group by", "categorize", "bucket by canonical form".

## Complexity

| | |
|---|---|
| **Time** | `O(n * k log k)  where n = number of strings, k = max string length` |
| **Space** | `O(n * k)` |

## Implementation

=== "Solution"

    ::: algo.arrays.group_anagrams
        options:
          show_source: true

=== "Tests"

    ```python title="tests/arrays/test_group_anagrams.py"
    --8<-- "tests/arrays/test_group_anagrams.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge arrays group_anagrams`

        Then implement the functions to make all tests pass.
        Use `just study arrays` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.arrays.group_anagrams
            options:
              show_source: true
