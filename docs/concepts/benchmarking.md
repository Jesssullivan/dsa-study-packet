---
title: Benchmarking (T-Strings)
---

# Interview Benchmarking with T-Strings

Reusable timing patterns for demonstrating algorithm performance during live
coding. T-strings (PEP 750) separate timing *data* from *presentation* ---
the same Template renders as human text or structured dict.

## Quick Usage

```python
from concepts.benchmarking import timed, bench_compare, bench_scaling

# Scoped timing
with timed("bucket sort"):
    result = top_k_frequent(data, k)

# Side-by-side comparison
bench_compare({
    "bucket O(n)":     lambda: top_k_frequent(data, 10),
    "heap O(n log k)": lambda: find_kth_largest(data, 10),
})

# Empirical Big-O verification
bench_scaling(
    lambda n: top_k_frequent(list(range(n)) * 3, 10),
    sizes=[1_000, 10_000, 100_000],
)
```

## The DRY T-String Pattern

The key insight: a t-string template captures data and text in a single
object.  Different renderers produce different output from the **same**
template --- no duplication.

```python
report = t"[bench] {label}: {elapsed_ms:.3f}ms ({elapsed_ns:,}ns)"
print(render(report))        # Human:   [bench] sort: 0.042ms (42,100ns)
data  = as_dict(report)      # Machine: {"label": "sort", "elapsed_ms": 0.042, ...}
```

---

::: concepts.benchmarking
    options:
      show_source: true
      members_order: source
