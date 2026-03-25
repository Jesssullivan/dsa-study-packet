I am pleased to announce I will never need to do another DSA / FAANG style interview again.   I'll just politely decline.  I encurage you to decline and disparage such interview practices too.  ^w^  




---


## Quick Start

```bash
direnv allow        # nix devshell + python 3.14 venv
just test           # 628 tests
just lint           # ruff + mypy strict
just docs           # mkdocs site at localhost:8000
```



```bash
just challenge arrays two_sum     # strip solution → implement
just study arrays                 # watch mode — tests re-run on save
just solution arrays two_sum      # peek if stuck
just challenge-done arrays two_sum
just challenge-progress
```

### Core 42

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

The remaining 27 implementations stay in the repo as extended practice and reference.

## Commands

```bash
just                              # list all commands

# ── Testing ──
just test                         # all 628 tests
just practice <topic>             # one topic
just study <topic>                # watch mode
just test-concepts                # concept modules (numpy/scipy/flask/pydantic)

# ── Challenge ──
just challenge <topic> <problem>  # strip solution, show failing tests
just solution <topic> <problem>   # restore solution
just challenge-done <t> <p>       # mark complete
just challenge-progress           # show progress

# ── Quality ──
just lint                         # ruff + mypy strict
just fmt                          # auto-format

# ── Docs ──
just docs                         # mkdocs serve
just pdf-booklet                  # printable reference booklet
```

## Structure

```
src/algo/         69 implementations, 15 topics (42 core + 27 extended)
src/concepts/     6 modules: t-strings, typing, hypothesis, FFT, Flask, Pydantic
src/practice/     3 code reading + 3 decomposition exercises
tests/            628 tests (pytest + hypothesis)
reference-sheets/ 9 printable reference sheets
docs/             mkdocs site
```

## Reference

- [Cross-Reference Guide](reference-sheets/08-cross-reference-guide.md) — pattern → implementation lookup
- [Interview Day Guide](reference-sheets/07-interview-day-guide.md) — printouts, tabs, strategy
- [Algorithm Templates](reference-sheets/03-algorithm-templates.md) — binary search, BFS/DFS, DP, backtracking
