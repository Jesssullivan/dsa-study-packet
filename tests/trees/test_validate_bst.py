"""Tests for validate binary search tree."""

from itertools import pairwise

from hypothesis import given
from hypothesis import strategies as st

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


def _inorder_vals(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return [*_inorder_vals(node.left), node.val, *_inorder_vals(node.right)]


def _strictly_increasing(xs: list[int]) -> bool:
    return all(a < b for a, b in pairwise(xs))


def _build_balanced_bst(vals: list[int]) -> TreeNode | None:
    if not vals:
        return None
    mid = len(vals) // 2
    return TreeNode(
        vals[mid],
        _build_balanced_bst(vals[:mid]),
        _build_balanced_bst(vals[mid + 1 :]),
    )


_random_trees = st.recursive(
    st.none() | st.builds(TreeNode, st.integers(min_value=-50, max_value=50)),
    lambda children: st.builds(
        TreeNode,
        st.integers(min_value=-50, max_value=50),
        children,
        children,
    ),
    max_leaves=20,
)


class TestIsValidBSTProperties:
    @given(tree=_random_trees)
    def test_matches_inorder_oracle(self, tree: TreeNode | None) -> None:
        """A tree is a BST iff its in-order traversal is strictly increasing."""
        expected = _strictly_increasing(_inorder_vals(tree))
        assert is_valid_bst(tree) is expected

    @given(
        vals=st.lists(
            st.integers(min_value=-50, max_value=50),
            min_size=1,
            max_size=20,
            unique=True,
        ),
    )
    def test_balanced_bst_from_sorted_distinct_is_valid(self, vals: list[int]) -> None:
        """A balanced tree built from sorted distinct values is always a BST."""
        tree = _build_balanced_bst(sorted(vals))
        assert is_valid_bst(tree) is True

    @given(
        vals=st.lists(
            st.integers(min_value=-50, max_value=50),
            min_size=2,
            max_size=20,
            unique=True,
        ),
    )
    def test_injected_violation_is_rejected(self, vals: list[int]) -> None:
        """Forcing the minimum node above the global max breaks the BST."""
        ordered = sorted(vals)
        root = _build_balanced_bst(ordered)
        assert root is not None
        node = root
        while node.left is not None:
            node = node.left
        # leftmost node is the minimum; push it above every other value
        node.val = ordered[-1] + 1
        assert is_valid_bst(root) is False
