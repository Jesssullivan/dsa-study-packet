"""Count islands in a 2D grid of '1's (land) and '0's (water).

Problem:
    Given an m x n 2D binary grid where '1' represents land and '0'
    represents water, return the number of islands. An island is
    surrounded by water and formed by connecting adjacent lands
    horizontally or vertically.

Approach:
    BFS flood fill. Iterate every cell; when a '1' is found, increment
    the island counter and BFS to mark all connected land as visited.

When to use:
    Connected components / flood fill — "count islands", "count regions",
    "label connected areas". BFS/DFS from each unvisited cell.
    Geospatial: land-use classification, satellite imagery segmentation.

Complexity:
    Time:  O(m * n) — each cell visited at most once
    Space: O(m * n) — visited set (or O(min(m, n)) BFS queue)
"""

from collections import deque


def num_islands(grid: list[list[str]]) -> int:
    """Return the number of islands in *grid*.

    >>> num_islands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]])
    2
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                count += 1
                _bfs(grid, r, c, rows, cols, visited)

    return count


def _bfs(
    grid: list[list[str]],
    start_r: int,
    start_c: int,
    rows: int,
    cols: int,
    visited: set[tuple[int, int]],
) -> None:
    queue: deque[tuple[int, int]] = deque([(start_r, start_c)])
    visited.add((start_r, start_c))

    while queue:
        cr, cc = queue.popleft()
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = cr + dr, cc + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == "1"
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append((nr, nc))
