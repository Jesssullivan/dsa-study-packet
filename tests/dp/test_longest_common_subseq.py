"""Tests for longest common subsequence."""

from hypothesis import given
from hypothesis import strategies as st

from algo.dp.longest_common_subseq import longest_common_subsequence


class TestLongestCommonSubsequence:
    def test_basic(self) -> None:
        assert longest_common_subsequence("abcde", "ace") == 3

    def test_no_common(self) -> None:
        assert longest_common_subsequence("abc", "def") == 0

    def test_identical(self) -> None:
        assert longest_common_subsequence("abc", "abc") == 3

    def test_one_empty(self) -> None:
        assert longest_common_subsequence("abc", "") == 0

    def test_subsequence_at_end(self) -> None:
        assert longest_common_subsequence("oxcpqrsvwf", "shmtulqrypy") == 2

    @given(s=st.text(alphabet="ab", min_size=0, max_size=20))
    def test_self_lcs_is_length(self, s: str) -> None:
        assert longest_common_subsequence(s, s) == len(s)
