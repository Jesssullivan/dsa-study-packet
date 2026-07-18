---
title: Getting Started
---

# Getting Started

The Woodshed has two parts. The practice workspace holds your comments, code,
and tests. The site and printable packet hold complete solutions and reference
material. Practice first; read when a rep exposes a gap. Nothing in the
practice workspace is committed.

!!! tip "The loop"
    Choose a comment format, fill the comments, delete your gate, implement and
    test, then keep one correction.

## 1. Start a rep

[:octicons-mark-github-24: Open in GitHub Codespaces](https://codespaces.new/Jesssullivan/dsa-study-packet?quickstart=1){ .md-button .md-button--primary }

Open Copilot Chat and enter one command:

```text
/reacto
/clarp
/umpire
/comments
```

With no arguments, the command draws the next due problem. To choose one,
append its topic and name:

```text
/reacto arrays two_sum
```

Each format asks for the same interview signals with different headings.

| Command | Comment headings |
|---------|------------------|
| `/reacto` | Repeat, Examples, Approach, Code, Test, Optimize |
| `/clarp` | Clarify, Lay out, Attack, Run, Polish |
| `/umpire` | Understand, Match, Plan, Implement, Review, Evaluate |
| `/comments` | Restate, Example, Invariant, Approach, Tests, Complexity |

Copilot needs no repository API key. It conducts the rep, while portable
`just` commands create the workspace and run tests. Without Copilot, start
from a terminal:

```bash
just practice-start reacto
just practice-start clarp arrays two_sum
```

## 2. Write before code

Starting a rep opens:

```text
.challenges/workspace/<problem>.py
.challenges/workspace/test_<problem>_candidate.py
```

In the source file:

1. Restate the problem and note any questions.
2. Write one example and one edge case.
3. Name an approach and its expected time and space cost.
4. Save, then delete the `THINKING GATE` yourself.
5. Implement the solution.
6. Add focused tests, trace one example, and update comments that no longer
   match the code.

The interviewer checks that each reasoning section is filled. It never writes
your code, tests, or gate. Save detection is explicit, so enter `/continue`
after a save or run `just practice-next`.

The workspace is gitignored. Starting a different rep archives the previous
workspace under `.challenges/history/`. Starting the same one resumes it. The
complete implementation under `src/algo/` remains unchanged.

## 3. Use focused feedback

```bash
just practice-next       # current state and one next action
just practice-test       # this problem's reference tests plus your tests
just practice-watch      # rerun the focused tests on changes
just practice-repl       # load your implementation interactively
just practice-open       # reopen both files
```

Test, watch, and REPL wait until the required comments are filled and the gate
is gone. This keeps reasoning before implementation without giving the agent
control of your work.

## 4. Stop cleanly

Name one specific thing that worked and the single change you want next time.
Then close the private log and spaced-review update together:

```bash
just practice-finish "trace the example before running tests"
```

The goal is a useful correction, not a solve count. An unfinished
implementation can still produce a good rep.

## 5. Run locally

Clone the repository and reopen it in the supplied VS Code Dev Container for
the closest match to Codespaces. Nix users can run `direnv allow`. With Python
3.14+, `uv`, and `just` already installed, use `uv sync --extra dev`.

```bash
just doctor
just test
just lint
```

See [Local VS Code](local-practice.md) for setup details.

## Choose the right surface

| Goal | Surface |
|------|---------|
| Reason, code, and test | editor rep |
| Form a plan without editor pressure | untimed conversation |
| Practice narration under a clock | timed board or observed mock |
| Select a pattern | [decision tree](when-to-use-what.md) |
| Review a finished technique | [algorithm library](../algorithms/index.md) |
| Work a curated sequence | [learning paths](learning-paths.md) |
