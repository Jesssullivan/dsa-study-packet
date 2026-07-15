"""Tests for the valid anagram problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.strings.valid_anagram import is_anagram, is_anagram_sorted


class TestIsAnagram:
    def test_basic_anagram(self) -> None:
        assert is_anagram("anagram", "nagaram")

    def test_not_anagram(self) -> None:
        assert not is_anagram("rat", "car")

    def test_empty_strings(self) -> None:
        assert is_anagram("", "")

    def test_different_lengths(self) -> None:
        assert not is_anagram("ab", "abc")

    def test_same_chars_different_counts(self) -> None:
        assert not is_anagram("aab", "abb")

    def test_single_char(self) -> None:
        assert is_anagram("a", "a")

    @given(s=st.text(alphabet="abcdef", min_size=0, max_size=30))
    def test_shuffled_string_is_anagram(self, s: str) -> None:
        # any permutation of s is an anagram of s
        import random

        shuffled = list(s)
        random.shuffle(shuffled)
        assert is_anagram(s, "".join(shuffled))


class TestIsAnagramSorted:
    """Cross-check the sort-based alternate against the primary implementation."""

    @given(
        s=st.text(alphabet="abcdef", min_size=0, max_size=20),
        t=st.text(alphabet="abcdef", min_size=0, max_size=20),
    )
    def test_matches_primary(self, s: str, t: str) -> None:
        assert is_anagram_sorted(s, t) == is_anagram(s, t)
