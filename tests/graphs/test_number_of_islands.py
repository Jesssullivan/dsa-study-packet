"""Tests for the number of islands problem."""

from algo.graphs.number_of_islands import num_islands


class TestNumIslands:
    def test_single_island(self) -> None:
        grid = [
            ["1", "1", "1"],
            ["0", "1", "0"],
            ["0", "0", "0"],
        ]
        assert num_islands(grid) == 1

    def test_two_islands(self) -> None:
        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
        assert num_islands(grid) == 3

    def test_all_water(self) -> None:
        grid = [["0", "0"], ["0", "0"]]
        assert num_islands(grid) == 0

    def test_all_land(self) -> None:
        grid = [["1", "1"], ["1", "1"]]
        assert num_islands(grid) == 1

    def test_empty_grid(self) -> None:
        assert num_islands([]) == 0
        assert num_islands([[]]) == 0

    def test_single_cell(self) -> None:
        assert num_islands([["1"]]) == 1
        assert num_islands([["0"]]) == 0
