"""Time for a signal to reach all nodes (Dijkstra variant).

Problem:
    Given a network of n nodes (1-indexed) and directed weighted edges
    ``times[i] = (u, v, w)``, send a signal from node k. Return the
    minimum time for all nodes to receive the signal, or -1 if not all
    nodes are reachable.

Approach:
    Run Dijkstra from source k. The answer is the maximum shortest
    distance among all nodes. If any node is unreachable, return -1.

When to use:
    "Can a signal/message reach all nodes, and how long?" — broadcast
    latency, all-nodes reachability. Run Dijkstra, answer is max(dist).
    Aviation: minimum propagation delay across a network of stations.

Complexity:
    Time:  O((V + E) log V)
    Space: O(V + E)
"""

import heapq

INF = float("inf")


def network_delay_time(
    times: list[tuple[int, int, int]],
    n: int,
    k: int,
) -> int:
    """Return minimum time for signal from *k* to reach all *n* nodes.

    Nodes are 1-indexed.  Returns -1 if any node is unreachable.

    >>> network_delay_time([(2,1,1),(2,3,1),(3,4,1)], 4, 2)
    2
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))

    dist: list[float] = [INF] * (n + 1)
    dist[k] = 0
    heap: list[tuple[float, int]] = [(0, k)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    max_dist = max(dist[1:])
    return int(max_dist) if max_dist < INF else -1
