---
title: Authoring & Overlay Architecture
---

# Authoring & Overlay Architecture

**How the pieces assemble so the public source can derive every artifact, while
company- and interviewer-specific data stays *overlaid* — never bundled into the
study material or the source that generates it.**

This is the design behind [Source of Truth](source-of-truth.md), stated in full.
It is the pattern to reuse whenever a study or practice artifact needs a private,
tailored variant without contaminating the public, teachable base.

## The problem

Two things must be true at once:

1. **The study and practice work is publishable and teachable.** The algorithms,
   the reference sheets, and the *method* — how to practice whiteboarding, narrate
   your thinking, manage panic, and "do the hard thing" under observation — are a
   general skill. They should live in the open, be forkable, and eventually teach.
2. **The tailored prep for a specific employer or interview panel must stay
   private and must never leak.** Company names, req numbers, panelist notes,
   recruiter details, dates, and claim-discipline strategy cannot appear anywhere
   in the public tree — not in the artifacts, and not in the source that derives
   them.

Naive approaches fail #2: a single repo with `if company == ...` branches, or a
"just don't commit that file" convention, leaks the moment someone runs a build
or greps history. The fix is a hard structural boundary enforced by the graph and
by a guard, not by discipline.

## Three layers

| Layer | What it is | Where it lives | Public? |
|-------|-----------|----------------|---------|
| **L1 — Neutral knowledge** | `src/algo`, `tests/`, `src/concepts`, reference sheets 01–09, `appendix-topics.json` | this repo | ✅ public SSOT |
| **L2 — Neutral practice method** | reference sheet 10 (performance & panic protocol), the `just challenge` loop, `study_schedule.py`, the on-camera + self-review rubric | this repo | ✅ public SSOT |
| **L3 — Private overlay** | employer/panel front & back matter, people, probes, dates, claim discipline, tailored positioning, personal rep logs & tapes | a **downstream private repo** | ⛔ never here |

The distinction that makes this safe: **L2 is a *method*, not a *dossier*.** "How to
stay calm and narrate at the whiteboard" is a general skill — it publishes. "The
eight people on Tuesday's panel and what each will probe" is L3 — it never touches
this repo. Your *specific* practice logs and company-tilted mock scripts are L3
too; the reusable protocol they exercise is L2.

## The graph edge is one-way

```
  downstream/private-superset            THIS REPO (public)
  ────────────────────────────          ─────────────────────────────
  bazel_dep(dsa_study_packet)  ───────▶  module(name = "dsa_study_packet")
  \includepdf{ @dsa_study_packet          //:booklet   (neutral PDF)
              //:booklet }                booklet.tex  (generated SSOT)
  + front_matter.tex  (L3)
  + back_matter.tex   (L3)
  → //:study_packets  (private)
```

The private repo **depends on** the public one; the public one has **zero
knowledge** of any downstream. There is no edge pointing back. The public module
exposes exactly one composition surface — `//:booklet`, the compiled neutral PDF —
and nothing about how it is wrapped.

## "Overlay, not bundle" — what that means concretely

Composition happens by **PDF inclusion by reference**, not by text concatenation
of source:

- The neutral booklet is compiled *here*, from *this* repo's source, into
  `//:booklet`. Its `.tex` contains no employer text — it cannot, because none
  exists in this tree.
- The private lane `\includepdf`s that already-compiled neutral PDF *between* its
  own private front and back matter. The employer-specific words live only in the
  private `.tex`; they are never merged into the neutral source and never appear
  in `//:booklet`.

So the two bodies of text are only ever *adjacent pages in a private output* — the
neutral source that derives the study artifacts stays clean. Delete the private
repo and the public SSOT is unchanged and complete.

A downstream lane is one macro call (from the private repo's `study_common`):

```python
study_packet_lane(company = "acme")   # stages neutral booklet + acme front/back → private packet
```

and the private aggregate deliberately lives in a filegroup (`//:study_packets`)
kept **out** of any public-facing target, so nothing that publishes the public
artifacts can ever sweep in a private packet.

## The boundary is enforced, not trusted

`scripts/check_public_boundary.py` (run it with `just public-boundary`) fails if
any tracked file in this repo contains a forbidden marker:

- SOPS secret files (`*.sops.yaml/yml/json`)
- known legacy tokens / age recipients (history-scrub tripwires)
- the legacy company-specific repo name
- the private downstream repo name
- **employer markers** — the specific company abbreviations this packet was ever
  tailored for

Wire it into CI and the pre-publish check. If a company name ever lands in a
reference sheet, a docstring, or a nav page, the build goes red *before* it ships.
That is the guarantee that L1/L2 stay neutral — a machine check, not a promise.

> When authoring here, keep it generic on purpose. Say "a Python/pseudocode round
> vs. a Python/C++ round," never the employer. Say "evidence-based
> performance-anxiety techniques," never a private source. If a sentence only
> makes sense for one employer, it belongs in L3.

## Learn the pattern from `examples/overlay-demo`

`examples/overlay-demo/` is a self-contained, lorem-ipsum demonstration of the
exact overlay: a fake company's front/back matter wrapping the neutral booklet via
the same `\includepdf` mechanism, buildable with no private inputs. It is the
fork-me reference for anyone reproducing the pattern for their own study work.

## Runbook — adding things without crossing the boundary

| I want to… | Do this | Layer |
|------------|---------|-------|
| Add/extend a neutral study or practice sheet | Drop `reference-sheets/NN-*.md` + a one-line `docs/reference/NN-*.md` wrapper; nav + per-sheet PDF pick it up automatically | L1/L2 |
| Add a neutral algorithm | Add `src/algo/<topic>/<problem>.py` + tests; the booklet and site regenerate | L1 |
| Prep for a specific employer/panel | Create a lane in the **private** downstream repo (`study_packet_lane`), author its front/back matter there | L3 |
| Keep my own practice tapes / mock scripts | Store them in the private repo (or an untracked local dir), never here | L3 |

**The golden rule:** if it names a company, a person, a date, a req number, or a
tailored claim, it goes downstream. Everything else — the knowledge and the method
— stays here, in the open, where it can eventually teach.
