---
title: target employer Algorithm Study Guide
---

# target employer Algorithm Study Guide

A comprehensive algorithm interview preparation kit targeting a **Senior Full-Stack (Backend) Engineer** role at [target employer](https://www.example.com/).

<div class="grid cards" markdown>

-   :material-code-braces:{ .lg .middle } **69 Implementations**

    ---

    13 topics from arrays to graphs, all typed Python 3.14+

    [:octicons-arrow-right-24: Algorithms](algorithms/index.md)

-   :material-test-tube:{ .lg .middle } **600+ Tests**

    ---

    Property-based testing with Hypothesis, class-based pytest

    [:octicons-arrow-right-24: Challenges](challenges/index.md)

-   :material-book-open-variant:{ .lg .middle } **6 Concept Modules**

    ---

    T-strings, typing, Hypothesis, FFT, Flask, Pydantic

    [:octicons-arrow-right-24: Concepts](concepts/index.md)

-   :material-file-document-multiple:{ .lg .middle } **9 Reference Sheets**

    ---

    Printable cheat sheets from stdlib to interview-day logistics

    [:octicons-arrow-right-24: Reference](reference/index.md)

</div>

---

## Quick Start

```bash
direnv allow          # activate .envrc
just test             # run all 600+ tests
just lint             # ruff + mypy strict
just practice graphs  # run tests for a specific topic
just study dp         # watch mode for a topic
```

---

## target employer Interview Overview

target employer's interview process consists of **5 rounds**:

| Round | Format | Duration | Focus |
|-------|--------|----------|-------|
| 1. Pre-screen | Phone call | 30 min | Recruiter screen, background |
| 2. HackerRank | Online coding | ~90 min | Algorithm problems (medium) |
| 3. Deep-dive coding | Video call | 2 x 60 min | Backend coding, frontend coding |
| 4. Technical onsite | In-person | 4-6 hrs | System design, practical problem solving |
| 5. CEO chat | In-person | 30 min | Culture fit, company direction |

**Difficulty:** LeetCode medium to medium-hard. FAANG-style interviews with emphasis on graph algorithms, system design, and code reading.

**Key domains:** Flight route optimization, geospatial indexing, real-time streaming, 4D trajectory prediction.

---

## What's Inside

### Algorithms (`src/algo/`)

69 implementations across 13 topics: arrays, two pointers, sliding window, stacks/queues, searching, linked lists, trees, graphs, dynamic programming, heaps, backtracking, greedy, bit manipulation, sorting, recursion, and strings.

### Concept Modules (`src/concepts/`)

6 production-level Python modules covering PEP 750 t-strings, advanced typing, property-based testing, signal processing, Flask 3.x, and Pydantic v2.

### Practice Exercises (`src/practice/`)

Code reading exercises (caching service, flight data pipeline, rate limiter) and problem decomposition exercises (flight route optimizer, vehicle tracking, geospatial pipeline).

### Reference Sheets (`reference-sheets/`)

9 printable reference sheets covering Python stdlib, data structures, algorithm templates, Python 3.14 patterns, Big-O complexity, common patterns, system design, interview day guide, and the master cross-reference.

---

## Start Studying

The fastest path from zero to interview-ready:

1. **Skim** the [decision tree](guide/when-to-use-what.md) to internalize problem-type branching
2. **Work through** the [7-day challenge plan](challenges/index.md) covering all 69 problems
3. **Review** the [reference sheets](reference/index.md) for quick recall
4. **Practice** [code reading](practice/index.md) for the practical problem solving round

[:material-rocket-launch: Start the 7-Day Challenge](challenges/index.md){ .md-button .md-button--primary }
[:material-map: When to Use What](guide/when-to-use-what.md){ .md-button }
