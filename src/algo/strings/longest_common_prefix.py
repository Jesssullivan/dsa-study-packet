"""Longest Common Prefix — find the longest common prefix among strings.

Problem:
    Given a list of strings, return the longest common prefix shared
    by all of them.

Approach:
    Vertical scanning: compare character-by-character across all strings.
    Use the first string as reference; stop when any string differs or
    is exhausted. Alternate longest_common_prefix_zip does the same
    columnar scan with zip() and itertools.takewhile.

When to use:
    Autocomplete, trie-based search, file path commonality. Simple but
    frequently asked.

Complexity:
    Time:  O(S) where S = sum of all string lengths
    Space: O(1) — only stores the prefix end index
"""

from collections.abc import Sequence
from itertools import takewhile


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
            if (
                i >= len(s) or s[i] != ch
            ):  # guard: reference string outran a shorter one
                return strs[0][:i]

    return strs[0]


# --- zip/takewhile columnar variant (stdlib idiom) ---
def longest_common_prefix_zip(strs: Sequence[str]) -> str:
    """Return the longest common prefix of all strings in *strs*, via zip().

    >>> longest_common_prefix_zip(["flower", "flow", "flight"])
    'fl'
    >>> longest_common_prefix_zip(["dog", "racecar", "car"])
    ''
    """
    if not strs:
        return ""

    # zip(*strs) truncates to the shortest string automatically — no explicit
    # length guard needed, unlike the vertical-scan version above
    columns = takewhile(lambda chars: len(set(chars)) == 1, zip(*strs, strict=False))
    return "".join(chars[0] for chars in columns)
