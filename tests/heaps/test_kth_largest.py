"""Tests for kth largest element."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.heaps.kth_largest import KthLargest, find_kth_largest


class TestFindKthLargest:
    def test_basic(self) -> None:
        assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    def test_k_equals_one(self) -> None:
        assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 1) == 6

    def test_k_equals_length(self) -> None:
        assert find_kth_largest([3, 2, 1], 3) == 1

    def test_duplicates(self) -> None:
        assert find_kth_largest([1, 1, 1, 1], 2) == 1

    def test_single_element(self) -> None:
        assert find_kth_largest([7], 1) == 7

    def test_k_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            find_kth_largest([1, 2, 3], 0)

    def test_k_too_large_raises(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            find_kth_largest([1, 2], 3)

    @given(
        data=st.lists(
            st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=100
        ),
    )
    def test_matches_sorted(self, data: list[int]) -> None:
        k = 1
        assert find_kth_largest(data, k) == sorted(data, reverse=True)[k - 1]


class TestKthLargestStream:
    def test_leetcode_example(self) -> None:
        kl = KthLargest(3, [4, 5, 8, 2])
        assert kl.add(3) == 4
        assert kl.add(5) == 5
        assert kl.add(10) == 5
        assert kl.add(9) == 8
        assert kl.add(4) == 8

    def test_empty_initial(self) -> None:
        kl = KthLargest(2, [])
        assert kl.add(1) == 1
        assert kl.add(3) == 1
        assert kl.add(5) == 3

    def test_k_one(self) -> None:
        kl = KthLargest(1, [])
        assert kl.add(10) == 10
        assert kl.add(20) == 20
        assert kl.add(5) == 20

    def test_all_same(self) -> None:
        kl = KthLargest(2, [5, 5, 5])
        assert kl.add(5) == 5
