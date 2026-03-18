---
title: Merge K Sorted Lists
---

# Merge K Sorted Lists

## Problem

Given an array of k sorted linked lists, merge them into one sorted
linked list.

## Approach

Use a min-heap of size k. Push (value, list_index, node) tuples.
Pop the smallest, append to result, and push the next node from
that list. The list_index breaks ties to avoid comparing nodes.

## When to Use

K-way merge for external sorting — "merge K sorted lists/arrays/files",
combining sorted partitions from distributed systems. Min-heap of size
k selects the next smallest element. See also: merge_two_sorted.

## Complexity

| | |
|---|---|
| **Time** | `O(n log k) where n = total nodes across all lists` |
| **Space** | `O(k) for the heap` |

## Implementation

=== "Solution"

    ::: algo.heaps.merge_k_sorted_lists
        options:
          show_source: true

=== "Tests"

    ```python title="tests/heaps/test_merge_k_sorted_lists.py"
    --8<-- "tests/heaps/test_merge_k_sorted_lists.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge heaps merge_k_sorted_lists`

        Then implement the functions to make all tests pass.
        Use `just study heaps` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.heaps.merge_k_sorted_lists
            options:
              show_source: true
