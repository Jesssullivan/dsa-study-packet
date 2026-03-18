"""Tests for A* search on weighted grids."""

from algo.graphs.a_star_search import a_star, manhattan_distance


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
            [1,   1, 1],
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
