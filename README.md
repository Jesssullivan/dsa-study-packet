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
src/algo/              58 algorithm implementations across 15 topics
  arrays/          (4) two_sum, group_anagrams, top_k_frequent, product_except_self
  two_pointers/    (3) three_sum, container_with_most_water, trapping_rain_water
  sliding_window/  (2) longest_substring_no_repeat, min_window_substring
  stacks_queues/   (3) valid_parentheses, min_stack, daily_temperatures
  searching/       (3) binary_search, search_rotated_array, find_minimum_rotated
  linked_lists/    (3) reverse_linked_list, merge_two_sorted, lru_cache
  trees/           (4) max_depth, invert_tree, validate_bst, level_order_traversal
  graphs/         (13) dijkstra, a_star, bellman_ford, topological_sort, MST, ...
  dp/              (8) coin_change, edit_distance, knapsack, TSP, CSP, ...
  heaps/           (3) kth_largest, merge_k_sorted_lists, task_scheduler
  backtracking/    (4) subsets, permutations, combination_sum, n_queens
  greedy/          (3) merge_intervals, jump_game, interval_scheduling
  bit_manipulation/(3) single_number, counting_bits, reverse_bits
  sorting/         (2) quickselect, merge_sort_inversions
  patterns/        (1) sliding_window (max_sum_subarray)
  strings/         (5) valid_palindrome, longest_palindromic_substring, valid_anagram, ...
  recursion/       (5) pow_x_n, generate_parentheses, flatten_nested_list, ...

src/concepts/      6 instructional modules (t-strings, typing, hypothesis, FFT, Flask, Pydantic)
src/practice/      Interview simulation exercises
  code_reading/    3 exercises for "Practical Problem Solving" round
  decomposition/   3 exercises for "Problem Decomposition" round

tests/             606 tests mirroring src/ structure (pytest + hypothesis)
reference-sheets/  9 printable reference sheets (01-08 + Python 3.14 patterns)
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

1. [Python Standard Library](reference-sheets/01-python-stdlib.md) — collections, itertools, functools, heapq, bisect
2. [Data Structures](reference-sheets/02-data-structures.md) — Big-O tables, implementation templates
3. [Algorithm Templates](reference-sheets/03-algorithm-templates.md) — binary search, BFS/DFS, DP, backtracking, etc.
4. [Python 3.14 & Modern Patterns](reference-sheets/03-python-314-and-modern-patterns.md) — PEP 750, typing, hypothesis, pytest
5. [Big-O Complexity](reference-sheets/04-big-o-complexity.md) — complexity tables, input size guidance
6. [Common Patterns](reference-sheets/05-common-patterns.md) — problem-type-to-algorithm mapping
7. [System Design](reference-sheets/06-system-design.md) — load balancing, caching, distributed systems, geospatial
8. [Interview Day Guide](reference-sheets/07-interview-day-guide.md) — printouts, browser tabs, round-by-round strategy
9. [Cross-Reference Guide](reference-sheets/08-cross-reference-guide.md) — "when to use what" master index

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
