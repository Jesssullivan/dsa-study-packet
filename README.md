# The DSA Woodshed

Company-neutral technical interview practice in a real editor. Each rep asks
you to explain the problem in comments, implement a solution, write focused
tests, and make one useful correction. Complete implementations, reference
sheets, and a printable packet remain available after the rep.

The same material is published at
**[dsa-woodshed.space](https://dsa-woodshed.space)**. Employer-specific prep
belongs in private downstream overlays; see the
[source-of-truth contract](docs/guide/source-of-truth.md). The
practice-flow contract future language tracks implement is
[TRACK-CONTRACT.md](TRACK-CONTRACT.md).

## Start in Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Jesssullivan/dsa-study-packet/tree/main)

When the editor opens, confirm Copilot Chat is signed in and available, then
enter `/comments`. The command starts a rep; the reasoning itself belongs in
ordinary source comments or docstrings, with no required labels or prefixes.

```text
/comments
```

No topic is required. The command draws the next due problem. To choose one,
append its topic and name, for example `/comments arrays two_sum`. If named
vocabulary helps you think, `/reacto`, `/clarp`, and `/umpire` start the same
loop with those optional labels.

The rep opens two gitignored files under `.challenges/workspace/`: your source
file and your test file. The committed implementation under `src/algo/` stays
unchanged.

1. Write reasoning in ordinary source comments or docstrings.
2. Save, then enter `/continue` or run `just practice-next`.
3. Implement the solution and add focused tests.
4. Save and continue again when you want the next instruction.
5. Run `just practice-test`, then close with `just practice-finish "one fix"`.

Write comments in the source file, not the Chat composer. There is no required
prefix, comment count, or gate deletion. The interviewer never writes your
code or tests. Copilot is optional;
the same flow starts from a terminal with `just practice-start comments`.

The named frameworks are vocabulary choices, not grading systems. Keep their
labels, replace them, or use ordinary source comments and docstrings in your
own words. `/continue` reads the saved source and test files, then returns one
next action. It does not grade wording; tests remain the correctness signal.

## Current-rep commands

```bash
just practice-next       # current state and one next action
just practice-test       # this problem's reference tests plus your tests
just practice-watch      # rerun the focused tests on changes
just practice-repl       # explore your implementation interactively
just practice-open       # reopen the source and test files
just practice-finish "one fix"
```

Use [Practice Drills](docs/challenges/index.md) to choose a problem and
[Getting Started](docs/guide/getting-started.md) for the full loop. Untimed
conversation and timed board-style practice remain available when those are
the skills you intend to train.

## Local development

The Dev Container provides the same toolchain as Codespaces. Nix users can
enter the pinned shell with `direnv allow`.

```bash
just doctor
just test
just lint
just docs
just packet
```

`just` is the front door. Cache-first Bazel builds use `just remote-*`, never
raw `bazel`. `//:booklet` is the neutral PDF composition surface for private
overlays. The tracked source also generates local docs, algorithm pages, and
reference-sheet PDFs; the reading site syncs that content separately.

## Repository map

- `src/algo/`: tested reference implementations
- `tests/`: reference tests
- `docs/`: web reading surface
- `reference-sheets/`: printable method and reference material
- `.challenges/`: private, gitignored practice state
- `scripts/core42.py`: core drill catalog (historical filename)

Run `just catalog` for every exact practice pair, or search natural names with
`just catalog "anagram, 2 sum and prime"`. Run `just --list` for all recipes.
See [WELCOME.md](WELCOME.md) for the shortest first-session guide.
