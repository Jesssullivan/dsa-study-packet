"""Tests for merge k sorted linked lists."""

from algo.heaps.merge_k_sorted_lists import from_list, merge_k_sorted, to_list


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
