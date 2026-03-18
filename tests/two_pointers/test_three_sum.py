"""Tests for the 3Sum problem."""

from algo.two_pointers.three_sum import three_sum


class TestThreeSum:
    def test_basic(self) -> None:
        assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]

    def test_all_zeros(self) -> None:
        assert three_sum([0, 0, 0]) == [[0, 0, 0]]

    def test_no_solution(self) -> None:
        assert three_sum([1, 2, 3]) == []

    def test_empty(self) -> None:
        assert three_sum([]) == []

    def test_duplicates_skipped(self) -> None:
        result = three_sum([-2, 0, 0, 2, 2])
        assert result == [[-2, 0, 2]]

    def test_multiple_triplets(self) -> None:
        result = three_sum([-1, 0, 1, 2, -1, -4, -2, -3, 3, 0, 4])
        # All triplets should sum to zero and be unique
        seen: set[tuple[int, ...]] = set()
        for triplet in result:
            assert sum(triplet) == 0
            key = tuple(triplet)
            assert key not in seen
            seen.add(key)
