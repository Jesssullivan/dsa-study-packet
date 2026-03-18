---
title: Minimum Spanning Tree
---

# Minimum Spanning Tree

## Problem

Given an undirected weighted graph, find a subset of edges that
connects all vertices with minimum total weight and no cycles.

## Approach

Kruskal: Sort edges by weight, greedily add edges that don't form
a cycle (checked via Union-Find).
Prim: Grow the MST from an arbitrary node using a min-heap.

## When to Use

Minimum cost to connect all nodes — cable/road/pipeline routing,
network backbone design. Kruskal for sparse graphs, Prim for dense.
Aviation: minimum-cost ground infrastructure linking airports.

## Implementation

=== "Solution"

    ::: algo.graphs.minimum_spanning_tree
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_minimum_spanning_tree.py"
    --8<-- "tests/graphs/test_minimum_spanning_tree.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs minimum_spanning_tree`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.minimum_spanning_tree
            options:
              show_source: true
