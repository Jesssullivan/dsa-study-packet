---
title: Source of Truth
---

# Source of Truth

This project treats source code, tests, and authored notes as durable study
material. Generated docs and PDFs should be reproducible from those inputs.

## Authored Material

| Path | Purpose |
|------|---------|
| `src/algo/` | Algorithm implementations and docstrings |
| `tests/` | Examples and property-based correctness checks |
| `src/concepts/` | Technical concept modules |
| `src/practice/` | Code-reading and decomposition exercises |
| `reference-sheets/` | Printable notes and quick-reference sheets |
| `reference-sheets/appendix-topics.json` | Structured appendix topics (concurrency, hashing internals, amortized analysis, recursion→iteration, numeric pitfalls) rendered into the booklet compile-safely |

## Generated Material

| Output | Command |
|--------|---------|
| `booklet.tex` | `uv run python scripts/gen_booklet.py` |
| `booklet.pdf` | `just packet` |
| `docs/assets/booklet.pdf` | `just packet` |
| `site/` | `just docs-build` |

## Packet Workflow

Run this before a study session or interview loop:

```bash
just packet
```

That command regenerates the LaTeX booklet from current code and notes,
compiles the printable PDF, and refreshes the PDF embedded in the docs site.

## Public Boundary

This repository is the public-safe, company-neutral packet. Keep employer
names, interview dates, panel notes, recruiter details, private strategy, and
tailored positioning out of this tree.

Private downstream repositories can depend on `@dsa_study_packet//:booklet`
and compose the neutral PDF with job-specific front or back matter. Those
private supersets own employer-specific context; this repository owns only the
generic study material.

## Downstream Composition (Bazel)

This repo is also a Bazel module (`dsa_study_packet`). `bazel build //:booklet`
compiles the SSOT `booklet.tex` into a cacheable, RBE-friendly PDF graph node.
Private superset repos can depend on `@dsa_study_packet//:booklet` and
`\includepdf` it between company-specific front and back matter. Refresh the
neutral content with `just packet`; downstream lanes pick it up on rebuild.
