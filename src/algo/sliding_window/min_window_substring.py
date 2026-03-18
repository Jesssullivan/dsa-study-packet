"""Minimum window substring.

Problem:
    Given strings s and t, find the minimum window substring of s
    that contains all characters of t (including duplicates).
    Return "" if no such window exists.

Approach:
    Variable-size sliding window with Counter for "need" and "have"
    tracking. Expand the right pointer to include characters, shrink
    the left pointer to minimize the window once all characters are
    satisfied.

When to use:
    Minimum window containing all required elements — "smallest substring
    with all chars", "shortest subarray covering set". Expand right to
    satisfy, shrink left to minimize. Streaming log/event filtering.

Complexity:
    Time:  O(n) where n = len(s) -- each character visited at most twice
    Space: O(k) where k = number of unique characters in t
"""

from collections import Counter


def min_window(s: str, t: str) -> str:
    """Return the minimum window in *s* that contains all chars of *t*.

    >>> min_window("ADOBECODEBANC", "ABC")
    'BANC'
    >>> min_window("a", "a")
    'a'
    >>> min_window("a", "aa")
    ''
    """
    if not t or not s:
        return ""

    need: Counter[str] = Counter(t)
    missing = len(t)
    left = start = end = 0

    for right, ch in enumerate(s, 1):  # right is 1-indexed
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        if missing == 0:
            # Shrink from left while window stays valid
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1

            if not end or right - left < end - start:
                start, end = left, right

            # Invalidate window to search for smaller ones
            need[s[left]] += 1
            missing += 1
            left += 1

    return s[start:end]
