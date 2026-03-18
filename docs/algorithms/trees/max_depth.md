---
title: Max Depth
---

# Max Depth

## Problem

Given the root of a binary tree, return its maximum depth (number of
nodes along the longest path from root to a leaf).

## Approach

DFS recursive: depth = 1 + max(depth(left), depth(right)).
Base case: empty tree has depth 0.

## When to Use

Recursive tree measurement — "max depth", "height", "diameter",
any metric that aggregates over subtrees with a simple recurrence.
Foundation for balanced-tree checks and tree diameter computation.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(h) where h = height of tree (call stack)` |

## Implementation

=== "Solution"

    ::: algo.trees.max_depth
        options:
          show_source: true

=== "Tests"

    ```python title="tests/trees/test_max_depth.py"
    --8<-- "tests/trees/test_max_depth.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge trees max_depth`

        Then implement the functions to make all tests pass.
        Use `just study trees` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.trees.max_depth
            options:
              show_source: true
