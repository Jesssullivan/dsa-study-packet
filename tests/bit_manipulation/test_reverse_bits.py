"""Tests for reverse bits."""

from hypothesis import given
from hypothesis import strategies as st

from algo.bit_manipulation.reverse_bits import (
    reverse_bits,
    reverse_bits_divide_conquer,
)


class TestReverseBits:
    def test_known_value(self) -> None:
        assert reverse_bits(0b00000010100101000001111010011100) == 964176192

    def test_all_ones(self) -> None:
        assert reverse_bits(0xFFFFFFFF) == 0xFFFFFFFF

    def test_zero(self) -> None:
        assert reverse_bits(0) == 0

    def test_one(self) -> None:
        # 1 = ...0001, reversed = 1000...0 = 2^31
        assert reverse_bits(1) == 1 << 31

    def test_double_reverse_is_identity(self) -> None:
        n = 43261596
        assert reverse_bits(reverse_bits(n)) == n


class TestReverseBitsDivideConquer:
    def test_known_value(self) -> None:
        n = 0b00000010100101000001111010011100
        assert reverse_bits_divide_conquer(n) == 964176192

    def test_zero(self) -> None:
        assert reverse_bits_divide_conquer(0) == 0

    @given(n=st.integers(min_value=0, max_value=0xFFFFFFFF))
    def test_matches_iterative(self, n: int) -> None:
        assert reverse_bits_divide_conquer(n) == reverse_bits(n)
