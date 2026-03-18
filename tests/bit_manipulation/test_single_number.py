"""Tests for single number."""

from hypothesis import given
from hypothesis import strategies as st

from algo.bit_manipulation.single_number import single_number


class TestSingleNumber:
    def test_basic(self) -> None:
        assert single_number([4, 1, 2, 1, 2]) == 4

    def test_single_element(self) -> None:
        assert single_number([1]) == 1

    def test_negative_numbers(self) -> None:
        assert single_number([-1, 2, -1]) == 2

    def test_zero_is_single(self) -> None:
        assert single_number([0, 3, 3]) == 0

    def test_larger_array(self) -> None:
        assert single_number([5, 3, 5, 3, 7]) == 7

    @given(
        unique=st.integers(min_value=-1000, max_value=1000),
        pairs=st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=0,
            max_size=20,
        ),
    )
    def test_always_finds_unique(self, unique: int, pairs: list[int]) -> None:
        nums = [unique]
        for p in pairs:
            if p == unique:
                continue
            nums.extend([p, p])
        assert single_number(nums) == unique
