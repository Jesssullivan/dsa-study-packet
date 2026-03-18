"""Longest substring without repeating characters.

Problem:
    Given a string s, find the length of the longest substring
    without repeating characters.

Approach:
    Sliding window with a dict tracking the last-seen index of each
    character. When a duplicate is found within the current window,
    jump the left pointer past the previous occurrence.

When to use:
    Longest valid window — "longest substring/subarray without repeats",
    "maximum window satisfying constraint". Expand right, contract left
    only when the window becomes invalid. Streaming uniqueness checks.

Complexity:
    Time:  O(n) -- single pass through the string
    Space: O(min(n, alphabet_size)) for the last-seen dict
"""


def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring with no repeating chars.

    >>> length_of_longest_substring("abcabcbb")
    3
    >>> length_of_longest_substring("bbbbb")
    1
    >>> length_of_longest_substring("")
    0
    """
    seen: dict[str, int] = {}
    left = best = 0

    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)

    return best
