"""Tests for maximum network flow (Edmonds-Karp)."""

from hypothesis import given
from hypothesis import strategies as st

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
            (0, 1, 10),
            (0, 2, 10),
            (1, 3, 10),
            (2, 3, 10),
            (1, 2, 1),
        ]
        assert edmonds_karp(4, edges, 0, 3) == 20

    def test_single_edge(self) -> None:
        assert edmonds_karp(2, [(0, 1, 7)], 0, 1) == 7


@st.composite
def random_flow_network(
    draw: st.DrawFn, max_nodes: int = 6
) -> tuple[int, list[tuple[int, int, int]], int, int]:
    n = draw(st.integers(min_value=2, max_value=max_nodes))
    source = draw(st.integers(min_value=0, max_value=n - 1))
    sink = draw(st.integers(min_value=0, max_value=n - 1))
    possible = [(u, v) for u in range(n) for v in range(n) if u != v]
    pairs = draw(st.lists(st.sampled_from(possible), max_size=n * 2))
    edges = [(u, v, draw(st.integers(min_value=1, max_value=20))) for u, v in pairs]
    return n, edges, source, sink


class TestEdmondsKarpProperties:
    @given(
        caps=st.lists(st.integers(min_value=1, max_value=50), min_size=1, max_size=8),
    )
    def test_chain_bottleneck(self, caps: list[int]) -> None:
        """Max flow through a simple chain equals the minimum edge capacity."""
        n = len(caps) + 1
        edges = [(i, i + 1, caps[i]) for i in range(len(caps))]
        assert edmonds_karp(n, edges, 0, n - 1) == min(caps)

    @given(data=random_flow_network())
    def test_flow_bounded_by_source_and_sink_cut(
        self, data: tuple[int, list[tuple[int, int, int]], int, int]
    ) -> None:
        """Max flow never exceeds capacity leaving source or entering sink."""
        n, edges, source, sink = data
        flow = edmonds_karp(n, edges, source, sink)
        out_cap = sum(cap for u, v, cap in edges if u == source)
        in_cap = sum(cap for u, v, cap in edges if v == sink)
        assert 0 <= flow <= out_cap
        assert 0 <= flow <= in_cap
