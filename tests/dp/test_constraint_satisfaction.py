"""Tests for constraint satisfaction / Sudoku solver."""

import copy

from hypothesis import given
from hypothesis import strategies as st

from algo.dp.constraint_satisfaction import CSP, solve_sudoku


@st.composite
def graph_coloring_csp(
    draw: st.DrawFn,
) -> tuple[list[str], dict[str, list[int]], dict[str, list[str]]]:
    """Strategy: a small random graph plus a domain of colors for each node.

    Returns (variables, domains, neighbors) ready to build a CSP[int].
    The number of colors is drawn independently of edge density, so both
    solvable and unsolvable instances are exercised.
    """
    n = draw(st.integers(min_value=1, max_value=6))
    variables = [f"n{i}" for i in range(n)]
    num_colors = draw(st.integers(min_value=1, max_value=4))
    domains = {v: list(range(num_colors)) for v in variables}

    neighbors: dict[str, set[str]] = {v: set() for v in variables}
    for i in range(n):
        for j in range(i + 1, n):
            if draw(st.booleans()):
                neighbors[variables[i]].add(variables[j])
                neighbors[variables[j]].add(variables[i])

    return variables, domains, {v: sorted(ns) for v, ns in neighbors.items()}


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


class TestCSPProperties:
    @given(instance=graph_coloring_csp())
    def test_solution_always_respects_neighbor_constraint(
        self,
        instance: tuple[list[str], dict[str, list[int]], dict[str, list[str]]],
    ) -> None:
        """Whenever solve() returns an assignment, no two neighbors share a color.

        This holds regardless of whether the instance was actually
        colorable, so no separate solvability oracle is needed.
        """
        variables, domains, neighbors = instance

        def not_equal(a: int, b: int) -> bool:
            return a != b

        csp: CSP[int] = CSP(variables, domains, neighbors, not_equal)
        result = csp.solve()

        if result is not None:
            assert set(result) == set(variables)
            for var, color in result.items():
                assert color in domains[var]
                for neighbor in neighbors[var]:
                    assert result[neighbor] != color


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
