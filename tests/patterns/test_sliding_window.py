"""Tests for the sliding window pattern."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.patterns.sliding_window import max_sum_subarray


class TestMaxSumSubarray:
    def test_basic(self) -> None:
        assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9

    def test_single_element_window(self) -> None:
        assert max_sum_subarray([4, 2, 7, 1], 1) == 7

    def test_full_array_window(self) -> None:
        assert max_sum_subarray([1, 2, 3], 3) == 6

    def test_negative_numbers(self) -> None:
        assert max_sum_subarray([-1, -2, 5, -1, 3], 2) == 4

    def test_k_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            max_sum_subarray([1, 2, 3], 0)

    def test_k_too_large_raises(self) -> None:
        with pytest.raises(ValueError):
            max_sum_subarray([1, 2], 3)

    @given(
        data=st.lists(
            st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=100
        ),
    )
    def test_result_matches_brute_force(self, data: list[int]) -> None:
        k = 1  # use k=1 so brute force is just max()
        assert max_sum_subarray(data, k) == max(data)
