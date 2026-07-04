# DSA Study Packet

Company-neutral technical-interview training: algorithm implementations with
tests, printable reference sheets, and a whiteboard **performance** method —
because these interviews score how you work out loud, not just what you know.

Code, tests, and authored notes are the single source of truth; every artifact
(printable PDF packet, web site, drills) is generated from them. Employer- or
panel-specific prep lives in private downstream overlays, never in this repo —
see [the contract](docs/guide/source-of-truth.md).

## Quick start

```bash
direnv allow        # nix devshell + Python 3.14 venv
just test           # pytest + hypothesis
just lint           # ruff + mypy strict + public-boundary guard
just docs           # local MkDocs site (drills, visualizer, progress)
just packet         # printable TeX -> PDF booklet
just pdf-all        # every reference sheet -> PDF
```

## The daily drill (board ↔ IDE)

```bash
just study-spaced 1                  # 1. spaced repetition picks today's drill
just interview arrays two_sum        # 2. cold problem: statement only, solution stripped
#    3. at the whiteboard: recording ON, run CLARP out loud (sheet 10)
just study arrays                    # 4. at the IDE: implement until tests pass
just rep "arrays/two_sum C2 L1 A2 R1 P2 <one fix>"   # 5. score the rep (private log)
just challenge-done arrays two_sum   # 6. feed spaced repetition
```

The method — what interviewers actually score, the CLARP loop, panic first-aid,
collaboration scripts, self-review rubric — is
[sheet 10](reference-sheets/10-whiteboard-performance-protocol.md).
The two-week day-by-day ramp is
[sheet 11](reference-sheets/11-14-day-whiteboard-ramp.md).
`just challenge` (statement + approach visible) remains as learning mode.

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

Further implementations stay in the repo as extended practice and reference.

## The overlay pattern

This repo is also a Bazel module (`dsa_study_packet`) exposing one composition
surface: `//:booklet`, the compiled neutral packet PDF. A private downstream
repo can wrap that PDF with its own front/back matter — people, probes,
positioning — without any of that ever touching this tree. The boundary is
machine-enforced (`just public-boundary`), and
[`examples/overlay-demo/`](examples/overlay-demo/) is a self-contained,
fork-me demonstration with placeholder content.

## Cache-first / remote builds

```bash
just remote-build            # //:booklet via GloriousFlywheel shared cache when attached
just remote-test             # bazel test, cache-first
just remote-check            # attachment/contract gate (exits 0 unattached)
```

The [GloriousFlywheel front-door kit](justfile.flywheel) is endpoint-free by
contract: no cache endpoints, tokens, or runner labels are committed; profile
and auth resolve at invocation. Unattached, everything degrades to a local
disk cache. Never call raw `bazel` — drive builds through `just remote-*`.
