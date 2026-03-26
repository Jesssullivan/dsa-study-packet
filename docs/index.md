---
title: DSA Study Guide
---

# Algorithm Study Guide

Full-stack (backend) interview prep for DSA exams.

<div class="grid cards" markdown>

-   :material-code-braces:{ .lg .middle } **69 Implementations**

    ---

    15 topics, typed Python 3.14+, 42 core daily drills

    [:octicons-arrow-right-24: Algorithms](algorithms/index.md)

-   :material-test-tube:{ .lg .middle } **647 Tests**

    ---

    Property-based testing with Hypothesis, class-based pytest

    [:octicons-arrow-right-24: Challenges](challenges/index.md)

-   :material-book-open-variant:{ .lg .middle } **7 Concept Modules**

    ---

    T-strings, typing, Hypothesis, benchmarking, FFT, Flask, Pydantic

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
just test             # 647 tests
just lint             # ruff + mypy strict
just docs             # this site, locally
```

---

## Interview Flow

| Stage | Round | Focus |
|-------|-------|-------|
| 1 | Pre-screen | Headhunter chats with CTO and hiring manager based on FOSS contributions, PR experience, etc. |
| 2 | Hiring manager interview | Role fit, experience, expectations. |
| 3 | Engineering lead interview | Technical depth, architecture thinking, team dynamics. |
| 4 | Backend algo deep dive | 1-3 hrs coding. Graphs, DP, strings, optimization. |
| 5 | Frontend / cross-team engineering | 1-3 hrs. Cross-team collaboration, full-stack breadth. |
| 6 | On-site intensive | 6-8 hrs. All-day in-person interviews across multiple rounds. |
| 7 | CEO interview | Culture, vision, team fit. |
| 8 | Offer & negotiation | Offer terms, agreements, logistics. |

---

## Daily Drill

42 core algorithms, all of them, every single day. Challenge mode strips solutions — Jess re-implements from the signature and docstring alone.

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

---

## Printable Booklet

123-page reference: decision trees, pattern keywords, and every algorithm with full implementation — one per page.

[:material-download: Download PDF](assets/booklet.pdf){ .md-button }

<div markdown class="pdf-viewer">
<iframe src="assets/booklet.pdf" width="100%" height="800px" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>
</div>
