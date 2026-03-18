"""Tests for climbing stairs."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.dp.climbing_stairs import climb_stairs


class TestClimbStairs:
    def test_one_step(self) -> None:
        assert climb_stairs(1) == 1

    def test_two_steps(self) -> None:
        assert climb_stairs(2) == 2

    def test_five_steps(self) -> None:
        assert climb_stairs(5) == 8

    def test_zero_steps(self) -> None:
        assert climb_stairs(0) == 1

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            climb_stairs(-1)

    @given(n=st.integers(min_value=2, max_value=30))
    def test_fibonacci_recurrence(self, n: int) -> None:
        assert climb_stairs(n) == climb_stairs(n - 1) + climb_stairs(n - 2)
