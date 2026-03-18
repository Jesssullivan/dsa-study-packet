"""Tests for the group-anagrams problem."""

from algo.arrays.group_anagrams import group_anagrams


def _normalize(groups: list[list[str]]) -> list[list[str]]:
    """Sort each group and sort groups for order-independent comparison."""
    return sorted(sorted(g) for g in groups)


class TestGroupAnagrams:
    def test_basic(self) -> None:
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        assert _normalize(result) == [
            ["ate", "eat", "tea"],
            ["bat"],
            ["nat", "tan"],
        ]

    def test_empty_input(self) -> None:
        assert group_anagrams([]) == []

    def test_single_string(self) -> None:
        assert group_anagrams(["a"]) == [["a"]]

    def test_all_same_anagram(self) -> None:
        result = group_anagrams(["abc", "bca", "cab"])
        assert _normalize(result) == [["abc", "bca", "cab"]]

    def test_no_anagrams(self) -> None:
        result = group_anagrams(["a", "b", "c"])
        assert _normalize(result) == [["a"], ["b"], ["c"]]

    def test_empty_strings(self) -> None:
        result = group_anagrams(["", ""])
        assert _normalize(result) == [["", ""]]
