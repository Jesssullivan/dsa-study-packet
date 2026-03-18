"""Tests for the valid palindrome problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.strings.valid_palindrome import is_palindrome


class TestIsPalindrome:
    def test_basic_palindrome(self) -> None:
        assert is_palindrome("A man, a plan, a canal: Panama")

    def test_not_palindrome(self) -> None:
        assert not is_palindrome("race a car")

    def test_empty_string(self) -> None:
        assert is_palindrome("")

    def test_single_character(self) -> None:
        assert is_palindrome("a")

    def test_only_non_alnum(self) -> None:
        assert is_palindrome(",.!?@#")

    def test_numeric_palindrome(self) -> None:
        assert is_palindrome("12321")

    @given(
        s=st.text(
            alphabet=st.characters(categories=("L", "N")), min_size=1, max_size=30
        )
    )
    def test_doubled_string_is_palindrome(self, s: str) -> None:
        # s + reverse(s) is always a palindrome
        assert is_palindrome(s + s[::-1])
