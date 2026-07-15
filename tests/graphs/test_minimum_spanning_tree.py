"""Tests for minimum spanning tree algorithms."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.minimum_spanning_tree import UnionFind, kruskal, prim


class TestUnionFind:
    def test_initial_components(self) -> None:
        uf = UnionFind(5)
        assert uf.components == 5

    def test_union_and_find(self) -> None:
        uf = UnionFind(4)
        assert uf.union(0, 1) is True
        assert uf.find(0) == uf.find(1)
        assert uf.components == 3

    def test_redundant_union(self) -> None:
        uf = UnionFind(3)
        uf.union(0, 1)
        assert uf.union(0, 1) is False

    def test_transitive(self) -> None:
        uf = UnionFind(3)
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.find(0) == uf.find(2)
        assert uf.components == 1


def _mst_weight(mst: list[tuple[int, int, float]]) -> float:
    return sum(w for _, _, w in mst)


class TestKruskal:
    def test_simple_triangle(self) -> None:
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]
        mst = kruskal(3, edges)
        assert _mst_weight(mst) == 3

    def test_four_nodes(self) -> None:
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]
        mst = kruskal(4, edges)
        assert len(mst) == 3
        assert _mst_weight(mst) == 7

    def test_single_node(self) -> None:
        assert kruskal(1, []) == []

    def test_two_nodes(self) -> None:
        mst = kruskal(2, [(0, 1, 5)])
        assert _mst_weight(mst) == 5


class TestPrim:
    def test_simple_triangle(self) -> None:
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]
        mst = prim(3, edges)
        assert _mst_weight(mst) == 3

    def test_four_nodes(self) -> None:
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]
        mst = prim(4, edges)
        assert len(mst) == 3
        assert _mst_weight(mst) == 7

    def test_single_node(self) -> None:
        assert prim(1, []) == []

    def test_two_nodes(self) -> None:
        mst = prim(2, [(0, 1, 5)])
        assert _mst_weight(mst) == 5


@st.composite
def connected_weighted_graphs(
    draw: st.DrawFn, max_nodes: int = 8
) -> tuple[int, list[tuple[int, int, float]]]:
    """A random connected undirected weighted graph."""
    n = draw(st.integers(min_value=1, max_value=max_nodes))
    edges: list[tuple[int, int, float]] = []
    # Random spanning tree guarantees connectivity.
    for i in range(1, n):
        parent = draw(st.integers(min_value=0, max_value=i - 1))
        w = draw(st.integers(min_value=1, max_value=20))
        edges.append((parent, i, float(w)))
    if n > 1:
        extra_pairs = draw(
            st.lists(
                st.tuples(
                    st.integers(min_value=0, max_value=n - 1),
                    st.integers(min_value=0, max_value=n - 1),
                ),
                max_size=n,
            )
        )
        for u, v in extra_pairs:
            if u != v:
                w = draw(st.integers(min_value=1, max_value=20))
                edges.append((u, v, float(w)))
    return n, edges


class TestMSTProperties:
    @given(data=connected_weighted_graphs())
    def test_kruskal_and_prim_agree(
        self, data: tuple[int, list[tuple[int, int, float]]]
    ) -> None:
        """Kruskal and Prim must find the same total weight and edge count."""
        n, edges = data
        mst_kruskal = kruskal(n, edges)
        mst_prim = prim(n, edges)
        expected_edge_count = max(n - 1, 0)
        assert len(mst_kruskal) == expected_edge_count
        assert len(mst_prim) == expected_edge_count
        assert _mst_weight(mst_kruskal) == _mst_weight(mst_prim)
