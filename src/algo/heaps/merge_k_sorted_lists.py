"""Merge k sorted linked lists.

Problem:
    Given an array of k sorted linked lists, merge them into one sorted
    linked list.

Approach:
    Use a min-heap of size k. Push (value, list_index, node) tuples.
    Pop the smallest, append to result, and push the next node from
    that list. The list_index breaks ties to avoid comparing nodes.

When to use:
    K-way merge for external sorting — "merge K sorted lists/arrays/files",
    combining sorted partitions from distributed systems. Min-heap of size
    k selects the next smallest element. See also: merge_two_sorted.

Complexity:
    Time:  O(n log k) where n = total nodes across all lists
    Space: O(k) for the heap
"""

import heapq
from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: ListNode | None = None


def merge_k_sorted(lists: list[ListNode | None]) -> ListNode | None:
    """Merge k sorted linked lists into one sorted linked list.

    >>> to_list(
    ...     merge_k_sorted(
    ...         [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
    ...     )
    ... )
    [1, 1, 2, 3, 4, 4, 5, 6]
    """
    heap: list[tuple[int, int, ListNode]] = []

    for i, node in enumerate(lists):
        if node:
            heap.append((node.val, i, node))

    heapq.heapify(heap)

    dummy = ListNode(0)
    tail = dummy

    while heap:
        _val, idx, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))

    return dummy.next


# --- helpers for testing ---
def from_list(vals: list[int]) -> ListNode | None:
    """Build a linked list from a Python list."""
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    """Collect linked list values into a Python list."""
    result: list[int] = []
    while head:
        result.append(head.val)
        head = head.next
    return result
