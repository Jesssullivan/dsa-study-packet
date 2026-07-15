"""Trapping Rain Water — total water trapped between bars.

Problem:
    Given n non-negative integers representing an elevation map where
    the width of each bar is 1, compute how much water can be trapped
    after raining.

Approach:
    Two pointers from both ends. Track left_max and right_max. Move
    the pointer on the side with the smaller max inward. Water at each
    position is (current_side_max - height[pointer]). Alternate
    trap_prefix_suffix precomputes left/right max arrays with
    itertools.accumulate instead of tracking them with two pointers.

When to use:
    Bounded accumulation between barriers — water trapping, histogram
    area, or any problem where capacity at each position depends on the
    max values to its left and right. Also: elevation profile analysis.

Complexity:
    Time:  O(n)
    Space: O(1)
"""

from collections.abc import Sequence
from itertools import accumulate


def trap(height: Sequence[int]) -> int:
    """Return total units of water trapped by the elevation map.

    >>> trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    """
    if len(height) < 3:
        return 0

    lo, hi = 0, len(height) - 1
    lo_max = hi_max = 0
    water = 0

    while lo < hi:
        # the smaller running max is the one that actually bounds the water at
        # its pointer — the far side is guaranteed to be at least as tall
        if height[lo] < height[hi]:
            lo_max = max(lo_max, height[lo])
            water += lo_max - height[lo]
            lo += 1
        else:
            hi_max = max(hi_max, height[hi])
            water += hi_max - height[hi]
            hi -= 1

    return water


# --- prefix/suffix max arrays via itertools.accumulate (O(n) space) ---
def trap_prefix_suffix(height: Sequence[int]) -> int:
    """Return total units of water trapped, via precomputed max arrays.

    >>> trap_prefix_suffix([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    """
    n = len(height)
    if n < 3:
        return 0

    left_max = list(accumulate(height, max))
    right_max = list(accumulate(reversed(height), max))[::-1]
    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
