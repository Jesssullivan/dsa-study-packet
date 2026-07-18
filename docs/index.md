---
title: The DSA Woodshed
---

# The DSA Woodshed

Practice technical interviews in a real editor: explain the problem in
comments, implement a solution, write focused tests, and keep one correction.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Start**

    ---

    Open Codespaces and begin an editor rep.

    [:octicons-mark-github-24: Open in Codespaces](https://codespaces.new/Jesssullivan/dsa-study-packet?quickstart=1)

-   :material-code-braces:{ .lg .middle } **Practice Drills**

    ---

    Choose from 42 core drills and extended problems.

    [:octicons-arrow-right-24: Choose a Drill](challenges/index.md)

-   :material-account-voice:{ .lg .middle } **Method**

    ---

    Learn the comment-first loop and its practice modes.

    [:octicons-arrow-right-24: Getting Started](guide/getting-started.md)

-   :material-book-open-variant:{ .lg .middle } **Library**

    ---

    Review complete solutions, concepts, and printable sheets.

    [:octicons-arrow-right-24: Browse Reference](reference/index.md)

</div>

## Your first rep

Open Copilot Chat in Codespaces and enter `/reacto`, `/clarp`, `/umpire`, or
`/comments`. With no arguments, the command draws the next due problem. Add a
topic and problem to choose one, such as `/reacto arrays two_sum`.

Your source and test file open under `.challenges/workspace/`. Fill the
reasoning comments, save, then delete the `THINKING GATE` yourself. Implement,
add focused tests, and enter `/continue` for the next instruction. Copilot is
optional; `just practice-start reacto` starts the same loop.

```bash
just practice-next
just practice-test
just practice-repl
just practice-finish "one fix"
```

The committed solutions under `src/algo/` stay unchanged. Your workspace and
rep history remain private and gitignored.

Use the [decision tree](guide/when-to-use-what.md) when pattern selection is
the gap, or browse [complete implementations](algorithms/index.md) after a rep.
The [practice evidence](guide/interview-practice-evidence.md) explains the
larger method. A printable packet is also available for offline review.

[:material-map: Read the Full Loop](guide/getting-started.md){ .md-button .md-button--primary }
[:material-download: Download PDF](assets/booklet.pdf){ .md-button }
