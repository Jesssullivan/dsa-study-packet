"""Deep copy an undirected graph.

Problem:
    Given a reference of a node in a connected undirected graph, return
    a deep copy (clone) of the graph. Each node contains a val and a
    list of its neighbors.

Approach:
    BFS with a hash map mapping original nodes to their clones. For
    each node dequeued, iterate its neighbors: clone unseen neighbors,
    then wire the cloned neighbor into the clone's neighbor list.
    Also provided: clone_graph_comprehension, which separates "discover
    every reachable node" (still a BFS loop) from "build the clones and
    wire their edges" (dict/list comprehensions) instead of doing both
    in one explicit loop.

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

    >>> n1, n2 = GraphNode(1), GraphNode(2)
    >>> n1.neighbors, n2.neighbors = [n2], [n1]
    >>> c = clone_graph(n1)
    >>> c is not n1 and c is not None and c.val == 1
    True
    """
    if node is None:
        return None

    # GraphNode defines no __eq__/__hash__, so this dict keys on object
    # identity — the only way to tell two same-valued nodes apart and to
    # stop a cyclic graph from being traversed forever.
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


# --- dict/list-comprehension form: discover nodes first, then build declaratively ---
def clone_graph_comprehension(node: GraphNode | None) -> GraphNode | None:
    """Return a deep copy of the graph, built via comprehensions after discovery.

    Same result as clone_graph, but splits the work into two steps: a BFS
    discovery pass that just collects every reachable node (traversal can't
    be a comprehension), then a dict comprehension to create the clones and
    a list comprehension per node to wire up their neighbor lists.

    >>> n1, n2 = GraphNode(1), GraphNode(2)
    >>> n1.neighbors, n2.neighbors = [n2], [n1]
    >>> c = clone_graph_comprehension(n1)
    >>> c is not n1 and c is not None and c.val == 1
    True
    """
    if node is None:
        return None

    all_nodes: list[GraphNode] = []
    seen: set[int] = {id(node)}
    queue: deque[GraphNode] = deque([node])
    while queue:
        current = queue.popleft()
        all_nodes.append(current)
        for neighbor in current.neighbors:
            if id(neighbor) not in seen:
                seen.add(id(neighbor))
                queue.append(neighbor)

    clones = {n: GraphNode(n.val) for n in all_nodes}
    for n in all_nodes:
        clones[n].neighbors = [clones[neighbor] for neighbor in n.neighbors]

    return clones[node]
