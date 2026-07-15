"""Tests for min stack."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.stacks_queues.min_stack import MinStack, MinStackTwoStacks


class TestMinStack:
    def test_basic_operations(self) -> None:
        ms = MinStack()
        ms.push(-2)
        ms.push(0)
        ms.push(-3)
        assert ms.get_min() == -3
        ms.pop()
        assert ms.top() == 0
        assert ms.get_min() == -2

    def test_single_element(self) -> None:
        ms = MinStack()
        ms.push(42)
        assert ms.top() == 42
        assert ms.get_min() == 42

    def test_ascending_pushes(self) -> None:
        ms = MinStack()
        ms.push(1)
        ms.push(2)
        ms.push(3)
        assert ms.get_min() == 1

    def test_descending_pushes(self) -> None:
        ms = MinStack()
        ms.push(3)
        ms.push(2)
        ms.push(1)
        assert ms.get_min() == 1
        ms.pop()
        assert ms.get_min() == 2

    def test_pop_empty_raises(self) -> None:
        ms = MinStack()
        with pytest.raises(IndexError):
            ms.pop()

    def test_top_empty_raises(self) -> None:
        ms = MinStack()
        with pytest.raises(IndexError):
            ms.top()

    def test_get_min_empty_raises(self) -> None:
        ms = MinStack()
        with pytest.raises(IndexError):
            ms.get_min()

    @given(
        values=st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=1,
            max_size=50,
        ),
    )
    def test_min_matches_builtin(self, values: list[int]) -> None:
        """get_min always agrees with min() of pushed values."""
        ms = MinStack()
        for v in values:
            ms.push(v)
        assert ms.get_min() == min(values)


class TestMinStackTwoStacks:
    def test_basic_operations(self) -> None:
        ms = MinStackTwoStacks()
        ms.push(-2)
        ms.push(0)
        ms.push(-3)
        assert ms.get_min() == -3
        ms.pop()
        assert ms.top() == 0
        assert ms.get_min() == -2

    def test_duplicate_min_survives_one_pop(self) -> None:
        """Ties at the minimum must be tracked so popping one doesn't lose it."""
        ms = MinStackTwoStacks()
        ms.push(1)
        ms.push(1)
        ms.pop()
        assert ms.get_min() == 1

    def test_pop_empty_raises(self) -> None:
        ms = MinStackTwoStacks()
        with pytest.raises(IndexError):
            ms.pop()

    def test_get_min_empty_raises(self) -> None:
        ms = MinStackTwoStacks()
        with pytest.raises(IndexError):
            ms.get_min()

    @given(
        values=st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=1,
            max_size=50,
        ),
    )
    def test_min_matches_builtin(self, values: list[int]) -> None:
        ms = MinStackTwoStacks()
        for v in values:
            ms.push(v)
        assert ms.get_min() == min(values)


@st.composite
def _stack_op_sequences(draw: st.DrawFn) -> list[tuple[str, int | None]]:
    """Draw a sequence of ops that never pops/reads an empty stack."""
    ops: list[tuple[str, int | None]] = []
    size = 0
    for _ in range(draw(st.integers(min_value=1, max_value=30))):
        kind = draw(st.sampled_from(["push", "pop", "top", "get_min"])) if size else "push"
        if kind == "push":
            ops.append(("push", draw(st.integers(min_value=-1000, max_value=1000))))
            size += 1
        else:
            ops.append((kind, None))
            size -= 1 if kind == "pop" else 0
    return ops


class TestMinStackCrossCheck:
    @given(ops=_stack_op_sequences())
    def test_two_stacks_matches_tuple_stack(
        self, ops: list[tuple[str, int | None]]
    ) -> None:
        """MinStackTwoStacks must agree with MinStack over any valid op sequence."""
        primary = MinStack()
        alt = MinStackTwoStacks()
        for kind, val in ops:
            if kind == "push":
                assert val is not None
                primary.push(val)
                alt.push(val)
            elif kind == "pop":
                primary.pop()
                alt.pop()
            elif kind == "top":
                assert primary.top() == alt.top()
            else:
                assert primary.get_min() == alt.get_min()
