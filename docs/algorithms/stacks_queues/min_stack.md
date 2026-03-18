---
title: Min Stack
---

# Min Stack

## Problem

Design a stack that supports push, pop, top, and retrieving the
minimum element, all in O(1) time.

## Approach

Store (value, current_min) tuples on the stack. Each entry records
the minimum at the time it was pushed, so getMin is always O(1)
by reading the top tuple's min field.

## When to Use

Augmented data structure for O(1) aggregate queries — "get min/max
while supporting push/pop". Pattern: store auxiliary data alongside
each element. Useful for real-time monitoring dashboards.

## Complexity

| | |
|---|---|
| **Time** | `O(1) for all operations` |
| **Space** | `O(n) -- one tuple per element` |

## Implementation

=== "Solution"

    ::: algo.stacks_queues.min_stack
        options:
          show_source: true

=== "Tests"

    ```python title="tests/stacks_queues/test_min_stack.py"
    --8<-- "tests/stacks_queues/test_min_stack.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge stacks_queues min_stack`

        Then implement the functions to make all tests pass.
        Use `just study stacks_queues` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.stacks_queues.min_stack
            options:
              show_source: true
