"""N-Queens — place n queens on n x n board with no attacks.

Problem:
    Place n queens on an n x n chessboard such that no two queens
    threaten each other (no shared row, column, or diagonal).
    Return all distinct solutions.

Approach:
    Backtracking row by row. Track occupied columns, positive
    diagonals (r + c), and negative diagonals (r - c) with sets.
    Only valid placements are explored.

When to use:
    Constraint placement — "place N items with mutual exclusion constraints",
    "non-attacking queens", "conflict-free assignment". Row-by-row
    backtracking with column/diagonal conflict sets. See also: CSP solver.

Complexity:
    Time:  O(n!)  (with pruning)
    Space: O(n)
"""


def solve_n_queens(n: int) -> list[list[str]]:
    """Return all solutions as lists of strings ('.' and 'Q').

    >>> len(solve_n_queens(4))
    2
    >>> solve_n_queens(1)
    [['Q']]
    """
    result: list[list[str]] = []
    cols: set[int] = set()
    pos_diag: set[int] = set()  # r + c constant on / diagonals
    neg_diag: set[int] = set()  # r - c constant on \\ diagonals
    queens: list[int] = []  # queens[row] = col

    def backtrack(r: int) -> None:
        if r == n:
            board = ["." * c + "Q" + "." * (n - c - 1) for c in queens]
            result.append(board)
            return
        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            queens.append(c)
            backtrack(r + 1)
            queens.pop()
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)

    backtrack(0)
    return result
