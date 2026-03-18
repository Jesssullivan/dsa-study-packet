"""Tests for the pow(x, n) problem."""

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.recursion.pow_x_n import my_pow


class TestMyPow:
    def test_positive_exponent(self) -> None:
        assert my_pow(2.0, 10) == pytest.approx(1024.0)

    def test_negative_exponent(self) -> None:
        assert my_pow(2.0, -2) == pytest.approx(0.25)

    def test_zero_exponent(self) -> None:
        assert my_pow(5.0, 0) == pytest.approx(1.0)

    def test_exponent_one(self) -> None:
        assert my_pow(3.0, 1) == pytest.approx(3.0)

    def test_fractional_base(self) -> None:
        assert my_pow(0.5, 3) == pytest.approx(0.125)

    def test_negative_base_odd_exponent(self) -> None:
        assert my_pow(-2.0, 3) == pytest.approx(-8.0)

    @given(
        x=st.floats(
            min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
        n=st.integers(min_value=0, max_value=20),
    )
    def test_matches_builtin_pow(self, x: float, n: int) -> None:
        result = my_pow(x, n)
        expected = math.pow(x, n)
        assert result == pytest.approx(expected, rel=1e-9)
