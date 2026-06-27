---
title: Practice Exercises
---

# Practice Exercises

Exercises designed for practical problem-solving rounds where the interviewer
shows you unfamiliar code and asks you to analyze it.

---

## Code Reading Exercises

These files contain intentionally buggy or suboptimal code. Your job: identify all issues, propose fixes, and estimate the complexity impact of each fix.

| Exercise | File | Domain |
|----------|------|--------|
| Caching Service | `src/practice/code_reading/ex01_caching_service.py` | Cache design, eviction, thread safety |
| Flight Data Pipeline | `src/practice/code_reading/ex02_flight_data_pipeline.py` | Streaming, batching, error handling |
| Rate Limiter | `src/practice/code_reading/ex03_rate_limiter.py` | Token bucket, sliding window, concurrency |

### How to work through code reading exercises

1. **Skim** -- read function signatures and docstrings first
2. **Trace** -- pick one execution path and follow it end to end
3. **Question** -- "What happens when input is empty? Very large? Malformed?"
4. **Measure** -- estimate time/space complexity of the hot path
5. **Propose** -- suggest 2-3 improvements ranked by impact

---

## Problem Decomposition Exercises

These are open-ended system design and algorithm decomposition prompts. Practice talking through them out loud -- record yourself.

| Exercise | File | Domain |
|----------|------|--------|
| Vehicle Tracking | `src/practice/decomposition/ex02_vehicle_tracking.md` | Geospatial indexing, real-time updates |

### What they're evaluating

- Can you read and understand code you didn't write?
- Can you identify performance bottlenecks?
- Can you spot bugs and edge cases?
- Can you suggest improvements with clear reasoning?
- Do you communicate your thought process clearly?

---

## Checklist for Code Review

Scan every code reading exercise for these red flags:

- [ ] **Nested loops** -- O(n^2) or worse hiding in plain sight
- [ ] **No streaming** -- loading all data into memory
- [ ] **Missing error handling** -- no try/except, no input validation
- [ ] **Thread safety** -- shared mutable state without locks
- [ ] **N+1 queries** -- database call inside a loop
- [ ] **Unbounded caches** -- no eviction policy, no TTL
- [ ] **Synchronous I/O** -- blocking calls in async context
