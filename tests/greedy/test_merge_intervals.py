"""Tests for merge intervals."""

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
