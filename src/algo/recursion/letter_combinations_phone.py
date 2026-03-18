"""Letter Combinations of a Phone Number — digit-to-letter mapping.

Problem:
    Given a string containing digits from 2-9, return all possible
    letter combinations that the number could represent on a phone keypad.

Approach:
    Recursive backtracking: map each digit to its letters, build
    combinations one digit at a time. At each level pick one letter
    for the current digit, then recurse on remaining digits.

When to use:
    Cartesian product generation, combinatorial enumeration. Similar
    structure to permutations but across different character sets.

Complexity:
    Time:  O(4^n) — where n = number of digits (worst case: 7 and 9 have 4 letters)
    Space: O(n) — recursion depth (excluding output)
"""

DIGIT_TO_LETTERS: dict[str, str] = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    """Return all letter combinations for the given phone *digits*.

    >>> letter_combinations("23")
    ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    >>> letter_combinations("")
    []
    """
    if not digits:
        return []

    result: list[str] = []

    def backtrack(index: int, current: list[str]) -> None:
        if index == len(digits):
            result.append("".join(current))
            return
        for letter in DIGIT_TO_LETTERS[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return result
