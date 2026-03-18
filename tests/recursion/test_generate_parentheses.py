"""Tests for the generate parentheses problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.recursion.generate_parentheses import generate_parentheses


def _is_valid_parentheses(s: str) -> bool:
    """Check if a parentheses string is balanced."""
    balance = 0
    for ch in s:
        if ch == "(":
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0


# Catalan numbers for n = 0..6
_CATALAN = [1, 1, 2, 5, 14, 42, 132]


class TestGenerateParentheses:
    def test_one_pair(self) -> None:
        assert generate_parentheses(1) == ["()"]

    def test_two_pairs(self) -> None:
        assert sorted(generate_parentheses(2)) == ["(())", "()()"]

    def test_three_pairs(self) -> None:
        result = sorted(generate_parentheses(3))
        assert result == ["((()))", "(()())", "(())()", "()(())", "()()()"]

    def test_zero_pairs(self) -> None:
        assert generate_parentheses(0) == []

    def test_count_matches_catalan(self) -> None:
        for n in range(1, 6):
            assert len(generate_parentheses(n)) == _CATALAN[n]

    @given(n=st.integers(min_value=1, max_value=5))
    def test_all_results_are_valid(self, n: int) -> None:
        results = generate_parentheses(n)
        for s in results:
            assert len(s) == 2 * n
            assert _is_valid_parentheses(s)
        # No duplicates
        assert len(results) == len(set(results))
