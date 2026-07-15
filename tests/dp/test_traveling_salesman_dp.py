"""Tests for traveling salesman DP."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.dp.traveling_salesman_dp import tsp, tsp_brute_force


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


@st.composite
def distance_matrix(draw: st.DrawFn) -> list[list[int]]:
    """Strategy: a small symmetric n x n distance matrix, zero diagonal."""
    n = draw(st.integers(min_value=1, max_value=6))
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w = draw(st.integers(min_value=1, max_value=30))
            dist[i][j] = w
            dist[j][i] = w
    return dist


class TestTSPProperties:
    @given(dist=distance_matrix())
    def test_matches_brute_force_oracle(self, dist: list[list[int]]) -> None:
        """The bitmask DP must always agree with the exhaustive permutation search."""
        assert tsp(dist) == tsp_brute_force(dist)
