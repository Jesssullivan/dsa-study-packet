"""Tests for clone graph."""

from algo.graphs.clone_graph import GraphNode, clone_graph


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
