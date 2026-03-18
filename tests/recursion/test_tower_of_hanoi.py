"""Tests for the Tower of Hanoi problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.recursion.tower_of_hanoi import tower_of_hanoi


class TestTowerOfHanoi:
    def test_one_disk(self) -> None:
        assert tower_of_hanoi(1) == [("A", "C")]

    def test_two_disks(self) -> None:
        assert tower_of_hanoi(2) == [("A", "B"), ("A", "C"), ("B", "C")]

    def test_three_disks(self) -> None:
        moves = tower_of_hanoi(3)
        assert len(moves) == 7
        assert moves[0] == ("A", "C")
        assert moves[-1] == ("A", "C")

    def test_zero_disks(self) -> None:
        assert tower_of_hanoi(0) == []

    def test_custom_peg_names(self) -> None:
        moves = tower_of_hanoi(1, source="X", target="Z", auxiliary="Y")
        assert moves == [("X", "Z")]

    @given(n=st.integers(min_value=1, max_value=10))
    def test_move_count_is_2n_minus_1(self, n: int) -> None:
        assert len(tower_of_hanoi(n)) == 2**n - 1

    @given(n=st.integers(min_value=1, max_value=8))
    def test_moves_are_valid(self, n: int) -> None:
        """Simulate moves and verify no larger disk is placed on a smaller one."""
        moves = tower_of_hanoi(n)
        pegs: dict[str, list[int]] = {
            "A": list(range(n, 0, -1)),
            "B": [],
            "C": [],
        }
        for src, tgt in moves:
            disk = pegs[src].pop()
            if pegs[tgt] and pegs[tgt][-1] < disk:
                msg = f"Invalid move: disk {disk} onto disk {pegs[tgt][-1]}"
                raise AssertionError(msg)
            pegs[tgt].append(disk)
        # All disks should be on target peg
        assert pegs["A"] == []
        assert pegs["B"] == []
        assert pegs["C"] == list(range(n, 0, -1))
