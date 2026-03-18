"""Tests for valid parentheses."""

from hypothesis import given
from hypothesis import strategies as st

from algo.stacks_queues.valid_parentheses import is_valid


class TestIsValid:
    def test_simple_valid(self) -> None:
        assert is_valid("()") is True

    def test_multiple_types(self) -> None:
        assert is_valid("()[]{}") is True

    def test_mismatched(self) -> None:
        assert is_valid("(]") is False

    def test_interleaved_invalid(self) -> None:
        assert is_valid("([)]") is False

    def test_nested_valid(self) -> None:
        assert is_valid("{[()]}") is True

    def test_empty_string(self) -> None:
        assert is_valid("") is True

    def test_single_opener(self) -> None:
        assert is_valid("(") is False

    def test_single_closer(self) -> None:
        assert is_valid(")") is False

    @given(
        n=st.integers(min_value=1, max_value=20),
    )
    def test_repeated_pairs_always_valid(self, n: int) -> None:
        """A string of repeated '()' pairs is always valid."""
        assert is_valid("()" * n) is True

    @given(
        n=st.integers(min_value=1, max_value=20),
    )
    def test_nested_parens_always_valid(self, n: int) -> None:
        """Deeply nested parentheses are valid."""
        assert is_valid("(" * n + ")" * n) is True
