"""Edit Distance — minimum operations to convert word1 to word2.

Problem:
    Given two strings, return the minimum number of single-character
    operations (insert, delete, replace) to convert word1 into word2.

Approach:
    2D DP where dp[i][j] is the edit distance between the first i
    characters of word1 and the first j characters of word2.
    Space-optimized to a single row since each cell only depends on
    the current and previous row.

When to use:
    String similarity / diff algorithms — "minimum edits", "Levenshtein
    distance", spell checking, DNA sequence alignment. Foundation for
    fuzzy matching and diff tools. See also: longest_common_subseq.

Complexity:
    Time:  O(m * n)
    Space: O(n)  (space-optimized)
"""


def edit_distance(word1: str, word2: str) -> int:
    """Return the minimum edit distance between *word1* and *word2*.

    >>> edit_distance("horse", "ros")
    3
    >>> edit_distance("intention", "execution")
    5
    """
    m, n = len(word1), len(word2)

    # dp[j] represents the distance for word2[:j]
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp

    return dp[n]
