"""Validate binary search tree.

Problem:
    Given the root of a binary tree, determine if it is a valid BST.
    A valid BST requires every node's value to be strictly between the
    values of its ancestors that constrain it.

Approach:
    Recursive with min/max bounds. At each node, check that the value
    is within (lo, hi) and recurse with tightened bounds.

When to use:
    Constraint propagation through a tree — "validate BST", "check
    ordering invariant". Pass tightening bounds (lo, hi) down the
    recursion. Also: range-constrained tree problems, interval checks.

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


def is_valid_bst(
    root: TreeNode | None,
    lo: float = float("-inf"),
    hi: float = float("inf"),
) -> bool:
    """Return True if the binary tree rooted at `root` is a valid BST.

    >>> is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3)))
    True
    >>> is_valid_bst(TreeNode(2, TreeNode(3), TreeNode(1)))
    False
    """
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return is_valid_bst(root.left, lo, root.val) and is_valid_bst(
        root.right, root.val, hi
    )
