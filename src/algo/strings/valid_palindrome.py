"""Valid Palindrome — check if string is a palindrome ignoring non-alnum and case.

Problem:
    Given a string, determine if it is a palindrome considering only
    alphanumeric characters and ignoring case.

Approach:
    Two pointers from both ends. Skip non-alphanumeric characters.
    Compare lowercase characters at each pointer position. Alternate
    is_palindrome_filtered builds a cleaned list via a comprehension
    and compares it to its reverse.

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
        # both skip-loops re-check left < right — otherwise an all-non-alnum
        # tail could walk a pointer past the other and misread the string
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# --- filter + reverse comprehension variant (O(n) space, stdlib idiom) ---
def is_palindrome_filtered(s: str) -> bool:
    """Return True if *s* is a palindrome, via a filtered comprehension.

    >>> is_palindrome_filtered("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome_filtered("race a car")
    False
    """
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
