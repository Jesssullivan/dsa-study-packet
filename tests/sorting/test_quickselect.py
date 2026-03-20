"""Tests for quickselect."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.sorting.quickselect import quickselect


class TestQuickselect:
    def test_basic(self) -> None:
        assert quickselect([3, 2, 1, 5, 6, 4], 2) == 2

    def test_single_element(self) -> None:
        assert quickselect([7], 1) == 7

    def test_kth_largest_equivalent(self) -> None:
        nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
        # 4th smallest = 3
        assert quickselect(list(nums), 4) == 3

    def test_k_equals_length(self) -> None:
        assert quickselect([5, 3, 1, 2, 4], 5) == 5

    def test_k_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError):
            quickselect([1, 2], 3)

    def test_k_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            quickselect([1, 2], 0)

    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100), min_size=1, max_size=50
        ),
    )
    def test_matches_sorted(self, data: list[int]) -> None:
        k = 1
        assert quickselect(list(data), k) == sorted(data)[k - 1]
