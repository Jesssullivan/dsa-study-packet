"""Flatten Nested List — recursively flatten arbitrarily deep lists.

Problem:
    Given a nested list of integers (can be arbitrarily deep), flatten
    it into a single list of integers.

Approach:
    Recursive: if element is a list, recurse into it; otherwise yield
    the integer. Also provide an iterative version using an explicit
    stack (process in reverse to maintain order).

When to use:
    Processing recursive/nested data structures — JSON, XML, file trees,
    AST traversal. Mission-systems relevance: nested geospatial data, hierarchical
    flight plans.

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


def flatten_iterative(nested: NestedList) -> list[int]:
    """Flatten *nested* list of integers iteratively using a stack.

    >>> flatten_iterative([1, [2, [3, 4], 5], 6])
    [1, 2, 3, 4, 5, 6]
    >>> flatten_iterative([])
    []
    """
    result: list[int] = []
    stack: list[int | list[Any]] = list(reversed(nested))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            for sub in reversed(item):
                stack.append(sub)
        else:
            result.append(item)
    return result
