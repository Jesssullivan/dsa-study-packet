"""Tests for longest increasing subsequence."""

from hypothesis import given
from hypothesis import strategies as st

from algo.dp.longest_increasing_subseq import length_of_lis


class TestLengthOfLIS:
    def test_basic(self) -> None:
        assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    def test_all_increasing(self) -> None:
        assert length_of_lis([1, 2, 3, 4, 5]) == 5

    def test_all_decreasing(self) -> None:
        assert length_of_lis([5, 4, 3, 2, 1]) == 1

    def test_single_element(self) -> None:
        assert length_of_lis([7]) == 1

    def test_empty(self) -> None:
        assert length_of_lis([]) == 0

    def test_duplicates(self) -> None:
        assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4

    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100), min_size=1, max_size=50
        ),
    )
    def test_result_within_bounds(self, data: list[int]) -> None:
        result = length_of_lis(data)
        assert 1 <= result <= len(data)
