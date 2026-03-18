"""Longest Common Prefix — find the longest common prefix among strings.

Problem:
    Given a list of strings, return the longest common prefix shared
    by all of them.

Approach:
    Vertical scanning: compare character-by-character across all strings.
    Use the first string as reference; stop when any string differs or
    is exhausted.

When to use:
    Autocomplete, trie-based search, file path commonality. Simple but
    frequently asked.

Complexity:
    Time:  O(S) where S = sum of all string lengths
    Space: O(1) — only stores the prefix end index
"""

from collections.abc import Sequence


def longest_common_prefix(strs: Sequence[str]) -> str:
    """Return the longest common prefix of all strings in *strs*.

    >>> longest_common_prefix(["flower", "flow", "flight"])
    'fl'
    >>> longest_common_prefix(["dog", "racecar", "car"])
    ''
    """
    if not strs:
        return ""

    for i, ch in enumerate(strs[0]):
        for s in strs[1:]:
            if i >= len(s) or s[i] != ch:
                return strs[0][:i]

    return strs[0]
