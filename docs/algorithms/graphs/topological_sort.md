---
title: Topological Sort
---

# Topological Sort

## Problem

Given a DAG represented as an adjacency list, return a valid
topological ordering of its vertices. If the graph has a cycle,
return an empty list.

## Approach

1. Kahn's algorithm (BFS): Track in-degrees; repeatedly dequeue
   nodes with in-degree 0 and decrement neighbors' in-degrees.
2. DFS-based: Post-order DFS; reverse the finish order.

### Algorithm Flow

```mermaid
flowchart TD
    A["Build adjacency list<br/>Compute in-degree for each node"] --> B["Enqueue all nodes<br/>with in-degree 0"]
    B --> C{"Queue empty?"}
    C -- Yes --> D{"len(order) == V?"}
    D -- Yes --> E["Return order<br/>(valid topological sort)"]
    D -- No --> F["Return [] — cycle detected"]
    C -- No --> G["Dequeue node u<br/>Append u to order"]
    G --> H["For each neighbor v of u:<br/>in-degree[v] -= 1"]
    H --> I{"in-degree[v] == 0?"}
    I -- Yes --> J["Enqueue v"]
    I -- No --> K["Continue"]
    J --> C
    K --> C

    style A fill:#7c3aed,color:#fff
    style E fill:#059669,color:#fff
    style F fill:#dc2626,color:#fff
```

## When to Use

Dependency resolution — "build order", "task scheduling with prereqs",
"compile order". Any DAG where you need a valid linear ordering.
Also: package managers, makefile targets, course planning.

## Complexity

| | |
|---|---|
| **Time** | `O(V + E)` |
| **Space** | `O(V + E)` |

## Implementation

=== "Solution"

    ::: algo.graphs.topological_sort
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_topological_sort.py"
    --8<-- "tests/graphs/test_topological_sort.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs topological_sort`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.topological_sort
            options:
              show_source: true
