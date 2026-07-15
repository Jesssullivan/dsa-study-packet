"""Flatten Nested List — recursively flatten arbitrarily deep lists.

Problem:
    Given a nested list of integers (can be arbitrarily deep), flatten
    it into a single list of integers.

Approach:
    flatten_recursive: recurse into list elements, yield everything
    else. flatten_iterative is the alternate using an explicit stack
    instead of the call stack (push in reverse to maintain order).

When to use:
    Processing recursive/nested data structures — JSON, XML, file trees,
    AST traversal.

Complexity:
    Time:  O(n) — where n = total elements across all nesting levels
    Space: O(d) recursive / O(n) iterative — d = max depth
"""

from collections.abc import Iterator, Sequence
from typing import Any

# Recursive nesting type — list[int | list[...]] can't be expressed finitely,
# so we use Sequence[int | list[Any]] for covariant read-only params.
type NestedList = Sequence[int | list[Any]]


def flatten_recursive(nested: NestedList) -> list[int]:
    """Flatten *nested* list of integers recursively.

    >>> flatten_recursive([1, [2, [3, 4], 5], 6])
    [1, 2, 3, 4, 5, 6]
    >>> flatten_recursive([])
    []
    """
    return list(_flatten_helper(nested))


def _flatten_helper(nested: NestedList) -> Iterator[int]:
    for item in nested:
        if isinstance(item, list):
            yield from _flatten_helper(item)
        else:
            yield item


# --- iterative alternate: explicit stack instead of the call stack ---
def flatten_iterative(nested: NestedList) -> list[int]:
    """Flatten *nested* list of integers iteratively using a stack.

    >>> flatten_iterative([1, [2, [3, 4], 5], 6])
    [1, 2, 3, 4, 5, 6]
    >>> flatten_iterative([])
    []
    """
    result: list[int] = []
    # push in reverse so pop() (LIFO) still yields items in original order
    stack: list[int | list[Any]] = list(reversed(nested))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            for sub in reversed(item):
                stack.append(sub)
        else:
            result.append(item)
    return result
