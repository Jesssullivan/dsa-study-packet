"""Merge two sorted linked lists.

Problem:
    Given the heads of two sorted linked lists, merge them into one sorted
    list built from the nodes of the two input lists.

Approach:
    Use a dummy head node and compare the fronts of both lists, advancing
    the smaller one each time.

When to use:
    Merge step of merge sort — combining two sorted sequences into one.
    Building block for merge_k_sorted_lists and external merge sort.
    Keywords: "merge sorted", "interleave ordered streams".

Complexity:
    Time:  O(n + m)
    Space: O(1) — only pointer manipulation, no new nodes allocated
"""

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: ListNode | None = None


def merge_two_sorted(
    l1: ListNode | None,
    l2: ListNode | None,
) -> ListNode | None:
    """Merge two sorted linked lists into one sorted list.

    >>> to_list(merge_two_sorted(from_list([1, 3, 5]), from_list([2, 4, 6])))
    [1, 2, 3, 4, 5, 6]
    """
    dummy = ListNode(0)
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2
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
