"""Tests for climbing stairs."""

import math

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
        with pytest.raises(ValueError):
            climb_stairs(-1)

    @given(n=st.integers(min_value=2, max_value=30))
    def test_fibonacci_recurrence(self, n: int) -> None:
        assert climb_stairs(n) == climb_stairs(n - 1) + climb_stairs(n - 2)

def _climb_enumerate(n: int) -> int:
    """Independent oracle: exhaustive count of 1/2-step sequences summing to n."""
    count = 0

    def rec(remaining: int) -> None:
        nonlocal count
        if remaining == 0:
            count += 1
            return
        rec(remaining - 1)
        if remaining >= 2:
            rec(remaining - 2)

    rec(n)
    return count

@given(n=st.integers(min_value=0, max_value=18))
def test_climb_matches_brute_force_enumeration(n: int) -> None:
    """climb_stairs equals an exhaustive enumeration of 1/2-step paths."""
    assert climb_stairs(n) == _climb_enumerate(n)

@given(n=st.integers(min_value=0, max_value=60))
def test_climb_matches_binomial_sum(n: int) -> None:
    """climb_stairs equals the closed form sum_j C(n - j, j) over 2-step counts."""
    expected = sum(math.comb(n - j, j) for j in range(n // 2 + 1))
    assert climb_stairs(n) == expected
