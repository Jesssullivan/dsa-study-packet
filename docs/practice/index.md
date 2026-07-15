---
title: Advanced Exercises
---

# Advanced Exercises

Use these after ordinary editor reps when you want to practice reading
unfamiliar code, finding operational risks, or decomposing an open-ended
system. They supplement the [Practice Drills](../challenges/index.md); they do
not replace the comments, code, and tests loop.

## Code reading

The Python files are intentionally buggy or inefficient. For each exercise:

1. Read signatures and docstrings.
2. Trace one execution path.
3. Test empty, large, malformed, and concurrent inputs where relevant.
4. Estimate the time and space cost of the hot path.
5. Propose two or three fixes, ordered by impact.

| Exercise | File | Focus |
|----------|------|-------|
| Caching Service | `src/practice/code_reading/ex01_caching_service.py` | eviction, thread safety |
| Flight Data Pipeline | `src/practice/code_reading/ex02_flight_data_pipeline.py` | streaming, batching, failures |
| Rate Limiter | `src/practice/code_reading/ex03_rate_limiter.py` | token buckets, windows, concurrency |

Check for unbounded memory, nested work on the hot path, missing validation,
shared mutable state, blocking I/O, and calls inside loops. Explain the impact
before proposing a change.

## Problem decomposition

The open-ended prompts train scope, interfaces, tradeoffs, and test strategy.

| Exercise | File | Focus |
|----------|------|-------|
| Vehicle Tracking | `src/practice/decomposition/ex02_vehicle_tracking.md` | geospatial indexing, live updates |

State assumptions, split the system into parts, identify the riskiest seam,
and describe how you would verify it. An untimed conversational rep works well
for a first pass; use an observed mock when concise narration is the target.

For a longer scheduled block, run `just practice-day 12` and follow the
printed stop conditions. Use the daily conductor only when you intend to run
the full block.
