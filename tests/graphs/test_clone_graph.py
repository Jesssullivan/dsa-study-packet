"""Tests for clone graph."""

from collections import deque

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.clone_graph import GraphNode, clone_graph, clone_graph_comprehension


def _build_graph(adj: dict[int, list[int]]) -> dict[int, GraphNode]:
    """Build a graph from an adjacency dict and return node map."""
    nodes: dict[int, GraphNode] = {v: GraphNode(v) for v in adj}
    for v, neighbors in adj.items():
        nodes[v].neighbors = [nodes[n] for n in neighbors]
    return nodes


class TestCloneGraph:
    def test_none_input(self) -> None:
        assert clone_graph(None) is None

    def test_single_node(self) -> None:
        node = GraphNode(1)
        cloned = clone_graph(node)
        assert cloned is not None
        assert cloned is not node
        assert cloned.val == 1
        assert cloned.neighbors == []

    def test_two_nodes(self) -> None:
        n1, n2 = GraphNode(1), GraphNode(2)
        n1.neighbors = [n2]
        n2.neighbors = [n1]
        cloned = clone_graph(n1)
        assert cloned is not None
        assert cloned.val == 1
        assert len(cloned.neighbors) == 1
        assert cloned.neighbors[0].val == 2
        assert cloned is not n1
        assert cloned.neighbors[0] is not n2

    def test_triangle(self) -> None:
        nodes = _build_graph({1: [2, 3], 2: [1, 3], 3: [1, 2]})
        cloned = clone_graph(nodes[1])
        assert cloned is not None
        assert cloned.val == 1
        neighbor_vals = sorted(n.val for n in cloned.neighbors)
        assert neighbor_vals == [2, 3]

    def test_deep_copy_identity(self) -> None:
        """Cloned nodes must be distinct objects."""
        nodes = _build_graph({1: [2], 2: [1]})
        cloned = clone_graph(nodes[1])
        assert cloned is not None
        original_ids = {id(n) for n in nodes.values()}
        clone_ids: set[int] = set()
        visited: set[int] = set()
        stack = [cloned]
        while stack:
            n = stack.pop()
            nid = id(n)
            if nid in visited:
                continue
            visited.add(nid)
            clone_ids.add(nid)
            stack.extend(n.neighbors)
        assert original_ids.isdisjoint(clone_ids)

    def test_four_node_cycle(self) -> None:
        nodes = _build_graph({1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
        cloned = clone_graph(nodes[1])
        assert cloned is not None
        assert cloned.val == 1
        assert len(cloned.neighbors) == 2


def _serialize(root: GraphNode | None) -> dict[int, list[int]]:
    """BFS the clone into {val: sorted neighbor vals} for structural comparison."""
    if root is None:
        return {}
    result: dict[int, list[int]] = {}
    seen: set[int] = {id(root)}
    queue: deque[GraphNode] = deque([root])
    while queue:
        node = queue.popleft()
        result[node.val] = sorted(n.val for n in node.neighbors)
        for neighbor in node.neighbors:
            if id(neighbor) not in seen:
                seen.add(id(neighbor))
                queue.append(neighbor)
    return result


@st.composite
def connected_undirected_graphs(
    draw: st.DrawFn, max_nodes: int = 8
) -> dict[int, list[int]]:
    """A random connected undirected graph as an adjacency dict."""
    n = draw(st.integers(min_value=1, max_value=max_nodes))
    adj: dict[int, set[int]] = {i: set() for i in range(n)}
    # Random spanning tree: each node i>0 attaches to some earlier node,
    # guaranteeing the whole graph stays connected.
    for i in range(1, n):
        parent = draw(st.integers(min_value=0, max_value=i - 1))
        adj[i].add(parent)
        adj[parent].add(i)
    if n > 1:
        extra = draw(
            st.lists(
                st.tuples(
                    st.integers(min_value=0, max_value=n - 1),
                    st.integers(min_value=0, max_value=n - 1),
                ),
                max_size=n,
            )
        )
        for u, v in extra:
            if u != v:
                adj[u].add(v)
                adj[v].add(u)
    return {k: sorted(v) for k, v in adj.items()}


class TestCloneGraphProperties:
    @given(adj=connected_undirected_graphs())
    def test_clone_matches_original_structure(self, adj: dict[int, list[int]]) -> None:
        nodes = _build_graph(adj)
        cloned = clone_graph(nodes[0])
        assert _serialize(cloned) == adj

    @given(adj=connected_undirected_graphs())
    def test_clone_is_disjoint_from_original(self, adj: dict[int, list[int]]) -> None:
        nodes = _build_graph(adj)
        original_ids = {id(n) for n in nodes.values()}
        cloned = clone_graph(nodes[0])
        clone_ids: set[int] = set()
        seen: set[int] = set()
        stack = [cloned] if cloned is not None else []
        while stack:
            n = stack.pop()
            if id(n) in seen:
                continue
            seen.add(id(n))
            clone_ids.add(id(n))
            stack.extend(n.neighbors)
        assert original_ids.isdisjoint(clone_ids)

    @given(adj=connected_undirected_graphs())
    def test_comprehension_alt_matches_primary(self, adj: dict[int, list[int]]) -> None:
        """clone_graph_comprehension must produce the same structure as clone_graph."""
        primary_nodes = _build_graph(adj)
        alt_nodes = _build_graph(adj)
        primary = clone_graph(primary_nodes[0])
        alt = clone_graph_comprehension(alt_nodes[0])
        assert _serialize(primary) == _serialize(alt)
