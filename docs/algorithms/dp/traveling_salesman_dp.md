---
title: Traveling Salesman Dp
---

# Traveling Salesman Dp

## Problem

Given a weighted adjacency matrix of n cities, find the minimum
cost of visiting every city exactly once and returning to the
starting city.

## Approach

Bitmask DP (Held-Karp algorithm). State is (visited_set, current_city).
Use an integer bitmask to represent the set of visited cities.
dp[mask][i] = minimum cost to visit the cities in `mask`, ending at city i.

## When to Use

Visit-all-nodes optimization — "shortest route visiting every city",
delivery/pickup routing, inspection tours. Bitmask DP (Held-Karp)
for exact solution when n <= 20. Aviation: multi-stop flight routing.

## Complexity

| | |
|---|---|
| **Time** | `O(n^2 * 2^n)` |
| **Space** | `O(n * 2^n)` |

## Implementation

=== "Solution"

    ::: algo.dp.traveling_salesman_dp
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_traveling_salesman_dp.py"
    --8<-- "tests/dp/test_traveling_salesman_dp.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp traveling_salesman_dp`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.traveling_salesman_dp
            options:
              show_source: true
