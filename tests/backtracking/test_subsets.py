"""Tests for subsets generation."""

from hypothesis import given
from hypothesis import strategies as st

from algo.backtracking.subsets import subsets


class TestSubsets:
    def test_three_elements(self) -> None:
        result = subsets([1, 2, 3])
        assert len(result) == 8
        assert [] in result
        assert [1, 2, 3] in result

    def test_single_element(self) -> None:
        assert sorted(subsets([0])) == [[], [0]]

    def test_empty(self) -> None:
        assert subsets([]) == [[]]

    def test_two_elements(self) -> None:
        result = subsets([1, 2])
        assert len(result) == 4
        assert [1] in result
        assert [2] in result

    def test_no_duplicates(self) -> None:
        result = subsets([1, 2, 3])
        tuples = [tuple(s) for s in result]
        assert len(tuples) == len(set(tuples))

    @given(
        data=st.lists(
            st.integers(min_value=-10, max_value=10),
            min_size=0,
            max_size=8,
            unique=True,
        ),
    )
    def test_power_set_size(self, data: list[int]) -> None:
        assert len(subsets(data)) == 2 ** len(data)
