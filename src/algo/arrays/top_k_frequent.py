"""Top K Frequent Elements — return the k most frequent elements.

Problem:
    Given an integer array and an integer k, return the k most frequent
    elements. The answer is guaranteed to be unique.

Approach:
    Bucket sort by frequency. Count occurrences, then place each number
    into a bucket indexed by its frequency. Walk buckets from highest
    frequency downward until k elements are collected.

When to use:
    Frequency counting + selection — "top K", "most common", "least common".
    Bucket sort avoids O(n log n); see also heaps/kth_largest for streaming variant.

Complexity:
    Time:  O(n)
    Space: O(n)
"""

from collections import Counter
from collections.abc import Sequence


def top_k_frequent(nums: Sequence[int], k: int) -> list[int]:
    """Return the *k* most frequent elements in *nums*.

    >>> sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
    [1, 2]
    """
    if k <= 0:
        return []

    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result: list[int] = []
    for i in range(len(buckets) - 1, -1, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]

    return result[:k]
