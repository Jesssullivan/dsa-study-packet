# Changelog

All notable changes to this project are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions
are CalVer tags (`vYYYY.M.PATCH`) cut as GitHub Releases — see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## [Unreleased]

## [v2026.7.0] — 2026-07-09

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
- `just doctor`, a full-slate `just challenge-reset`, and a genericized
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
