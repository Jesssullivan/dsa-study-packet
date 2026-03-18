"""Tests for the container-with-most-water problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.two_pointers.container_with_most_water import max_area


class TestMaxArea:
    def test_basic(self) -> None:
        assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    def test_two_lines(self) -> None:
        assert max_area([1, 1]) == 1

    def test_ascending(self) -> None:
        assert max_area([1, 2, 3, 4, 5]) == 6  # min(2,5)*3=6

    def test_descending(self) -> None:
        assert max_area([5, 4, 3, 2, 1]) == 6  # min(5,2)*3=6

    def test_equal_heights(self) -> None:
        assert max_area([4, 4, 4, 4]) == 12  # min(4,4)*3=12

    def test_empty_and_single(self) -> None:
        assert max_area([]) == 0
        assert max_area([5]) == 0

    @given(
        data=st.lists(
            st.integers(min_value=0, max_value=100),
            min_size=2,
            max_size=50,
        ),
    )
    def test_result_matches_brute_force(self, data: list[int]) -> None:
        expected = 0
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                expected = max(expected, min(data[i], data[j]) * (j - i))
        assert max_area(data) == expected
