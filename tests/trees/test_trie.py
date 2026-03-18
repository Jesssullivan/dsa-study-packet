"""Tests for the trie (prefix tree) implementation."""

from hypothesis import given, settings
from hypothesis import strategies as st

from algo.trees.trie import Trie


class TestInsertAndSearch:
    def test_basic_insert_and_search(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.search("apple") is True

    def test_search_missing_word(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.search("orange") is False

    def test_search_prefix_is_not_word(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.search("app") is False

    def test_empty_string(self) -> None:
        t = Trie()
        t.insert("")
        assert t.search("") is True

    def test_multiple_words(self) -> None:
        t = Trie()
        for word in ["cat", "car", "card", "care"]:
            t.insert(word)
        assert t.search("car") is True
        assert t.search("card") is True
        assert t.search("ca") is False


class TestStartsWith:
    def test_prefix_match(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.starts_with("app") is True

    def test_full_word_as_prefix(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.starts_with("apple") is True

    def test_empty_prefix_matches_any(self) -> None:
        t = Trie()
        t.insert("hello")
        assert t.starts_with("") is True

    def test_no_match(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.starts_with("xyz") is False

    def test_empty_trie(self) -> None:
        t = Trie()
        assert t.starts_with("a") is False


class TestDelete:
    def test_delete_existing_word(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.delete("apple") is True
        assert t.search("apple") is False

    def test_delete_nonexistent_word(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.delete("orange") is False

    def test_delete_prefix_of_another_word(self) -> None:
        t = Trie()
        t.insert("app")
        t.insert("apple")
        assert t.delete("app") is True
        assert t.search("app") is False
        assert t.search("apple") is True

    def test_delete_word_sharing_prefix(self) -> None:
        t = Trie()
        t.insert("app")
        t.insert("apple")
        assert t.delete("apple") is True
        assert t.search("apple") is False
        assert t.search("app") is True

    def test_delete_cleans_empty_nodes(self) -> None:
        t = Trie()
        t.insert("abc")
        t.delete("abc")
        assert not t.root.children


class TestAutocomplete:
    def test_returns_matching_words(self) -> None:
        t = Trie()
        for word in ["bat", "bar", "ball", "cat"]:
            t.insert(word)
        results = t.autocomplete("ba")
        assert sorted(results) == ["ball", "bar", "bat"]

    def test_respects_limit(self) -> None:
        t = Trie()
        for word in ["aa", "ab", "ac", "ad", "ae"]:
            t.insert(word)
        results = t.autocomplete("a", limit=3)
        assert len(results) == 3

    def test_empty_prefix_returns_all(self) -> None:
        t = Trie()
        words = ["cat", "car", "bat"]
        for word in words:
            t.insert(word)
        results = t.autocomplete("")
        assert sorted(results) == sorted(words)

    def test_no_matches(self) -> None:
        t = Trie()
        t.insert("apple")
        assert t.autocomplete("xyz") == []

    def test_exact_word_included(self) -> None:
        t = Trie()
        t.insert("app")
        t.insert("apple")
        results = t.autocomplete("app")
        assert sorted(results) == ["app", "apple"]


class TestTrieProperties:
    @given(
        words=st.lists(
            st.text(alphabet="abcdefghij", min_size=1, max_size=10),
            min_size=1,
            max_size=20,
        ),
    )
    @settings(max_examples=50)
    def test_inserted_words_are_searchable(self, words: list[str]) -> None:
        t = Trie()
        for word in words:
            t.insert(word)
        for word in words:
            assert t.search(word) is True

    @given(
        words=st.lists(
            st.text(alphabet="abc", min_size=1, max_size=6),
            min_size=1,
            max_size=15,
        ),
        query=st.text(alphabet="xyz", min_size=1, max_size=6),
    )
    @settings(max_examples=50)
    def test_non_inserted_words_not_found(
        self, words: list[str], query: str
    ) -> None:
        t = Trie()
        for word in words:
            t.insert(word)
        assert t.search(query) is False
