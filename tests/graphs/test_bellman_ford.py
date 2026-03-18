"""Tests for Bellman-Ford shortest path algorithm."""

import pytest

from algo.graphs.bellman_ford import INF, NegativeCycleError, bellman_ford


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
