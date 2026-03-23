---
title: Hypothesis Patterns
---

# Hypothesis Patterns -- Property-Based Testing

## Why This Matters in Interviews

Reaching for Hypothesis during a coding interview signals testing sophistication
well beyond unit tests. Three things it demonstrates:

1. **You test the specification, not specific cases.** Instead of checking that
   `sort([3, 1, 2]) == [1, 2, 3]`, you assert `result == sorted(result)` for
   *any* generated input. This catches edge cases you'd never think to write by hand.

2. **You know the oracle pattern.** Compare your optimized solution against a
   known-correct brute-force reference. For example, validate `top_k_frequent`
   (bucket sort, O(n)) against `Counter.most_common(k)` --- the obvious but
   slower approach. One line of property, thousands of test cases.

3. **You can articulate invariants.** "The output is always sorted", "every
   returned element exists in the input", "length never exceeds k" are
   *properties*, not examples. Hypothesis tests them across hundreds of random
   inputs automatically.

## How the Tests Are Wired Up

The source module below (`src/concepts/hypothesis_patterns.py`) defines two
systems-under-test: `SortedList` and `BoundedCounter`. The **real tutorial**
lives in the test file (`tests/concepts/test_hypothesis_patterns.py`), which
walks through six Hypothesis patterns with runnable, heavily-commented code:

| Pattern | What It Does | When to Reach for It |
|---------|-------------|---------------------|
| `@composite` | Build complex test data step by step | Inter-dependent constraints (e.g., pre-filled data structures) |
| `RuleBasedStateMachine` | Stateful testing with an oracle | Sequences of operations that must maintain invariants |
| `@example` | Pin specific inputs | Regression tests, known edge cases |
| `@settings` | Control intensity | CI (high) vs local dev (fast) profiles |
| `st.builds` | Auto-generate dataclass instances | Any `__init__` that takes simple args |
| `st.recursive` | Generate nested/tree structures | JSON-like data, ASTs, recursive types |

## Quick Interview Demo

To demonstrate PBT mastery in under 2 minutes during an interview:

```python
from hypothesis import given
from hypothesis import strategies as st

@given(data=st.lists(st.integers(), min_size=1))
def test_top_1_matches_counter(data: list[int]) -> None:
    """Oracle pattern: compare O(n) bucket sort against Counter."""
    from collections import Counter
    result = top_k_frequent(data, 1)
    expected_freq = Counter(data).most_common(1)[0][1]
    assert Counter(data)[result[0]] == expected_freq
```

This single test generates hundreds of random inputs and validates your
implementation against the stdlib oracle. No hand-written edge cases needed.

---

## Systems Under Test

::: concepts.hypothesis_patterns
    options:
      show_source: true
      members_order: source
