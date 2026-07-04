"""Tests for merge intervals."""

from hypothesis import given
from hypothesis import strategies as st

from algo.greedy.merge_intervals import merge_intervals


class TestMergeIntervals:
    def test_basic(self) -> None:
        result = merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
        assert result == [[1, 6], [8, 10], [15, 18]]

    def test_fully_overlapping(self) -> None:
        assert merge_intervals([[1, 4], [2, 3]]) == [[1, 4]]

    def test_no_overlap(self) -> None:
        result = merge_intervals([[1, 2], [3, 4], [5, 6]])
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_single_interval(self) -> None:
        assert merge_intervals([[1, 5]]) == [[1, 5]]

    def test_empty(self) -> None:
        assert merge_intervals([]) == []

    def test_touching_intervals(self) -> None:
        result = merge_intervals([[1, 2], [2, 3]])
        assert result == [[1, 3]]


def _covered(intervals: list[list[int]]) -> set[int]:
    """Integer point-set covered by a list of inclusive intervals."""
    points: set[int] = set()
    for start, end in intervals:
        points.update(range(start, end + 1))
    return points


class TestMergeIntervalsProperties:
    @given(
        raw=st.lists(
            st.tuples(
                st.integers(min_value=-50, max_value=50),
                st.integers(min_value=0, max_value=50),
            ),
            max_size=20,
        ),
    )
    def test_disjoint_sorted_same_coverage(self, raw: list[tuple[int, int]]) -> None:
        """Output is well-formed, strictly separated, and covers the same points."""
        intervals = [[start, start + length] for start, length in raw]
        merged = merge_intervals(intervals)

        # every output interval is well-formed (start <= end)
        for iv in merged:
            assert iv[0] <= iv[1]

        # sorted by start and strictly separated (touching intervals merge)
        for i in range(len(merged) - 1):
            assert merged[i + 1][0] > merged[i][1]

        # identical integer point coverage to the input
        assert _covered(merged) == _covered(intervals)

        # merging never increases the interval count
        assert len(merged) <= len(intervals)
