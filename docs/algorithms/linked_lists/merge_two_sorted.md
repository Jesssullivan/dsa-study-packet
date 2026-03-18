---
title: Merge Two Sorted
---

# Merge Two Sorted

## Problem

Given the heads of two sorted linked lists, merge them into one sorted
list built from the nodes of the two input lists.

## Approach

Use a dummy head node and compare the fronts of both lists, advancing
the smaller one each time.

## When to Use

Merge step of merge sort — combining two sorted sequences into one.
Building block for merge_k_sorted_lists and external merge sort.
Keywords: "merge sorted", "interleave ordered streams".

## Complexity

| | |
|---|---|
| **Time** | `O(n + m)` |
| **Space** | `O(1) — only pointer manipulation, no new nodes allocated` |

## Implementation

=== "Solution"

    ::: algo.linked_lists.merge_two_sorted
        options:
          show_source: true

=== "Tests"

    ```python title="tests/linked_lists/test_merge_two_sorted.py"
    --8<-- "tests/linked_lists/test_merge_two_sorted.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge linked_lists merge_two_sorted`

        Then implement the functions to make all tests pass.
        Use `just study linked_lists` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.linked_lists.merge_two_sorted
            options:
              show_source: true
