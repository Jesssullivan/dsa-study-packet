"""Tests for the flatten nested list problem."""

from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from algo.recursion.flatten_nested_list import flatten_iterative, flatten_recursive


class TestFlattenRecursive:
    def test_basic(self) -> None:
        assert flatten_recursive([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]

    def test_empty(self) -> None:
        assert flatten_recursive([]) == []

    def test_already_flat(self) -> None:
        assert flatten_recursive([1, 2, 3]) == [1, 2, 3]

    def test_deeply_nested(self) -> None:
        assert flatten_recursive([[[[[1]]]]]) == [1]

    def test_mixed_nesting(self) -> None:
        assert flatten_recursive([1, [2], [[3]], [[[4]]]]) == [1, 2, 3, 4]

    def test_empty_sublists(self) -> None:
        assert flatten_recursive([1, [], [2, []], 3]) == [1, 2, 3]


class TestFlattenIterative:
    def test_basic(self) -> None:
        assert flatten_iterative([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]

    def test_empty(self) -> None:
        assert flatten_iterative([]) == []

    def test_already_flat(self) -> None:
        assert flatten_iterative([1, 2, 3]) == [1, 2, 3]

    def test_deeply_nested(self) -> None:
        assert flatten_iterative([[[[[1]]]]]) == [1]

    def test_empty_sublists(self) -> None:
        assert flatten_iterative([1, [], [2, []], 3]) == [1, 2, 3]


class TestFlattenEquivalence:
    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100),
            min_size=0,
            max_size=20,
        ),
    )
    def test_both_match_on_flat_input(self, data: list[int]) -> None:
        assert flatten_recursive(data) == flatten_iterative(data) == data

    def test_both_match_on_nested_input(self) -> None:
        nested: list[int | list[Any]] = [1, [2, 3], [4, [5, [6]]], 7, [[8]]]
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        assert flatten_recursive(nested) == expected
        assert flatten_iterative(nested) == expected
