---
title: Container With Most Water
---

# Container With Most Water

## Problem

Given n non-negative integers representing vertical line heights at
positions 0..n-1, find the two lines that together with the x-axis
form a container holding the most water.

## Approach

Start with two pointers at the outermost lines. The area is limited
by the shorter line, so always move the pointer at the shorter side
inward to try for a taller line.

## When to Use

Maximizing area/product with two boundaries — shrink from both ends,
always moving the weaker constraint inward.
Keywords: "maximize rectangle", "widest pair", "two-boundary optimization".

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.two_pointers.container_with_most_water
        options:
          show_source: true

=== "Tests"

    ```python title="tests/two_pointers/test_container_with_most_water.py"
    --8<-- "tests/two_pointers/test_container_with_most_water.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge two_pointers container_with_most_water`

        Then implement the functions to make all tests pass.
        Use `just study two_pointers` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.two_pointers.container_with_most_water
            options:
              show_source: true
