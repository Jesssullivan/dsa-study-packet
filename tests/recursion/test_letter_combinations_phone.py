"""Tests for the letter combinations of a phone number problem."""

import math

from hypothesis import given
from hypothesis import strategies as st

from algo.recursion.letter_combinations_phone import (
    DIGIT_TO_LETTERS,
    letter_combinations,
)


class TestLetterCombinations:
    def test_two_digits(self) -> None:
        result = letter_combinations("23")
        assert result == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]

    def test_single_digit(self) -> None:
        assert letter_combinations("2") == ["a", "b", "c"]

    def test_empty_string(self) -> None:
        assert letter_combinations("") == []

    def test_digit_with_four_letters(self) -> None:
        result = letter_combinations("7")
        assert result == ["p", "q", "r", "s"]

    def test_three_digits(self) -> None:
        result = letter_combinations("234")
        assert len(result) == 3 * 3 * 3  # 27
        assert result[0] == "adg"
        assert result[-1] == "cfi"

    @given(
        digits=st.text(
            alphabet=st.sampled_from("23456789"),
            min_size=1,
            max_size=4,
        ),
    )
    def test_result_count_is_product_of_letter_counts(self, digits: str) -> None:
        result = letter_combinations(digits)
        expected_count = math.prod(len(DIGIT_TO_LETTERS[d]) for d in digits)
        assert len(result) == expected_count
        # All results have correct length
        for combo in result:
            assert len(combo) == len(digits)
        # No duplicates
        assert len(result) == len(set(result))
