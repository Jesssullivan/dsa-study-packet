"""Valid Palindrome — check if string is a palindrome ignoring non-alnum and case.

Problem:
    Given a string, determine if it is a palindrome considering only
    alphanumeric characters and ignoring case.

Approach:
    Two pointers from both ends. Skip non-alphanumeric characters.
    Compare lowercase characters at each pointer position.

When to use:
    String validity checks, symmetry problems. Foundation for palindrome
    family (longest palindromic substring, palindrome partitioning).

Complexity:
    Time:  O(n)
    Space: O(1)
"""


def is_palindrome(s: str) -> bool:
    """Return True if *s* is a palindrome (alphanumeric only, case-insensitive).

    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("race a car")
    False
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
