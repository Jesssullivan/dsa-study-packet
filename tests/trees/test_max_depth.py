"""Tests for maximum depth of binary tree."""

from algo.trees.max_depth import TreeNode, max_depth


class TestMaxDepth:
    def test_balanced_tree(self) -> None:
        tree = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        assert max_depth(tree) == 3

    def test_empty_tree(self) -> None:
        assert max_depth(None) == 0

    def test_single_node(self) -> None:
        assert max_depth(TreeNode(1)) == 1

    def test_left_skewed(self) -> None:
        tree = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
        assert max_depth(tree) == 4

    def test_right_skewed(self) -> None:
        tree = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        assert max_depth(tree) == 3

    def test_asymmetric(self) -> None:
        tree = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
        assert max_depth(tree) == 3
