"""Product of Array Except Self — product of all elements except self.

Problem:
    Given an integer array, return an array where each element is the
    product of all other elements. Do not use division.

Approach:
    Two-pass prefix/suffix products. First pass builds prefix products
    left-to-right, second pass multiplies in suffix products right-to-left.
    Uses the output array itself to store prefix, then folds in suffix
    with a running variable.

When to use:
    Prefix/suffix accumulation without division — product, sum, or any
    associative operation where you need "everything except index i".
    Also: running totals, range queries without a segment tree.

Complexity:
    Time:  O(n)
    Space: O(1)  (output array not counted)
"""

from collections.abc import Sequence


def product_except_self(nums: Sequence[int]) -> list[int]:
    """Return array of products of all elements except nums[i].

    >>> product_except_self([1, 2, 3, 4])
    [24, 12, 8, 6]
    """
    n = len(nums)
    result = [1] * n

    # Prefix pass: result[i] = product of nums[0..i-1]
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Suffix pass: multiply in product of nums[i+1..n-1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
