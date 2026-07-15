"""Tests for the top-k-frequent-elements problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.arrays.top_k_frequent import top_k_frequent, top_k_frequent_heap


class TestTopKFrequent:
    def test_basic(self) -> None:
        assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]

    def test_single_element(self) -> None:
        assert top_k_frequent([1], 1) == [1]

    def test_all_same_frequency(self) -> None:
        result = top_k_frequent([1, 2, 3], 2)
        assert len(result) == 2
        assert all(x in [1, 2, 3] for x in result)

    def test_k_equals_unique_count(self) -> None:
        assert sorted(top_k_frequent([1, 1, 2, 2, 3, 3], 3)) == [1, 2, 3]

    def test_negative_numbers(self) -> None:
        assert sorted(top_k_frequent([-1, -1, 2, 2, 2, 3], 2)) == [-1, 2]

    def test_k_zero(self) -> None:
        assert top_k_frequent([1, 2, 3], 0) == []

    @given(
        data=st.lists(
            st.integers(min_value=-100, max_value=100),
            min_size=1,
            max_size=50,
        ),
    )
    def test_top_1_is_most_frequent(self, data: list[int]) -> None:
        from collections import Counter

        result = top_k_frequent(data, 1)
        assert len(result) == 1
        counter = Counter(data)
        max_freq = counter.most_common(1)[0][1]
        assert counter[result[0]] == max_freq


class TestTopKFrequentHeap:
    """Cross-check the heap alternate against the primary implementation."""

    @given(
        data=st.lists(
            st.integers(min_value=-20, max_value=20),
            min_size=1,
            max_size=30,
        ),
        k=st.integers(min_value=1, max_value=10),
    )
    def test_matches_primary_frequency_profile(self, data: list[int], k: int) -> None:
        # ties at the cutoff can break differently between the two
        # implementations, so compare frequency profiles, not exact elements
        from collections import Counter

        counter = Counter(data)
        bucket_result = top_k_frequent(data, k)
        heap_result = top_k_frequent_heap(data, k)
        assert len(bucket_result) == len(heap_result)
        assert sorted(counter[x] for x in bucket_result) == sorted(
            counter[x] for x in heap_result
        )
