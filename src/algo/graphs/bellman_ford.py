"""Shortest paths allowing negative edge weights.

Problem:
    Given a weighted directed graph, find the shortest path from a
    source to all other vertices. Unlike Dijkstra, this handles
    negative edge weights and can detect negative-weight cycles.

Approach:
    Relax all edges V-1 times. After V-1 iterations, if any edge can
    still be relaxed, a negative cycle exists.

When to use:
    Shortest paths with negative edge weights — currency arbitrage
    detection, cost networks with rebates/discounts. Detects negative
    cycles. Prefer Dijkstra when all weights are non-negative.

Complexity:
    Time:  O(V * E)
    Space: O(V)
"""

from collections.abc import Sequence

INF = float("inf")


class NegativeCycleError(Exception):
    """Raised when a negative-weight cycle is detected."""


def bellman_ford(
    num_nodes: int,
    edges: Sequence[tuple[int, int, float]],
    source: int,
) -> list[float]:
    """Return shortest distances from *source* to all nodes.

    *edges* is a list of (u, v, weight).
    Raises :class:`NegativeCycleError` if a negative cycle is
    reachable from *source*.

    >>> bellman_ford(4, [(0, 1, 1), (1, 2, 3), (0, 2, 10), (2, 3, 2)], 0)
    [0, 1, 4, 6]
    """
    dist: list[float] = [INF] * num_nodes
    dist[source] = 0

    # A shortest path visits at most V-1 edges (no repeated vertices), so
    # V-1 relaxation rounds are guaranteed to converge if no negative cycle.
    for _ in range(num_nodes - 1):
        updated = False
        for u, v, w in edges:
            # dist[u] < INF guard: skip relaxing from a still-unreached node
            # so we never treat "infinity" as a real distance to propagate.
            if dist[u] < INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    # If any edge can still relax after V-1 rounds, that relaxation could
    # only come from a negative-weight cycle reachable from source.
    for u, v, w in edges:
        if dist[u] < INF and dist[u] + w < dist[v]:
            raise NegativeCycleError(
                "Graph contains a negative-weight cycle reachable from source"
            )

    return dist
