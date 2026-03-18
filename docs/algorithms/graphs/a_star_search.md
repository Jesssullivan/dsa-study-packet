---
title: A Star Search
---

# A Star Search

## Problem

Given a 2D grid where each cell has a non-negative traversal cost,
find the shortest (least-cost) path from a start cell to a goal
cell using A* search with Manhattan distance heuristic.

## Approach

Priority queue ordered by f(n) = g(n) + h(n), where g is the cost
so far and h is the Manhattan distance heuristic. Expand the node
with lowest f; skip already-settled nodes.

## When to Use

Shortest path when you have a good heuristic (estimated distance to goal).
Better than Dijkstra when goal is known — avoids exploring irrelevant nodes.
target employer relevance: flight route optimization with destination-aware pruning.
Use Manhattan distance for grids, great-circle distance for geospatial.

## Complexity

| | |
|---|---|
| **Time** | `O(E log V) with a good heuristic (grid: E ~ 4V)` |
| **Space** | `O(V)` |

## Implementation

=== "Solution"

    ::: algo.graphs.a_star_search
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_a_star_search.py"
    --8<-- "tests/graphs/test_a_star_search.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs a_star_search`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.a_star_search
            options:
              show_source: true
