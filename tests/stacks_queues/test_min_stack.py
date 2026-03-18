"""Tests for min stack."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.stacks_queues.min_stack import MinStack


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
        with pytest.raises(IndexError, match="pop from empty"):
            ms.pop()

    def test_top_empty_raises(self) -> None:
        ms = MinStack()
        with pytest.raises(IndexError, match="top from empty"):
            ms.top()

    def test_get_min_empty_raises(self) -> None:
        ms = MinStack()
        with pytest.raises(IndexError, match="get_min from empty"):
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
