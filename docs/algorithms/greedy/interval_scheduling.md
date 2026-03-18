---
title: Interval Scheduling
---

# Interval Scheduling

## Problem

Given a collection of intervals, find the maximum number of
non-overlapping intervals (activity selection problem).

## Approach

Sort intervals by end time. Greedily select the next interval
whose start time is >= the end time of the last selected interval.
This maximizes the number of non-overlapping intervals.

## When to Use

Activity selection / resource booking — "max non-overlapping intervals",
"minimum removals for no overlap", "room scheduling". Sort by end time,
greedily pick earliest-finishing. Aviation: gate/runway slot allocation.

## Complexity

| | |
|---|---|
| **Time** | `O(n log n)` |
| **Space** | `O(1)  (excluding input sort)` |

## Implementation

=== "Solution"

    ::: algo.greedy.interval_scheduling
        options:
          show_source: true

=== "Tests"

    ```python title="tests/greedy/test_interval_scheduling.py"
    --8<-- "tests/greedy/test_interval_scheduling.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge greedy interval_scheduling`

        Then implement the functions to make all tests pass.
        Use `just study greedy` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.greedy.interval_scheduling
            options:
              show_source: true
