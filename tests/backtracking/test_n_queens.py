"""Tests for N-Queens."""

from algo.backtracking.n_queens import solve_n_queens


class TestNQueens:
    def test_one_queen(self) -> None:
        assert solve_n_queens(1) == [["Q"]]

    def test_four_queens(self) -> None:
        result = solve_n_queens(4)
        assert len(result) == 2

    def test_eight_queens(self) -> None:
        result = solve_n_queens(8)
        assert len(result) == 92

    def test_no_solution_for_two(self) -> None:
        assert solve_n_queens(2) == []

    def test_no_solution_for_three(self) -> None:
        assert solve_n_queens(3) == []

    def test_board_validity(self) -> None:
        """Check that no two queens attack each other in any 4-queens solution."""
        for board in solve_n_queens(4):
            queens = [(r, row.index("Q")) for r, row in enumerate(board)]
            # No shared column
            cols = [c for _, c in queens]
            assert len(cols) == len(set(cols))
            # No shared diagonal
            for i in range(len(queens)):
                for j in range(i + 1, len(queens)):
                    r1, c1 = queens[i]
                    r2, c2 = queens[j]
                    assert abs(r1 - r2) != abs(c1 - c2)
