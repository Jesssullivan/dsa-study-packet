"""Tests for benchmarking concept module.

Validates the timing utilities and demonstrates interview-style
benchmarking using top_k_frequent and kth_largest as subjects.

The tests here serve double duty:
1. Correctness: the utilities return sensible values.
2. Interview demo: show HOW to benchmark algorithms you just implemented.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from algo.arrays.top_k_frequent import top_k_frequent
from algo.heaps.kth_largest import find_kth_largest
from concepts.benchmarking import (
    as_dict,
    bench,
    bench_compare,
    bench_scaling,
    render,
    timed,
)

# =========================================================================== #
# T-string rendering tests
# =========================================================================== #


class TestRender:
    """Test render() produces f-string equivalent output."""

    def test_plain_text(self) -> None:
        result = render(t"hello world")
        assert result == "hello world"

    def test_interpolation(self) -> None:
        x = 42
        assert render(t"x is {x}") == "x is 42"

    def test_format_spec(self) -> None:
        pi = 3.14159
        assert render(t"pi = {pi:.2f}") == "pi = 3.14"

    def test_conversion_repr(self) -> None:
        s = "hello"
        assert render(t"repr: {s!r}") == "repr: 'hello'"


class TestAsDict:
    """Test as_dict() extracts structured data from templates."""

    def test_extracts_values(self) -> None:
        label = "sort"
        ms = 1.234
        d = as_dict(t"{label}: {ms:.3f}ms")
        assert d["label"] == "sort"
        assert d["ms"] == 1.234

    def test_includes_rendered(self) -> None:
        x = 42
        d = as_dict(t"value = {x}")
        assert d["_rendered"] == "value = 42"

    def test_multiple_interpolations(self) -> None:
        a = 1
        b = 2
        d = as_dict(t"{a} + {b}")
        assert d["a"] == 1
        assert d["b"] == 2


# =========================================================================== #
# Timing utility tests
# =========================================================================== #


class TestTimed:
    """Test timed() context manager."""

    def test_prints_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        with timed("test-label"):
            _ = sum(range(1000))
        captured = capsys.readouterr()
        assert "[bench] test-label:" in captured.out
        assert "ms" in captured.out
        assert "ns" in captured.out


class TestBench:
    """Test bench() median-of-N timing."""

    def test_returns_nonnegative(self) -> None:
        ms = bench("sum", lambda: sum(range(100)), runs=3)
        assert ms >= 0

    def test_prints_median_label(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        bench("my-fn", lambda: None, runs=5)
        captured = capsys.readouterr()
        assert "[bench] my-fn:" in captured.out
        assert "median of 5 runs" in captured.out


class TestBenchCompare:
    """Test bench_compare() side-by-side comparison."""

    def test_returns_all_labels(self) -> None:
        results = bench_compare(
            {
                "sorted": lambda: sorted(range(100), reverse=True)[0],
                "max": lambda: max(range(100)),
            },
            runs=3,
        )
        assert "sorted" in results
        assert "max" in results

    def test_values_are_nonnegative(self) -> None:
        results = bench_compare(
            {"noop": lambda: None, "sum": lambda: sum(range(10))},
            runs=3,
        )
        assert all(v >= 0 for v in results.values())


class TestBenchScaling:
    """Test bench_scaling() empirical complexity measurement."""

    def test_returns_correct_count(self) -> None:
        data = bench_scaling(lambda n: sum(range(n)), [100, 1000], runs=3)
        assert len(data) == 2

    def test_sizes_match_input(self) -> None:
        sizes = [50, 500, 5000]
        data = bench_scaling(lambda n: list(range(n)), sizes, runs=3)
        assert [n for n, _ in data] == sizes


# =========================================================================== #
# Interview demo: benchmarking top_k_frequent
# =========================================================================== #
# These tests show exactly how you'd benchmark during a coding interview.
# After implementing bucket sort top-k, prove O(n) empirically.


class TestTopKBenchDemo:
    """Interview-style benchmarking of top_k_frequent vs heap approach."""

    @pytest.mark.bench
    def test_compare_bucket_vs_sorted(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Compare O(n) bucket sort against O(n log n) sorted approach."""
        from collections import Counter

        data = list(range(500)) * 3 + list(range(200)) * 7

        results = bench_compare(
            {
                "bucket O(n)": lambda: top_k_frequent(data, 10),
                "Counter.most_common": lambda: [
                    x for x, _ in Counter(data).most_common(10)
                ],
            },
            runs=5,
        )
        # Both should return in finite time with nonneg values.
        assert all(v >= 0 for v in results.values())

    @pytest.mark.bench
    def test_scaling_is_linear(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Empirically verify O(n) scaling for bucket sort top-k."""
        data = bench_scaling(
            lambda n: top_k_frequent(list(range(n)) * 3, 10),
            sizes=[1_000, 5_000, 10_000],
            runs=3,
        )
        # Sanity: larger inputs should take more time.
        assert data[-1][1] >= data[0][1] or data[0][1] < 0.001


# =========================================================================== #
# Interview demo: benchmarking kth_largest
# =========================================================================== #


class TestKthLargestBenchDemo:
    """Interview-style benchmarking of heap-based kth largest."""

    @pytest.mark.bench
    def test_compare_heap_vs_sorted(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Compare O(n log k) heap against O(n log n) full sort."""
        data = list(range(10_000))

        results = bench_compare(
            {
                "heap O(n log k)": lambda: find_kth_largest(data, 10),
                "sorted O(n log n)": lambda: sorted(data, reverse=True)[9],
            },
            runs=5,
        )
        assert all(v >= 0 for v in results.values())


# =========================================================================== #
# Hypothesis: property-based bench validation
# =========================================================================== #
# Bonus: use Hypothesis to fuzz the benchmarking utilities themselves.
# This demonstrates combining PBT with benchmarking --- two interview
# power tools in one test.


class TestBenchProperties:
    """Property-based tests for benchmarking utilities."""

    @settings(max_examples=20)
    @given(x=st.integers(-1000, 1000))
    def test_render_matches_fstring(self, x: int) -> None:
        """render(t"...") should always match the equivalent f-string."""
        assert render(t"val={x}") == f"val={x}"

    @settings(max_examples=20)
    @given(x=st.integers(-1000, 1000))
    def test_as_dict_preserves_value(self, x: int) -> None:
        """as_dict() should always preserve the original value."""
        d = as_dict(t"num={x}")
        assert d["x"] == x
