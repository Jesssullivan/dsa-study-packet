"""Tests for the trapping-rain-water problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.two_pointers.trapping_rain_water import trap


class TestTrap:
    def test_basic(self) -> None:
        assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    def test_v_shape(self) -> None:
        assert trap([4, 2, 0, 3, 2, 5]) == 9

    def test_flat(self) -> None:
        assert trap([3, 3, 3]) == 0

    def test_ascending(self) -> None:
        assert trap([1, 2, 3, 4]) == 0

    def test_descending(self) -> None:
        assert trap([4, 3, 2, 1]) == 0

    def test_empty_and_short(self) -> None:
        assert trap([]) == 0
        assert trap([5]) == 0
        assert trap([3, 1]) == 0

    @given(
        data=st.lists(
            st.integers(min_value=0, max_value=50),
            min_size=0,
            max_size=50,
        ),
    )
    def test_result_matches_prefix_suffix_approach(self, data: list[int]) -> None:
        """Verify two-pointer result against the prefix/suffix max approach."""
        n = len(data)
        if n < 3:
            assert trap(data) == 0
            return

        left_max = [0] * n
        right_max = [0] * n
        left_max[0] = data[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], data[i])
        right_max[n - 1] = data[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], data[i])

        expected = sum(
            min(left_max[i], right_max[i]) - data[i] for i in range(n)
        )
        assert trap(data) == expected
