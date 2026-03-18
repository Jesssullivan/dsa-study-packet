"""Tests for constraint satisfaction / Sudoku solver."""

import copy

from algo.dp.constraint_satisfaction import CSP, solve_sudoku


class TestCSP:
    def test_simple_coloring(self) -> None:
        """Graph coloring: 3 nodes in a triangle, 3 colors."""
        variables = ["A", "B", "C"]
        domains: dict[str, list[str]] = {
            "A": ["R", "G", "B"],
            "B": ["R", "G", "B"],
            "C": ["R", "G", "B"],
        }
        neighbors = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}

        def not_equal(a: str, b: str) -> bool:
            return a != b

        csp: CSP[str] = CSP(variables, domains, neighbors, not_equal)
        result = csp.solve()
        assert result is not None
        assert result["A"] != result["B"]
        assert result["A"] != result["C"]
        assert result["B"] != result["C"]

    def test_unsolvable(self) -> None:
        """Two connected variables with one color each (same color)."""
        variables = ["A", "B"]
        domains: dict[str, list[str]] = {"A": ["R"], "B": ["R"]}
        neighbors = {"A": ["B"], "B": ["A"]}

        def not_equal(a: str, b: str) -> bool:
            return a != b

        csp: CSP[str] = CSP(variables, domains, neighbors, not_equal)
        assert csp.solve() is None


class TestSolveSudoku:
    def test_valid_puzzle(self) -> None:
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        result = solve_sudoku(board)
        assert result is not None
        # Check all rows have 1-9
        for row in result:
            assert sorted(row) == list(range(1, 10))
        # Check all columns have 1-9
        for c in range(9):
            col = [result[r][c] for r in range(9)]
            assert sorted(col) == list(range(1, 10))

    def test_already_solved(self) -> None:
        board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
        original = copy.deepcopy(board)
        result = solve_sudoku(board)
        assert result == original

    def test_preserves_given_values(self) -> None:
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        original = copy.deepcopy(board)
        result = solve_sudoku(board)
        assert result is not None
        for r in range(9):
            for c in range(9):
                if original[r][c] != 0:
                    assert result[r][c] == original[r][c]
