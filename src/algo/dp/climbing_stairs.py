"""Climbing Stairs — ways to climb n stairs taking 1 or 2 steps.

Problem:
    You are climbing a staircase with n steps. Each time you can climb
    1 or 2 steps. Return the number of distinct ways to reach the top.

Approach:
    Fibonacci variant. The number of ways to reach step i equals the
    sum of ways to reach step i-1 (take 1 step) and step i-2 (take 2
    steps). Use two rolling variables instead of an array (climb_stairs).
    An alternate top-down form (climb_stairs_memo) shows the same
    recurrence via memoized recursion using functools.cache.

When to use:
    Counting paths / Fibonacci family — "how many ways to reach step N",
    "count distinct paths with step choices". Rolling-variable DP when
    each state depends on a fixed number of previous states.

Complexity:
    Time:  O(n)
    Space: O(1)
"""

import functools


def climb_stairs(n: int) -> int:
    """Return the number of distinct ways to climb *n* stairs.

    >>> climb_stairs(1)
    1
    >>> climb_stairs(5)
    8
    """
    if n < 0:
        msg = f"n must be non-negative, got {n}"
        raise ValueError(msg)
    if n <= 1:
        return 1

    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        # tuple assignment evaluates the RHS first, so both rolling
        # variables advance from their *old* values simultaneously
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


# --- top-down memoized alternate (functools.cache instead of a rolling loop) ---
@functools.cache
def climb_stairs_memo(n: int) -> int:
    """Return the number of distinct ways to climb *n* stairs (top-down).

    >>> climb_stairs_memo(1)
    1
    >>> climb_stairs_memo(5)
    8
    """
    if n < 0:
        msg = f"n must be non-negative, got {n}"
        raise ValueError(msg)
    if n <= 1:
        return 1
    return climb_stairs_memo(n - 1) + climb_stairs_memo(n - 2)
