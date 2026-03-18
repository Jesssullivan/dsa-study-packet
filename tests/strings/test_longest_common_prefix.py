"""Tests for the longest common prefix problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.strings.longest_common_prefix import longest_common_prefix


class TestLongestCommonPrefix:
    def test_basic(self) -> None:
        assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"

    def test_no_common_prefix(self) -> None:
        assert longest_common_prefix(["dog", "racecar", "car"]) == ""

    def test_empty_list(self) -> None:
        assert longest_common_prefix([]) == ""

    def test_single_string(self) -> None:
        assert longest_common_prefix(["alone"]) == "alone"

    def test_identical_strings(self) -> None:
        assert longest_common_prefix(["abc", "abc", "abc"]) == "abc"

    def test_empty_string_in_list(self) -> None:
        assert longest_common_prefix(["", "abc", "abd"]) == ""

    @given(
        prefix=st.text(alphabet="abc", min_size=1, max_size=10),
        suffixes=st.lists(
            st.text(alphabet="xyz", min_size=0, max_size=10),
            min_size=1,
            max_size=5,
        ),
    )
    def test_constructed_prefix_is_found(
        self, prefix: str, suffixes: list[str]
    ) -> None:
        strs = [prefix + s for s in suffixes]
        result = longest_common_prefix(strs)
        assert result.startswith(prefix) or prefix.startswith(result)
        # result must be at least as long as prefix
        assert len(result) >= len(prefix)
