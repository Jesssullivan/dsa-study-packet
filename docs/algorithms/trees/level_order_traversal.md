---
title: Level Order Traversal
---

# Level Order Traversal

## Problem

Given the root of a binary tree, return the level-order traversal
as a list of lists, where each inner list contains the values at
that depth level.

## Approach

BFS with a deque. Process one level at a time by iterating over
the current queue length, appending children for the next level.

## When to Use

BFS on trees — "level order", "zigzag order", "right side view", any
problem requiring per-level processing. Also: shortest-path-like
queries on trees, hierarchical data serialization.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(w) where w = max width of the tree (up to n/2)` |

## Implementation

=== "Solution"

    ::: algo.trees.level_order_traversal
        options:
          show_source: true

=== "Tests"

    ```python title="tests/trees/test_level_order_traversal.py"
    --8<-- "tests/trees/test_level_order_traversal.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge trees level_order_traversal`

        Then implement the functions to make all tests pass.
        Use `just study trees` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.trees.level_order_traversal
            options:
              show_source: true
