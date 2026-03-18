"""Tests for interval scheduling."""

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
