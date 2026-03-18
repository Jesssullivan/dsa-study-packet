"""Maximum depth of a binary tree.

Problem:
    Given the root of a binary tree, return its maximum depth (number of
    nodes along the longest path from root to a leaf).

Approach:
    DFS recursive: depth = 1 + max(depth(left), depth(right)).
    Base case: empty tree has depth 0.

When to use:
    Recursive tree measurement — "max depth", "height", "diameter",
    any metric that aggregates over subtrees with a simple recurrence.
    Foundation for balanced-tree checks and tree diameter computation.

Complexity:
    Time:  O(n)
    Space: O(h) where h = height of tree (call stack)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def max_depth(root: TreeNode | None) -> int:
    """Return the maximum depth of a binary tree.

    >>> max_depth(TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), None)))
    3
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
