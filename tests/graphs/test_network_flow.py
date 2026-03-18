"""Tests for maximum network flow (Edmonds-Karp)."""

from algo.graphs.network_flow import edmonds_karp


class TestEdmondsKarp:
    def test_simple_two_paths(self) -> None:
        # s->a->t and s->b->t, each capacity 10
        edges = [(0, 1, 10), (0, 2, 10), (1, 3, 10), (2, 3, 10)]
        assert edmonds_karp(4, edges, 0, 3) == 20

    def test_bottleneck(self) -> None:
        edges = [(0, 1, 100), (1, 2, 1), (2, 3, 100)]
        assert edmonds_karp(4, edges, 0, 3) == 1

    def test_no_path(self) -> None:
        edges = [(0, 1, 5)]
        assert edmonds_karp(3, edges, 0, 2) == 0

    def test_parallel_edges(self) -> None:
        edges = [(0, 1, 5), (0, 1, 3)]
        assert edmonds_karp(2, edges, 0, 1) == 8

    def test_diamond_with_cross(self) -> None:
        edges = [
            (0, 1, 10), (0, 2, 10),
            (1, 3, 10), (2, 3, 10),
            (1, 2, 1),
        ]
        assert edmonds_karp(4, edges, 0, 3) == 20

    def test_single_edge(self) -> None:
        assert edmonds_karp(2, [(0, 1, 7)], 0, 1) == 7
