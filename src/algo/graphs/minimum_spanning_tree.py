"""Minimum spanning tree: Kruskal's and Prim's algorithms.

Problem:
    Given an undirected weighted graph, find a subset of edges that
    connects all vertices with minimum total weight and no cycles.

Approach:
    Kruskal: Sort edges by weight, greedily add edges that don't form
    a cycle (checked via Union-Find).
    Prim: Grow the MST from an arbitrary node using a min-heap.

When to use:
    Minimum cost to connect all nodes — cable/road/pipeline routing,
    network backbone design. Kruskal for sparse graphs, Prim for dense.
    Aviation: minimum-cost ground infrastructure linking airports.

Complexity:
    Kruskal: O(E log E)  (sort-dominated)
    Prim:    O(E log V)  (heap-dominated)
"""

import heapq
from collections.abc import Sequence


class UnionFind:
    """Disjoint-set / Union-Find with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        """Find the root of *x* with path compression."""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """Merge sets containing *x* and *y*. Return False if already same set."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True


def kruskal(
    num_nodes: int,
    edges: Sequence[tuple[int, int, float]],
) -> list[tuple[int, int, float]]:
    """Return MST edges using Kruskal's algorithm.

    *edges* is a list of (u, v, weight) for an undirected graph.
    Returns the MST as a list of (u, v, weight) edges.

    >>> kruskal(4, [(0,1,1),(1,2,2),(0,2,3),(2,3,4)])
    [(0, 1, 1), (1, 2, 2), (2, 3, 4)]
    """
    sorted_edges = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(num_nodes)
    mst: list[tuple[int, int, float]] = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == num_nodes - 1:
                break

    return mst


def prim(
    num_nodes: int,
    edges: Sequence[tuple[int, int, float]],
) -> list[tuple[int, int, float]]:
    """Return MST edges using Prim's algorithm.

    *edges* is a list of (u, v, weight) for an undirected graph.

    >>> sorted(prim(4, [(0,1,1),(1,2,2),(0,2,3),(2,3,4)]), key=lambda e: e[2])
    [(0, 1, 1), (1, 2, 2), (2, 3, 4)]
    """
    adj: list[list[tuple[int, float]]] = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    in_mst = [False] * num_nodes
    mst: list[tuple[int, int, float]] = []
    heap: list[tuple[float, int, int]] = [(0, -1, 0)]

    while heap and len(mst) < num_nodes - 1:
        w, frm, to = heapq.heappop(heap)
        if in_mst[to]:
            continue
        in_mst[to] = True
        if frm != -1:
            mst.append((frm, to, w))
        for neighbor, weight in adj[to]:
            if not in_mst[neighbor]:
                heapq.heappush(heap, (weight, to, neighbor))

    return mst
