"""Tests for Bellman-Ford shortest path algorithm."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.bellman_ford import INF, NegativeCycleError, bellman_ford
from algo.graphs.dijkstra import dijkstra


class TestBellmanFord:
    def test_simple_graph(self) -> None:
        edges = [(0, 1, 1), (1, 2, 3), (0, 2, 10), (2, 3, 2)]
        assert bellman_ford(4, edges, 0) == [0, 1, 4, 6]

    def test_negative_weight(self) -> None:
        edges = [(0, 1, 4), (0, 2, 5), (1, 2, -3)]
        assert bellman_ford(3, edges, 0) == [0, 4, 1]

    def test_negative_cycle_raises(self) -> None:
        edges = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
        with pytest.raises(NegativeCycleError):
            bellman_ford(3, edges, 0)

    def test_unreachable_node(self) -> None:
        edges = [(0, 1, 5)]
        dist = bellman_ford(3, edges, 0)
        assert dist == [0, 5, INF]

    def test_single_node(self) -> None:
        assert bellman_ford(1, [], 0) == [0]

    def test_all_zero_weights(self) -> None:
        edges = [(0, 1, 0), (1, 2, 0)]
        assert bellman_ford(3, edges, 0) == [0, 0, 0]


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


class TestBellmanFordProperties:
    @given(data=_nonneg_weighted_graphs())
    def test_matches_dijkstra_oracle(
        self, data: tuple[int, list[tuple[int, int, float]], int]
    ) -> None:
        """On non-negative weights, no negative cycle can exist, and the
        result must agree with Dijkstra."""
        n, edges, source = data
        assert bellman_ford(n, edges, source) == dijkstra(n, edges, source)
