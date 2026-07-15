"""Tests for A* search on weighted grids."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.a_star_search import a_star, manhattan_distance
from algo.graphs.dijkstra import dijkstra


class TestManhattanDistance:
    def test_same_point(self) -> None:
        assert manhattan_distance((0, 0), (0, 0)) == 0

    def test_basic(self) -> None:
        assert manhattan_distance((0, 0), (3, 4)) == 7


class TestAStar:
    def test_simple_grid(self) -> None:
        grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        path = a_star(grid, (0, 0), (2, 2))
        assert path is not None
        assert path[0] == (0, 0)
        assert path[-1] == (2, 2)
        assert len(path) == 5  # Manhattan distance + 1

    def test_start_equals_goal(self) -> None:
        grid = [[1, 1], [1, 1]]
        path = a_star(grid, (0, 0), (0, 0))
        assert path == [(0, 0)]

    def test_obstacle_avoidance(self) -> None:
        grid = [
            [1, 999, 1],
            [1, 999, 1],
            [1, 1, 1],
        ]
        path = a_star(grid, (0, 0), (0, 2))
        assert path is not None
        assert path[0] == (0, 0)
        assert path[-1] == (0, 2)
        # Should go around the wall
        total_cost = sum(grid[r][c] for r, c in path[1:])
        assert total_cost < 999

    def test_empty_grid(self) -> None:
        assert a_star([], (0, 0), (0, 0)) is None

    def test_out_of_bounds(self) -> None:
        grid = [[1, 1], [1, 1]]
        assert a_star(grid, (5, 5), (0, 0)) is None

    def test_weighted_preference(self) -> None:
        grid = [
            [1, 1, 1],
            [1, 10, 1],
            [1, 1, 1],
        ]
        path = a_star(grid, (0, 0), (2, 2))
        assert path is not None
        # Should not go through (1,1) since weight 10
        assert (1, 1) not in path


@st.composite
def _grids_with_endpoints(
    draw: st.DrawFn, max_rows: int = 5, max_cols: int = 5
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    """A random grid of positive cell costs plus in-bounds start/goal cells."""
    rows = draw(st.integers(min_value=1, max_value=max_rows))
    cols = draw(st.integers(min_value=1, max_value=max_cols))
    cells = draw(
        st.lists(
            st.integers(min_value=1, max_value=9),
            min_size=rows * cols,
            max_size=rows * cols,
        )
    )
    grid = [cells[r * cols : (r + 1) * cols] for r in range(rows)]
    sr = draw(st.integers(min_value=0, max_value=rows - 1))
    sc = draw(st.integers(min_value=0, max_value=cols - 1))
    gr = draw(st.integers(min_value=0, max_value=rows - 1))
    gc = draw(st.integers(min_value=0, max_value=cols - 1))
    return grid, (sr, sc), (gr, gc)


def _grid_shortest_cost(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> float:
    """Dijkstra oracle: shortest entry-cost path over the grid's 4-neighbor graph."""
    rows, cols = len(grid), len(grid[0])

    def idx(r: int, c: int) -> int:
        return r * cols + c

    edges: list[tuple[int, int, float]] = []
    for r in range(rows):
        for c in range(cols):
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    edges.append((idx(r, c), idx(nr, nc), float(grid[nr][nc])))

    dist = dijkstra(rows * cols, edges, idx(*start))
    return dist[idx(*goal)]


class TestAStarProperties:
    @given(data=_grids_with_endpoints())
    def test_path_cost_matches_dijkstra_oracle(
        self, data: tuple[list[list[int]], tuple[int, int], tuple[int, int]]
    ) -> None:
        """A* path cost must match Dijkstra's shortest-path cost on the same grid."""
        grid, start, goal = data
        path = a_star(grid, start, goal)
        assert path is not None
        cost = sum(grid[r][c] for r, c in path[1:])
        assert cost == _grid_shortest_cost(grid, start, goal)
