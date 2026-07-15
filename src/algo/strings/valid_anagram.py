"""Valid Anagram — check if two strings are anagrams of each other.

Problem:
    Given two strings, determine if one is an anagram of the other
    (same characters, same frequencies, different order allowed).

Approach:
    Counter comparison — count character frequencies for both strings
    and check equality. Alternate is_anagram_sorted compares the two
    strings sorted instead.

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
    # Counter equality also fails on unequal length — no separate len check needed
    return Counter(s) == Counter(t)


# --- sort-and-compare variant (O(n log n), no extra structures) ---
def is_anagram_sorted(s: str, t: str) -> bool:
    """Return True if *s* and *t* are anagrams of each other, via sorting.

    >>> is_anagram_sorted("anagram", "nagaram")
    True
    >>> is_anagram_sorted("rat", "car")
    False
    """
    return sorted(s) == sorted(t)
