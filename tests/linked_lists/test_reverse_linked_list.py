"""Tests for reverse linked list."""

from hypothesis import given
from hypothesis import strategies as st

from algo.linked_lists.reverse_linked_list import (
    from_list,
    reverse_iterative,
    reverse_recursive,
    to_list,
)


class TestReverseIterative:
    def test_basic(self) -> None:
        assert to_list(reverse_iterative(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]

    def test_single_node(self) -> None:
        assert to_list(reverse_iterative(from_list([42]))) == [42]

    def test_two_nodes(self) -> None:
        assert to_list(reverse_iterative(from_list([1, 2]))) == [2, 1]

    def test_empty_list(self) -> None:
        assert reverse_iterative(None) is None

    def test_negative_values(self) -> None:
        assert to_list(reverse_iterative(from_list([-3, -1, 0, 2]))) == [2, 0, -1, -3]

    @given(data=st.lists(st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=50))
    def test_double_reverse_is_identity(self, data: list[int]) -> None:
        head = from_list(data)
        assert to_list(reverse_iterative(reverse_iterative(head))) == data


class TestReverseRecursive:
    def test_basic(self) -> None:
        assert to_list(reverse_recursive(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]

    def test_single_node(self) -> None:
        assert to_list(reverse_recursive(from_list([42]))) == [42]

    def test_two_nodes(self) -> None:
        assert to_list(reverse_recursive(from_list([1, 2]))) == [2, 1]

    def test_empty_list(self) -> None:
        assert reverse_recursive(None) is None

    @given(data=st.lists(st.integers(min_value=-1000, max_value=1000), min_size=1, max_size=50))
    def test_matches_iterative(self, data: list[int]) -> None:
        assert to_list(reverse_recursive(from_list(data))) == to_list(
            reverse_iterative(from_list(data))
        )
