"""Find the kth largest element.

Problem:
    Given an unsorted array and an integer k, return the kth largest element.
    Also implement a streaming version that supports adding new values.

Approach:
    Maintain a min-heap of size k. The heap top is always the kth largest.
    For each new element larger than the heap top, replace it.

When to use:
    Streaming top-K — "kth largest in a stream", "maintain running top K".
    Min-heap of size k keeps only the K largest seen so far.
    Also: real-time leaderboard, top-K sensor readings in telemetry.

Complexity:
    find_kth_largest: O(n log k) time, O(k) space
    KthLargest.add:   O(log k) time per call, O(k) space total
"""

import heapq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def find_kth_largest(nums: Sequence[int], k: int) -> int:
    """Return the kth largest element in the array.

    >>> find_kth_largest([3, 2, 1, 5, 6, 4], 2)
    5
    """
    if k <= 0 or k > len(nums):
        msg = f"k={k} out of range for length {len(nums)}"
        raise ValueError(msg)

    heap = list(nums[:k])
    heapq.heapify(heap)

    for n in nums[k:]:
        if n > heap[0]:
            heapq.heapreplace(heap, n)

    return heap[0]


class KthLargest:
    """Stream version: maintain the kth largest over a growing dataset.

    >>> kl = KthLargest(3, [4, 5, 8, 2])
    >>> kl.add(3)
    4
    >>> kl.add(5)
    5
    >>> kl.add(10)
    5
    """

    def __init__(self, k: int, nums: Sequence[int]) -> None:
        self._k = k
        self._heap: list[int] = []
        for n in nums:
            self.add(n)

    def add(self, val: int) -> int:
        """Add a value and return the current kth largest element."""
        if len(self._heap) < self._k:
            heapq.heappush(self._heap, val)
        elif val > self._heap[0]:
            heapq.heapreplace(self._heap, val)
        return self._heap[0]
