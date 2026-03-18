# target employer Interview Study Guide

69 algorithm implementations, 628 tests, 6 concept modules — for a senior
full-stack (backend-focused) interview at
[target employer](https://www.example.com/).

## Quick Start

```bash
direnv allow        # nix devshell + python 3.14 venv
just test           # 628 tests
just lint           # ruff + mypy strict
just docs           # mkdocs site at localhost:8000
```

## Daily Practice (7-day full-coverage cycle)

All 69 algorithms, every day, for 7 days straight. Use challenge mode to
strip each solution and re-implement from scratch against the test suite.

```bash
just challenge arrays two_sum     # strips solution → you implement
just study arrays                 # watch mode — tests re-run on save
just solution arrays two_sum      # peek if stuck
just challenge-done arrays two_sum  # mark complete
just challenge-progress           # see daily stats
```

## Commands

```bash
just                              # list all commands

# ── Testing ──
just test                         # run all 628 tests
just practice <topic>             # run tests for one topic
just study <topic>                # watch mode for a topic
just test-concepts                # concept modules (installs numpy/scipy/flask/pydantic)
just study-concept                # watch mode for concepts

# ── Quality ──
just lint                         # ruff + mypy strict
just fmt                          # auto-format

# ── Challenge mode ──
just challenge <topic> <problem>  # strip solution, show failing tests
just solution <topic> <problem>   # restore full solution
just challenge-done <t> <p>       # mark complete
just challenge-progress           # show progress

# ── Docs & PDF ──
just docs                         # mkdocs serve (localhost:8000)
just docs-build                   # build static site
just docs-deploy                  # deploy to gh-pages
just pdf-booklet                  # printable reference booklet

# ── Scaffolding ──
just new <topic> <name>           # scaffold new problem + test
```

## Project Structure

```
src/algo/         69 implementations across 15 topics
src/concepts/     6 modules: t-strings, typing, hypothesis, FFT, Flask, Pydantic
src/practice/     3 code reading + 3 decomposition exercises
tests/            628 tests (pytest + hypothesis)
reference-sheets/ 9 printable reference sheets
docs/             mkdocs site source
scripts/          gen_algo_pages.py, strip_solution.py
```

### Algorithm Topics

| Topic | # | Highlights |
|-------|---|-----------|
| arrays | 4 | two_sum, group_anagrams, top_k_frequent, product_except_self |
| two_pointers | 3 | three_sum, container_with_most_water, trapping_rain_water |
| sliding_window | 2 | min_window_substring, longest_substring_no_repeat |
| stacks_queues | 3 | valid_parentheses, min_stack, daily_temperatures |
| searching | 3 | binary_search, search_rotated_array, find_minimum_rotated |
| linked_lists | 3 | reverse_linked_list, merge_two_sorted, lru_cache |
| trees | 5 | max_depth, invert_tree, validate_bst, level_order, trie |
| graphs | 13 | dijkstra, a_star, bellman_ford, MST, network_flow, geohash, kd_tree, ... |
| dp | 8 | coin_change, edit_distance, knapsack, TSP, CSP, LIS, LCS, ... |
| heaps | 3 | kth_largest, merge_k_sorted_lists, task_scheduler |
| backtracking | 4 | subsets, permutations, combination_sum, n_queens |
| greedy | 3 | merge_intervals, jump_game, interval_scheduling |
| strings | 5 | valid_palindrome, longest_palindromic_substring, atoi, ... |
| recursion | 5 | pow_x_n, generate_parentheses, flatten_nested_list, hanoi, ... |
| bit_manipulation | 3 | single_number, counting_bits, reverse_bits |
| sorting | 2 | quickselect, merge_sort_inversions |
| patterns | 1 | sliding_window (max_sum_subarray) |

## Reference

- [Cross-Reference Guide](reference-sheets/08-cross-reference-guide.md) — "when to use what" master index
- [Interview Day Guide](reference-sheets/07-interview-day-guide.md) — printouts, tabs, round-by-round strategy
- [Algorithm Templates](reference-sheets/03-algorithm-templates.md) — binary search, BFS/DFS, DP, backtracking
- [CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md) — AI agent configuration
