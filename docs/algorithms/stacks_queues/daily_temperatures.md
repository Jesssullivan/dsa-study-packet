---
title: Daily Temperatures
---

# Daily Temperatures

## Problem

Given an array of daily temperatures, return an array where each
element is the number of days you would have to wait until a warmer
temperature. If there is no future warmer day, put 0.

## Approach

Monotonic decreasing stack of indices. For each temperature, pop
all stack entries whose temperature is lower than the current one
and record the distance.

## When to Use

Next-greater-element pattern — "next warmer day", "next higher price",
"first element greater than X to the right". Monotonic stack scans
linearly. Also: stock span, histogram largest rectangle.

## Complexity

| | |
|---|---|
| **Time** | `O(n) -- each index pushed and popped at most once` |
| **Space** | `O(n) -- stack in worst case (strictly decreasing input)` |

## Implementation

=== "Solution"

    ::: algo.stacks_queues.daily_temperatures
        options:
          show_source: true

=== "Tests"

    ```python title="tests/stacks_queues/test_daily_temperatures.py"
    --8<-- "tests/stacks_queues/test_daily_temperatures.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge stacks_queues daily_temperatures`

        Then implement the functions to make all tests pass.
        Use `just study stacks_queues` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.stacks_queues.daily_temperatures
            options:
              show_source: true
