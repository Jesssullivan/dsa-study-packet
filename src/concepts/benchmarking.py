"""Interview benchmarking with Python 3.14 t-strings.

Clean, reusable timing patterns for demonstrating algorithm performance
during live coding interviews.  T-strings (PEP 750) separate timing
*data* from *presentation* --- the same Template renders as human-readable
text or as a structured dict for programmatic use.

Patterns demonstrated
---------------------
1. ``timed()`` context manager --- scoped wall-clock measurement
2. ``bench()`` --- median-of-N timing for a single callable
3. ``bench_compare()`` --- side-by-side comparison with ratios
4. ``bench_scaling()`` --- empirical Big-O verification

DRY principle
-------------
Define timing once, use everywhere.  T-string templates embody the same
idea: define the template once, render it multiple ways (human, dict, CSV).
The ``render()`` / ``as_dict()`` pair demonstrates this --- one Template,
two outputs, zero duplication.

Interview tip
-------------
After implementing a solution, add 3--5 lines of timing to demonstrate you
understand performance *empirically*, not just theoretically::

    import time
    start = time.perf_counter_ns()
    result = top_k_frequent(data, k)
    ms = (time.perf_counter_ns() - start) / 1_000_000
    report = t"top_k: {ms:.3f}ms for n={len(data):,}"

References
----------
* PEP 750 t-strings  --- https://peps.python.org/pep-0750/
* time.perf_counter_ns --- https://docs.python.org/3/library/time.html#time.perf_counter_ns
* statistics.median    --- https://docs.python.org/3/library/statistics.html
"""

import statistics
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager

# string.templatelib ships with Python 3.14 (PEP 750).
from string.templatelib import Interpolation, Template

# --------------------------------------------------------------------------- #
# T-string rendering: one template, multiple presentations
# --------------------------------------------------------------------------- #
# A t-string like  t"top_k: {ms:.3f}ms"  returns a Template object
# containing both static text and Interpolation objects.  Unlike f-strings,
# the template is NOT eagerly evaluated --- you choose HOW to render it.
#
# This is DRY in action: the timing data is captured ONCE in the template.
# Different renderers produce different output from the SAME data.
#
# Quick interview demo of the dual-rendering pattern:
# 1. Create one t-string template capturing label, elapsed_ms, elapsed_ns
# 2. render(template)  -> human-readable:  "[bench] sort: 0.042ms (42,100ns)"
# 3. as_dict(template) -> machine dict:    {"label": "sort", "elapsed_ms": 0.042}


def _convert(value: object, conversion: str | None) -> object:
    """Apply ``!s`` / ``!r`` / ``!a`` conversion flag from an Interpolation.

    >>> _convert(42, "s")
    '42'
    >>> _convert("hello", "r")
    "'hello'"
    >>> _convert("hello", None)
    'hello'
    """
    if conversion == "s":
        return str(value)
    if conversion == "r":
        return repr(value)
    if conversion == "a":
        return ascii(value)
    return value


def render(template: Template) -> str:
    """Render a Template to a plain string --- f-string equivalent.

    >>> x = 42
    >>> render(t"x is {x}")
    'x is 42'
    >>> render(t"pi = {3.14159:.2f}")
    'pi = 3.14'
    """
    parts: list[str] = []
    for item in template:
        match item:
            case str() as s:
                parts.append(s)
            case Interpolation(value=v, conversion=c, format_spec=spec):
                parts.append(format(_convert(v, c), spec))
    return "".join(parts)


def as_dict(template: Template) -> dict[str, object]:
    """Extract interpolation names and values as a structured dict.

    Same template, machine-parseable output.  Useful for logging bench
    results or feeding them into a comparison framework.

    >>> label = "sort"
    >>> ms = 1.234
    >>> d = as_dict(t"{label}: {ms:.3f}ms")
    >>> d["label"], d["ms"]
    ('sort', 1.234)
    """
    result: dict[str, object] = {}
    rendered: list[str] = []
    for item in template:
        match item:
            case str() as s:
                rendered.append(s)
            case Interpolation(
                value=v, expression=expr, conversion=c, format_spec=spec
            ):
                result[expr] = v
                rendered.append(format(_convert(v, c), spec))
    result["_rendered"] = "".join(rendered)
    return result


# --------------------------------------------------------------------------- #
# 1. timed() --- context manager for scoped timing
# --------------------------------------------------------------------------- #
# Simplest pattern: wrap any block in ``with timed("label"):``.
# Uses ``perf_counter_ns`` for nanosecond resolution (not ``time.time``,
# which has platform-dependent resolution as low as 15ms on Windows).


