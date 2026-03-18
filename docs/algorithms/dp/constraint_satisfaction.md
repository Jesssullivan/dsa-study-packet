---
title: Constraint Satisfaction
---

# Constraint Satisfaction

## Problem

Solve constraint satisfaction problems using backtracking with
constraint propagation (arc consistency / forward checking).

## Approach

Generic CSP framework: variables have domains, constraints link
variable pairs. Backtrack with MRV (Minimum Remaining Values)
heuristic and forward checking to prune domains early.
Includes a Sudoku solver built on the generic framework.

## When to Use

Puzzle solving, scheduling, configuration — "Sudoku", "N-Queens via
CSP", "timetable generation", "resource assignment with constraints".
Backtracking + forward checking prunes aggressively in practice.

## Complexity

| | |
|---|---|
| **Time** | `Exponential worst case, but constraint propagation prunes` |
| **Space** | `O(n * d) where n = variables, d = max domain size.` |

## Implementation

=== "Solution"

    ::: algo.dp.constraint_satisfaction
        options:
          show_source: true

=== "Tests"

    ```python title="tests/dp/test_constraint_satisfaction.py"
    --8<-- "tests/dp/test_constraint_satisfaction.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge dp constraint_satisfaction`

        Then implement the functions to make all tests pass.
        Use `just study dp` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.dp.constraint_satisfaction
            options:
              show_source: true
