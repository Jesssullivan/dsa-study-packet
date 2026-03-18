"""Tests for course schedule (cycle detection)."""

from algo.graphs.course_schedule import can_finish, find_order


class TestCanFinish:
    def test_no_prerequisites(self) -> None:
        assert can_finish(3, []) is True

    def test_simple_chain(self) -> None:
        assert can_finish(2, [[1, 0]]) is True

    def test_cycle(self) -> None:
        assert can_finish(2, [[1, 0], [0, 1]]) is False

    def test_larger_dag(self) -> None:
        assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True

    def test_larger_cycle(self) -> None:
        assert can_finish(3, [[0, 1], [1, 2], [2, 0]]) is False

    def test_single_course(self) -> None:
        assert can_finish(1, []) is True


class TestFindOrder:
    def test_valid_order(self) -> None:
        order = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
        assert len(order) == 4
        assert order.index(0) < order.index(1)
        assert order.index(0) < order.index(2)
        assert order.index(1) < order.index(3)
        assert order.index(2) < order.index(3)

    def test_cycle_returns_empty(self) -> None:
        assert find_order(2, [[1, 0], [0, 1]]) == []

    def test_no_deps(self) -> None:
        order = find_order(3, [])
        assert sorted(order) == [0, 1, 2]

    def test_single_course(self) -> None:
        assert find_order(1, []) == [0]
