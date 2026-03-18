"""Container With Most Water — max area between two vertical lines.

Problem:
    Given n non-negative integers representing vertical line heights at
    positions 0..n-1, find the two lines that together with the x-axis
    form a container holding the most water.

Approach:
    Start with two pointers at the outermost lines. The area is limited
    by the shorter line, so always move the pointer at the shorter side
    inward to try for a taller line.

When to use:
    Maximizing area/product with two boundaries — shrink from both ends,
    always moving the weaker constraint inward.
    Keywords: "maximize rectangle", "widest pair", "two-boundary optimization".

Complexity:
    Time:  O(n)
    Space: O(1)
"""

from collections.abc import Sequence


def max_area(height: Sequence[int]) -> int:
    """Return the maximum water area between any two lines in *height*.

    >>> max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])
    49
    """
    lo, hi = 0, len(height) - 1
    best = 0

    while lo < hi:
        area = min(height[lo], height[hi]) * (hi - lo)
        best = max(best, area)
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1

    return best
