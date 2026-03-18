"""Tests for word ladder (BFS shortest transformation)."""

from algo.graphs.word_ladder import ladder_length


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
