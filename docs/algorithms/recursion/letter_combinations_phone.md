---
title: Letter Combinations Phone
---

# Letter Combinations Phone

## Problem

Given a string containing digits from 2-9, return all possible
letter combinations that the number could represent on a phone keypad.

## Approach

Recursive backtracking: map each digit to its letters, build
combinations one digit at a time. At each level pick one letter
for the current digit, then recurse on remaining digits.

## When to Use

Cartesian product generation, combinatorial enumeration. Similar
structure to permutations but across different character sets.

## Complexity

| | |
|---|---|
| **Time** | `O(4^n) — where n = number of digits (worst case: 7 and 9 have 4 letters)` |
| **Space** | `O(n) — recursion depth (excluding output)` |

## Implementation

=== "Solution"

    ::: algo.recursion.letter_combinations_phone
        options:
          show_source: true

=== "Tests"

    ```python title="tests/recursion/test_letter_combinations_phone.py"
    --8<-- "tests/recursion/test_letter_combinations_phone.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge recursion letter_combinations_phone`

        Then implement the functions to make all tests pass.
        Use `just study recursion` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.recursion.letter_combinations_phone
            options:
              show_source: true
