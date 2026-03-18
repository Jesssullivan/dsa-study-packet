"""Deep copy an undirected graph.

Problem:
    Given a reference of a node in a connected undirected graph, return
    a deep copy (clone) of the graph. Each node contains a val and a
    list of its neighbors.

Approach:
    BFS with a hash map mapping original nodes to their clones. For
    each node dequeued, iterate its neighbors: clone unseen neighbors,
    then wire the cloned neighbor into the clone's neighbor list.

When to use:
    Graph deep copy — "clone graph", "copy linked structure with cycles".
    BFS/DFS with a hash map from original to clone prevents revisiting.
    Also: snapshotting mutable graph state, undo/redo systems.

Complexity:
    Time:  O(V + E)
    Space: O(V)
"""

from collections import deque


class GraphNode:
    """Node in an undirected graph."""

    def __init__(
        self,
        val: int = 0,
        neighbors: list[GraphNode] | None = None,
    ) -> None:
        self.val = val
        self.neighbors: list[GraphNode] = neighbors if neighbors is not None else []

    def __repr__(self) -> str:
        neighbor_vals = [n.val for n in self.neighbors]
        return f"GraphNode({self.val}, neighbors={neighbor_vals})"


def clone_graph(node: GraphNode | None) -> GraphNode | None:
    """Return a deep copy of the graph rooted at *node*.

    >>> n1 = GraphNode(1)
    ... n2 = GraphNode(2)
    >>> n1.neighbors = [n2]
    ... n2.neighbors = [n1]
    >>> c = clone_graph(n1)
    >>> c is not n1 and c is not None and c.val == 1
    True
    """
    if node is None:
        return None

    clones: dict[GraphNode, GraphNode] = {node: GraphNode(node.val)}
    queue: deque[GraphNode] = deque([node])

    while queue:
        current = queue.popleft()
        for neighbor in current.neighbors:
            if neighbor not in clones:
                clones[neighbor] = GraphNode(neighbor.val)
                queue.append(neighbor)
            clones[current].neighbors.append(clones[neighbor])

    return clones[node]
