---
title: Dijkstra
---

# Dijkstra

## Problem

Given a weighted directed graph and a source vertex, find the
shortest path from the source to every other reachable vertex.

## Approach

Dijkstra's algorithm using a min-heap (priority queue). Greedily
expand the nearest unvisited node and relax its outgoing edges.

### Algorithm Flow

```mermaid
flowchart TD
    A["Initialize dist[source] = 0<br/>dist[all others] = inf"] --> B["Push (0, source)<br/>to min-heap"]
    B --> C{"Heap empty?"}
    C -- Yes --> D["Return dist array"]
    C -- No --> E["Pop (d, u) with<br/>smallest distance"]
    E --> F{"d > dist[u]?<br/>(stale entry)"}
    F -- Yes --> C
    F -- No --> G["For each neighbor v<br/>of u with weight w"]
    G --> H{"d + w < dist[v]?"}
    H -- Yes --> I["dist[v] = d + w<br/>Push (d+w, v) to heap"]
    H -- No --> J["Skip — no improvement"]
    I --> G
    J --> G
    G -- "All neighbors<br/>processed" --> C

    style A fill:#7c3aed,color:#fff
    style D fill:#059669,color:#fff
    style F fill:#f59e0b,color:#000
```

## When to Use

Shortest path with NON-NEGATIVE weights. Flight routing, network latency,
road navigation. For negative weights use Bellman-Ford instead.
target employer relevance: core of route optimization in domain platform.

## Complexity

| | |
|---|---|
| **Time** | `O((V + E) log V)` |
| **Space** | `O(V + E)` |

## Implementation

=== "Solution"

    ::: algo.graphs.dijkstra
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_dijkstra.py"
    --8<-- "tests/graphs/test_dijkstra.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs dijkstra`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.dijkstra
            options:
              show_source: true
