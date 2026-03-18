"""Tests for merge sort inversions."""

from hypothesis import given
from hypothesis import strategies as st

from algo.sorting.merge_sort_inversions import count_inversions


class TestCountInversions:
    def test_basic(self) -> None:
        assert count_inversions([2, 4, 1, 3, 5]) == 3

    def test_sorted_array(self) -> None:
        assert count_inversions([1, 2, 3, 4, 5]) == 0

    def test_reverse_sorted(self) -> None:
        assert count_inversions([5, 4, 3, 2, 1]) == 10

    def test_single_element(self) -> None:
        assert count_inversions([1]) == 0

    def test_empty(self) -> None:
        assert count_inversions([]) == 0

    def test_two_elements_inverted(self) -> None:
        assert count_inversions([2, 1]) == 1

    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100), min_size=0, max_size=50
        ),
    )
    def test_matches_brute_force(self, data: list[int]) -> None:
        expected = sum(
            1
            for i in range(len(data))
            for j in range(i + 1, len(data))
            if data[i] > data[j]
        )
        assert count_inversions(data) == expected
