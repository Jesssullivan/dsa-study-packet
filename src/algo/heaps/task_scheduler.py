"""Task scheduler with cooldown.

Problem:
    Given a list of tasks (characters) and a cooldown period n, find the
    minimum number of intervals needed to execute all tasks. The same task
    must wait at least n intervals before being executed again.

Approach:
    Use a max-heap (negated counts) to always schedule the most frequent
    task first. After executing a task, place it in a cooldown queue with
    the time it becomes available. When that time arrives, push it back
    onto the heap.

When to use:
    Scheduling with cooldown constraints — "minimum time to complete all
    tasks with cooldown", "CPU scheduling", "rate-limited job execution".
    Max-heap ensures the most frequent task is scheduled first.
    Aviation: runway scheduling with minimum separation times.

Complexity:
    Time:  O(t) where t = total intervals (bounded by len(tasks) * (n+1))
    Space: O(1) — at most 26 distinct task types
"""

from __future__ import annotations

import heapq
from collections import Counter, deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def least_interval(tasks: Sequence[str], n: int) -> int:
    """Return the minimum number of intervals to complete all tasks.

    >>> least_interval(["A", "A", "A", "B", "B", "B"], 2)
    8
    """
    if not tasks:
        return 0

    counts = list(Counter(tasks).values())
    max_heap = [-c for c in counts]
    heapq.heapify(max_heap)

    time = 0
    cooldown: deque[tuple[int, int]] = deque()  # (available_time, neg_count)

    while max_heap or cooldown:
        time += 1

        if max_heap:
            cnt = heapq.heappop(max_heap) + 1  # execute one (cnt is negative)
            if cnt:
                cooldown.append((time + n, cnt))

        if cooldown and cooldown[0][0] == time:
            heapq.heappush(max_heap, cooldown.popleft()[1])

    return time
