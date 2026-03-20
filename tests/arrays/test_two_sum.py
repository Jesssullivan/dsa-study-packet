"""Tests for the two-sum problem."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.arrays.two_sum import two_sum


class TestTwoSum:
    def test_basic(self) -> None:
        assert two_sum([2, 7, 11, 15], 9) == (0, 1)

    def test_target_at_end(self) -> None:
        assert two_sum([3, 2, 4], 6) == (1, 2)

    def test_negative_numbers(self) -> None:
        assert two_sum([-3, 4, 3, 90], 0) == (0, 2)

    def test_same_value_twice(self) -> None:
        assert two_sum([3, 3], 6) == (0, 1)

    def test_large_target(self) -> None:
        assert two_sum([1, 5, 100, 200], 300) == (2, 3)

    def test_no_solution_raises(self) -> None:
        with pytest.raises(ValueError):
            two_sum([1, 2, 3], 100)

    @given(
        data=st.lists(
            st.integers(min_value=-500, max_value=500),
            min_size=2,
            max_size=50,
            unique=True,
        ),
    )
    def test_returned_indices_sum_to_target(self, data: list[int]) -> None:
        target = data[0] + data[1]
        i, j = two_sum(data, target)
        assert i != j
        assert data[i] + data[j] == target
