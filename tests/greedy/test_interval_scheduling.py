"""Tests for interval scheduling."""

import itertools

from hypothesis import given
from hypothesis import strategies as st

from algo.greedy.interval_scheduling import max_non_overlapping, min_removals


class TestMaxNonOverlapping:
    def test_basic(self) -> None:
        assert max_non_overlapping([[1, 3], [2, 4], [3, 5], [0, 6]]) == 2

    def test_no_overlap(self) -> None:
        assert max_non_overlapping([[1, 2], [3, 4], [5, 6]]) == 3

    def test_all_overlap(self) -> None:
        assert max_non_overlapping([[1, 10], [2, 5], [3, 8]]) == 1

    def test_single_interval(self) -> None:
        assert max_non_overlapping([[0, 1]]) == 1

    def test_empty(self) -> None:
        assert max_non_overlapping([]) == 0

    def test_touching_intervals(self) -> None:
        assert max_non_overlapping([[1, 2], [2, 3], [3, 4]]) == 3


class TestMinRemovals:
    def test_basic(self) -> None:
        assert min_removals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1

    def test_no_removals_needed(self) -> None:
        assert min_removals([[1, 2], [3, 4]]) == 0

    def test_all_same(self) -> None:
        assert min_removals([[1, 2], [1, 2], [1, 2]]) == 2


def _max_non_overlapping_brute_force(intervals: list[list[int]]) -> int:
    """Independent oracle: try every subset, keep the largest non-overlapping one."""
    best = 0
    for size in range(len(intervals), 0, -1):
        for combo in itertools.combinations(intervals, size):
            ordered = sorted(combo, key=lambda iv: iv[0])
            if all(ordered[i][1] <= ordered[i + 1][0] for i in range(len(ordered) - 1)):
                best = max(best, size)
                break
        if best:
            break
    return best


class TestMaxNonOverlappingProperties:
    @given(
        raw=st.lists(
            st.tuples(
                st.integers(min_value=0, max_value=20),
                st.integers(min_value=1, max_value=10),
            ),
            max_size=8,
        ),
    )
    def test_matches_brute_force_oracle(self, raw: list[tuple[int, int]]) -> None:
        intervals = [[start, start + length] for start, length in raw]
        assert max_non_overlapping(intervals) == _max_non_overlapping_brute_force(
            intervals
        )
