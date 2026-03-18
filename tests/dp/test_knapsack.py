"""Tests for 0/1 knapsack."""

from algo.dp.knapsack import knapsack, knapsack_2d


class TestKnapsack:
    def test_basic(self) -> None:
        assert knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9

    def test_zero_capacity(self) -> None:
        assert knapsack([1, 2], [10, 20], 0) == 0

    def test_single_item_fits(self) -> None:
        assert knapsack([5], [10], 5) == 10

    def test_single_item_too_heavy(self) -> None:
        assert knapsack([5], [10], 4) == 0

    def test_all_items_fit(self) -> None:
        assert knapsack([1, 2, 3], [6, 10, 12], 10) == 28

    def test_empty(self) -> None:
        assert knapsack([], [], 10) == 0


class TestKnapsack2D:
    def test_matches_1d(self) -> None:
        weights = [1, 3, 4, 5]
        values = [1, 4, 5, 7]
        assert knapsack_2d(weights, values, 7) == knapsack(weights, values, 7)

    def test_basic(self) -> None:
        assert knapsack_2d([2, 3, 4, 5], [3, 4, 5, 6], 5) == 7

    def test_zero_capacity(self) -> None:
        assert knapsack_2d([1], [5], 0) == 0

    def test_no_items(self) -> None:
        assert knapsack_2d([], [], 5) == 0
