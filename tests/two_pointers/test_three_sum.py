"""Tests for the 3Sum problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.two_pointers.three_sum import three_sum


class TestThreeSum:
    def test_basic(self) -> None:
        assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]

    def test_all_zeros(self) -> None:
        assert three_sum([0, 0, 0]) == [[0, 0, 0]]

    def test_no_solution(self) -> None:
        assert three_sum([1, 2, 3]) == []

    def test_empty(self) -> None:
        assert three_sum([]) == []

    def test_duplicates_skipped(self) -> None:
        result = three_sum([-2, 0, 0, 2, 2])
        assert result == [[-2, 0, 2]]

    def test_multiple_triplets(self) -> None:
        result = three_sum([-1, 0, 1, 2, -1, -4, -2, -3, 3, 0, 4])
        # All triplets should sum to zero and be unique
        seen: set[tuple[int, ...]] = set()
        for triplet in result:
            assert sum(triplet) == 0
            key = tuple(triplet)
            assert key not in seen
            seen.add(key)

    @given(
        data=st.lists(
            st.integers(min_value=-10, max_value=10),
            min_size=0,
            max_size=15,
        ),
    )
    def test_all_triplets_sum_to_zero_and_are_unique(self, data: list[int]) -> None:
        result = three_sum(data)
        seen: set[tuple[int, ...]] = set()
        for triplet in result:
            assert sum(triplet) == 0
            key = tuple(triplet)
            assert key not in seen
            seen.add(key)
            # every element of the triplet must come from the input
            for val in triplet:
                assert data.count(val) > 0
