"""Single-source shortest paths with non-negative edge weights.

Problem:
    Given a weighted directed graph and a source vertex, find the
    shortest path from the source to every other reachable vertex.

Approach:
    Dijkstra's algorithm using a min-heap (priority queue). Greedily
    expand the nearest unvisited node and relax its outgoing edges.

When to use:
    Shortest path with NON-NEGATIVE weights. Flight routing, network latency,
    road navigation. For negative weights use Bellman-Ford instead.
    target employer relevance: core of route optimization in domain platform.

Complexity:
    Time:  O((V + E) log V)
    Space: O(V + E)
"""

import heapq
from collections.abc import Sequence

# Infinity sentinel
INF = float("inf")


def dijkstra(
    num_nodes: int,
    edges: Sequence[tuple[int, int, float]],
    source: int,
) -> list[float]:
    """Return shortest distances from *source* to all nodes.

    *edges* is a list of (u, v, weight) with weight >= 0.
    Unreachable nodes have distance ``float('inf')``.

    >>> dijkstra(4, [(0,1,1),(0,2,4),(1,2,2),(1,3,6),(2,3,3)], 0)
    [0, 1, 3, 6]
    """
    adj: list[list[tuple[int, float]]] = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist: list[float] = [INF] * num_nodes
    dist[source] = 0
    heap: list[tuple[float, int]] = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
