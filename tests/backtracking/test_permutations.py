"""Tests for permutations generation."""

import math

from hypothesis import given
from hypothesis import strategies as st

from algo.backtracking.permutations import permutations, permutations_itertools


class TestPermutations:
    def test_three_elements(self) -> None:
        result = permutations([1, 2, 3])
        assert len(result) == 6
        assert [1, 2, 3] in result
        assert [3, 2, 1] in result

    def test_single_element(self) -> None:
        assert permutations([1]) == [[1]]

    def test_two_elements(self) -> None:
        result = permutations([1, 2])
        assert sorted(result) == [[1, 2], [2, 1]]

    def test_empty(self) -> None:
        assert permutations([]) == [[]]

    def test_no_duplicates(self) -> None:
        result = permutations([1, 2, 3])
        tuples = [tuple(p) for p in result]
        assert len(tuples) == len(set(tuples))

    @given(
        data=st.lists(
            st.integers(min_value=-10, max_value=10),
            min_size=1,
            max_size=5,
            unique=True,
        ),
    )
    def test_factorial_count(self, data: list[int]) -> None:
        assert len(permutations(data)) == math.factorial(len(data))

    @given(
        data=st.lists(
            st.integers(min_value=-10, max_value=10),
            min_size=0,
            max_size=5,
            unique=True,
        ),
    )
    def test_matches_itertools_alternate(self, data: list[int]) -> None:
        """The stdlib alternate must produce the same set of permutations."""
        got = {tuple(p) for p in permutations(data)}
        expected = {tuple(p) for p in permutations_itertools(data)}
        assert got == expected
