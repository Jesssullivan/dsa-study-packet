"""Invert (mirror) a binary tree.

Problem:
    Given the root of a binary tree, invert the tree so that every left
    child becomes the right child and vice versa.

Approach:
    Recursive swap: at each node, swap left and right children, then
    recurse into both subtrees.

When to use:
    Tree transformation — "mirror", "invert", "flip". Any problem
    requiring symmetric restructuring of a tree in-place.
    Pattern: swap children, then recurse into both subtrees.

Complexity:
    Time:  O(n)
    Space: O(h) where h = height of tree (call stack)
"""

from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """Invert a binary tree in place and return the root.

    >>> t = TreeNode(1, TreeNode(2), TreeNode(3))
    >>> r = invert_tree(t)
    >>> r.left.val, r.right.val  # type: ignore[union-attr]
    (3, 2)
    """
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root
