---
title: Flatten Nested List
---

# Flatten Nested List

## Problem

Given a nested list of integers (can be arbitrarily deep), flatten
it into a single list of integers.

## Approach

Recursive: if element is a list, recurse into it; otherwise yield
the integer. Also provide an iterative version using an explicit
stack (process in reverse to maintain order).

## When to Use

Processing recursive/nested data structures — JSON, XML, file trees,
AST traversal. target employer relevance: nested geospatial data, hierarchical
flight plans.

## Complexity

| | |
|---|---|
| **Time** | `O(n) — where n = total elements across all nesting levels` |
| **Space** | `O(d) recursive / O(n) iterative — d = max depth` |

## Implementation

=== "Solution"

    ::: algo.recursion.flatten_nested_list
        options:
          show_source: true

=== "Tests"

    ```python title="tests/recursion/test_flatten_nested_list.py"
    --8<-- "tests/recursion/test_flatten_nested_list.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge recursion flatten_nested_list`

        Then implement the functions to make all tests pass.
        Use `just study recursion` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.recursion.flatten_nested_list
            options:
              show_source: true
