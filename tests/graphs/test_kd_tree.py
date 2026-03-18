"""Tests for KD-tree nearest neighbor search."""

import math

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
