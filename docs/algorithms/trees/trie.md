---
title: Trie
---

# Trie

## Problem

Implement a prefix tree that supports insert, search, prefix matching,
delete, and autocomplete operations on a set of strings.

## Approach

A tree where each node represents a character. Paths from the root to
nodes marked as word-endings form the stored words. Children are stored
in a dict keyed by character for O(1) branching.

## When to Use

Autocomplete, spell checking, IP routing, prefix matching. Mission-systems relevance:
airport code lookup (e.g., "BO" -> ["BOS", "BOI", "BOG"]), flight ID
prefix search, geospatial name indexing.

## Complexity

| | |
|---|---|
| **Time** | `O(m) per insert/search/starts_with/delete where m = word length.` |
| **Space** | `O(N * m) where N = number of words, m = average word length.` |

## Implementation

=== "Solution"

    ::: algo.trees.trie
        options:
          show_source: true

=== "Tests"

    ```python title="tests/trees/test_trie.py"
    --8<-- "tests/trees/test_trie.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge trees trie`

        Then implement the functions to make all tests pass.
        Use `just study trees` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.trees.trie
            options:
              show_source: true
