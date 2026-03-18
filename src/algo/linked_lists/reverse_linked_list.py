"""Reverse a singly linked list.

Problem:
    Given the head of a singly linked list, reverse the list and return
    the new head.

Approach:
    Iterative: Walk the list with prev/curr pointers, reversing each link.
    Recursive: Reverse the rest of the list, then point the next node back.

When to use:
    In-place linked list reversal — "reverse list", "reverse sublist",
    pointer manipulation without extra space. Building block for
    palindrome check, k-group reversal, and reorder-list problems.

Complexity:
    Time:  O(n)
    Space: O(1) iterative, O(n) recursive (call stack)
"""

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: ListNode | None = None


def reverse_iterative(head: ListNode | None) -> ListNode | None:
    """Reverse a linked list in place using iteration.

    >>> to_list(reverse_iterative(from_list([1, 2, 3])))
    [3, 2, 1]
    """
    prev: ListNode | None = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def reverse_recursive(head: ListNode | None) -> ListNode | None:
    """Reverse a linked list using recursion.

    >>> to_list(reverse_recursive(from_list([1, 2, 3])))
    [3, 2, 1]
    """
    if not head or not head.next:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


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
