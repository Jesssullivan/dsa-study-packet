"""Tests for network delay time."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.dijkstra import dijkstra
from algo.graphs.network_delay_time import network_delay_time


class TestNetworkDelayTime:
    def test_basic(self) -> None:
        times = [(2, 1, 1), (2, 3, 1), (3, 4, 1)]
        assert network_delay_time(times, 4, 2) == 2

    def test_unreachable(self) -> None:
        times = [(1, 2, 1)]
        assert network_delay_time(times, 3, 1) == -1

    def test_single_node(self) -> None:
        assert network_delay_time([], 1, 1) == 0

    def test_two_paths(self) -> None:
        times = [(1, 2, 10), (1, 3, 1), (3, 2, 2)]
        assert network_delay_time(times, 3, 1) == 3

    def test_all_directly_connected(self) -> None:
        times = [(1, 2, 5), (1, 3, 3), (1, 4, 7)]
        assert network_delay_time(times, 4, 1) == 7


@st.composite
def random_delay_network(
    draw: st.DrawFn, max_nodes: int = 6
) -> tuple[list[tuple[int, int, int]], int, int]:
    """A random 1-indexed directed network, plus a signal source."""
    n = draw(st.integers(min_value=1, max_value=max_nodes))
    k = draw(st.integers(min_value=1, max_value=n))
    possible = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
    times: list[tuple[int, int, int]] = []
    if possible:
        pairs = draw(st.lists(st.sampled_from(possible), max_size=n * 2))
        times = [(u, v, draw(st.integers(min_value=1, max_value=20))) for u, v in pairs]
    return times, n, k


class TestNetworkDelayTimeProperties:
    @given(data=random_delay_network())
    def test_matches_dijkstra_oracle(
        self, data: tuple[list[tuple[int, int, int]], int, int]
    ) -> None:
        times, n, k = data
        result = network_delay_time(times, n, k)
        edges = [(u, v, float(w)) for u, v, w in times]
        dist = dijkstra(n + 1, edges, k)
        max_dist = max(dist[1:])
        expected = int(max_dist) if max_dist < float("inf") else -1
        assert result == expected
