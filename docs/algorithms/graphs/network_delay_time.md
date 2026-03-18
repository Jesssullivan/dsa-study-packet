---
title: Network Delay Time
---

# Network Delay Time

## Problem

Given a network of n nodes (1-indexed) and directed weighted edges
``times[i] = (u, v, w)``, send a signal from node k. Return the
minimum time for all nodes to receive the signal, or -1 if not all
nodes are reachable.

## Approach

Run Dijkstra from source k. The answer is the maximum shortest
distance among all nodes. If any node is unreachable, return -1.

## When to Use

"Can a signal/message reach all nodes, and how long?" — broadcast
latency, all-nodes reachability. Run Dijkstra, answer is max(dist).
Aviation: minimum propagation delay across a network of stations.

## Complexity

| | |
|---|---|
| **Time** | `O((V + E) log V)` |
| **Space** | `O(V + E)` |

## Implementation

=== "Solution"

    ::: algo.graphs.network_delay_time
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_network_delay_time.py"
    --8<-- "tests/graphs/test_network_delay_time.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs network_delay_time`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.network_delay_time
            options:
              show_source: true
