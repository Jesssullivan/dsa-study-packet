"""Tests for invert binary tree."""

from algo.trees.invert_tree import TreeNode, invert_tree


def _to_list(root: TreeNode | None) -> list[int | None]:
    """BFS serialization for easy comparison."""
    if not root:
        return []
    from collections import deque

    result: list[int | None] = []
    queue: deque[TreeNode | None] = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # Strip trailing Nones for cleaner output.
    while result and result[-1] is None:
        result.pop()
    return result


class TestInvertTree:
    def test_basic(self) -> None:
        tree = TreeNode(
            4,
            TreeNode(2, TreeNode(1), TreeNode(3)),
            TreeNode(7, TreeNode(6), TreeNode(9)),
        )
        result = invert_tree(tree)
        assert _to_list(result) == [4, 7, 2, 9, 6, 3, 1]

    def test_empty_tree(self) -> None:
        assert invert_tree(None) is None

    def test_single_node(self) -> None:
        tree = TreeNode(1)
        result = invert_tree(tree)
        assert _to_list(result) == [1]

    def test_left_only(self) -> None:
        tree = TreeNode(1, TreeNode(2))
        result = invert_tree(tree)
        assert result is not None
        assert result.left is None
        assert result.right is not None
        assert result.right.val == 2

    def test_double_invert_restores(self) -> None:
        tree = TreeNode(1, TreeNode(2, TreeNode(4), None), TreeNode(3))
        original = _to_list(tree)
        invert_tree(tree)
        invert_tree(tree)
        assert _to_list(tree) == original

    def test_returns_same_root(self) -> None:
        tree = TreeNode(5, TreeNode(3), TreeNode(8))
        result = invert_tree(tree)
        assert result is tree
