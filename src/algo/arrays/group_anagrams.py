"""Group Anagrams — group strings that are anagrams of each other.

Problem:
    Given a list of strings, group the anagrams together. An anagram is a
    word formed by rearranging the letters of another.

Approach:
    Use the sorted characters of each string as a hash key.
    All anagrams produce the same sorted tuple, so they land in the
    same bucket in a defaultdict. Alternate group_anagrams_countkey
    keys on a 26-length character-count vector instead of sorting,
    trading the sort for a fixed-size linear scan.

When to use:
    Grouping items by equivalence class — anagrams, isomorphic strings, etc.
    Keywords: "group by", "categorize", "bucket by canonical form".

Complexity:
    Time:  O(n * k log k)  where n = number of strings, k = max string length
    Space: O(n * k)
"""

from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Return groups of anagram strings.

    >>> sorted(
    ...     sorted(g)
    ...     for g in group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    ... )
    [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
    """
    groups: defaultdict[tuple[str, ...], list[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # tuple, not list — the key must be hashable
        groups[key].append(s)
    return list(groups.values())


# --- character-count key variant (avoids sorting each string) ---
def group_anagrams_countkey(strs: list[str]) -> list[list[str]]:
    """Group anagrams using a 26-length lowercase character-count vector.

    Assumes lowercase a-z input (as is typical for this problem). Trades
    the O(k log k) sort for an O(k) count pass per string.

    >>> sorted(
    ...     sorted(g)
    ...     for g in group_anagrams_countkey(["eat", "tea", "tan", "ate", "nat", "bat"])
    ... )
    [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
    """
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord("a")] += 1  # counts as key sidesteps the sort entirely
        groups[tuple(counts)].append(s)
    return list(groups.values())
