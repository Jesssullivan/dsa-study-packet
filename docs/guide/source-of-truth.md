---
title: Source of Truth
---

# Source of Truth

This project treats source code, tests, and authored notes as durable study
material. Generated docs and PDFs must be reproducible from those inputs, and
employer-specific interview prep must never enter this tree. This page is the
whole contract.

## Authored Material

| Path | Purpose |
|------|---------|
| `src/algo/` | Algorithm implementations and docstrings |
| `tests/` | Examples and property-based correctness checks |
| `src/concepts/` | Technical concept modules |
| `src/practice/` | Code-reading and decomposition exercises |
| `reference-sheets/` | Printable notes, quick-reference sheets, and the practice method (sheets 10–11) |
| `reference-sheets/appendix-topics.json` | Structured appendix topics rendered into the booklet compile-safely |

## Generated Material

| Output | Command |
|--------|---------|
| `booklet.tex` / `booklet.pdf` / `docs/assets/booklet.pdf` | `just packet` |
| `reference-sheets/pdf/*.pdf` | `just pdf-all` |
| `site/` | `just docs-build` |

## Three Layers

| Layer | What | Where | Public? |
|-------|------|-------|---------|
| **L1 — knowledge** | algorithms, tests, concepts, reference sheets 01–09 | this repo | ✅ |
| **L2 — practice method** | sheets 10–11, `just interview` / `just rep`, spaced repetition | this repo | ✅ |
| **L3 — private overlay** | employer/panel front & back matter, people, dates, tailored positioning, personal rep logs | a private downstream repo | ⛔ never here |

The distinction that keeps this publishable: L2 is a *method* ("how to stay
calm and narrate at a whiteboard" — a general, teachable skill); L3 is a
*dossier* (who is on Tuesday's panel). Method publishes; dossier never touches
this tree. **If a sentence only makes sense for one employer, it is L3.**

## The Graph Edge Is One-Way

```
private superset repo                    THIS REPO (public)
─────────────────────                    ──────────────────
bazel_dep + path/git override   ──────▶  module(name = "dsa_study_packet")
\includepdf{@dsa_study_packet            //:booklet  (neutral PDF)
            //:booklet}
+ private front/back matter (L3)
→ private //:study_packets
```

The private repo depends on this one; this repo knows nothing about any
downstream. Composition is **overlay, not bundle**: the neutral booklet is
compiled *here* from *this* tree (so it cannot contain employer text), and a
private lane `\includepdf`s the finished PDF between its own front and back
matter. The two bodies of text only ever meet as adjacent pages in a private
output — never in source. Delete the private repo and this SSOT is unchanged
and complete. `examples/overlay-demo/` is a self-contained, fork-me
demonstration of the pattern with placeholder content.

## The Boundary Is Enforced

`scripts/check_public_boundary.py` (`just public-boundary`) fails if any
tracked file contains a forbidden marker: tracked SOPS files, legacy secret
tripwires, the private downstream repo's name, or the employer markers this
packet was ever tailored for. Neutrality is a machine check, not a promise.
Personal rep scores (`.challenges/reps.md`) are gitignored by default —
publish aggregates deliberately, or not at all.

## Runbook

| I want to… | Do this | Layer |
|------------|---------|-------|
| Add/extend a study or practice sheet | `reference-sheets/NN-*.md` + one-line `docs/reference/NN-*.md` wrapper; nav + PDF pick it up | L1/L2 |
| Add an algorithm | `src/algo/<topic>/<problem>.py` + tests; booklet and site regenerate | L1 |
| Prep for a specific employer/panel | Create a lane in the private downstream repo; author front/back matter there | L3 |
| Keep practice tapes / mock scripts / rep scores | Private repo or gitignored local dir — never tracked here | L3 |
