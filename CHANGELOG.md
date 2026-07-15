# Changelog

All notable changes to this project are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
are CalVer tags (`vYYYY.M.PATCH`) cut as GitHub Releases; see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## [Unreleased]

### Added

- Editor-first practice workspaces under gitignored
  `.challenges/workspace/`: paradigm-specific reasoning comments, a
  candidate-owned test tab, a candidate-owned `THINKING GATE`, and focused
  reference-plus-candidate test, watch, REPL, status, and reopen recipes.
- Native Copilot workspace prompts: `/reacto`, `/clarp`, `/umpire`, and
  `/comments`. The slash invocation is the mode choice and draws from
  spaced repetition when no problem is supplied.
- `just practice-next`, which returns one stable state and one next action, and
  `just practice-finish`, which records the rep and schedules review together.
- A clarity guard for agent and onboarding word budgets, ambiguous command
  placeholders, and em dashes on the learner control plane.

### Changed

- Codespaces now defaults to its built-in Copilot Chat and the portable
  `just practice-*` loop. It no longer requires interviewer secrets or
  auto-starts an external CLI in a split terminal; external agents remain
  manual options.
- Codespaces installs its three small command-line tools from versioned,
  checksum-verified release archives, pins the base image and workflow actions,
  and exports the tool path for clean editor terminals.
- VS Code applies the root `AGENTS.md` authority once; the generated
  `.github/copilot-instructions.md` remains available to GitHub.com without
  duplicating the persona in Codespaces prompts.
- Starting a rep renders from the committed reference source into an isolated
  candidate workspace instead of rewriting `src/algo/`. Candidates record
  reasoning in live comments, save explicitly, remove the thinking gate
  themselves, implement, and add focused tests.
- Helper functions and classes stay as candidate-owned cold stubs during tests
  and in the REPL; committed helper implementations are never injected.
- Conversational and board-style practice remain available as slower
  and mock-practice modes, while the normal Codespaces path begins in the
  editor.
- Agent handoff now uses the compact THINK, BUILD, REFLECT, and CLOSE state
  loop. Generic practice-day routing no longer captures single-rep requests.
- Repository onboarding, local documentation, learning paths, and the 14-day
  calendar now share one editor-first flow and a smaller Start, Practice,
  Library, Method, and Project information architecture.
- Destructive legacy recipes that rewrote tracked algorithm sources were
  removed. The unused save-polling hook is gone too; `/continue` is the explicit
  turn boundary. Editor practice stays in the isolated `.challenges/workspace/`.

## [v2026.7.0] - 2026-07-09

First tagged release: the packet as a one-click, agent-conducted practice
environment, with its reading surface live at https://dsa-woodshed.space.

### Added

- Zero-click Codespaces interviewer: devcontainer boot pre-authenticates and
  opens the resident interviewer in a split terminal on attach, with model
  defaults and a `WELCOME.md` walkthrough for Claude Code, Codex, and Copilot.
- Save-gated comment-driven IDE rep (rung 2): `just interview-comment` seeds a
  five-part reasoning scaffold (restate, example, invariant, approach,
  complexity) with a candidate-owned LOCK line, reviewed at save boundaries
  instead of interrupting mid-typing.
- `just doctor`, a full-slate challenge reset helper, and a genericized
  `practice-day` skill so the daily 4-5h block runs the same way for any
  candidate.

### Changed

- Docs and product surfaces unified: the resident-interviewer persona now
  lives once in `AGENTS.md` and fans out to Copilot's instruction files via
  `just gen-agents`, with a drift guard keeping the generated copies honest.
- Hardened the public-boundary and doc-count guards so hand-typed counts and
  private-prep leakage are caught in CI, not just at review time.

### Fixed

- `just challenge-done` made portable to GNU sed (Linux/Codespaces), not just
  BSD sed (macOS).
