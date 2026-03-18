"""Tests for find minimum in rotated sorted array."""

from hypothesis import given
from hypothesis import strategies as st

from algo.searching.find_minimum_rotated import find_min


class TestFindMin:
    def test_basic(self) -> None:
        assert find_min([3, 4, 5, 1, 2]) == 1

    def test_larger_rotation(self) -> None:
        assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0

    def test_not_rotated(self) -> None:
        assert find_min([1, 2, 3, 4, 5]) == 1

    def test_single_element(self) -> None:
        assert find_min([1]) == 1

    def test_two_elements(self) -> None:
        assert find_min([2, 1]) == 1

    def test_two_elements_sorted(self) -> None:
        assert find_min([1, 2]) == 1

    @given(
        data=st.lists(
            st.integers(min_value=-500, max_value=500),
            min_size=1,
            max_size=50,
            unique=True,
        ),
        pivot=st.integers(min_value=0, max_value=1000),
    )
    def test_matches_builtin_min(self, data: list[int], pivot: int) -> None:
        """find_min must agree with built-in min() for any rotation."""
        data.sort()
        k = pivot % len(data)
        rotated = data[k:] + data[:k]
        assert find_min(rotated) == min(data)
