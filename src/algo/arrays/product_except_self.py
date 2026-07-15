"""Product of Array Except Self — product of all elements except self.

Problem:
    Given an integer array, return an array where each element is the
    product of all other elements. Do not use division.

Approach:
    Two-pass prefix/suffix products. First pass builds prefix products
    left-to-right, second pass multiplies in suffix products right-to-left.
    Uses the output array itself to store prefix, then folds in suffix
    with a running variable. Alternate product_except_self_accumulate
    builds the same prefix/suffix products with itertools.accumulate.

When to use:
    Prefix/suffix accumulation without division — product, sum, or any
    associative operation where you need "everything except index i".
    Also: running totals, range queries without a segment tree.

Complexity:
    Time:  O(n)
    Space: O(1)  (output array not counted)
"""

from collections.abc import Sequence
from itertools import accumulate
from operator import mul


def product_except_self(nums: Sequence[int]) -> list[int]:
    """Return array of products of all elements except nums[i].

    >>> product_except_self([1, 2, 3, 4])
    [24, 12, 8, 6]
    """
    n = len(nums)
    result = [1] * n

    # result[] doubles as the prefix table, so no extra O(n) array is needed
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # fold in the suffix product via a running variable, right to left
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


# --- itertools.accumulate prefix/suffix variant (stdlib, O(n) extra space) ---
def product_except_self_accumulate(nums: Sequence[int]) -> list[int]:
    """Return array of products of all elements except nums[i], via accumulate.

    >>> product_except_self_accumulate([1, 2, 3, 4])
    [24, 12, 8, 6]
    """
    n = len(nums)
    prefix = [1, *accumulate(nums, mul)][:n]
    suffix = [1, *accumulate(reversed(nums), mul)][:n][::-1]
    return [p * s for p, s in zip(prefix, suffix, strict=True)]
