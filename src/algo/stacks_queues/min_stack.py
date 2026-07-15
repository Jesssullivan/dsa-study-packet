"""Min stack.

Problem:
    Design a stack that supports push, pop, top, and retrieving the
    minimum element, all in O(1) time.

Approach:
    Store (value, current_min) tuples on the stack. Each entry records
    the minimum at the time it was pushed, so getMin is always O(1)
    by reading the top tuple's min field. Alternate MinStackTwoStacks
    tracks the running minimum in a separate auxiliary stack instead.

When to use:
    Augmented data structure for O(1) aggregate queries — "get min/max
    while supporting push/pop". Pattern: store auxiliary data alongside
    each element. Useful for real-time monitoring dashboards.

Complexity:
    Time:  O(1) for all operations
    Space: O(n) -- one tuple per element
"""


class MinStack:
    """Stack supporting O(1) push, pop, top, and get_min.

    >>> ms = MinStack()
    >>> ms.push(-2)
    >>> ms.push(0)
    >>> ms.push(-3)
    >>> ms.get_min()
    -3
    >>> ms.pop()
    >>> ms.get_min()
    -2
    """

    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        # store the running min alongside val; a single shared min var would
        # break once that min is popped, since we couldn't recover the prior one
        current_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, current_min))

    def pop(self) -> None:
        if not self._stack:
            msg = "pop from empty stack"
            raise IndexError(msg)
        self._stack.pop()

    def top(self) -> int:
        if not self._stack:
            msg = "top from empty stack"
            raise IndexError(msg)
        return self._stack[-1][0]

    def get_min(self) -> int:
        if not self._stack:
            msg = "get_min from empty stack"
            raise IndexError(msg)
        return self._stack[-1][1]


# --- two-stack alternate: separate stack tracks the running minimum ---
class MinStackTwoStacks:
    """Stack supporting O(1) push, pop, top, and get_min via an aux min stack.

    >>> ms = MinStackTwoStacks()
    >>> ms.push(-2)
    >>> ms.push(0)
    >>> ms.push(-3)
    >>> ms.get_min()
    -3
    >>> ms.pop()
    >>> ms.get_min()
    -2
    """

    def __init__(self) -> None:
        self._stack: list[int] = []
        self._min_stack: list[int] = []

    def push(self, val: int) -> None:
        self._stack.append(val)
        if not self._min_stack or val <= self._min_stack[-1]:
            # ties must be pushed too, else popping one min desyncs the other
            self._min_stack.append(val)

    def pop(self) -> None:
        if not self._stack:
            msg = "pop from empty stack"
            raise IndexError(msg)
        val = self._stack.pop()
        if self._min_stack and val == self._min_stack[-1]:
            self._min_stack.pop()

    def top(self) -> int:
        if not self._stack:
            msg = "top from empty stack"
            raise IndexError(msg)
        return self._stack[-1]

    def get_min(self) -> int:
        if not self._min_stack:
            msg = "get_min from empty stack"
            raise IndexError(msg)
        return self._min_stack[-1]
