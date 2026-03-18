"""Group Anagrams — group strings that are anagrams of each other.

Problem:
    Given a list of strings, group the anagrams together. An anagram is a
    word formed by rearranging the letters of another.

Approach:
    Use the sorted characters of each string as a hash key.
    All anagrams produce the same sorted tuple, so they land in the
    same bucket in a defaultdict.

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
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
