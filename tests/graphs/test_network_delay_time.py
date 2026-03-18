"""Tests for network delay time."""

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
