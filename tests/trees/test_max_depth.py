"""Tests for maximum depth of binary tree."""

from collections import deque

from hypothesis import given
from hypothesis import strategies as st

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


def _height_iterative(root: TreeNode | None) -> int:
    """Independent oracle: count levels via BFS instead of top-down recursion."""
    if root is None:
        return 0
    depth = 0
    queue: deque[TreeNode] = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth


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


class TestMaxDepthProperties:
    @given(tree=_random_trees)
    def test_matches_bfs_level_count_oracle(self, tree: TreeNode | None) -> None:
        assert max_depth(tree) == _height_iterative(tree)
