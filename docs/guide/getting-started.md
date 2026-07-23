---
title: Getting Started
description: Start an editor-first interview rep with natural comments, candidate-owned code, focused tests, and one concrete correction.
---

# Getting Started

The Woodshed has two parts. The practice workspace holds your comments, code,
and tests. The site and printable packet hold complete solutions and reference
material. Practice first; read when a rep exposes a gap. Nothing in the
practice workspace is committed.

!!! tip "The loop"
    Start with ordinary comments or choose a named framework. Fill the comments,
    delete your gate, implement and test, then keep one correction.

## 1. Start a rep

[:octicons-mark-github-24: Open in GitHub Codespaces](https://codespaces.new/Jesssullivan/dsa-study-packet?quickstart=1){ .md-button .md-button--primary }

Open Copilot Chat and enter one command:

```text
/comments
/reacto
/clarp
/umpire
```

With no arguments, the command draws the next due problem. To choose one,
append its topic and name:

```text
/comments arrays two_sum
```

Each command asks for the same interview signals. Plain comments use natural
language; the named frameworks add optional headings.

| Command | Scaffolding |
|---------|-------------|
| `/comments` | Ordinary comments in your own words, with no required labels or prefixes |
| `/reacto` | Repeat, Examples, Approach, Code, Test, Optimize |
| `/clarp` | Clarify, Lay out, Attack, Run, Polish |
| `/umpire` | Understand, Match, Plan, Implement, Review, Evaluate |

Copilot needs no repository API key. It conducts the rep, while portable
`just` commands create the workspace and run tests. Without Copilot, start
from a terminal:

```bash
just practice-start comments
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

The interviewer checks that saved reasoning comments are present, not that you
used a particular prefix or label. It never writes your code, tests, or gate.
Save detection is explicit, so enter `/continue` after a save or run `just
practice-next`.

The workspace is gitignored. Starting a different rep archives the previous
workspace under `.challenges/history/`. Starting the same unfinished rep
resumes it; starting after closeout creates a new rep. The complete
implementation under `src/algo/` remains unchanged.

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

Name one win and the one fix you want next time.
Then close the private log and spaced-review update together:

```bash
just practice-finish "trace the example before running tests"
```

The goal is a useful correction, not a solve count. An unfinished
implementation or failing test can still produce a good rep. At `STATE:
CLOSE`, `practice-finish` reruns the focused tests once and records the result.
An earlier closeout records `not_run`. Either path closes the rep instead of
trapping you in it.

For a talk-only or board rep, use one atomic closeout with the exact draw:

```bash
just rep-finish arrays two_sum \
  "talk arrays/two_sum C2 L2 A1 R0 P0 h1 trace before optimizing"
```

Change the values to match the rep. The command logs it and schedules review
together.

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
