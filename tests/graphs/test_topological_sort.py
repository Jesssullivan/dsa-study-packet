"""Tests for topological sort algorithms."""

from hypothesis import given
from hypothesis import strategies as st

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


@st.composite
def random_dag_edges(
    draw: st.DrawFn, max_nodes: int = 8
) -> tuple[int, list[tuple[int, int]]]:
    """A random DAG: edges only run earlier -> later in a random permutation."""
    n = draw(st.integers(min_value=1, max_value=max_nodes))
    order = draw(st.permutations(range(n)))
    possible = [(order[i], order[j]) for i in range(n) for j in range(i + 1, n)]
    edges = (
        draw(st.lists(st.sampled_from(possible), max_size=n * 2)) if possible else []
    )
    return n, edges


class TestTopologicalSortProperties:
    @given(data=random_dag_edges())
    def test_kahn_and_dfs_agree_and_are_valid(
        self, data: tuple[int, list[tuple[int, int]]]
    ) -> None:
        n, edges = data
        kahn = topological_sort_kahn(n, edges)
        dfs = topological_sort_dfs(n, edges)
        assert len(kahn) == n
        assert len(dfs) == n
        assert _is_valid_topo_order(n, edges, kahn)
        assert _is_valid_topo_order(n, edges, dfs)

    @given(n=st.integers(min_value=2, max_value=8))
    def test_full_cycle_returns_empty(self, n: int) -> None:
        edges = [(i, (i + 1) % n) for i in range(n)]
        assert topological_sort_kahn(n, edges) == []
        assert topological_sort_dfs(n, edges) == []
