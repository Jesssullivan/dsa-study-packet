---
title: Word Ladder
---

# Word Ladder

## Problem

Given two words and a dictionary, find the length of the shortest
transformation sequence from beginWord to endWord, such that only
one letter can be changed at a time and each intermediate word
must exist in the word list.

## Approach

BFS level-by-level. At each level, for every word generate all
possible one-character mutations and check if they exist in the
remaining word set.

## When to Use

BFS for shortest transformation sequence — "minimum edits", "fewest
steps to transform X into Y", unweighted shortest path in an implicit
graph. Keywords: "word ladder", "gene mutation", "lock combination".

## Complexity

| | |
|---|---|
| **Time** | `O(n * m^2) where n = |word_list|, m = word length` |
| **Space** | `O(n * m)` |

## Implementation

=== "Solution"

    ::: algo.graphs.word_ladder
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_word_ladder.py"
    --8<-- "tests/graphs/test_word_ladder.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs word_ladder`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.word_ladder
            options:
              show_source: true
