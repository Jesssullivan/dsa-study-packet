---
title: Single Number
---

# Single Number

## Problem

Given a non-empty array where every element appears twice except
for one, find that single element.

## Approach

XOR all elements. Since a ^ a = 0 and a ^ 0 = a, all pairs
cancel out, leaving only the single element.

## When to Use

XOR uniqueness — "find the element appearing once while others appear
twice". XOR cancels pairs: a ^ a = 0. Extends to "two unique numbers"
by splitting on a differing bit. Keywords: "unique", "missing", "duplicate".

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.bit_manipulation.single_number
        options:
          show_source: true

=== "Tests"

    ```python title="tests/bit_manipulation/test_single_number.py"
    --8<-- "tests/bit_manipulation/test_single_number.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge bit_manipulation single_number`

        Then implement the functions to make all tests pass.
        Use `just study bit_manipulation` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.bit_manipulation.single_number
            options:
              show_source: true
