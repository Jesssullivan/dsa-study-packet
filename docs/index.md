---
title: target employer Algorithm Study Guide
---

# target employer Algorithm Study Guide

Senior full-stack (backend) interview prep for [target employer](https://www.example.com/).

<div class="grid cards" markdown>

-   :material-code-braces:{ .lg .middle } **69 Implementations**

    ---

    15 topics, typed Python 3.14+, 42 core daily drills

    [:octicons-arrow-right-24: Algorithms](algorithms/index.md)

-   :material-test-tube:{ .lg .middle } **628 Tests**

    ---

    Property-based testing with Hypothesis, class-based pytest

    [:octicons-arrow-right-24: Challenges](challenges/index.md)

-   :material-book-open-variant:{ .lg .middle } **6 Concept Modules**

    ---

    T-strings, typing, Hypothesis, FFT, Flask, Pydantic

    [:octicons-arrow-right-24: Concepts](concepts/index.md)

-   :material-file-document-multiple:{ .lg .middle } **9 Reference Sheets**

    ---

    Printable cheat sheets from stdlib to system design

    [:octicons-arrow-right-24: Reference](reference/index.md)

</div>

---

## Quick Start

```bash
direnv allow          # nix devshell + python 3.14 venv
just test             # 628 tests
just lint             # ruff + mypy strict
just docs             # this site, locally
```

---

## Interview Rounds

| Round | Format | Focus |
|-------|--------|-------|
| Algorithms | 75 min, video | Medium to medium-hard. Graphs, DP, strings. |
| Practical Problem Solving | Video | Read their code, identify issues, suggest improvements. |
| Problem Decomposition | Video | Break ambiguous problems into sub-problems. |
| System Design | 60 min (L7+) | Real-time pipelines, geospatial, streaming. |
| CEO Chat | In-person | Culture, motivation, trajectory. |

---

## Daily Drill

42 core algorithms, all of them, every single day. Challenge mode strips solutions — you re-implement from the signature and docstring alone.

```bash
just challenge graphs dijkstra    # strip solution
just study graphs                 # watch mode — tests re-run on save
just solution graphs dijkstra     # peek if stuck
just challenge-done graphs dijkstra
just challenge-progress
```

The [decision tree](guide/when-to-use-what.md) maps problem signals to patterns.
The [cross-reference guide](reference/08-cross-reference-guide.md) maps patterns to implementations.

[:material-rocket-launch: Start Drilling](challenges/index.md){ .md-button .md-button--primary }
[:material-map: Decision Tree](guide/when-to-use-what.md){ .md-button }
