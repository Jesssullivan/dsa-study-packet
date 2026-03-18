---
title: Merge Intervals
---

# Merge Intervals

## Problem

Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals and return the non-overlapping
result covering the same ranges.

## Approach

Sort intervals by start time. Iterate and merge: if the current
interval overlaps with the last merged one, extend the end;
otherwise append a new interval.

## When to Use

Overlapping range consolidation — "merge intervals", "insert interval",
"meeting room conflicts". Sort by start, sweep and merge.
Aviation: airspace reservation merging, calendar/schedule compression.

## Complexity

| | |
|---|---|
| **Time** | `O(n log n)` |
| **Space** | `O(n)  (for the output)` |

## Implementation

=== "Solution"

    ::: algo.greedy.merge_intervals
        options:
          show_source: true

=== "Tests"

    ```python title="tests/greedy/test_merge_intervals.py"
    --8<-- "tests/greedy/test_merge_intervals.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge greedy merge_intervals`

        Then implement the functions to make all tests pass.
        Use `just study greedy` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.greedy.merge_intervals
            options:
              show_source: true
