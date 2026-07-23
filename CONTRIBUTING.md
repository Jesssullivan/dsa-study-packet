# Contributing

Company-neutral technical-interview study packet. Code, tests, and authored
notes are the source of truth; the printable booklet is generated from them,
and the reading surface at https://dsa-woodshed.space syncs its content from
this repo at build time.

## Set up the loop

```bash
uv sync --extra dev
just test           # pytest + hypothesis
just lint           # ruff + mypy + repo guards
```

`just --list` shows every recipe. If you use the devcontainer / Codespaces,
setup is automatic; see `README.md` for the one-click flow.

## Add a drill

1. Add the topic/problem pair to `CORE_42` in
   [`scripts/core42.py`](scripts/core42.py) — the single catalog SSOT shared
   by the docs generator and the spaced-repetition scheduler.
2. Scaffold the files: `just new <topic> <problem>` (creates
   `src/algo/<topic>/<problem>.py` and its test).
3. Implement the solution and tests until `just test` is green.
4. Run `just lint`. Drill, implementation, concept, and reference-sheet counts
   are machine-guarded (`scripts/check_doc_counts.py`) against `core42.py` —
   do not hand-edit a count in prose anywhere; if a doc states one, it must
   already match the SSOT or the guard fails the build.

## Agent surfaces are generated — never hand-edit them

The resident-interviewer persona lives once, in the `AGENTS.md` persona
region. The portable Codex skill lives at
`.agents/skills/interviewer/SKILL.md`. GitHub Copilot's instruction files are
generated from the persona, and Claude's interviewer skill is generated from
the portable skill. If you change either source:

```bash
just gen-agents
```

and commit the regenerated files alongside your `AGENTS.md` edit.
`scripts/check_agent_instructions.py` fails CI if the generated files drift
from what `AGENTS.md` would produce. Never edit the generated files directly —
your changes will be silently overwritten and the drift guard will still fail.

## Codespaces acceptance

Acceptance evidence must come from a newly created workspace at the current
`main`, not a resumed Codespace. Open
`https://codespaces.new/Jesssullivan/dsa-study-packet/tree/main`, create the
Codespace, and record:

```bash
git rev-parse HEAD
git rev-parse origin/main
```

The SHAs must match. Then verify Copilot Chat separately in the VS Code UI:
the extension is present, the account is signed in, and the account has
Copilot access. Codespaces detection alone proves none of those.

## The public-boundary rule (hard rule)

This repo is company-neutral by design. Employer names, panel/interviewer
notes, req numbers, clearance facts, tailored positioning, and personal rep
logs never enter this tree — they belong in a private downstream overlay
only. `scripts/check_public_boundary.py` (wired into `just lint` and CI)
enforces the structural rules. Read the full contract before adding anything
that might be employer- or session-specific:
[`docs/guide/source-of-truth.md`](docs/guide/source-of-truth.md).

## Pull requests

- Run `just lint` and `just test` locally; both must be green.
- If you touched anything counted by the doc-count guard or the persona
  region, regenerate and commit the derived surfaces (see above).
- Fill out the PR template checklist honestly — it mirrors this file.

## Versioning and releases

Releases use CalVer tags: `vYYYY.M.PATCH` (e.g. `v2026.7.0`), one release per
notable batch of changes, not per commit. Pushing a tag matching `v*` runs
[`.github/workflows/release.yml`](.github/workflows/release.yml), which
builds the printable booklet and reference-sheet PDFs and attaches them to a
GitHub Release created from the tag. Maintainers cut a release with:

```bash
git tag v2026.7.0
git push origin v2026.7.0
```

Release notes are auto-generated from merged PRs; see `CHANGELOG.md` for a
human-curated running summary between releases.
