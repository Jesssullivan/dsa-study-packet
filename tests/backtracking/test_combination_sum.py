"""Tests for combination sum."""

from hypothesis import given
from hypothesis import strategies as st

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

def _combos_oracle(candidates: list[int], target: int) -> set[tuple[int, ...]]:
    """Independent coins-outer DP enumerating unique sorted combinations.

    Distinct from the recursive backtracker under test: iterates candidates in
    the outer loop and sums in the inner loop (classic unbounded-knapsack
    counting), which yields each multiset exactly once.
    """
    cands = sorted(set(candidates))
    dp: list[set[tuple[int, ...]]] = [set() for _ in range(target + 1)]
    dp[0].add(())
    for c in cands:
        for s in range(c, target + 1):
            for combo in dp[s - c]:
                dp[s].add((*combo, c))
    return dp[target]

class TestCombinationSumProperties:
    @given(
        candidates=st.lists(
            st.integers(min_value=1, max_value=10),
            min_size=1,
            max_size=5,
            unique=True,
        ),
        target=st.integers(min_value=0, max_value=12),
    )
    def test_matches_dp_oracle(self, candidates: list[int], target: int) -> None:
        result = combination_sum(candidates, target)
        got = {tuple(combo) for combo in result}

        # no duplicate combinations are returned
        assert len(got) == len(result)

        allowed = set(candidates)
        for combo in result:
            assert sum(combo) == target
            assert all(x in allowed for x in combo)
            assert list(combo) == sorted(combo)

        # exact agreement with the independent oracle
        assert got == _combos_oracle(candidates, target)
