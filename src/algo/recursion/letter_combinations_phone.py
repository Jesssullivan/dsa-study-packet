"""Letter Combinations of a Phone Number — digit-to-letter mapping.

Problem:
    Given a string containing digits from 2-9, return all possible
    letter combinations that the number could represent on a phone keypad.

Approach:
    letter_combinations: recursive backtracking that maps each digit to
    its letters and builds combinations one digit at a time, picking one
    letter per level then recursing on the rest. letter_combinations_itertools
    is the stdlib alternate using itertools.product over each digit's letters.

When to use:
    Cartesian product generation, combinatorial enumeration. Similar
    structure to permutations but across different character sets.

Complexity:
    Time:  O(4^n) — where n = number of digits (worst case: 7 and 9 have 4 letters)
    Space: O(n) — recursion depth (excluding output)
"""

import itertools

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
        # digits are assumed 2-9 (problem constraint) -- 0/1 aren't mapped
        for letter in DIGIT_TO_LETTERS[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])
    return result


# --- stdlib alternate: itertools.product over each digit's letters ---
def letter_combinations_itertools(digits: str) -> list[str]:
    """Return all letter combinations for the given phone *digits*.

    >>> letter_combinations_itertools("23")
    ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    >>> letter_combinations_itertools("")
    []
    """
    if not digits:
        return []

    letter_groups = (DIGIT_TO_LETTERS[d] for d in digits)
    return ["".join(combo) for combo in itertools.product(*letter_groups)]
