"""Tests for the string-to-integer (atoi) problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.strings.string_to_integer_atoi import INT_MAX, INT_MIN, my_atoi


class TestMyAtoi:
    def test_positive_number(self) -> None:
        assert my_atoi("42") == 42

    def test_negative_with_whitespace(self) -> None:
        assert my_atoi("   -42") == -42

    def test_trailing_non_digits(self) -> None:
        assert my_atoi("4193 with words") == 4193

    def test_overflow_positive(self) -> None:
        assert my_atoi("91283472332") == INT_MAX

    def test_overflow_negative(self) -> None:
        assert my_atoi("-91283472332") == INT_MIN

    def test_empty_string(self) -> None:
        assert my_atoi("") == 0

    def test_only_whitespace(self) -> None:
        assert my_atoi("   ") == 0

    def test_leading_non_digit(self) -> None:
        assert my_atoi("words and 987") == 0

    def test_plus_sign(self) -> None:
        assert my_atoi("+1") == 1

    @given(n=st.integers(min_value=INT_MIN, max_value=INT_MAX))
    def test_roundtrip_in_range(self, n: int) -> None:
        assert my_atoi(str(n)) == n
