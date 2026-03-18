---
title: Valid Parentheses
---

# Valid Parentheses

## Problem

Given a string containing just the characters '(', ')', '{', '}',
'[' and ']', determine if the input string is valid. A string is
valid if every open bracket is closed by the same type of bracket
in the correct order.

## Approach

Use a stack. Push opening brackets; on a closing bracket, check
that the stack top matches. The string is valid iff the stack is
empty at the end.

## When to Use

Matching/nesting validation — balanced brackets, HTML tags, expression
parsing. Any problem where openers must be closed in LIFO order.
Keywords: "valid", "balanced", "nested", "well-formed".

## Complexity

| | |
|---|---|
| **Time** | `O(n) -- single pass` |
| **Space** | `O(n) -- stack in worst case (all openers)` |

## Implementation

=== "Solution"

    ::: algo.stacks_queues.valid_parentheses
        options:
          show_source: true

=== "Tests"

    ```python title="tests/stacks_queues/test_valid_parentheses.py"
    --8<-- "tests/stacks_queues/test_valid_parentheses.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge stacks_queues valid_parentheses`

        Then implement the functions to make all tests pass.
        Use `just study stacks_queues` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.stacks_queues.valid_parentheses
            options:
              show_source: true
