"""Valid Anagram — check if two strings are anagrams of each other.

Problem:
    Given two strings, determine if one is an anagram of the other
    (same characters, same frequencies, different order allowed).

Approach:
    Counter comparison — count character frequencies for both strings
    and check equality.

When to use:
    Equivalence class membership — same chars different order. Group
    anagrams builds on this. Also: frequency matching, permutation
    checking.

Complexity:
    Time:  O(n) with Counter, O(n log n) with sort
    Space: O(1) — bounded by alphabet size (26 for lowercase English)
"""

from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    """Return True if *s* and *t* are anagrams of each other.

    >>> is_anagram("anagram", "nagaram")
    True
    >>> is_anagram("rat", "car")
    False
    """
    return Counter(s) == Counter(t)
