"""Tests for level-order traversal."""

from algo.trees.level_order_traversal import TreeNode, level_order


class TestLevelOrder:
    def test_basic(self) -> None:
        tree = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        assert level_order(tree) == [[3], [9, 20], [15, 7]]

    def test_empty_tree(self) -> None:
        assert level_order(None) == []

    def test_single_node(self) -> None:
        assert level_order(TreeNode(1)) == [[1]]

    def test_left_skewed(self) -> None:
        tree = TreeNode(1, TreeNode(2, TreeNode(3)))
        assert level_order(tree) == [[1], [2], [3]]

    def test_complete_tree(self) -> None:
        tree = TreeNode(
            1,
            TreeNode(2, TreeNode(4), TreeNode(5)),
            TreeNode(3, TreeNode(6), TreeNode(7)),
        )
        assert level_order(tree) == [[1], [2, 3], [4, 5, 6, 7]]

    def test_sparse_tree(self) -> None:
        """Tree with missing children at various levels."""
        tree = TreeNode(1, None, TreeNode(3, TreeNode(5), None))
        assert level_order(tree) == [[1], [3], [5]]
