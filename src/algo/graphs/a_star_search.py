"""A* pathfinding on a weighted grid.

Problem:
    Given a 2D grid where each cell has a non-negative traversal cost,
    find the shortest (least-cost) path from a start cell to a goal
    cell using A* search with Manhattan distance heuristic.

Approach:
    Priority queue ordered by f(n) = g(n) + h(n), where g is the cost
    so far and h is the Manhattan distance heuristic. Expand the node
    with lowest f; skip already-settled nodes.

When to use:
    Shortest path when you have a good heuristic (estimated distance to goal).
    Better than Dijkstra when goal is known — avoids exploring irrelevant nodes.
    Use Manhattan distance for grids, great-circle distance for geospatial.

Note:
    Optimality requires an admissible heuristic (never overestimates the true
    remaining cost) and, for this no-closed-set form, a consistent one.
    Manhattan distance satisfies both on a 4-connected grid with per-cell cost
    >= 1, so the path is optimal when the goal is first popped.

Complexity:
    Time:  O(E log V) with a good heuristic (grid: E ~ 4V)
    Space: O(V)
"""

import heapq


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return the Manhattan distance between two grid points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]] | None:
    """Return the shortest path from *start* to *goal* on *grid*.

    ``grid[r][c]`` is the cost to enter cell (r, c). Returns a list of
    (row, col) coordinates from start to goal inclusive, or ``None`` if
    no path exists.

    >>> a_star([[1, 1, 1], [1, 1, 1], [1, 1, 1]], (0, 0), (2, 2))
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    """
    if not grid or not grid[0]:
        return None

    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    gr, gc = goal

    if not (0 <= sr < rows and 0 <= sc < cols):
        return None
    if not (0 <= gr < rows and 0 <= gc < cols):
        return None

    open_heap: list[tuple[int, int, int, int]] = [
        (manhattan_distance(start, goal), 0, sr, sc),
    ]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], int] = {start: 0}

    while open_heap:
        _f, g, r, c = heapq.heappop(open_heap)
        if (r, c) == goal:
            return _reconstruct_path(came_from, goal)

        if g > g_score.get((r, c), float("inf")):
            continue

        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                ng = g + grid[nr][nc]
                if ng < g_score.get((nr, nc), float("inf")):
                    g_score[(nr, nc)] = ng
                    f = ng + manhattan_distance((nr, nc), goal)
                    heapq.heappush(open_heap, (f, ng, nr, nc))
                    came_from[(nr, nc)] = (r, c)

    return None


def _reconstruct_path(
    came_from: dict[tuple[int, int], tuple[int, int]],
    current: tuple[int, int],
) -> list[tuple[int, int]]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
