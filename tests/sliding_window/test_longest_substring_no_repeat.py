"""Tests for longest substring without repeating characters."""

from hypothesis import given
from hypothesis import strategies as st

from algo.sliding_window.longest_substring_no_repeat import (
    length_of_longest_substring,
)


class TestLongestSubstringNoRepeat:
    def test_basic(self) -> None:
        assert length_of_longest_substring("abcabcbb") == 3

    def test_all_same(self) -> None:
        assert length_of_longest_substring("bbbbb") == 1

    def test_mixed(self) -> None:
        assert length_of_longest_substring("pwwkew") == 3

    def test_empty_string(self) -> None:
        assert length_of_longest_substring("") == 0

    def test_single_char(self) -> None:
        assert length_of_longest_substring("z") == 1

    def test_all_unique(self) -> None:
        assert length_of_longest_substring("abcdef") == 6

    @given(
        s=st.text(
            alphabet=st.sampled_from("abcde"),
            min_size=1,
            max_size=50,
        ),
    )
    def test_result_bounded_by_unique_chars(self, s: str) -> None:
        """Result cannot exceed the number of unique characters in s."""
        result = length_of_longest_substring(s)
        assert 1 <= result <= len(set(s))

    @given(
        s=st.text(
            alphabet=st.sampled_from("abcde"),
            min_size=1,
            max_size=50,
        ),
    )
    def test_matches_brute_force(self, s: str) -> None:
        """Cross-check against O(n^2) brute force."""
        expected = 0
        for i in range(len(s)):
            seen: set[str] = set()
            for j in range(i, len(s)):
                if s[j] in seen:
                    break
                seen.add(s[j])
            expected = max(expected, len(seen))
        assert length_of_longest_substring(s) == expected
