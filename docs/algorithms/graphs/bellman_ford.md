---
title: Bellman Ford
---

# Bellman Ford

## Problem

Given a weighted directed graph, find the shortest path from a
source to all other vertices. Unlike Dijkstra, this handles
negative edge weights and can detect negative-weight cycles.

## Approach

Relax all edges V-1 times. After V-1 iterations, if any edge can
still be relaxed, a negative cycle exists.

## When to Use

Shortest paths with negative edge weights — currency arbitrage
detection, cost networks with rebates/discounts. Detects negative
cycles. Prefer Dijkstra when all weights are non-negative.

## Complexity

| | |
|---|---|
| **Time** | `O(V * E)` |
| **Space** | `O(V)` |

## Implementation

=== "Solution"

    ::: algo.graphs.bellman_ford
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_bellman_ford.py"
    --8<-- "tests/graphs/test_bellman_ford.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs bellman_ford`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.bellman_ford
            options:
              show_source: true
