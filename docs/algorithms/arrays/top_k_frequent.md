---
title: Top K Frequent
---

# Top K Frequent

## Problem

Given an integer array and an integer k, return the k most frequent
elements. The answer is guaranteed to be unique.

## Approach

Bucket sort by frequency. Count occurrences, then place each number
into a bucket indexed by its frequency. Walk buckets from highest
frequency downward until k elements are collected.

## When to Use

Frequency counting + selection — "top K", "most common", "least common".
Bucket sort avoids O(n log n); see also heaps/kth_largest for streaming variant.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.arrays.top_k_frequent
        options:
          show_source: true

=== "Tests"

    ```python title="tests/arrays/test_top_k_frequent.py"
    --8<-- "tests/arrays/test_top_k_frequent.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge arrays top_k_frequent`

        Then implement the functions to make all tests pass.
        Use `just study arrays` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.arrays.top_k_frequent
            options:
              show_source: true
