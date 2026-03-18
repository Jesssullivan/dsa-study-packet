"""Constraint Satisfaction Problem — generic CSP solver with Sudoku example.

Problem:
    Solve constraint satisfaction problems using backtracking with
    constraint propagation (arc consistency / forward checking).

Approach:
    Generic CSP framework: variables have domains, constraints link
    variable pairs. Backtrack with MRV (Minimum Remaining Values)
    heuristic and forward checking to prune domains early.
    Includes a Sudoku solver built on the generic framework.

When to use:
    Puzzle solving, scheduling, configuration — "Sudoku", "N-Queens via
    CSP", "timetable generation", "resource assignment with constraints".
    Backtracking + forward checking prunes aggressively in practice.

Complexity:
    Time:  Exponential worst case, but constraint propagation prunes
           heavily. Sudoku typically solves in milliseconds.
    Space: O(n * d) where n = variables, d = max domain size.
"""

from collections.abc import Callable, Mapping, Sequence

type Constraint[T] = Callable[[T, T], bool]


class CSP[T]:
    """Generic CSP solver using backtracking with forward checking."""

    def __init__(
        self,
        variables: Sequence[str],
        domains: dict[str, list[T]],
        neighbors: Mapping[str, Sequence[str]],
        constraint: Constraint[T],
    ) -> None:
        self.variables = list(variables)
        self.domains = {v: list(d) for v, d in domains.items()}
        self.neighbors = neighbors
        self.constraint = constraint

    def solve(self) -> dict[str, T] | None:
        """Return an assignment satisfying all constraints, or None."""
        assignment: dict[str, T] = {}
        return self._backtrack(assignment)

    def _select_unassigned(self, assignment: dict[str, T]) -> str:
        """MRV heuristic: pick variable with fewest remaining values."""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(self.domains[v]))

    def _is_consistent(self, var: str, val: T, assignment: dict[str, T]) -> bool:
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and not self.constraint(
                val, assignment[neighbor]
            ):
                return False
        return True

    def _forward_check(
        self, var: str, val: T, assignment: dict[str, T]
    ) -> dict[str, list[T]] | None:
        """Prune neighbor domains. Return removed values or None on wipeout."""
        removed: dict[str, list[T]] = {}
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment:
                continue
            to_remove: list[T] = []
            for nval in self.domains[neighbor]:
                if not self.constraint(nval, val):
                    to_remove.append(nval)
            if to_remove:
                removed[neighbor] = to_remove
                for rv in to_remove:
                    self.domains[neighbor].remove(rv)
                if not self.domains[neighbor]:
                    # Domain wipeout -- restore and fail
                    for nb, vals in removed.items():
                        self.domains[nb].extend(vals)
                    return None
        return removed

    def _backtrack(self, assignment: dict[str, T]) -> dict[str, T] | None:
        if len(assignment) == len(self.variables):
            return dict(assignment)

        var = self._select_unassigned(assignment)

        for val in list(self.domains[var]):
            if not self._is_consistent(var, val, assignment):
                continue

            assignment[var] = val
            removed = self._forward_check(var, val, assignment)

            if removed is not None:
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                # Restore pruned domains
                for nb, vals in removed.items():
                    self.domains[nb].extend(vals)

            del assignment[var]

        return None


# ---------------------------------------------------------------------------
# Sudoku solver built on the CSP framework
# ---------------------------------------------------------------------------

type Grid = list[list[int]]

_CELLS = [f"R{r}C{c}" for r in range(9) for c in range(9)]


def _sudoku_neighbors() -> dict[str, list[str]]:
    """Build neighbor map: cells sharing a row, column, or 3x3 box."""
    neighbors: dict[str, set[str]] = {cell: set() for cell in _CELLS}
    for r in range(9):
        for c in range(9):
            cell = f"R{r}C{c}"
            for k in range(9):
                if k != c:
                    neighbors[cell].add(f"R{r}C{k}")
                if k != r:
                    neighbors[cell].add(f"R{k}C{c}")
            br, bc = 3 * (r // 3), 3 * (c // 3)
            for dr in range(3):
                for dc in range(3):
                    other = f"R{br + dr}C{bc + dc}"
                    if other != cell:
                        neighbors[cell].add(other)
    return {k: sorted(v) for k, v in neighbors.items()}


_NEIGHBORS = _sudoku_neighbors()


def solve_sudoku(board: Grid) -> Grid | None:
    """Solve a 9x9 Sudoku board in-place and return it, or None if unsolvable.

    *board* is a 9x9 list of ints where 0 represents an empty cell.

    >>> board = [
    ...     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    ...     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    ...     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    ...     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    ...     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    ...     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    ...     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    ...     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    ...     [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ... ]
    >>> result = solve_sudoku(board)
    >>> result is not None
    True
    """
    domains: dict[str, list[int]] = {}
    variables: list[str] = []

    for r in range(9):
        for c in range(9):
            cell = f"R{r}C{c}"
            if board[r][c] != 0:
                domains[cell] = [board[r][c]]
            else:
                domains[cell] = list(range(1, 10))
            variables.append(cell)

    def not_equal(a: int, b: int) -> bool:
        return a != b

    csp: CSP[int] = CSP(variables, domains, _NEIGHBORS, not_equal)
    solution = csp.solve()

    if solution is None:
        return None

    for r in range(9):
        for c in range(9):
            board[r][c] = solution[f"R{r}C{c}"]
    return board
