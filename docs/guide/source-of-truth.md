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
