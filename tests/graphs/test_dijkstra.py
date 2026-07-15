"""Tests for Dijkstra's shortest-path algorithm."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.bellman_ford import bellman_ford
from algo.graphs.dijkstra import INF, dijkstra


class TestDijkstra:
    def test_simple_path(self) -> None:
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 4)]
        assert dijkstra(3, edges, 0) == [0, 1, 3]

    def test_diamond_graph(self) -> None:
        edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]
        assert dijkstra(4, edges, 0) == [0, 1, 3, 6]

    def test_unreachable_node(self) -> None:
        edges = [(0, 1, 5)]
        dist = dijkstra(3, edges, 0)
        assert dist[0] == 0
        assert dist[1] == 5
        assert dist[2] == INF

    def test_single_node(self) -> None:
        assert dijkstra(1, [], 0) == [0]

    def test_parallel_edges(self) -> None:
        edges = [(0, 1, 10), (0, 1, 3)]
        assert dijkstra(2, edges, 0) == [0, 3]

    def test_longer_graph(self) -> None:
        edges = [
            (0, 1, 7),
            (0, 2, 9),
            (0, 5, 14),
            (1, 2, 10),
            (1, 3, 15),
            (2, 3, 11),
            (2, 5, 2),
            (3, 4, 6),
            (4, 5, 9),
        ]
        dist = dijkstra(6, edges, 0)
        assert dist == [0, 7, 9, 20, 26, 11]


@st.composite
def _nonneg_weighted_graphs(
    draw: st.DrawFn, max_nodes: int = 8
) -> tuple[int, list[tuple[int, int, float]], int]:
    """A random directed graph with non-negative weights, plus a source."""
    n = draw(st.integers(min_value=1, max_value=max_nodes))
    possible = [(u, v) for u in range(n) for v in range(n) if u != v]
    edges: list[tuple[int, int, float]] = []
    if possible:
        pairs = draw(st.lists(st.sampled_from(possible), max_size=n * 2))
        edges = [
            (u, v, float(draw(st.integers(min_value=0, max_value=25))))
            for u, v in pairs
        ]
    source = draw(st.integers(min_value=0, max_value=n - 1))
    return n, edges, source


class TestDijkstraProperties:
    @given(data=_nonneg_weighted_graphs())
    def test_matches_bellman_ford_oracle(
        self, data: tuple[int, list[tuple[int, int, float]], int]
    ) -> None:
        """On non-negative weights, Dijkstra must agree with Bellman-Ford."""
        n, edges, source = data
        assert dijkstra(n, edges, source) == bellman_ford(n, edges, source)
