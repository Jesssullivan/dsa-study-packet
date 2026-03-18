"""Tests for edit distance."""

from hypothesis import given
from hypothesis import strategies as st

from algo.dp.edit_distance import edit_distance


class TestEditDistance:
    def test_horse_ros(self) -> None:
        assert edit_distance("horse", "ros") == 3

    def test_intention_execution(self) -> None:
        assert edit_distance("intention", "execution") == 5

    def test_identical(self) -> None:
        assert edit_distance("abc", "abc") == 0

    def test_empty_to_word(self) -> None:
        assert edit_distance("", "hello") == 5

    def test_word_to_empty(self) -> None:
        assert edit_distance("hello", "") == 5

    def test_both_empty(self) -> None:
        assert edit_distance("", "") == 0

    @given(s=st.text(alphabet="abc", min_size=0, max_size=10))
    def test_symmetric(self, s: str) -> None:
        t = s[::-1]
        assert edit_distance(s, t) == edit_distance(t, s)
