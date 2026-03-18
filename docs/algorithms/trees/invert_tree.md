---
title: Invert Tree
---

# Invert Tree

## Problem

Given the root of a binary tree, invert the tree so that every left
child becomes the right child and vice versa.

## Approach

Recursive swap: at each node, swap left and right children, then
recurse into both subtrees.

## When to Use

Tree transformation — "mirror", "invert", "flip". Any problem
requiring symmetric restructuring of a tree in-place.
Pattern: swap children, then recurse into both subtrees.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(h) where h = height of tree (call stack)` |

## Implementation

=== "Solution"

    ::: algo.trees.invert_tree
        options:
          show_source: true

=== "Tests"

    ```python title="tests/trees/test_invert_tree.py"
    --8<-- "tests/trees/test_invert_tree.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge trees invert_tree`

        Then implement the functions to make all tests pass.
        Use `just study trees` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.trees.invert_tree
            options:
              show_source: true
