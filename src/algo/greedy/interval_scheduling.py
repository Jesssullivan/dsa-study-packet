"""Interval Scheduling — maximum non-overlapping intervals.

Problem:
    Given a collection of intervals, find the maximum number of
    non-overlapping intervals (activity selection problem).

Approach:
    Sort intervals by end time. Greedily select the next interval
    whose start time is >= the end time of the last selected interval.
    This maximizes the number of non-overlapping intervals.

When to use:
    Activity selection / resource booking — "max non-overlapping intervals",
    "minimum removals for no overlap", "room scheduling". Sort by end time,
    greedily pick earliest-finishing. Aviation: gate/runway slot allocation.

Complexity:
    Time:  O(n log n)
    Space: O(1)  (excluding input sort)
"""

from collections.abc import Sequence


def max_non_overlapping(intervals: Sequence[Sequence[int]]) -> int:
    """Return the maximum number of non-overlapping intervals.

    >>> max_non_overlapping([[1, 3], [2, 4], [3, 5], [0, 6]])
    2
    """
    if not intervals:
        return 0

    sorted_iv = sorted(intervals, key=lambda iv: iv[1])
    count = 1
    end = sorted_iv[0][1]

    for start, finish in sorted_iv[1:]:
        if start >= end:
            count += 1
            end = finish

    return count


def min_removals(intervals: Sequence[Sequence[int]]) -> int:
    """Return the minimum number of intervals to remove for no overlap.

    Equivalent to len(intervals) - max_non_overlapping(intervals).

    >>> min_removals([[1, 2], [2, 3], [3, 4], [1, 3]])
    1
    """
    return len(intervals) - max_non_overlapping(intervals)
