"""Tests for topological sort algorithms."""

from algo.graphs.topological_sort import topological_sort_dfs, topological_sort_kahn


def _is_valid_topo_order(
    num_nodes: int,
    edges: list[tuple[int, int]],
    order: list[int],
) -> bool:
    """Check that *order* is a valid topological ordering."""
    if len(order) != num_nodes:
        return False
    pos = {node: i for i, node in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


class TestTopologicalSortKahn:
    def test_linear_chain(self) -> None:
        order = topological_sort_kahn(3, [(0, 1), (1, 2)])
        assert order == [0, 1, 2]

    def test_diamond(self) -> None:
        edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
        order = topological_sort_kahn(4, edges)
        assert _is_valid_topo_order(4, edges, order)

    def test_no_edges(self) -> None:
        order = topological_sort_kahn(3, [])
        assert sorted(order) == [0, 1, 2]

    def test_cycle_returns_empty(self) -> None:
        assert topological_sort_kahn(3, [(0, 1), (1, 2), (2, 0)]) == []

    def test_single_node(self) -> None:
        assert topological_sort_kahn(1, []) == [0]


class TestTopologicalSortDFS:
    def test_linear_chain(self) -> None:
        order = topological_sort_dfs(3, [(0, 1), (1, 2)])
        assert _is_valid_topo_order(3, [(0, 1), (1, 2)], order)

    def test_diamond(self) -> None:
        edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
        order = topological_sort_dfs(4, edges)
        assert _is_valid_topo_order(4, edges, order)

    def test_no_edges(self) -> None:
        order = topological_sort_dfs(3, [])
        assert sorted(order) == [0, 1, 2]

    def test_cycle_returns_empty(self) -> None:
        assert topological_sort_dfs(3, [(0, 1), (1, 2), (2, 0)]) == []

    def test_single_node(self) -> None:
        assert topological_sort_dfs(1, []) == [0]
