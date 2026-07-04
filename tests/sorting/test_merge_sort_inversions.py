"""Tests for merge sort inversions."""

from hypothesis import given
from hypothesis import strategies as st

from algo.sorting.merge_sort_inversions import count_inversions


class TestCountInversions:
    def test_basic(self) -> None:
        assert count_inversions([2, 4, 1, 3, 5]) == 3

    def test_sorted_array(self) -> None:
        assert count_inversions([1, 2, 3, 4, 5]) == 0

    def test_reverse_sorted(self) -> None:
        assert count_inversions([5, 4, 3, 2, 1]) == 10

    def test_single_element(self) -> None:
        assert count_inversions([1]) == 0

    def test_empty(self) -> None:
        assert count_inversions([]) == 0

    def test_two_elements_inverted(self) -> None:
        assert count_inversions([2, 1]) == 1

    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100), min_size=0, max_size=50
        ),
    )
    def test_matches_brute_force(self, data: list[int]) -> None:
        expected = sum(
            1
            for i in range(len(data))
            for j in range(i + 1, len(data))
            if data[i] > data[j]
        )
        assert count_inversions(data) == expected


def _inversions_via_bubble_sort(nums: list[int]) -> int:
    """Independent oracle: inversion count equals adjacent swaps in bubble sort."""
    arr = list(nums)
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
    return swaps


@given(
    data=st.lists(st.integers(min_value=-50, max_value=50), min_size=0, max_size=30),
)
def test_inversions_match_bubble_sort_swaps(data: list[int]) -> None:
    """Inversion count equals the number of adjacent swaps bubble sort performs."""
    assert count_inversions(data) == _inversions_via_bubble_sort(data)


@given(
    data=st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=0,
        max_size=30,
        unique=True,
    ),
)
def test_inversions_reversal_complement_unique(data: list[int]) -> None:
    """For distinct values, inv(xs) + inv(reversed xs) == C(n, 2)."""
    n = len(data)
    assert (
        count_inversions(data) + count_inversions(list(reversed(data)))
        == n * (n - 1) // 2
    )
