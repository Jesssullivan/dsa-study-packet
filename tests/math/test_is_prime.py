"""Tests for math / is_prime."""

from hypothesis import given
from hypothesis import strategies as st

from algo.math.is_prime import is_prime


def _trial_division(n: int) -> bool:
    if n < 2:
        return False
    return all(n % factor for factor in range(2, n))


class TestIsPrime:
    def test_values_below_two_are_not_prime(self) -> None:
        assert not is_prime(-17)
        assert not is_prime(0)
        assert not is_prime(1)

    def test_small_primes(self) -> None:
        assert all(is_prime(value) for value in (2, 3, 5, 7, 11, 13))

    def test_squares_and_small_composites(self) -> None:
        assert all(not is_prime(value) for value in (4, 9, 25, 49, 77, 121))

    def test_larger_prime_and_composite(self) -> None:
        assert is_prime(104_729)
        assert not is_prime(104_729 * 17)

    @given(n=st.integers(min_value=-100, max_value=1_000))
    def test_matches_direct_trial_division(self, n: int) -> None:
        assert is_prime(n) is _trial_division(n)
