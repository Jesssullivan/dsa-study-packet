"""Tests for the group-anagrams problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.arrays.group_anagrams import group_anagrams, group_anagrams_countkey


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

    @given(
        strs=st.lists(
            st.text(alphabet="abc", min_size=0, max_size=8),
            min_size=0,
            max_size=20,
        ),
    )
    def test_every_input_string_appears_exactly_once(self, strs: list[str]) -> None:
        result = group_anagrams(strs)
        flattened = [s for group in result for s in group]
        assert sorted(flattened) == sorted(strs)


class TestGroupAnagramsCountkey:
    """Cross-check the count-key alternate against the primary implementation."""

    @given(
        strs=st.lists(
            st.text(alphabet="abc", min_size=0, max_size=8),
            min_size=0,
            max_size=20,
        ),
    )
    def test_matches_primary(self, strs: list[str]) -> None:
        assert _normalize(group_anagrams_countkey(strs)) == _normalize(
            group_anagrams(strs)
        )
