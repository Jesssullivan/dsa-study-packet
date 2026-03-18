---
title: N Queens
---

# N Queens

## Problem

Place n queens on an n x n chessboard such that no two queens
threaten each other (no shared row, column, or diagonal).
Return all distinct solutions.

## Approach

Backtracking row by row. Track occupied columns, positive
diagonals (r + c), and negative diagonals (r - c) with sets.
Only valid placements are explored.

## When to Use

Constraint placement — "place N items with mutual exclusion constraints",
"non-attacking queens", "conflict-free assignment". Row-by-row
backtracking with column/diagonal conflict sets. See also: CSP solver.

## Complexity

| | |
|---|---|
| **Time** | `O(n!)  (with pruning)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.backtracking.n_queens
        options:
          show_source: true

=== "Tests"

    ```python title="tests/backtracking/test_n_queens.py"
    --8<-- "tests/backtracking/test_n_queens.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge backtracking n_queens`

        Then implement the functions to make all tests pass.
        Use `just study backtracking` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.backtracking.n_queens
            options:
              show_source: true
