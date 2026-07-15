"""Edit Distance — minimum operations to convert word1 to word2.

Problem:
    Given two strings, return the minimum number of single-character
    operations (insert, delete, replace) to convert word1 into word2.

Approach:
    2D DP where ``dp[i][j]`` is the edit distance between the first i
    characters of word1 and the first j characters of word2.
    edit_distance space-optimizes this to a single rolling row since
    each cell only depends on the current and previous row; the
    edit_distance_2d alternate keeps the full table for clarity.

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
            # save the pre-overwrite value: it's dp[i-1][j-1] (diagonal) for
            # the *next* j, since dp[j] is about to become dp[i][j]
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp

    return dp[n]


# --- full 2D table alternate (explicit rows, no rolling overwrite) ---
def edit_distance_2d(word1: str, word2: str) -> int:
    """Return the minimum edit distance using the full 2D DP table.

    >>> edit_distance_2d("horse", "ros")
    3
    >>> edit_distance_2d("intention", "execution")
    5
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
