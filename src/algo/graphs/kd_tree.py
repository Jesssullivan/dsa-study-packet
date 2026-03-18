"""K-dimensional tree for nearest neighbor search.

Problem:
    Given a set of k-dimensional points, build a data structure that
    supports efficient nearest-neighbor queries.

Approach:
    Recursively partition points by cycling through dimensions,
    splitting on the median. For nearest-neighbor queries, traverse
    the tree pruning branches whose bounding hyperplane is farther
    than the current best distance.

When to use:
    Nearest neighbor in multi-dimensional space — "closest point",
    "k-nearest neighbors", range search in 2D/3D. Aviation: closest
    waypoint/airport lookup, collision avoidance in 3D airspace.
    See also: geohash_grid for grid-based spatial indexing.

Complexity:
    Build: O(n log n)
    Query: O(log n) average, O(n) worst case
    Space: O(n)
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

type Point = tuple[float, ...]


class KDNode:
    """A node in a KD-tree."""

    __slots__ = ("axis", "left", "point", "right")

    def __init__(
        self,
        point: Point,
        axis: int,
        left: KDNode | None = None,
        right: KDNode | None = None,
    ) -> None:
        self.point = point
        self.axis = axis
        self.left = left
        self.right = right


class KDTree:
    """K-dimensional tree for nearest neighbor search.

    >>> tree = KDTree([(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)])
    >>> tree.nearest((5, 5))
    (5, 4)
    """

    def __init__(self, points: Sequence[Point]) -> None:
        if not points:
            self.root: KDNode | None = None
            self._k = 0
        else:
            self._k = len(points[0])
            self.root = self._build(list(points), depth=0)

    def _build(self, points: list[Point], depth: int) -> KDNode | None:
        if not points:
            return None

        axis = depth % self._k
        points.sort(key=lambda p: p[axis])
        mid = len(points) // 2

        return KDNode(
            point=points[mid],
            axis=axis,
            left=self._build(points[:mid], depth + 1),
            right=self._build(points[mid + 1 :], depth + 1),
        )

    def nearest(self, target: Point) -> Point | None:
        """Return the nearest point to *target*, or None if tree is empty."""
        if self.root is None:
            return None

        best: list[tuple[float, Point]] = [(float("inf"), target)]
        self._search(self.root, target, best)
        return best[0][1]

    def _search(
        self,
        node: KDNode | None,
        target: Point,
        best: list[tuple[float, Point]],
    ) -> None:
        if node is None:
            return

        dist = _squared_distance(node.point, target)
        if dist < best[0][0]:
            best[0] = (dist, node.point)

        axis = node.axis
        diff = target[axis] - node.point[axis]

        # Search the side of the splitting plane that contains target first
        near = node.left if diff <= 0 else node.right
        far = node.right if diff <= 0 else node.left

        self._search(near, target, best)

        # Only search the far side if the splitting plane is closer than best
        if diff * diff < best[0][0]:
            self._search(far, target, best)

    def range_search(self, target: Point, radius: float) -> list[Point]:
        """Return all points within *radius* of *target*."""
        results: list[Point] = []
        r_sq = radius * radius
        self._range_search(self.root, target, r_sq, results)
        return results

    def _range_search(
        self,
        node: KDNode | None,
        target: Point,
        r_sq: float,
        results: list[Point],
    ) -> None:
        if node is None:
            return

        dist = _squared_distance(node.point, target)
        if dist <= r_sq:
            results.append(node.point)

        axis = node.axis
        diff = target[axis] - node.point[axis]

        near = node.left if diff <= 0 else node.right
        far = node.right if diff <= 0 else node.left

        self._range_search(near, target, r_sq, results)
        if diff * diff <= r_sq:
            self._range_search(far, target, r_sq, results)


def _squared_distance(a: Point, b: Point) -> float:
    return sum((ai - bi) ** 2 for ai, bi in zip(a, b, strict=True))
