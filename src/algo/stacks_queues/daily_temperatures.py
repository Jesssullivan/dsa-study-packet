"""Daily temperatures.

Problem:
    Given an array of daily temperatures, return an array where each
    element is the number of days you would have to wait until a warmer
    temperature. If there is no future warmer day, put 0.

Approach:
    Monotonic decreasing stack of indices. For each temperature, pop
    all stack entries whose temperature is lower than the current one
    and record the distance. Alternate daily_temperatures_brute checks
    each future day directly.

When to use:
    Next-greater-element pattern — "next warmer day", "next higher price",
    "first element greater than X to the right". Monotonic stack scans
    linearly. Also: stock span, histogram largest rectangle.

Complexity:
    Time:  O(n) -- each index pushed and popped at most once
    Space: O(n) -- stack in worst case (strictly decreasing input)
"""

from collections.abc import Sequence


def daily_temperatures(temps: Sequence[int]) -> list[int]:
    """Return days until a warmer temperature for each day.

    >>> daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
    [1, 1, 4, 2, 1, 1, 0, 0]
    >>> daily_temperatures([30, 40, 50, 60])
    [1, 1, 1, 0]
    """
    result = [0] * len(temps)
    stack: list[int] = []  # indices with decreasing temps

    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:  # current day is warmer than stack top
            j = stack.pop()
            result[j] = i - j  # distance from j's day to the first warmer day found
        stack.append(i)

    return result


# --- brute-force alternate: scan forward for the first warmer day (O(n^2)) ---
def daily_temperatures_brute(temps: Sequence[int]) -> list[int]:
    """Return days until a warmer temperature via a direct forward scan.

    >>> daily_temperatures_brute([73, 74, 75, 71, 69, 72, 76, 73])
    [1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temps)
    return [
        next((j - i for j in range(i + 1, n) if temps[j] > temps[i]), 0)
        for i in range(n)
    ]
