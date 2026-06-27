# DSA Study Packet

Company-neutral study material for technical interviews that expect whiteboarding,
algorithm fluency, system design discussion, and printable non-electronic notes.

The repo is organized so source code, tests, and authored notes are the source of
truth. The web docs, TeX, and PDF packet are generated from those materials.
Employer-specific interview prep belongs in private downstream supersets, not
in this repository.

## Quick Start

```bash
direnv allow        # nix devshell + Python 3.14 venv
just test           # pytest + hypothesis
just lint           # ruff + mypy strict
just docs           # local MkDocs site
just packet         # latest printable TeX -> PDF packet
```

## Source Of Truth

| Path | Role |
|------|------|
| `src/algo/` | Implementations and docstrings for DSA study |
| `tests/` | Examples, properties, and correctness checks |
| `src/concepts/` | Supporting technical concepts: typing, validation, Flask, FFT/DCT, benchmarking |
| `src/practice/` | Code-reading and decomposition drills |
| `reference-sheets/` | Authored printable notes and quick-reference sheets |
| `scripts/gen_booklet.py` | Builds the printable LaTeX packet from code and notes |
| `scripts/gen_algo_pages.py` | Builds MkDocs algorithm pages from code docstrings |

Generated artifacts:

| Artifact | Command |
|----------|---------|
| `booklet.tex` | `uv run python scripts/gen_booklet.py` |
| `booklet.pdf` | `just packet` |
| `docs/assets/booklet.pdf` | `just packet` |
| `site/` | `just docs-build` |

## Daily Drill

```bash
just challenge arrays two_sum     # strip solution -> implement
just study arrays                 # watch mode, tests re-run on save
just solution arrays two_sum      # restore solution if stuck
just challenge-done arrays two_sum
just challenge-progress
```

## Core 42

| Topic | # | Drill set |
|-------|---|-----------|
| arrays | 3 | two_sum, group_anagrams, product_except_self |
| two_pointers | 2 | three_sum, trapping_rain_water |
| sliding_window | 2 | min_window_substring, longest_substring_no_repeat |
| stacks_queues | 2 | valid_parentheses, daily_temperatures |
| searching | 2 | binary_search, search_rotated_array |
| linked_lists | 2 | reverse_linked_list, lru_cache |
| trees | 3 | validate_bst, level_order_traversal, trie |
| graphs | 7 | dijkstra, a_star, bellman_ford, topo_sort, islands, MST, course_schedule |
| dp | 5 | coin_change, edit_distance, knapsack, LIS, LCS |
| heaps | 2 | kth_largest, merge_k_sorted_lists |
| backtracking | 3 | subsets, combination_sum, n_queens |
| greedy | 2 | merge_intervals, jump_game |
| strings | 2 | valid_palindrome, longest_palindromic_substring |
| recursion | 2 | generate_parentheses, flatten_nested_list |
| bit_manipulation | 1 | single_number |
| sorting | 1 | quickselect |

The remaining implementations stay in the repo as extended practice and
reference material.
