"""Tests for KD-tree nearest neighbor search."""

import math

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.kd_tree import KDTree


class TestKDTree:
    def test_nearest_basic(self) -> None:
        points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
        tree = KDTree(points)
        assert tree.nearest((5, 5)) == (5, 4)

    def test_exact_match(self) -> None:
        points = [(1, 2), (3, 4), (5, 6)]
        tree = KDTree(points)
        assert tree.nearest((3, 4)) == (3, 4)

    def test_single_point(self) -> None:
        tree = KDTree([(10, 20)])
        assert tree.nearest((0, 0)) == (10, 20)

    def test_empty_tree(self) -> None:
        tree = KDTree([])
        assert tree.nearest((1, 2)) is None

    def test_three_dimensions(self) -> None:
        points = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        tree = KDTree(points)
        assert tree.nearest((0.9, 0.1, 0.1)) == (1, 0, 0)

    def test_range_search(self) -> None:
        points = [(0, 0), (1, 0), (2, 0), (10, 10)]
        tree = KDTree(points)
        results = tree.range_search((0, 0), 1.5)
        result_set = set(results)
        assert (0, 0) in result_set
        assert (1, 0) in result_set
        assert (10, 10) not in result_set

    def test_range_search_empty(self) -> None:
        points = [(10, 10), (20, 20)]
        tree = KDTree(points)
        assert tree.range_search((0, 0), 1.0) == []

    def test_nearest_brute_force_agreement(self) -> None:
        """Nearest result matches brute-force on a larger set."""
        points = [(float(i), float(i % 7)) for i in range(50)]
        tree = KDTree(points)
        target = (12.3, 4.5)
        result = tree.nearest(target)
        assert result is not None
        brute = min(points, key=lambda p: math.dist(p, target))
        assert result == brute


def _sq_dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b, strict=True))


_points_2d = st.lists(
    st.tuples(
        st.integers(min_value=-50, max_value=50),
        st.integers(min_value=-50, max_value=50),
    ),
    min_size=1,
    max_size=30,
)
_point_2d = st.tuples(
    st.integers(min_value=-50, max_value=50), st.integers(min_value=-50, max_value=50)
)


class TestKDTreeProperties:
    @given(points=_points_2d, target=_point_2d)
    def test_nearest_matches_brute_force(
        self, points: list[tuple[int, int]], target: tuple[int, int]
    ) -> None:
        tree = KDTree(points)
        result = tree.nearest(target)
        assert result is not None
        brute = min(_sq_dist(p, target) for p in points)
        # Compare distances (not identity) since ties may resolve to any
        # equally-close point.
        assert _sq_dist(result, target) == brute

    @given(
        points=_points_2d,
        target=_point_2d,
        radius=st.floats(min_value=0, max_value=80, allow_nan=False),
    )
    def test_range_search_matches_brute_force(
        self,
        points: list[tuple[int, int]],
        target: tuple[int, int],
        radius: float,
    ) -> None:
        tree = KDTree(points)
        result = set(tree.range_search(target, radius))
        r_sq = radius * radius
        expected = {p for p in points if _sq_dist(p, target) <= r_sq}
        assert result == expected
