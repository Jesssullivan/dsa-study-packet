"""Tests for merge k sorted linked lists."""

from hypothesis import given
from hypothesis import strategies as st

from algo.heaps.merge_k_sorted_lists import (
    from_list,
    merge_k_sorted,
    merge_k_sorted_sorted,
    to_list,
)


class TestMergeKSorted:
    def test_basic(self) -> None:
        lists = [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
        assert to_list(merge_k_sorted(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_empty_input(self) -> None:
        assert merge_k_sorted([]) is None

    def test_all_empty_lists(self) -> None:
        assert merge_k_sorted([None, None, None]) is None

    def test_single_list(self) -> None:
        assert to_list(merge_k_sorted([from_list([1, 2, 3])])) == [1, 2, 3]

    def test_some_empty_lists(self) -> None:
        lists = [from_list([1, 3]), None, from_list([2, 4])]
        assert to_list(merge_k_sorted(lists)) == [1, 2, 3, 4]

    def test_single_element_lists(self) -> None:
        lists = [from_list([5]), from_list([1]), from_list([3])]
        assert to_list(merge_k_sorted(lists)) == [1, 3, 5]

    def test_negative_values(self) -> None:
        lists = [from_list([-5, -1, 3]), from_list([-3, 0, 2])]
        assert to_list(merge_k_sorted(lists)) == [-5, -3, -1, 0, 2, 3]

    @given(
        lists=st.lists(
            st.lists(st.integers(min_value=-100, max_value=100), max_size=10),
            max_size=6,
        ),
    )
    def test_matches_sorted_concatenation(self, lists: list[list[int]]) -> None:
        """Merging k sorted lists must equal sorting their concatenation."""
        sorted_lists = [sorted(nums) for nums in lists]
        linked = [from_list(nums) for nums in sorted_lists]
        expected = sorted(n for nums in sorted_lists for n in nums)
        assert to_list(merge_k_sorted(linked)) == expected


class TestMergeKSortedSorted:
    def test_basic(self) -> None:
        lists = [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
        assert to_list(merge_k_sorted_sorted(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_empty_input(self) -> None:
        assert merge_k_sorted_sorted([]) is None

    @given(
        lists=st.lists(
            st.lists(st.integers(min_value=-100, max_value=100), max_size=10),
            max_size=6,
        ),
    )
    def test_matches_heap_merge(self, lists: list[list[int]]) -> None:
        """The sort-all alternate must always agree with the heap-based primary."""
        sorted_lists = [sorted(nums) for nums in lists]
        linked_a = [from_list(nums) for nums in sorted_lists]
        linked_b = [from_list(nums) for nums in sorted_lists]
        assert to_list(merge_k_sorted_sorted(linked_a)) == to_list(
            merge_k_sorted(linked_b)
        )
