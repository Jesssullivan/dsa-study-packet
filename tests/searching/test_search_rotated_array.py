"""Tests for search in rotated sorted array."""

from hypothesis import given
from hypothesis import strategies as st

from algo.searching.search_rotated_array import search_rotated


class TestSearchRotated:
    def test_found_in_right_half(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4

    def test_found_in_left_half(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 5) == 1

    def test_not_found(self) -> None:
        assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1

    def test_single_element_found(self) -> None:
        assert search_rotated([1], 1) == 0

    def test_single_element_not_found(self) -> None:
        assert search_rotated([1], 0) == -1

    def test_not_rotated(self) -> None:
        assert search_rotated([1, 2, 3, 4, 5], 3) == 2

    def test_rotated_by_one(self) -> None:
        assert search_rotated([5, 1, 2, 3, 4], 5) == 0

    @given(
        data=st.lists(
            st.integers(min_value=-500, max_value=500),
            min_size=1,
            max_size=50,
            unique=True,
        ),
        pivot=st.integers(min_value=0, max_value=1000),
    )
    def test_finds_all_elements_in_rotated(self, data: list[int], pivot: int) -> None:
        """Every element should be found regardless of rotation amount."""
        data.sort()
        k = pivot % len(data)
        rotated = data[k:] + data[:k]
        for i, val in enumerate(rotated):
            assert search_rotated(rotated, val) == i
