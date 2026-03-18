---
title: Validate Bst
---

# Validate Bst

## Problem

Given the root of a binary tree, determine if it is a valid BST.
A valid BST requires every node's value to be strictly between the
values of its ancestors that constrain it.

## Approach

Recursive with min/max bounds. At each node, check that the value
is within (lo, hi) and recurse with tightened bounds.

## When to Use

Constraint propagation through a tree — "validate BST", "check
ordering invariant". Pass tightening bounds (lo, hi) down the
recursion. Also: range-constrained tree problems, interval checks.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(h) where h = height of tree (call stack)` |

## Implementation

=== "Solution"

    ::: algo.trees.validate_bst
        options:
          show_source: true

=== "Tests"

    ```python title="tests/trees/test_validate_bst.py"
    --8<-- "tests/trees/test_validate_bst.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge trees validate_bst`

        Then implement the functions to make all tests pass.
        Use `just study trees` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.trees.validate_bst
            options:
              show_source: true
