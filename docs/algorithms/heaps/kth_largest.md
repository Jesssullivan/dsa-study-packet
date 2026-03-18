---
title: Kth Largest
---

# Kth Largest

## Problem

Given an unsorted array and an integer k, return the kth largest element.
Also implement a streaming version that supports adding new values.

## Approach

Maintain a min-heap of size k. The heap top is always the kth largest.
For each new element larger than the heap top, replace it.

## When to Use

Streaming top-K — "kth largest in a stream", "maintain running top K".
Min-heap of size k keeps only the K largest seen so far.
Also: real-time leaderboard, top-K sensor readings in telemetry.

## Implementation

=== "Solution"

    ::: algo.heaps.kth_largest
        options:
          show_source: true

=== "Tests"

    ```python title="tests/heaps/test_kth_largest.py"
    --8<-- "tests/heaps/test_kth_largest.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge heaps kth_largest`

        Then implement the functions to make all tests pass.
        Use `just study heaps` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.heaps.kth_largest
            options:
              show_source: true
