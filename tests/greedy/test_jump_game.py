"""Tests for jump game I and II."""

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
