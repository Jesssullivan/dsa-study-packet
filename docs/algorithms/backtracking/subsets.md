---
title: Subsets
---

# Subsets

## Problem

Given an integer array of unique elements, return all possible
subsets (the power set). The solution must not contain duplicate
subsets.

## Approach

Backtracking. At each index, decide to include or exclude the
element. Append a snapshot of the current path at every node.

## When to Use

Power set / feature combinations — "generate all subsets", "all
combinations of features", "enumerate configurations". Include/exclude
decision at each element. Also: feature selection, test coverage sets.

## Complexity

| | |
|---|---|
| **Time** | `O(n * 2^n)` |
| **Space** | `O(n)  (excluding output; recursion depth is n)` |

## Implementation

=== "Solution"

    ::: algo.backtracking.subsets
        options:
          show_source: true

=== "Tests"

    ```python title="tests/backtracking/test_subsets.py"
    --8<-- "tests/backtracking/test_subsets.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge backtracking subsets`

        Then implement the functions to make all tests pass.
        Use `just study backtracking` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.backtracking.subsets
            options:
              show_source: true
