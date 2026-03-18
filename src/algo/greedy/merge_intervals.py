"""Merge Intervals — merge overlapping intervals.

Problem:
    Given an array of intervals where intervals[i] = [start_i, end_i],
    merge all overlapping intervals and return the non-overlapping
    result covering the same ranges.

Approach:
    Sort intervals by start time. Iterate and merge: if the current
    interval overlaps with the last merged one, extend the end;
    otherwise append a new interval.

When to use:
    Overlapping range consolidation — "merge intervals", "insert interval",
    "meeting room conflicts". Sort by start, sweep and merge.
    Aviation: airspace reservation merging, calendar/schedule compression.

Complexity:
    Time:  O(n log n)
    Space: O(n)  (for the output)
"""

from collections.abc import Sequence


def merge_intervals(intervals: Sequence[Sequence[int]]) -> list[list[int]]:
    """Return merged non-overlapping intervals.

    >>> merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
    [[1, 6], [8, 10], [15, 18]]
    """
    if not intervals:
        return []

    sorted_iv = sorted(intervals, key=lambda iv: iv[0])
    merged: list[list[int]] = [list(sorted_iv[0])]

    for start, end in sorted_iv[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
