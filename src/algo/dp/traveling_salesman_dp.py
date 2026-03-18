"""Traveling Salesman Problem — bitmask DP solution.

Problem:
    Given a weighted adjacency matrix of n cities, find the minimum
    cost of visiting every city exactly once and returning to the
    starting city.

Approach:
    Bitmask DP (Held-Karp algorithm). State is (visited_set, current_city).
    Use an integer bitmask to represent the set of visited cities.
    dp[mask][i] = minimum cost to visit the cities in `mask`, ending at city i.

When to use:
    Visit-all-nodes optimization — "shortest route visiting every city",
    delivery/pickup routing, inspection tours. Bitmask DP (Held-Karp)
    for exact solution when n <= 20. Aviation: multi-stop flight routing.

Complexity:
    Time:  O(n^2 * 2^n)
    Space: O(n * 2^n)

Note:
    Only practical for small n (typically n <= 20).
"""

from collections.abc import Sequence

INF = float("inf")


def tsp(dist: Sequence[Sequence[int | float]]) -> int | float:
    """Return the minimum cost tour visiting all cities and returning to start.

    *dist* is an n x n adjacency matrix where dist[i][j] is the cost
    from city i to city j.

    >>> tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])
    80
    """
    n = len(dist)
    if n <= 1:
        return 0

    full_mask = (1 << n) - 1

    # dp[mask][i] = min cost to reach city i having visited cities in mask
    dp: list[list[int | float]] = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                cost = dp[mask][u] + dist[u][v]
                if cost < dp[new_mask][v]:
                    dp[new_mask][v] = cost

    # Close the tour: return to city 0
    result: int | float = INF
    for u in range(1, n):
        cost = dp[full_mask][u] + dist[u][0]
        if cost < result:
            result = cost

    return result
