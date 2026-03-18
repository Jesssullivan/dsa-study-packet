"""Tests for Dijkstra's shortest-path algorithm."""

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
