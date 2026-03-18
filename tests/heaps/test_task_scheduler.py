"""Tests for task scheduler."""

from algo.heaps.task_scheduler import least_interval


class TestLeastInterval:
    def test_basic(self) -> None:
        assert least_interval(["A", "A", "A", "B", "B", "B"], 2) == 8

    def test_no_cooldown(self) -> None:
        assert least_interval(["A", "A", "A", "B", "B", "B"], 0) == 6

    def test_single_task_type(self) -> None:
        assert least_interval(["A", "A", "A"], 2) == 7

    def test_all_unique(self) -> None:
        assert least_interval(["A", "B", "C", "D"], 2) == 4

    def test_empty_tasks(self) -> None:
        assert least_interval([], 5) == 0

    def test_one_task(self) -> None:
        assert least_interval(["A"], 100) == 1

    def test_cooldown_one(self) -> None:
        # A B A B A => 5 intervals (cooldown of 1 means 1 gap between same tasks)
        assert least_interval(["A", "A", "A", "B", "B"], 1) == 5
