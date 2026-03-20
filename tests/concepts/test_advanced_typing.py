"""Tests for modern type-system demonstrations.

Each test class targets one section of ``concepts.advanced_typing``
and verifies the runtime behaviour that the type annotations describe.
"""

import pytest

from concepts.advanced_typing import (
    Circle,
    Container,
    Drawable,
    Stack,
    add_logging,
    is_str_list,
    process,
    render,
)

# --------------------------------------------------------------------------- #
# Protocol
# --------------------------------------------------------------------------- #


class TestProtocol:
    """Structural subtyping via ``Drawable`` protocol."""

    def test_circle_is_drawable_instance(self) -> None:
        """``@runtime_checkable`` enables isinstance checks."""
        c = Circle(5.0)
        assert isinstance(c, Drawable)

    def test_render_returns_draw_output(self) -> None:
        c = Circle(3.0)
        assert render(c) == "Circle(radius=3.0)"

    def test_non_drawable_fails_isinstance(self) -> None:
        """An object without a ``.draw()`` method is not Drawable."""
        assert not isinstance("just a string", Drawable)


# --------------------------------------------------------------------------- #
# Container (TypeVar with default / PEP 695 generics)
# --------------------------------------------------------------------------- #


class TestContainer:
    """Generic container with ``.transform()``."""

    def test_stores_value(self) -> None:
        c = Container(42)
        assert c.value == 42

    def test_transform_applies_function(self) -> None:
        c = Container(10)
        result = c.transform(lambda x: x * 3)
        assert result.value == 30

    def test_transform_changes_type(self) -> None:
        """transform can map Container[int] -> Container[str]."""
        c = Container(42)
        result = c.transform(str)
        assert result.value == "42"
        assert isinstance(result.value, str)

    def test_repr(self) -> None:
        assert repr(Container("hi")) == "Container('hi')"


# --------------------------------------------------------------------------- #
# Logging decorator with ParamSpec and Concatenate
# --------------------------------------------------------------------------- #


class TestAddLogging:
    """Decorator that prepends a ``verbose`` parameter."""

    def test_function_behavior_preserved(self) -> None:
        @add_logging
        def add(a: int, b: int) -> int:
            return a + b

        # verbose=False — just runs the function.
        assert add(False, 3, 4) == 7

    def test_verbose_flag_records_call(self) -> None:
        @add_logging
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(True, 6, 7)
        assert result == 42
        # The wrapper records log messages in ``._calls``.
        assert len(multiply._calls) == 1  # type: ignore[attr-defined]
        assert "multiply" in multiply._calls[0]  # type: ignore[attr-defined]

    def test_non_verbose_does_not_log(self) -> None:
        @add_logging
        def noop() -> None:
            pass

        noop(False)
        assert len(noop._calls) == 0  # type: ignore[attr-defined]


# --------------------------------------------------------------------------- #
# TypeGuard
# --------------------------------------------------------------------------- #


class TestTypeGuard:
    """``is_str_list`` narrows ``list[object]`` to ``list[str]``."""

    def test_all_strings(self) -> None:
        assert is_str_list(["a", "b", "c"]) is True

    def test_mixed_list_returns_false(self) -> None:
        assert is_str_list(["a", 1, "b"]) is False

    def test_empty_list_is_str_list(self) -> None:
        assert is_str_list([]) is True

    def test_no_strings_returns_false(self) -> None:
        assert is_str_list([1, 2, 3]) is False


# --------------------------------------------------------------------------- #
# @overload
# --------------------------------------------------------------------------- #


class TestOverload:
    """``process`` dispatches on input type."""

    def test_int_returns_doubled_int(self) -> None:
        assert process(5) == 10

    def test_str_returns_char_list(self) -> None:
        assert process("hi") == ["h", "i"]

    def test_int_type(self) -> None:
        result = process(3)
        assert isinstance(result, int)

    def test_str_type(self) -> None:
        result = process("abc")
        assert isinstance(result, list)


# --------------------------------------------------------------------------- #
# Generic LIFO stack
# --------------------------------------------------------------------------- #


class TestStack:
    """Generic LIFO stack."""

    def test_push_and_pop(self) -> None:
        s: Stack[int] = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek_returns_top(self) -> None:
        s: Stack[str] = Stack()
        s.push("a")
        s.push("b")
        assert s.peek() == "b"
        # peek does NOT remove the element.
        assert len(s) == 2

    def test_is_empty(self) -> None:
        s: Stack[int] = Stack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()

    def test_pop_empty_raises(self) -> None:
        s: Stack[int] = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_peek_empty_raises(self) -> None:
        s: Stack[int] = Stack()
        with pytest.raises(IndexError):
            s.peek()

    def test_lifo_order(self) -> None:
        s: Stack[int] = Stack()
        for i in range(5):
            s.push(i)
        popped = [s.pop() for _ in range(5)]
        assert popped == [4, 3, 2, 1, 0]
