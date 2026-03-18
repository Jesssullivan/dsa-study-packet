"""Tests for minimum window substring."""

from hypothesis import given
from hypothesis import strategies as st

from algo.sliding_window.min_window_substring import min_window


class TestMinWindow:
    def test_basic(self) -> None:
        assert min_window("ADOBECODEBANC", "ABC") == "BANC"

    def test_single_char_match(self) -> None:
        assert min_window("a", "a") == "a"

    def test_t_longer_than_s(self) -> None:
        assert min_window("a", "aa") == ""

    def test_empty_s(self) -> None:
        assert min_window("", "ABC") == ""

    def test_empty_t(self) -> None:
        assert min_window("ABC", "") == ""

    def test_entire_string_is_window(self) -> None:
        assert min_window("abc", "abc") == "abc"

    def test_duplicate_chars_in_t(self) -> None:
        assert min_window("aabbc", "abc") == "abbc"

    def test_window_at_end(self) -> None:
        assert min_window("xxxxxABC", "ABC") == "ABC"

    @given(
        t=st.text(
            alphabet=st.sampled_from("abc"),
            min_size=1,
            max_size=5,
        ),
    )
    def test_result_contains_all_t_chars(self, t: str) -> None:
        """Any non-empty result must contain all characters of t."""
        from collections import Counter

        s = "aabbccabc"
        result = min_window(s, t)
        if result:
            result_counts = Counter(result)
            for ch, cnt in Counter(t).items():
                assert result_counts[ch] >= cnt
