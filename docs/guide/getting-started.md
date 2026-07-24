---
title: Getting Started
description: Start an editor-first interview rep with source comments or docstrings, candidate-owned code, focused tests, and one concrete correction.
---

# Getting Started

The Woodshed has two parts. The practice workspace holds your comments, code,
and tests. The site and printable packet hold complete solutions and reference
material. Practice first; read when a rep exposes a gap. Nothing in the
practice workspace is committed.

!!! tip "The loop"
    Start with ordinary source comments or docstrings, or choose a named
    framework. Save and continue explicitly, implement and test, then keep one
    correction.

## Your first ten minutes

1. Click Start in Codespaces. The container builds in about two minutes;
   nothing beyond a GitHub account is required.
2. Ask Copilot Chat for a first practice rep. One placement question comes
   back: "Where do you want to work today: reason and code in the editor,
   talk a problem through with no clock, or do a timed board-style rep?"
3. There is no menu, and no clock unless you ask for one. A nervous first
   session starts as a conversation.
4. Stop clean: one thing that worked, one fix, done. The next draw is queued
   for tomorrow.

What a first session can sound like (illustrative; the interviewer adapts to
you):

> **Interviewer:** Two Sum, no code required. Tell me what the problem asks
> in your own words.
>
> **You:** Find two numbers in an array that add to a target... I would check
> every pair? That is O(n²) and feels wrong.
>
> **Interviewer:** Not wrong: a baseline. Say it like that: brute force is n
> squared, and here is what I would trade to beat it.
>
> **You:** Okay, a hash map. One pass, check for the complement as I go.
>
> **Interviewer:** That is the whole move. Walk me through [3, 1, 4] with
> target 5 and we are done for today. One clean rep is the win.

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

Copilot needs no repository API key, but you must confirm that Chat is signed
in and available in the VS Code UI. It conducts the rep, while portable `just`
commands create the workspace and run tests. Without Copilot, start from a
terminal:

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
4. Save, then enter `/continue` or run `just practice-next`.
5. Implement the solution, using comments alongside code where they help.
6. Add focused tests, trace one example, and update comments that no longer
   match the code.

Use ordinary source comments or candidate-authored docstrings in your own
words. Write them in the file, not the Chat composer. There is no required
prefix, comment count, or gate deletion. The interviewer reads only saved
work, so enter `/continue` after a save or run `just practice-next`. It never
writes your code or tests.

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

Test, watch, and REPL follow the saved practice state. The explicit
save-and-continue boundary keeps you in control of when the interviewer reads
your work.

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
