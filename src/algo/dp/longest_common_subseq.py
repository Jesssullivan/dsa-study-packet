"""Longest Common Subsequence — length of LCS of two strings.

Problem:
    Given two strings, return the length of their longest common
    subsequence. A subsequence is a sequence derived by deleting some
    (or no) characters without changing the relative order.

Approach:
    2D DP. If characters match, extend the diagonal; otherwise take
    the max of skipping one character from either string.
    Space-optimized to a single row.

When to use:
    Diff / alignment — "longest common subsequence", "diff two files",
    DNA sequence alignment. Foundation for unified-diff algorithms.
    See also: edit_distance for minimum-cost transformation.

Complexity:
    Time:  O(m * n)
    Space: O(min(m, n))
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Return the length of the LCS of *text1* and *text2*.

    >>> longest_common_subsequence("abcde", "ace")
    3
    >>> longest_common_subsequence("abc", "def")
    0
    """
    # Ensure text2 is the shorter string for O(min(m,n)) space
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i - 1] == text2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    return dp[n]
