"""Tests for combination sum."""

from algo.backtracking.combination_sum import combination_sum


class TestCombinationSum:
    def test_basic(self) -> None:
        result = combination_sum([2, 3, 6, 7], 7)
        assert sorted(result) == [[2, 2, 3], [7]]

    def test_single_candidate(self) -> None:
        result = combination_sum([2], 4)
        assert result == [[2, 2]]

    def test_no_solution(self) -> None:
        assert combination_sum([3], 2) == []

    def test_target_zero(self) -> None:
        result = combination_sum([1, 2], 0)
        assert result == [[]]

    def test_multiple_combinations(self) -> None:
        result = combination_sum([2, 3, 5], 8)
        expected = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
        assert sorted(result) == sorted(expected)

    def test_all_sums_match_target(self) -> None:
        result = combination_sum([1, 2, 3], 5)
        for combo in result:
            assert sum(combo) == 5
