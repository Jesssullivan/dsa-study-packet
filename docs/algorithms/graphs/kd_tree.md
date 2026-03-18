---
title: Kd Tree
---

# Kd Tree

## Problem

Given a set of k-dimensional points, build a data structure that
supports efficient nearest-neighbor queries.

## Approach

Recursively partition points by cycling through dimensions,
splitting on the median. For nearest-neighbor queries, traverse
the tree pruning branches whose bounding hyperplane is farther
than the current best distance.

## When to Use

Nearest neighbor in multi-dimensional space — "closest point",
"k-nearest neighbors", range search in 2D/3D. Aviation: closest
waypoint/airport lookup, collision avoidance in 3D airspace.
See also: geohash_grid for grid-based spatial indexing.

## Complexity

| | |
|---|---|
| **Time** | `` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.graphs.kd_tree
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_kd_tree.py"
    --8<-- "tests/graphs/test_kd_tree.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs kd_tree`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.kd_tree
            options:
              show_source: true
