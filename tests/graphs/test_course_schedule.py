"""Tests for course schedule (cycle detection)."""

from hypothesis import given
from hypothesis import strategies as st

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


@st.composite
def random_dag(draw: st.DrawFn, max_courses: int = 8) -> tuple[int, list[list[int]]]:
    """A random DAG's prerequisites: edges only run earlier -> later in a
    random permutation, so a cycle can never occur."""
    n = draw(st.integers(min_value=1, max_value=max_courses))
    order = draw(st.permutations(range(n)))
    possible_edges = [[order[j], order[i]] for i in range(n) for j in range(i + 1, n)]
    prereqs = (
        draw(st.lists(st.sampled_from(possible_edges), max_size=n * 2))
        if possible_edges
        else []
    )
    return n, prereqs


class TestCourseScheduleProperties:
    @given(data=random_dag())
    def test_acyclic_is_always_finishable(
        self, data: tuple[int, list[list[int]]]
    ) -> None:
        n, prereqs = data
        assert can_finish(n, prereqs) is True
        order = find_order(n, prereqs)
        assert len(order) == n
        pos = {course: i for i, course in enumerate(order)}
        assert all(pos[prereq] < pos[course] for course, prereq in prereqs)

    @given(n=st.integers(min_value=2, max_value=8))
    def test_full_chain_with_back_edge_is_cyclic(self, n: int) -> None:
        """A chain 0<-1<-...<-(n-1) plus a back edge (n-1)->0 forms one cycle."""
        prereqs = [[i, i - 1] for i in range(1, n)]
        prereqs.append([0, n - 1])  # course 0 also requires course n-1
        assert can_finish(n, prereqs) is False
        assert find_order(n, prereqs) == []
