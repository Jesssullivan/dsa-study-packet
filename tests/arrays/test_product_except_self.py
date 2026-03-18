"""Tests for the product-except-self problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.arrays.product_except_self import product_except_self


class TestProductExceptSelf:
    def test_basic(self) -> None:
        assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]

    def test_contains_zero(self) -> None:
        assert product_except_self([0, 1, 2, 3]) == [6, 0, 0, 0]

    def test_two_zeros(self) -> None:
        assert product_except_self([0, 0, 2]) == [0, 0, 0]

    def test_negative_numbers(self) -> None:
        assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    def test_two_elements(self) -> None:
        assert product_except_self([5, 3]) == [3, 5]

    def test_single_element(self) -> None:
        assert product_except_self([42]) == [1]

    @given(
        data=st.lists(
            st.integers(min_value=-10, max_value=10),
            min_size=1,
            max_size=20,
        ),
    )
    def test_matches_brute_force(self, data: list[int]) -> None:
        import math

        result = product_except_self(data)
        for i, val in enumerate(result):
            expected = math.prod(data[:i]) * math.prod(data[i + 1 :])
            assert val == expected
