"""Tests for daily temperatures."""

from hypothesis import given
from hypothesis import strategies as st

from algo.stacks_queues.daily_temperatures import daily_temperatures


class TestDailyTemperatures:
    def test_basic(self) -> None:
        assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [
            1,
            1,
            4,
            2,
            1,
            1,
            0,
            0,
        ]

    def test_ascending(self) -> None:
        assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]

    def test_descending(self) -> None:
        assert daily_temperatures([60, 50, 40, 30]) == [0, 0, 0, 0]

    def test_single_element(self) -> None:
        assert daily_temperatures([70]) == [0]

    def test_all_same(self) -> None:
        assert daily_temperatures([50, 50, 50]) == [0, 0, 0]

    def test_warm_at_end(self) -> None:
        assert daily_temperatures([30, 20, 10, 40]) == [3, 2, 1, 0]

    @given(
        temps=st.lists(
            st.integers(min_value=30, max_value=100),
            min_size=1,
            max_size=50,
        ),
    )
    def test_matches_brute_force(self, temps: list[int]) -> None:
        """Cross-check against O(n^2) brute force."""
        expected = [0] * len(temps)
        for i in range(len(temps)):
            for j in range(i + 1, len(temps)):
                if temps[j] > temps[i]:
                    expected[i] = j - i
                    break
        assert daily_temperatures(temps) == expected
