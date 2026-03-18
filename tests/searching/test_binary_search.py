"""Tests for binary search."""

from hypothesis import given
from hypothesis import strategies as st

from algo.searching.binary_search import binary_search, binary_search_recursive


class TestBinarySearch:
    def test_found_middle(self) -> None:
        assert binary_search([1, 3, 5, 7, 9], 5) == 2

    def test_found_first(self) -> None:
        assert binary_search([1, 3, 5, 7, 9], 1) == 0

    def test_found_last(self) -> None:
        assert binary_search([1, 3, 5, 7, 9], 9) == 4

    def test_not_found(self) -> None:
        assert binary_search([1, 3, 5, 7, 9], 4) == -1

    def test_empty_array(self) -> None:
        assert binary_search([], 1) == -1

    def test_single_element_found(self) -> None:
        assert binary_search([5], 5) == 0

    def test_single_element_not_found(self) -> None:
        assert binary_search([5], 3) == -1

    @given(
        data=st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=1,
            max_size=100,
            unique=True,
        ),
    )
    def test_finds_all_present_elements(self, data: list[int]) -> None:
        """Every element in the sorted array should be found."""
        data.sort()
        for i, val in enumerate(data):
            assert binary_search(data, val) == i


class TestBinarySearchRecursive:
    def test_found(self) -> None:
        assert binary_search_recursive([2, 4, 6, 8, 10], 8) == 3

    def test_not_found(self) -> None:
        assert binary_search_recursive([2, 4, 6, 8, 10], 5) == -1

    def test_empty(self) -> None:
        assert binary_search_recursive([], 1) == -1

    def test_single_element(self) -> None:
        assert binary_search_recursive([7], 7) == 0

    @given(
        data=st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=1,
            max_size=100,
            unique=True,
        ),
    )
    def test_agrees_with_iterative(self, data: list[int]) -> None:
        """Recursive and iterative must return the same result."""
        data.sort()
        target = data[0]
        assert binary_search_recursive(data, target) == binary_search(data, target)
