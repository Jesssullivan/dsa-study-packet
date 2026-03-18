"""Longest Palindromic Substring — find the longest palindromic substring.

Problem:
    Given a string, return the longest substring that is a palindrome.

Approach:
    Expand around center for each position. Try both odd-length (single
    center) and even-length (two-char center) expansions. Track the best
    start and length.

When to use:
    Substring search with symmetry constraint. Related to Manacher's
    algorithm for O(n).

Complexity:
    Time:  O(n²)
    Space: O(1)
"""


def longest_palindromic_substring(s: str) -> str:
    """Return the longest palindromic substring of *s*.

    >>> longest_palindromic_substring("babad") in ("bab", "aba")
    True
    >>> longest_palindromic_substring("cbbd")
    'bb'
    """
    if len(s) < 2:
        return s

    start = 0
    max_len = 1

    def _expand(left: int, right: int) -> None:
        nonlocal start, max_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        length = right - left - 1
        if length > max_len:
            start = left + 1
            max_len = length

    for i in range(len(s)):
        _expand(i, i)  # odd length
        _expand(i, i + 1)  # even length

    return s[start : start + max_len]
