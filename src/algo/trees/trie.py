"""Trie (prefix tree) for efficient string operations.

Problem:
    Implement a prefix tree that supports insert, search, prefix matching,
    delete, and autocomplete operations on a set of strings.

Approach:
    A tree where each node represents a character. Paths from the root to
    nodes marked as word-endings form the stored words. Children are stored
    in a dict keyed by character for O(1) branching.

When to use:
    Autocomplete, spell checking, IP routing, prefix matching. Mission-systems relevance:
    airport code lookup (e.g., "BO" -> ["BOS", "BOI", "BOG"]), flight ID
    prefix search, geospatial name indexing.

Complexity:
    Time:  O(m) per insert/search/starts_with/delete where m = word length.
           O(p + k) for autocomplete where p = prefix length, k = total
           characters in matching subtree.
    Space: O(N * m) where N = number of words, m = average word length.
"""

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    children: dict[str, TrieNode] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    """Prefix tree supporting insert, search, prefix matching, and autocomplete.

    >>> t = Trie()
    >>> t.insert("apple")
    >>> t.search("apple")
    True
    >>> t.starts_with("app")
    True
    >>> t.search("app")
    False
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie.

        >>> t = Trie()
        >>> t.insert("cat")
        >>> t.search("cat")
        True
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if the exact word exists in the trie.

        >>> t = Trie()
        >>> t.insert("hello")
        >>> t.search("hello")
        True
        >>> t.search("hell")
        False
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with the given prefix.

        >>> t = Trie()
        >>> t.insert("hello")
        >>> t.starts_with("hel")
        True
        >>> t.starts_with("xyz")
        False
        """
        return self._find_node(prefix) is not None

    def delete(self, word: str) -> bool:
        """Remove a word from the trie, cleaning up empty nodes.

        Returns True if the word was found and deleted, False otherwise.

        >>> t = Trie()
        >>> t.insert("cat")
        >>> t.delete("cat")
        True
        >>> t.search("cat")
        False
        """
        return self._delete(self.root, word, 0)

    def autocomplete(self, prefix: str, limit: int = 10) -> list[str]:
        """Return up to `limit` words starting with the given prefix.

        >>> t = Trie()
        >>> for w in ["bar", "bat", "ball"]:
        ...     t.insert(w)
        >>> sorted(t.autocomplete("ba"))
        ['ball', 'bar', 'bat']
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        results: list[str] = []
        self._collect(node, prefix, limit, results)
        return results

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Traverse the trie following the prefix, returning the final node."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _delete(self, node: TrieNode, word: str, depth: int) -> bool:
        """Recursively delete a word and prune empty branches."""
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return True

        ch = word[depth]
        if ch not in node.children:
            return False

        deleted = self._delete(node.children[ch], word, depth + 1)
        if deleted:
            child = node.children[ch]
            if not child.is_end and not child.children:
                del node.children[ch]
        return deleted

    def _collect(
        self,
        node: TrieNode,
        prefix: str,
        limit: int,
        results: list[str],
    ) -> None:
        """DFS to collect words under a node up to the limit."""
        if len(results) >= limit:
            return
        if node.is_end:
            results.append(prefix)
        for ch in sorted(node.children):
            if len(results) >= limit:
                return
            self._collect(node.children[ch], prefix + ch, limit, results)
