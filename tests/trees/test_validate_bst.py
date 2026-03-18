"""Tests for validate binary search tree."""

from algo.trees.validate_bst import TreeNode, is_valid_bst


class TestIsValidBST:
    def test_valid_bst(self) -> None:
        tree = TreeNode(2, TreeNode(1), TreeNode(3))
        assert is_valid_bst(tree) is True

    def test_invalid_bst(self) -> None:
        tree = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
        assert is_valid_bst(tree) is False

    def test_empty_tree(self) -> None:
        assert is_valid_bst(None) is True

    def test_single_node(self) -> None:
        assert is_valid_bst(TreeNode(0)) is True

    def test_equal_values_invalid(self) -> None:
        """BST requires strictly less/greater, not equal."""
        tree = TreeNode(1, TreeNode(1))
        assert is_valid_bst(tree) is False

    def test_deep_violation(self) -> None:
        """Value in left subtree exceeds the root."""
        #     5
        #    / \
        #   3   7
        #  / \
        # 2   6  <-- 6 > 5, violates BST
        tree = TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(6)), TreeNode(7))
        assert is_valid_bst(tree) is False

    def test_valid_large_bst(self) -> None:
        #       8
        #      / \
        #     4   12
        #    / \  / \
        #   2  6 10 14
        tree = TreeNode(
            8,
            TreeNode(4, TreeNode(2), TreeNode(6)),
            TreeNode(12, TreeNode(10), TreeNode(14)),
        )
        assert is_valid_bst(tree) is True