@contextmanager
def timed(label: str) -> Iterator[None]:
    """Context manager that prints wall-clock time using a t-string.

    Usage::

        with timed("bucket sort"):
            result = top_k_frequent(data, k)
        # prints: [bench] bucket sort: 0.042ms (42,100ns)
    """
    start = time.perf_counter_ns()
    yield
    elapsed_ns = time.perf_counter_ns() - start
    elapsed_ms = elapsed_ns / 1_000_000
    # T-string captures structured data.  render() gives human output;
    # as_dict() on the same template would give {"label": ..., "elapsed_ms": ...}.
    report = t"[bench] {label}: {elapsed_ms:.3f}ms ({elapsed_ns:,}ns)"
    print(render(report))


# --------------------------------------------------------------------------- #
# 2. bench() --- median-of-N timing
# --------------------------------------------------------------------------- #
# Median is more robust than mean --- it resists GC pauses and OS
# scheduling jitter.  Odd default (7) gives a true median without
# interpolation.


def bench(label: str, fn: Callable[[], object], *, runs: int = 7) -> float:
    """Run *fn* multiple times, print and return median elapsed ms.

    Usage::

        ms = bench("top_k O(n)", lambda: top_k_frequent(data, 10))
        # prints: [bench] top_k O(n): 0.053ms median of 7 runs
    """
    times_ns: list[int] = []
    for _ in range(runs):
        start = time.perf_counter_ns()
        fn()
        times_ns.append(time.perf_counter_ns() - start)

    median_ns = statistics.median(times_ns)
    median_ms = median_ns / 1_000_000
    report = t"[bench] {label}: {median_ms:.3f}ms median of {runs} runs"
    print(render(report))
    return median_ms


# --------------------------------------------------------------------------- #
# 3. bench_compare() --- side-by-side implementation comparison
# --------------------------------------------------------------------------- #
# Prints a table with the fastest implementation as 1.0x baseline.
# Returns a dict for programmatic assertions (e.g., O(n) < O(n log n)).


def bench_compare(
    implementations: dict[str, Callable[[], object]],
    *,
    runs: int = 7,
) -> dict[str, float]:
    """Compare implementations side-by-side with relative ratios.

    Usage::

        bench_compare({
            "bucket O(n)":     lambda: top_k_frequent(data, 10),
            "heap O(n log k)": lambda: heapq.nlargest(10, data),
        })
        # prints:
        #   bucket O(n)            0.053ms  (  1.0x)
        #   heap O(n log k)        0.087ms  (  1.6x)
    """
    results: dict[str, float] = {}
    for label, fn in implementations.items():
        times_ns: list[int] = []
        for _ in range(runs):
            start = time.perf_counter_ns()
            fn()
            times_ns.append(time.perf_counter_ns() - start)
        results[label] = statistics.median(times_ns) / 1_000_000

    fastest = min(results.values()) if results else 1.0
    for label, ms in results.items():
        ratio = ms / fastest if fastest > 0 else 1.0
        row = t"  {label:<20s}  {ms:>8.3f}ms  ({ratio:>5.1f}x)"
        print(render(row))
    return results


# --------------------------------------------------------------------------- #
# 4. bench_scaling() --- empirical Big-O verification
# --------------------------------------------------------------------------- #
# Measures runtime at increasing input sizes and prints growth ratios.
# O(n) shows ~10x growth per 10x input; O(n log n) ~13x; O(n^2) ~100x.
# This lets you PROVE your complexity claim during an interview.


def bench_scaling(
    fn: Callable[[int], object],
    sizes: list[int] | None = None,
    *,
    runs: int = 5,
) -> list[tuple[int, float]]:
    """Measure how runtime scales with input size.

    Pass a function that accepts an integer size parameter.

    Usage::

        bench_scaling(
            lambda n: top_k_frequent(list(range(n)) * 3, 10),
            sizes=[1_000, 10_000, 100_000],
        )
        # prints:
        #   1,000         0.102ms        --
        #   10,000        0.987ms      9.7x   <-- ~10x = O(n)
        #   100,000       9.842ms     10.0x
    """
    if sizes is None:
        sizes = [100, 1_000, 10_000, 100_000]

    results: list[tuple[int, float]] = []
    for n in sizes:
        times_ns: list[int] = []
        for _ in range(runs):
            start = time.perf_counter_ns()
            fn(n)
            times_ns.append(time.perf_counter_ns() - start)
        results.append((n, statistics.median(times_ns) / 1_000_000))

    # Scaling table with growth ratios between successive sizes.
    prev_ms = 0.0
    for n, ms in results:
        n_str = f"{n:,}"
        ms_str = f"{ms:.3f}ms"
        growth_str = f"{ms / prev_ms:.1f}x" if prev_ms > 0 else "--"
        row = t"  {n_str:<12s}  {ms_str:>10s}  {growth_str:>8s}"
        print(render(row))
        prev_ms = ms
    return results
