# target employer Interview Study Guide

Prepping for a senior full-stack (backend-focused) algorithm interview at
[target employer](https://www.example.com/). target employer builds the
domain platform platform for aviation route optimization (Python + Rust backend,
React/TS frontend, AWS/K8s infra, ML).

## Quick Start

```bash
direnv allow   # activates nix devshell + python venv
just test      # run all tests
```

## Project Structure

```
src/algo/           Algorithm implementations by topic
  arrays/           two_sum, group_anagrams, product_except_self, ...
  two_pointers/     three_sum, container_with_most_water, ...
  sliding_window/   longest_substring_no_repeat, min_window_substring
  linked_lists/     reverse_linked_list, merge_two_sorted, lru_cache
  stacks_queues/    valid_parentheses
  graphs/           number_of_islands, clone_graph
  trees/            (in progress)
  dp/               (in progress)
  greedy/           (in progress)
  heaps/            (in progress)
  backtracking/     (in progress)
  searching/        (in progress)
  sorting/          (in progress)
  strings/          (in progress)
  bit_manipulation/ (in progress)
  recursion/        (in progress)

src/concepts/       Instructional modules: t-strings, typing, Flask, FFT/DCT, validation, hypothesis
src/practice/       Interview simulation exercises
  code_reading/     "Practical Problem Solving" round prep
  decomposition/    "Problem Decomposition" round prep

tests/              Mirrors src/algo/ structure; pytest
reference-sheets/   Printable cheat sheets (Markdown + PDF)
reference/          Supplementary notes and resources
```

## Just Commands

| Command | Description |
|---|---|
| `just test` | Run all tests |
| `just practice <topic>` | Run tests for a specific topic |
| `just study <topic>` | Watch mode for a topic (re-runs on save) |
| `just bench` | Run benchmark suite |
| `just lint` | Ruff linter + mypy |
| `just fmt` | Format with ruff |
| `just new <topic> <name>` | Scaffold a new problem + test file |
| `just test-concepts` | Run concept module tests (installs optional deps) |
| `just study-concept` | Watch mode for concept modules (re-runs on save) |
| `just pdf-all` | Convert all reference sheets to PDF |
| `just pdf-booklet` | Combine sheets into one printable booklet |

## Interview Structure (5 Rounds)

1. **Algorithms** (75 min) -- LeetCode medium to medium-hard. Graph problems, DP,
   string manipulation. Python preferred.
2. **Practical Problem Solving** -- Read existing code, identify bugs and
   performance issues, suggest improvements. Simulates real code review.
3. **Problem Decomposition** -- Break an ambiguous problem into sub-problems,
   define interfaces, discuss tradeoffs. Think out loud.
4. **System Design** (L7+ / Staff) -- Design real-time data pipelines, geospatial
   APIs, streaming architectures. domain flavored.
5. **CEO Chat** -- Culture fit, motivation, career trajectory.

## Reference Sheets

1. [Python Standard Library](reference-sheets/01-python-stdlib.md)
2. [Data Structures](reference-sheets/02-data-structures.md)
3. [Algorithm Templates](reference-sheets/03-algorithm-templates.md)
4. [Big-O Complexity](reference-sheets/04-big-o-complexity.md)
5. [Common Patterns](reference-sheets/05-common-patterns.md)
6. [System Design](reference-sheets/06-system-design.md)
7. [Interview Day Guide](reference-sheets/07-interview-day-guide.md)

## Concept Modules

Interactive instructional modules in `src/concepts/` covering topics beyond pure algorithm
prep. Each module is a standalone Python file with docstrings, examples, and companion
tests in `tests/concepts/`. Run with `just test-concepts` or `just study-concept` (watch mode).

| Module | File | Topic |
|--------|------|-------|
| T-Strings | `src/concepts/t_strings.py` | PEP 750 template strings (Python 3.14+). Lazy interpolation, safe SQL/HTML templating. |
| Advanced Typing | `src/concepts/advanced_typing.py` | Modern Python type system: `Protocol`, `TypeVar`, `ParamSpec`, `TypeGuard`, `@overload`. |
| Hypothesis Patterns | `src/concepts/hypothesis_patterns.py` | Property-based testing with Hypothesis. Strategies, `@given`, `@composite`, stateful testing. |
| FFT / DCT | `src/concepts/fft_dct.py` | Signal processing fundamentals: FFT, inverse FFT, DCT, frequency analysis with NumPy/SciPy. |
| Modern Flask | `src/concepts/modern_flask.py` | Flask 3.x patterns: async views, class-based views, nested blueprints, error handling. |
| Validation | `src/concepts/validation.py` | Data validation with Pydantic v2: model validators, discriminated unions, serialization. |

## Cross-Reference Guide

See [reference-sheets/08-cross-reference-guide.md](reference-sheets/08-cross-reference-guide.md) —
the "when to use what" master reference mapping problem types to implementations in this repo.

## For AI Agents

- [CLAUDE.md](CLAUDE.md) — project instructions for Claude Code
- [AGENTS.md](AGENTS.md) — agent workflows, MCP servers, pre/post interview automation
