---
title: Clone Graph
---

# Clone Graph

## Problem

Given a reference of a node in a connected undirected graph, return
a deep copy (clone) of the graph. Each node contains a val and a
list of its neighbors.

## Approach

BFS with a hash map mapping original nodes to their clones. For
each node dequeued, iterate its neighbors: clone unseen neighbors,
then wire the cloned neighbor into the clone's neighbor list.

## When to Use

Graph deep copy — "clone graph", "copy linked structure with cycles".
BFS/DFS with a hash map from original to clone prevents revisiting.
Also: snapshotting mutable graph state, undo/redo systems.

## Complexity

| | |
|---|---|
| **Time** | `O(V + E)` |
| **Space** | `O(V)` |

## Implementation

=== "Solution"

    ::: algo.graphs.clone_graph
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_clone_graph.py"
    --8<-- "tests/graphs/test_clone_graph.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs clone_graph`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.clone_graph
            options:
              show_source: true
