"""Tests for counting bits."""

from hypothesis import given
from hypothesis import strategies as st

from algo.bit_manipulation.counting_bits import counting_bits


class TestCountingBits:
    def test_zero(self) -> None:
        assert counting_bits(0) == [0]

    def test_five(self) -> None:
        assert counting_bits(5) == [0, 1, 1, 2, 1, 2]

    def test_two(self) -> None:
        assert counting_bits(2) == [0, 1, 1]

    def test_one(self) -> None:
        assert counting_bits(1) == [0, 1]

    def test_length(self) -> None:
        assert len(counting_bits(10)) == 11

    @given(n=st.integers(min_value=0, max_value=500))
    def test_matches_bin_count(self, n: int) -> None:
        result = counting_bits(n)
        for i in range(n + 1):
            assert result[i] == bin(i).count("1")
