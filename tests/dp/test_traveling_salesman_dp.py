"""Tests for traveling salesman DP."""

import pytest

from algo.dp.traveling_salesman_dp import tsp


class TestTSP:
    def test_four_cities(self) -> None:
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ]
        assert tsp(dist) == 80

    def test_two_cities(self) -> None:
        dist = [[0, 5], [5, 0]]
        assert tsp(dist) == 10

    def test_single_city(self) -> None:
        assert tsp([[0]]) == 0

    def test_three_cities_symmetric(self) -> None:
        dist = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]
        # Optimal: 0->1->2->0 = 1+3+2 = 6 or 0->2->1->0 = 2+3+1 = 6
        assert tsp(dist) == 6

    @pytest.mark.slow
    def test_five_cities(self) -> None:
        dist = [
            [0, 3, 4, 2, 7],
            [3, 0, 4, 6, 3],
            [4, 4, 0, 5, 8],
            [2, 6, 5, 0, 6],
            [7, 3, 8, 6, 0],
        ]
        result = tsp(dist)
        assert isinstance(result, int)
        assert result > 0
