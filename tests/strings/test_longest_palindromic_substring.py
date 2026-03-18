"""Tests for the longest palindromic substring problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.strings.longest_palindromic_substring import longest_palindromic_substring


class TestLongestPalindromicSubstring:
    def test_odd_length(self) -> None:
        result = longest_palindromic_substring("babad")
        assert result in ("bab", "aba")

    def test_even_length(self) -> None:
        assert longest_palindromic_substring("cbbd") == "bb"

    def test_single_char(self) -> None:
        assert longest_palindromic_substring("a") == "a"

    def test_empty_string(self) -> None:
        assert longest_palindromic_substring("") == ""

    def test_entire_string(self) -> None:
        assert longest_palindromic_substring("racecar") == "racecar"

    def test_no_repeats(self) -> None:
        result = longest_palindromic_substring("abcd")
        assert len(result) == 1

    @given(s=st.text(alphabet="abc", min_size=1, max_size=40))
    def test_result_is_palindrome_and_substring(self, s: str) -> None:
        result = longest_palindromic_substring(s)
        assert result in s
        assert result == result[::-1]
