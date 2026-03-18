"""Trapping Rain Water — total water trapped between bars.

Problem:
    Given n non-negative integers representing an elevation map where
    the width of each bar is 1, compute how much water can be trapped
    after raining.

Approach:
    Two pointers from both ends. Track left_max and right_max. Move
    the pointer on the side with the smaller max inward. Water at each
    position is (current_side_max - height[pointer]).

When to use:
    Bounded accumulation between barriers — water trapping, histogram
    area, or any problem where capacity at each position depends on the
    max values to its left and right. Also: elevation profile analysis.

Complexity:
    Time:  O(n)
    Space: O(1)
"""

from collections.abc import Sequence


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
        if height[lo] < height[hi]:
            lo_max = max(lo_max, height[lo])
            water += lo_max - height[lo]
            lo += 1
        else:
            hi_max = max(hi_max, height[hi])
            water += hi_max - height[hi]
            hi -= 1

    return water
