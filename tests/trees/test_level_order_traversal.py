"""Tests for level-order traversal."""

from collections import Counter

from hypothesis import given
from hypothesis import strategies as st

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


def _levels_by_dfs(
    node: TreeNode | None, depth: int, acc: dict[int, list[int]]
) -> None:
    if node is None:
        return
    acc.setdefault(depth, []).append(node.val)
    _levels_by_dfs(node.left, depth + 1, acc)
    _levels_by_dfs(node.right, depth + 1, acc)


def _all_values(node: TreeNode | None) -> list[int]:
    if node is None:
        return []
    return [node.val, *_all_values(node.left), *_all_values(node.right)]


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


class TestLevelOrderProperties:
    @given(tree=_random_trees)
    def test_matches_depth_grouping_oracle(self, tree: TreeNode | None) -> None:
        """Level order equals values grouped by depth, left-to-right per level.

        A pre-order DFS visits same-depth nodes in the same left-to-right order
        as BFS, so grouping DFS values by depth reproduces level order exactly.
        """
        acc: dict[int, list[int]] = {}
        _levels_by_dfs(tree, 0, acc)
        expected = [acc[depth] for depth in sorted(acc)]
        assert level_order(tree) == expected

    @given(tree=_random_trees)
    def test_flatten_preserves_all_values(self, tree: TreeNode | None) -> None:
        """Concatenating the levels yields exactly every node value once."""
        flat = [v for level in level_order(tree) for v in level]
        assert Counter(flat) == Counter(_all_values(tree))
        # no empty levels are ever emitted
        assert all(level for level in level_order(tree))
