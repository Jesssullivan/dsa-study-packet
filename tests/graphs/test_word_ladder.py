"""Tests for word ladder (BFS shortest transformation)."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.word_ladder import ladder_length, ladder_length_comprehension


class TestLadderLength:
    def test_basic(self) -> None:
        words = ["hot", "dot", "dog", "lot", "log", "cog"]
        assert ladder_length("hit", "cog", words) == 5

    def test_no_path(self) -> None:
        words = ["hot", "dot", "dog", "lot", "log"]
        assert ladder_length("hit", "cog", words) == 0

    def test_end_not_in_list(self) -> None:
        assert ladder_length("hit", "cog", ["hot"]) == 0

    def test_one_step(self) -> None:
        assert ladder_length("hot", "dot", ["dot"]) == 2

    def test_already_equal(self) -> None:
        assert ladder_length("abc", "abc", ["abc"]) == 1

    def test_empty_word_list(self) -> None:
        assert ladder_length("a", "b", []) == 0


class TestLadderLengthComprehensionAlt:
    @given(
        words=st.lists(
            st.text(alphabet="abc", min_size=3, max_size=3), min_size=0, max_size=10
        ),
        begin=st.text(alphabet="abc", min_size=3, max_size=3),
        end=st.text(alphabet="abc", min_size=3, max_size=3),
    )
    def test_matches_primary(self, words: list[str], begin: str, end: str) -> None:
        """The comprehension-based neighbor generator must find the same
        shortest ladder length as the index-mutation primary."""
        assert ladder_length_comprehension(begin, end, words) == ladder_length(
            begin, end, words
        )
