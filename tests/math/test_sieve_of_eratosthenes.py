"""Tests for math / sieve_of_eratosthenes."""

from math import isqrt

from hypothesis import example, given
from hypothesis import strategies as st

from algo.math.sieve_of_eratosthenes import sieve_of_eratosthenes, sieve_slices


class TestSieveOfEratosthenes:
    def test_n_zero(self) -> None:
        assert sieve_of_eratosthenes(0) == []

    def test_n_one(self) -> None:
        assert sieve_of_eratosthenes(1) == []

    def test_n_two(self) -> None:
        assert sieve_of_eratosthenes(2) == [2]

    def test_n_ten(self) -> None:
        assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]

    def test_n_hundred_matches_pi_of_100(self) -> None:
        primes = sieve_of_eratosthenes(100)
        assert len(primes) == 25  # pi(100) = 25
        assert primes[-1] == 97

    def test_negative_n(self) -> None:
        assert sieve_of_eratosthenes(-5) == []

    def test_n_three_boundary(self) -> None:
        # p*p (== 4) exceeds n here, so the strike loop never runs; 3 must
        # still survive as prime.
        assert sieve_of_eratosthenes(3) == [2, 3]

    @given(n=st.integers(min_value=0, max_value=500))
    def test_no_returned_value_has_a_divisor_up_to_its_sqrt(self, n: int) -> None:
        for value in sieve_of_eratosthenes(n):
            assert value >= 2
            assert all(value % d != 0 for d in range(2, isqrt(value) + 1))

    @given(n=st.integers(min_value=0, max_value=500))
    def test_complement_of_result_is_all_composite(self, n: int) -> None:
        primes = set(sieve_of_eratosthenes(n))
        for value in range(2, n + 1):
            if value not in primes:
                assert any(value % d == 0 for d in range(2, isqrt(value) + 1))

    @given(n=st.integers(min_value=0, max_value=2000))
    @example(n=1000)  # pi(1000) = 168, a commonly memorized landmark value
    def test_pi_of_1000_is_168(self, n: int) -> None:
        if n == 1000:
            assert len(sieve_of_eratosthenes(n)) == 168


class TestSieveSlices:
    def test_matches_examples(self) -> None:
        assert sieve_slices(10) == [2, 3, 5, 7]
        assert sieve_slices(1) == []

    @given(n=st.integers(min_value=0, max_value=1000))
    def test_matches_whiteboard_form(self, n: int) -> None:
        """Cross-check: the slice-assignment form must agree with the loop form."""
        assert sieve_slices(n) == sieve_of_eratosthenes(n)
