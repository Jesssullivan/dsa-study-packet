---
title: Network Flow
---

# Network Flow

## Problem

Given a directed graph with edge capacities, find the maximum
flow from a source node to a sink node.

## Approach

Edmonds-Karp: repeatedly find augmenting paths using BFS on the
residual graph. Each BFS finds the shortest augmenting path,
guaranteeing polynomial time.

## When to Use

Maximum throughput — "max bandwidth", "maximum matching", "supply
chain optimization". Model as source -> sink capacity network.
Aviation: air traffic flow management, gate assignment optimization.

## Complexity

| | |
|---|---|
| **Time** | `O(V * E^2)` |
| **Space** | `O(V^2) for the capacity matrix` |

## Implementation

=== "Solution"

    ::: algo.graphs.network_flow
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_network_flow.py"
    --8<-- "tests/graphs/test_network_flow.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs network_flow`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.network_flow
            options:
              show_source: true
