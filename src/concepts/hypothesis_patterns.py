"""Systems-under-test for Hypothesis property-based testing patterns.

This module provides two deliberately simple but non-trivial classes
that are ideal targets for Hypothesis strategies and stateful testing:

1. ``SortedList``   — a list that maintains sorted order via ``bisect``
2. ``BoundedCounter`` — an integer counter clamped to [min_val, max_val]

The *real* tutorial lives in the corresponding test file
(``tests/concepts/test_hypothesis_patterns.py``), which demonstrates
``@composite``, ``RuleBasedStateMachine``, ``@example``, settings
profiles, ``st.builds``, and ``st.recursive``.

References
----------
* ``bisect`` module — https://docs.python.org/3.14/library/bisect.html
* Hypothesis docs  — https://hypothesis.readthedocs.io/en/latest/
"""

import bisect
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# SortedList — always-sorted collection backed by bisect
# --------------------------------------------------------------------------- #


class SortedList:
    """A list that maintains its elements in sorted order at all times.

    Insertions use ``bisect.insort`` for O(n) insertion with O(log n)
    position finding.  Searching uses ``bisect.bisect_left`` for
    O(log n) membership checks.

    >>> sl = SortedList()
    >>> sl.insert(3)
    >>> sl.insert(1)
    >>> sl.insert(2)
    >>> sl.to_list()
    [1, 2, 3]
    >>> sl.search(2)
    True
    >>> sl.search(4)
    False
    """

    def __init__(self) -> None:
        self._data: list[int] = []

    def insert(self, val: int) -> None:
        """Insert *val* in sorted position.

        >>> sl = SortedList()
        >>> sl.insert(5)
        >>> sl.insert(2)
        >>> sl.to_list()
        [2, 5]
        """
        # bisect.insort maintains sort invariant in O(n) time.
        bisect.insort(self._data, val)

    def search(self, val: int) -> bool:
        """Return ``True`` if *val* exists in the list.

        Uses binary search via ``bisect_left`` — O(log n).

        >>> sl = SortedList()
        >>> sl.insert(10)
        >>> sl.search(10)
        True
        >>> sl.search(99)
        False
        """
        idx = bisect.bisect_left(self._data, val)
        return idx < len(self._data) and self._data[idx] == val

    def remove(self, val: int) -> None:
        """Remove one occurrence of *val*.

        Raises ``ValueError`` if *val* is not present.

        >>> sl = SortedList()
        >>> sl.insert(1)
        >>> sl.remove(1)
        >>> sl.to_list()
        []
        """
        idx = bisect.bisect_left(self._data, val)
        if idx < len(self._data) and self._data[idx] == val:
            self._data.pop(idx)
        else:
            msg = f"{val} not in SortedList"
            raise ValueError(msg)

    def to_list(self) -> list[int]:
        """Return a copy of the internal sorted list.

        >>> sl = SortedList()
        >>> sl.insert(3)
        >>> sl.insert(1)
        >>> sl.to_list()
        [1, 3]
        """
        return list(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"SortedList({self._data!r})"


# --------------------------------------------------------------------------- #
# BoundedCounter — counter with min/max bounds
# --------------------------------------------------------------------------- #


@dataclass
class BoundedCounter:
    """An integer counter clamped between *min_val* and *max_val*.

    Attempting to increment past *max_val* or decrement past *min_val*
    raises ``ValueError``.

    >>> bc = BoundedCounter(min_val=0, max_val=3)
    >>> bc.increment()
    >>> bc.increment()
    >>> bc.value
    2
    >>> bc.decrement()
    >>> bc.value
    1
    """

    min_val: int = 0
    max_val: int = 10
    _count: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.min_val > self.max_val:
            msg = f"min_val ({self.min_val}) > max_val ({self.max_val})"
            raise ValueError(msg)
        # Start the counter at min_val.
        self._count = self.min_val

    @property
    def value(self) -> int:
        """Current counter value.

        >>> BoundedCounter(min_val=5, max_val=10).value
        5
        """
        return self._count

    def increment(self) -> None:
        """Add 1, raising ``ValueError`` if at *max_val*.

        >>> bc = BoundedCounter(min_val=0, max_val=1)
        >>> bc.increment()
        >>> bc.increment()
        Traceback (most recent call last):
            ...
        ValueError: counter at maximum (1)
        """
        if self._count >= self.max_val:
            msg = f"counter at maximum ({self.max_val})"
            raise ValueError(msg)
        self._count += 1

    def decrement(self) -> None:
        """Subtract 1, raising ``ValueError`` if at *min_val*.

        >>> bc = BoundedCounter(min_val=0, max_val=5)
        >>> bc.decrement()
        Traceback (most recent call last):
            ...
        ValueError: counter at minimum (0)
        """
        if self._count <= self.min_val:
            msg = f"counter at minimum ({self.min_val})"
            raise ValueError(msg)
        self._count -= 1
