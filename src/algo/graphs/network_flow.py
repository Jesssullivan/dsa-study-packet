"""Maximum flow via Edmonds-Karp (BFS-based Ford-Fulkerson).

Problem:
    Given a directed graph with edge capacities, find the maximum
    flow from a source node to a sink node.

Approach:
    Edmonds-Karp: repeatedly find augmenting paths using BFS on the
    residual graph. Each BFS finds the shortest augmenting path,
    guaranteeing polynomial time.

When to use:
    Maximum throughput — "max bandwidth", "maximum matching", "supply
    chain optimization". Model as source -> sink capacity network.
    Aviation: air traffic flow management, gate assignment optimization.

Complexity:
    Time:  O(V * E^2)
    Space: O(V^2) for the capacity matrix
"""

from collections import deque
from sys import maxsize


def edmonds_karp(
    num_nodes: int,
    edges: list[tuple[int, int, int]],
    source: int,
    sink: int,
) -> int:
    """Return the maximum flow from *source* to *sink*.

    *edges* is a list of (u, v, capacity).

    >>> edmonds_karp(4, [(0,1,10),(0,2,10),(1,3,10),(2,3,10),(1,2,1)], 0, 3)
    20
    """
    capacity: list[list[int]] = [[0] * num_nodes for _ in range(num_nodes)]
    adj: list[list[int]] = [[] for _ in range(num_nodes)]

    for u, v, cap in edges:
        capacity[u][v] += cap
        adj[u].append(v)
        adj[v].append(u)  # reverse edge for residual graph

    total_flow = 0

    while True:
        parent = _bfs(adj, capacity, source, sink, num_nodes)
        if parent is None:
            break

        # Find bottleneck along the path
        path_flow = maxsize
        node = sink
        while node != source:
            prev = parent[node]
            path_flow = min(path_flow, capacity[prev][node])
            node = prev

        # Update residual capacities
        node = sink
        while node != source:
            prev = parent[node]
            capacity[prev][node] -= path_flow
            capacity[node][prev] += path_flow
            node = prev

        total_flow += path_flow

    return total_flow


def _bfs(
    adj: list[list[int]],
    capacity: list[list[int]],
    source: int,
    sink: int,
    num_nodes: int,
) -> list[int] | None:
    """BFS to find an augmenting path. Returns parent array or None."""
    parent = [-1] * num_nodes
    parent[source] = source
    queue: deque[int] = deque([source])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if parent[v] == -1 and capacity[u][v] > 0:
                parent[v] = u
                if v == sink:
                    return parent
                queue.append(v)

    return None
