---
title: String To Integer Atoi
---

# String To Integer Atoi

## Problem

Implement atoi which converts a string to a 32-bit signed integer.
Handle leading whitespace, an optional +/- sign, consecutive digits,
and clamp the result to [-2^31, 2^31 - 1].

## Approach

Linear scan with state tracking: skip whitespace, read optional sign,
accumulate digits, clamp on overflow. Stop at first non-digit after
sign processing.

## When to Use

Parsing problems, state machine patterns. Tests attention to edge
cases (whitespace, signs, overflow, trailing non-digits).

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.strings.string_to_integer_atoi
        options:
          show_source: true

=== "Tests"

    ```python title="tests/strings/test_string_to_integer_atoi.py"
    --8<-- "tests/strings/test_string_to_integer_atoi.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge strings string_to_integer_atoi`

        Then implement the functions to make all tests pass.
        Use `just study strings` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.strings.string_to_integer_atoi
            options:
              show_source: true
