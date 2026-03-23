# CLAUDE.md — Project Instructions for Claude Code

## Project Overview

Algorithm interview study guide for a senior full-stack (backend-focused) role at
target employer (target employer). Python 3.14+, strict typing, property-based testing.

## Quick Reference

```bash
just test              # run all 647 tests
just lint              # ruff + mypy strict
just practice graphs   # run tests for a specific topic
just study dp          # watch mode for a topic
just test-concepts     # run concept module tests (installs numpy/scipy/flask/pydantic)
just new <topic> <name>  # scaffold new problem + test
just pdf-booklet       # printable reference booklet
```

## Code Conventions

### Source files (`src/algo/{topic}/{problem}.py`)
- Module docstring: Problem statement, Approach, Complexity (Time + Space)
- Fully typed (Python 3.14, mypy strict, `explicit_package_bases = true`)
- Use `Sequence` for read-only collection params, `list` for return types
- Doctest examples in function docstrings
- Minimal comments — only for non-obvious logic

### Test files (`tests/{topic}/test_{problem}.py`)
- Class-based: `class TestFunctionName:`
- 4-6 test cases: basic, edge cases, error cases
- Hypothesis `@given` property tests where valuable (brute-force comparison, roundtrip, invariants)
- No fixtures unless truly needed — keep tests self-contained

### Concept modules (`src/concepts/{concept}.py`)
- Heavy inline comments explaining each concept
- Web reference URLs (PEPs, docs, blogs) as comments
- Sectioned with `# ──────` dividers
- Paired tests are educational — comments explain what's being tested
- External deps use `pytest.importorskip()` so `just test` works without them

## Project Structure

```
src/algo/          68 implementations across 15 topics
src/concepts/      7 instructional modules (t-strings, typing, hypothesis, benchmarking, FFT, Flask, Pydantic)
src/practice/      3 code reading + 3 decomposition exercises
tests/             647 tests mirroring src/ (pytest + hypothesis)
reference-sheets/  9 reference sheets (01-08 + Python 3.14 patterns)
```

## Key Files

- `RESEARCH.md` — target employer company research, tech stack, products
- `algorithm-interview-resources.md` — books, platforms, YouTube, domain resources
- `reference-sheets/07-interview-day-guide.md` — test day printouts, tabs, strategies
- `AGENTS.md` — how to use AI agents with this repo

## When Adding New Problems

1. `just new <topic> <problem>` to scaffold
2. Implement in `src/algo/{topic}/{problem}.py` — follow existing style
3. Write tests in `tests/{topic}/test_{problem}.py`
4. Run `just lint` before considering it done
5. Add a "When to use" comment in the docstring

## Domain Context

target employer builds the domain platform platform for aviation route optimization. Their stack:
- **Backend**: Python, Rust
- **Frontend**: React, TypeScript
- **Infra**: AWS, Kubernetes
- **ML**: Transformers, LightGBM, time-series forecasting
- **Domain**: geospatial indexing, graph algorithms, real-time streaming, weather data

Graph algorithms (A*, Dijkstra, Bellman-Ford), geospatial data structures (geohash, KD-tree),
and optimization problems are especially relevant.

## Lint Rules

- **ruff**: pyflakes, pycodestyle, isort, pep8-naming, pyupgrade, bugbear, comprehensions,
  simplify, type-checking, pytest-style, return, unused-args, eradicate
- **mypy**: strict mode, explicit_package_bases, warn_unreachable
- **TC003 suppressed**: PEP 649 lazy annotations make TYPE_CHECKING blocks unnecessary noise
- **practice/ ignored by mypy**: intentionally buggy code for reading exercises
