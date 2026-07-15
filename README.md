# The DSA Woodshed

Company-neutral technical interview practice in a real editor. Each rep asks
you to explain the problem in comments, implement a solution, write focused
tests, and make one useful correction. Complete implementations, reference
sheets, and a printable packet remain available after the rep.

The same material is published at
**[dsa-woodshed.space](https://dsa-woodshed.space)**. Employer-specific prep
belongs in private downstream overlays; see the
[source-of-truth contract](docs/guide/source-of-truth.md).

## Start in Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Jesssullivan/dsa-study-packet?quickstart=1)

When the editor opens, use Copilot Chat to choose a comment format:

```text
/reacto
/clarp
/umpire
/comments
```

No topic is required. The command draws the next due problem. To choose one,
append its topic and name, for example `/reacto arrays two_sum`.

The rep opens two gitignored files under `.challenges/workspace/`: your source
file and your test file. The committed implementation under `src/algo/` stays
unchanged.

1. Fill the reasoning comments and save.
2. Delete the `THINKING GATE` yourself.
3. Implement the solution and add focused tests.
4. Enter `/continue` or run `just practice-next` for the next instruction.
5. Run `just practice-test`, then close with `just practice-finish "one fix"`.

The interviewer never writes your code, tests, or gate. Copilot is optional;
the same flow starts from a terminal with `just practice-start reacto`.

The four comment formats are vocabulary choices, not different grading
systems. Pick the labels that help you show the work. `/continue` checks which
sections are filled and returns one next action; it does not judge an approach
while you are still forming it. Tests remain the correctness signal.

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
overlays. The repository also generates the site, algorithm pages, and
reference-sheet PDFs from the tracked source.

## Repository map

- `src/algo/`: tested reference implementations
- `tests/`: reference tests
- `docs/`: web reading surface
- `reference-sheets/`: printable method and reference material
- `.challenges/`: private, gitignored practice state
- `scripts/core42.py`: core drill catalog (historical filename)

Run `just catalog` for the current drill list and `just --list` for all
recipes. See [WELCOME.md](WELCOME.md) for the shortest first-session guide.
