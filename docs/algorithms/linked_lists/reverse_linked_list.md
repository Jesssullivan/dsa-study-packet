---
title: Reverse Linked List
---

# Reverse Linked List

## Problem

Given the head of a singly linked list, reverse the list and return
the new head.

## Approach

Iterative: Walk the list with prev/curr pointers, reversing each link.
Recursive: Reverse the rest of the list, then point the next node back.

## When to Use

In-place linked list reversal — "reverse list", "reverse sublist",
pointer manipulation without extra space. Building block for
palindrome check, k-group reversal, and reorder-list problems.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1) iterative, O(n) recursive (call stack)` |

## Implementation

=== "Solution"

    ::: algo.linked_lists.reverse_linked_list
        options:
          show_source: true

=== "Tests"

    ```python title="tests/linked_lists/test_reverse_linked_list.py"
    --8<-- "tests/linked_lists/test_reverse_linked_list.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge linked_lists reverse_linked_list`

        Then implement the functions to make all tests pass.
        Use `just study linked_lists` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.linked_lists.reverse_linked_list
            options:
              show_source: true
