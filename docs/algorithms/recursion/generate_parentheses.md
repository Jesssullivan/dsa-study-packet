---
title: Generate Parentheses
---

# Generate Parentheses

## Problem

Given n pairs of parentheses, generate all combinations of
well-formed (balanced) parentheses.

## Approach

Backtracking: maintain counts of open and close parens placed so far.
Add '(' if open < n. Add ')' if close < open. Base case: length == 2*n.

## When to Use

Generating all valid structures (expressions, trees, paths). Classic
backtracking with pruning. Output count follows Catalan numbers.

## Complexity

| | |
|---|---|
| **Time** | `O(4^n / sqrt(n)) — nth Catalan number` |
| **Space** | `O(n) — recursion depth (excluding output)` |

## Implementation

=== "Solution"

    ::: algo.recursion.generate_parentheses
        options:
          show_source: true

=== "Tests"

    ```python title="tests/recursion/test_generate_parentheses.py"
    --8<-- "tests/recursion/test_generate_parentheses.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge recursion generate_parentheses`

        Then implement the functions to make all tests pass.
        Use `just study recursion` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.recursion.generate_parentheses
            options:
              show_source: true
