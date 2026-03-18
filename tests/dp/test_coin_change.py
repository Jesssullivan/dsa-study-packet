"""Tests for coin change."""

from algo.dp.coin_change import coin_change


class TestCoinChange:
    def test_basic(self) -> None:
        assert coin_change([1, 5, 10, 25], 30) == 2

    def test_standard_example(self) -> None:
        assert coin_change([1, 2, 5], 11) == 3

    def test_impossible(self) -> None:
        assert coin_change([2], 3) == -1

    def test_zero_amount(self) -> None:
        assert coin_change([1], 0) == 0

    def test_single_coin_exact(self) -> None:
        assert coin_change([3], 9) == 3

    def test_large_denomination(self) -> None:
        assert coin_change([1, 2, 5], 100) == 20
