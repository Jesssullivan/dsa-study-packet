"""Tests for merge two sorted linked lists."""

from hypothesis import given
from hypothesis import strategies as st

from algo.linked_lists.merge_two_sorted import from_list, merge_two_sorted, to_list


class TestMergeTwoSorted:
    def test_basic(self) -> None:
        result = merge_two_sorted(from_list([1, 3, 5]), from_list([2, 4, 6]))
        assert to_list(result) == [1, 2, 3, 4, 5, 6]

    def test_overlapping_values(self) -> None:
        result = merge_two_sorted(from_list([1, 2, 4]), from_list([1, 3, 4]))
        assert to_list(result) == [1, 1, 2, 3, 4, 4]

    def test_first_empty(self) -> None:
        result = merge_two_sorted(None, from_list([1, 2, 3]))
        assert to_list(result) == [1, 2, 3]

    def test_second_empty(self) -> None:
        result = merge_two_sorted(from_list([1, 2, 3]), None)
        assert to_list(result) == [1, 2, 3]

    def test_both_empty(self) -> None:
        assert merge_two_sorted(None, None) is None

    def test_single_elements(self) -> None:
        result = merge_two_sorted(from_list([2]), from_list([1]))
        assert to_list(result) == [1, 2]

    @given(
        a=st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=30),
        b=st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=30),
    )
    def test_result_is_sorted(self, a: list[int], b: list[int]) -> None:
        a.sort()
        b.sort()
        result = to_list(merge_two_sorted(from_list(a), from_list(b)))
        assert result == sorted(a + b)
