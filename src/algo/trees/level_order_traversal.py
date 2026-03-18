"""Level-order (BFS) traversal of a binary tree.

Problem:
    Given the root of a binary tree, return the level-order traversal
    as a list of lists, where each inner list contains the values at
    that depth level.

Approach:
    BFS with a deque. Process one level at a time by iterating over
    the current queue length, appending children for the next level.

When to use:
    BFS on trees — "level order", "zigzag order", "right side view", any
    problem requiring per-level processing. Also: shortest-path-like
    queries on trees, hierarchical data serialization.

Complexity:
    Time:  O(n)
    Space: O(w) where w = max width of the tree (up to n/2)
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def level_order(root: TreeNode | None) -> list[list[int]]:
    """Return level-order traversal as a list of lists.

    >>> level_order(TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))))
    [[3], [9, 20], [15, 7]]
    """
    if not root:
        return []

    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result
