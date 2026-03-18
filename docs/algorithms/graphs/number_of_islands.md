---
title: Number Of Islands
---

# Number Of Islands

## Problem

Given an m x n 2D binary grid where '1' represents land and '0'
represents water, return the number of islands. An island is
surrounded by water and formed by connecting adjacent lands
horizontally or vertically.

## Approach

BFS flood fill. Iterate every cell; when a '1' is found, increment
the island counter and BFS to mark all connected land as visited.

## When to Use

Connected components / flood fill — "count islands", "count regions",
"label connected areas". BFS/DFS from each unvisited cell.
Geospatial: land-use classification, satellite imagery segmentation.

## Complexity

| | |
|---|---|
| **Time** | `O(m * n) — each cell visited at most once` |
| **Space** | `O(m * n) — visited set (or O(min(m, n)) BFS queue)` |

## Implementation

=== "Solution"

    ::: algo.graphs.number_of_islands
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_number_of_islands.py"
    --8<-- "tests/graphs/test_number_of_islands.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs number_of_islands`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.number_of_islands
            options:
              show_source: true
