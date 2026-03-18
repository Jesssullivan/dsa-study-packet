"""Shortest transformation sequence from beginWord to endWord.

Problem:
    Given two words and a dictionary, find the length of the shortest
    transformation sequence from beginWord to endWord, such that only
    one letter can be changed at a time and each intermediate word
    must exist in the word list.

Approach:
    BFS level-by-level. At each level, for every word generate all
    possible one-character mutations and check if they exist in the
    remaining word set.

When to use:
    BFS for shortest transformation sequence — "minimum edits", "fewest
    steps to transform X into Y", unweighted shortest path in an implicit
    graph. Keywords: "word ladder", "gene mutation", "lock combination".

Complexity:
    Time:  O(n * m^2) where n = |word_list|, m = word length
           (m patterns per word, each pattern is O(m) to build)
    Space: O(n * m)
"""

from collections import deque


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """Return the number of words in the shortest transformation sequence.

    Returns 0 if no such sequence exists. The count includes both
    begin_word and end_word.

    >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue: deque[str] = deque([begin_word])
    visited: set[str] = {begin_word}
    level = 1

    while queue:
        for _ in range(len(queue)):
            word = queue.popleft()
            if word == end_word:
                return level
            for neighbor in _neighbors(word, word_set, visited):
                visited.add(neighbor)
                queue.append(neighbor)
        level += 1

    return 0


def _neighbors(
    word: str,
    word_set: set[str],
    visited: set[str],
) -> list[str]:
    """Generate valid one-edit neighbors of *word*."""
    result: list[str] = []
    word_arr = list(word)
    for i in range(len(word_arr)):
        original = word_arr[i]
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c == original:
                continue
            word_arr[i] = c
            candidate = "".join(word_arr)
            if candidate in word_set and candidate not in visited:
                result.append(candidate)
        word_arr[i] = original
    return result
