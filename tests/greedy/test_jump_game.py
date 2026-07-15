"""Tests for jump game I and II."""

from hypothesis import given
from hypothesis import strategies as st

from algo.greedy.jump_game import can_jump, jump_game_ii


class TestCanJump:
    def test_reachable(self) -> None:
        assert can_jump([2, 3, 1, 1, 4]) is True

    def test_unreachable(self) -> None:
        assert can_jump([3, 2, 1, 0, 4]) is False

    def test_single_element(self) -> None:
        assert can_jump([0]) is True

    def test_all_zeros_except_first(self) -> None:
        assert can_jump([4, 0, 0, 0, 0]) is True

    def test_zero_at_start(self) -> None:
        assert can_jump([0, 1]) is False


class TestJumpGameII:
    def test_basic(self) -> None:
        assert jump_game_ii([2, 3, 1, 1, 4]) == 2

    def test_single_element(self) -> None:
        assert jump_game_ii([1]) == 0

    def test_two_elements(self) -> None:
        assert jump_game_ii([1, 1]) == 1

    def test_large_first_jump(self) -> None:
        assert jump_game_ii([5, 1, 1, 1, 1]) == 1

    def test_all_ones(self) -> None:
        assert jump_game_ii([1, 1, 1, 1]) == 3


def _can_jump_bfs(nums: list[int]) -> bool:
    """Independent oracle: BFS over indices reachable by any jump length."""
    n = len(nums)
    seen = {0}
    frontier = {0}
    while frontier:
        nxt = set()
        for i in frontier:
            for j in range(i + 1, min(i + nums[i], n - 1) + 1):
                if j not in seen:
                    seen.add(j)
                    nxt.add(j)
        frontier = nxt
    return (n - 1) in seen


def _min_jumps_bfs(nums: list[int]) -> int:
    """Independent oracle: BFS layer count to reach the last index."""
    n = len(nums)
    seen = {0}
    frontier = {0}
    jumps = 0
    while (n - 1) not in seen:
        nxt: set[int] = set()
        for i in frontier:
            for j in range(i + 1, min(i + nums[i], n - 1) + 1):
                if j not in seen:
                    seen.add(j)
                    nxt.add(j)
        frontier = nxt
        jumps += 1
    return jumps


class TestJumpGameProperties:
    @given(
        nums=st.lists(st.integers(min_value=0, max_value=10), min_size=1, max_size=15)
    )
    def test_can_jump_matches_bfs_oracle(self, nums: list[int]) -> None:
        assert can_jump(nums) == _can_jump_bfs(nums)

    @given(
        # each step guarantees at least 1 forward progress, so the last
        # index is always reachable -- matches jump_game_ii's precondition
        steps=st.lists(st.integers(min_value=1, max_value=5), min_size=1, max_size=15),
    )
    def test_jump_game_ii_matches_bfs_oracle(self, steps: list[int]) -> None:
        """Greedy min-jump count must equal an independent BFS shortest-path oracle."""
        nums = [*steps, 1]
        assert can_jump(nums) is True
        assert jump_game_ii(nums) == _min_jumps_bfs(nums)
