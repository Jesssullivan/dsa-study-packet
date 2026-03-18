---
title: Permutations
---

# Permutations

## Problem

Given an array of distinct integers, return all possible
permutations in any order.

## Approach

Backtracking with a visited set. At each position, try every
unused element, mark it used, recurse, then unmark.

## When to Use

All orderings — "generate all permutations", "all arrangements",
brute-force over orderings for small n. Building block for
next-permutation and ranking/unranking algorithms.

## Complexity

| | |
|---|---|
| **Time** | `O(n * n!)` |
| **Space** | `O(n)  (recursion depth + visited set)` |

## Implementation

=== "Solution"

    ::: algo.backtracking.permutations
        options:
          show_source: true

=== "Tests"

    ```python title="tests/backtracking/test_permutations.py"
    --8<-- "tests/backtracking/test_permutations.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge backtracking permutations`

        Then implement the functions to make all tests pass.
        Use `just study backtracking` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.backtracking.permutations
            options:
              show_source: true
