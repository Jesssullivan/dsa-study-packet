# The DSA Woodshed

Company-neutral technical-interview training: algorithm implementations with
tests, printable reference sheets, and a whiteboard **performance** method —
because these interviews score how you work out loud, not just what you know.

Code, tests, and authored notes are the single source of truth; every artifact
(printable PDF packet, web site, drills) is generated from them. Employer- or
panel-specific prep lives in private downstream overlays, never in this repo —
see [the contract](docs/guide/source-of-truth.md).

Prefer reading to running commands first? The same drills, sheets, and method
are published at **[dsa-woodshed.space](https://dsa-woodshed.space)**.

## Try it in one click

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Jesssullivan/dsa-study-packet?quickstart=1)

**Your first ten minutes:**

1. **Click the badge** and wait for the terminal banner. The container builds
   in a couple of minutes — no setup, no secrets.
2. **Say the line.** If you set an interviewer secret ([WELCOME.md](WELCOME.md)),
   your interviewer is already running in the focused terminal pane — just say:
   **"Start my first practice rep."** No secret? Open Copilot Chat in the
   sidebar, or run `claude` or `codex` yourself, and say the same line.
3. **Talk, don't grind.** The interviewer asks one placement question, then
   runs an untimed conversational rep: restate the problem, pick an example,
   think out loud. No clock, no score — minutes of silence are fine, and you
   end when *you* have a plan.
4. **Stop clean.** One specific win, one fix, logged with `just rep` +
   `just challenge-done` — and tomorrow's draw is already queued.

`just doctor` checks the toolchain · `just challenge-reset` restores a
pristine slate · `just --list` shows every recipe.

**Interviewer options.** Copilot needs zero keys (activate Copilot Free once
at [github.com/settings/copilot](https://github.com/settings/copilot); the
free tier is metered, so long sessions run best on a CLI). Set one Codespaces
secret and every Codespace opens with your interviewer **already running in a
split terminal**: `CLAUDE_CODE_OAUTH_TOKEN` (Claude Pro/Max, from
`claude setup-token`) or `ANTHROPIC_API_KEY` for Claude Code, `OPENAI_API_KEY`
for Codex — the two-minute walkthrough lives in [WELCOME.md](WELCOME.md),
including which model to run (short version: don't pin one; plan defaults are
already right). If you have the Gemini CLI installed, it picks up the same
persona via `.gemini/settings.json`. **No agent at all also works** — the
entire loop is plain `just` recipes with the method on printable reference
sheets.

This is a template repository — **Use this template** gives you your own copy
with a fresh, private practice log (`.challenges/` is gitignored). Forks that
want faster boots can enable Codespaces prebuilds on their own account (repo
Settings → Codespaces); they stay off upstream so your minutes are yours.

## Local quick start (Nix power users)

The maintainer's local flow uses the Nix devshell; the devcontainer above
never touches it.

```bash
direnv allow        # nix devshell + Python 3.14 venv
just test           # pytest + hypothesis
just lint           # ruff + mypy strict + public-boundary guard
just docs           # local MkDocs site (drills, visualizer, progress)
just packet         # printable TeX -> PDF booklet
just pdf-all        # every reference sheet -> PDF
just study-tonight  # Day 12 block: print it, run it, stop building
```

## The daily drill (board ↔ IDE)

```bash
just study-spaced 1                  # 1. spaced repetition picks today's drill
just interview arrays two_sum        # 2. cold problem: statement only, solution stripped
#    3. at the whiteboard: recording ON, run CLARP out loud (sheet 10)
just study arrays                    # 4. at the IDE: implement until tests pass
just rep "arrays/two_sum C2 L1 A2 R1 P2 <one fix>"   # 5. score the rep (private log)
just challenge-done arrays two_sum   # 6. feed spaced repetition
```

The method — what interviewers actually score, the CLARP loop, panic first-aid,
collaboration scripts, self-review rubric — is
[sheet 10](reference-sheets/10-whiteboard-performance-protocol.md).
The two-week day-by-day ramp is
[sheet 11](reference-sheets/11-14-day-whiteboard-ramp.md).
`just challenge` (statement + approach visible) remains as learning mode.

## Drill Catalog

The core drill set lives in [`scripts/core42.py`](scripts/core42.py), not in a
hand-maintained README table. Run `just catalog` for the current topic counts
and drill list. Further implementations stay in the repo as extended practice
and reference.

## The overlay pattern

This repo is also a Bazel module (`dsa_study_packet`) exposing one composition
surface: `//:booklet`, the compiled neutral packet PDF. A private downstream
repo can wrap that PDF with its own front/back matter — people, probes,
positioning — without any of that ever touching this tree. The boundary is
machine-enforced (`just public-boundary`), and
[`examples/overlay-demo/`](examples/overlay-demo/) is a self-contained,
fork-me demonstration with placeholder content.

## Cache-first / remote builds

```bash
just remote-build            # //:booklet via GloriousFlywheel shared cache when attached
just remote-test             # bazel test, cache-first
just remote-check            # attachment/contract gate (exits 0 unattached)
```

The [GloriousFlywheel front-door kit](justfile.flywheel) is endpoint-free by
contract: no cache endpoints, tokens, or runner labels are committed; profile
and auth resolve at invocation. Unattached, everything degrades to a local
disk cache. Never call raw `bazel` — drive builds through `just remote-*`.

## Aspirations

Codespaces is the one-click front door, not a hard dependency: the design is
terminal-first, so the same devcontainer, `just` recipes, and
resident-interviewer persona are meant to work from local VS Code, a bare
`just doctor` + `uv` checkout, [DevPod](https://devpod.sh), or a self-hosted
[Coder](https://coder.com) template — and to run against on-prem or
self-hosted models via endpoint overrides, not only hosted APIs. That work is
tracked in [#49](https://github.com/Jesssullivan/dsa-study-packet/issues/49).
