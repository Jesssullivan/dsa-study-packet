---
title: Learning Paths
---

# Learning Paths

!!! abstract "What this page is"
    Four curated sequences through the existing drills in `src/algo/`. Each path
    has **prerequisites**, an **ordered problem list** (real problem names you can
    drill verbatim), a one-line **why this order**, and the exact **challenge-mode
    commands**. Work a path top to bottom: every step reuses an idea from the step
    before it.

The [decision tree](when-to-use-what.md) tells you *which* pattern a problem
needs. These paths tell you *what order* to learn the patterns in so each one
builds on the last.

---

## The universal drill loop

Every problem in every path is drilled the same way. Challenge mode strips the
solution body so you re-implement from the signature and docstring alone, then
restores it on demand.

```bash
just challenge <topic> <problem>   # strip the solution body, show failing tests
just study <topic>                 # watch mode: tests re-run on every save
just solution <topic> <problem>    # restore the reference solution if stuck
just challenge-done <topic> <problem>
just challenge-progress            # see what you have cleared
```

`<topic>` is the directory under `src/algo/` (e.g. `two_pointers`,
`stacks_queues`, `sliding_window`); `<problem>` is the file stem
(e.g. `three_sum`). The per-path tables below give you the exact pairs.

!!! tip "One screen, two panes"
    Open `just study <topic>` in a watcher pane and edit in the other. Green tests
    mean the drill is done. New to the format? Start at the
    [challenge guide](../challenges/index.md).

---

## Choosing a path

| Path | What you build | Prerequisites | Core drills |
|------|----------------|---------------|-------------|
| **1 · Foundations** | Scanning a sequence with auxiliary state | Python fluency, [Big-O basics](../reference/04-big-o-complexity.md) | 11 |
| **2 · Graphs & Trees** | Traversal, ordering, weighted/heuristic search | Path 1, [data-structure sheet](../reference/02-data-structures.md) | 16 |
| **3 · DP & Backtracking** | Recursion trees, then memoized optimization | Path 1, recursion comfort | 16 |
| **4 · Systems & CS Fundamentals** | Building-block structures + the theory behind them | Path 1, [system-design sheet](../reference/06-system-design.md) | 14 + appendix |

!!! note "Suggested sequencing"
    Do **Foundations first** — every other path leans on hashing, pointers, and
    stack/queue mechanics. After that, Graphs & Trees and DP & Backtracking are
    independent; do them in either order. Take Systems & CS Fundamentals last:
    it ties the appendix theory back to structures you have already drilled.

---

## Path 1 · Foundations

!!! abstract "Goal"
    Learn to walk a sequence once while carrying just enough auxiliary state —
    a hash map, a pair of pointers, or a window. This is the substrate for
    everything else.

**Prerequisites:** comfortable Python; know array/dict/set costs from the
[Big-O sheet](../reference/04-big-o-complexity.md).

!!! tip "Why this order"
    Hashing → pointer movement → windows → stacks: each step keeps the
    single-pass scan and adds exactly one new piece of bookkeeping.

| # | Problem | What it teaches |
|---|---------|-----------------|
| 1 | [`arrays/two_sum`](../algorithms/arrays/two_sum.md) | Trade space for time with a hash map |
| 2 | [`arrays/group_anagrams`](../algorithms/arrays/group_anagrams.md) | Hash a *canonical key*, not the value |
| 3 | [`arrays/product_except_self`](../algorithms/arrays/product_except_self.md) | Prefix/suffix passes without division |
| 4 | [`two_pointers/three_sum`](../algorithms/two_pointers/three_sum.md) | Sort, then converge two pointers |
| 5 | [`two_pointers/container_with_most_water`](../algorithms/two_pointers/container_with_most_water.md) | Move the pointer that can only help |
| 6 | [`two_pointers/trapping_rain_water`](../algorithms/two_pointers/trapping_rain_water.md) | Pointers plus running maxima |
| 7 | [`sliding_window/longest_substring_no_repeat`](../algorithms/sliding_window/longest_substring_no_repeat.md) | Variable window + a seen-set |
| 8 | [`sliding_window/min_window_substring`](../algorithms/sliding_window/min_window_substring.md) | Window with need/have counts |
| 9 | [`stacks_queues/valid_parentheses`](../algorithms/stacks_queues/valid_parentheses.md) | LIFO matching |
| 10 | [`stacks_queues/daily_temperatures`](../algorithms/stacks_queues/daily_temperatures.md) | Monotonic stack for "next greater" |
| 11 | [`stacks_queues/min_stack`](../algorithms/stacks_queues/min_stack.md) | Design: O(1) min via an auxiliary stack |

??? note "Drill commands (run in order)"
    ```bash
    just challenge arrays two_sum
    just challenge arrays group_anagrams
    just challenge arrays product_except_self
    just challenge two_pointers three_sum
    just challenge two_pointers container_with_most_water
    just challenge two_pointers trapping_rain_water
    just challenge sliding_window longest_substring_no_repeat
    just challenge sliding_window min_window_substring
    just challenge stacks_queues valid_parentheses
    just challenge stacks_queues daily_temperatures
    just challenge stacks_queues min_stack
    ```

!!! example "Extensions when this clicks"
    The reusable window skeleton lives in `patterns/sliding_window`
    (`just challenge patterns sliding_window`). Reinforce with the string
    drills: [`strings/valid_anagram`](../algorithms/strings/valid_anagram.md) and
    [`strings/valid_palindrome`](../algorithms/strings/valid_palindrome.md) (hashing
    and two pointers on text), plus
    [`arrays/top_k_frequent`](../algorithms/arrays/top_k_frequent.md).

---

## Path 2 · Graphs & Trees

!!! abstract "Goal"
    Move from traversing acyclic trees to general graphs, then layer on
    dependency ordering, edge weights, and heuristics.

**Prerequisites:** Path 1 (recursion, stack/queue mechanics); skim the
[data-structure sheet](../reference/02-data-structures.md) for adjacency lists,
queues, and union-find.

!!! tip "Why this order"
    A tree is a graph with no cycles — master traversal there, then generalize to
    BFS/DFS, ordering, weights, and finally global structure (MST, flow).

| # | Problem | What it teaches |
|---|---------|-----------------|
| 1 | [`trees/max_depth`](../algorithms/trees/max_depth.md) | Recursion baseline on a tree |
| 2 | [`trees/invert_tree`](../algorithms/trees/invert_tree.md) | Structural recursion |
| 3 | [`trees/level_order_traversal`](../algorithms/trees/level_order_traversal.md) | BFS with a queue |
| 4 | [`trees/validate_bst`](../algorithms/trees/validate_bst.md) | DFS carrying bounds / inorder |
| 5 | [`trees/trie`](../algorithms/trees/trie.md) | Design a multiway prefix tree |
| 6 | [`graphs/number_of_islands`](../algorithms/graphs/number_of_islands.md) | Grid DFS/BFS flood fill |
| 7 | [`graphs/clone_graph`](../algorithms/graphs/clone_graph.md) | Traversal + a visited map |
| 8 | [`graphs/course_schedule`](../algorithms/graphs/course_schedule.md) | Cycle detection in a DAG |
| 9 | [`graphs/topological_sort`](../algorithms/graphs/topological_sort.md) | Dependency ordering (Kahn / DFS) |
| 10 | [`graphs/word_ladder`](../algorithms/graphs/word_ladder.md) | BFS shortest path on an *implicit* graph |
| 11 | [`graphs/dijkstra`](../algorithms/graphs/dijkstra.md) | Weighted shortest path (non-negative) |
| 12 | [`graphs/network_delay_time`](../algorithms/graphs/network_delay_time.md) | Apply Dijkstra to a real prompt |
| 13 | [`graphs/bellman_ford`](../algorithms/graphs/bellman_ford.md) | Negative edges, relaxation |
| 14 | [`graphs/a_star_search`](../algorithms/graphs/a_star_search.md) | Heuristic-guided search |
| 15 | [`graphs/minimum_spanning_tree`](../algorithms/graphs/minimum_spanning_tree.md) | Global structure + union-find |
| 16 | [`graphs/network_flow`](../algorithms/graphs/network_flow.md) | Max flow / min cut (capstone) |

??? note "Drill commands (run in order)"
    ```bash
    just challenge trees max_depth
    just challenge trees invert_tree
    just challenge trees level_order_traversal
    just challenge trees validate_bst
    just challenge trees trie
    just challenge graphs number_of_islands
    just challenge graphs clone_graph
    just challenge graphs course_schedule
    just challenge graphs topological_sort
    just challenge graphs word_ladder
    just challenge graphs dijkstra
    just challenge graphs network_delay_time
    just challenge graphs bellman_ford
    just challenge graphs a_star_search
    just challenge graphs minimum_spanning_tree
    just challenge graphs network_flow
    ```

!!! example "Spatial extensions"
    For nearest-neighbor and proximity prompts, drill
    [`graphs/geohash_grid`](../algorithms/graphs/geohash_grid.md) and
    [`graphs/kd_tree`](../algorithms/graphs/kd_tree.md).

---

## Path 3 · DP & Backtracking

!!! abstract "Goal"
    See the recursion tree first (backtracking enumerates it), then collapse
    overlapping subproblems into dynamic programming.

**Prerequisites:** Path 1; be comfortable writing and tracing recursion.

!!! tip "Why this order"
    Backtracking makes the recursion tree concrete; DP is "the same recursion,
    but memoized once you notice the overlap" — so the sequence grows recursion →
    backtracking → 1D DP → 2D DP → bitmask DP.

| # | Problem | What it teaches |
|---|---------|-----------------|
| 1 | [`recursion/pow_x_n`](../algorithms/recursion/pow_x_n.md) | Divide-and-conquer recursion |
| 2 | [`recursion/tower_of_hanoi`](../algorithms/recursion/tower_of_hanoi.md) | Classic recursive decomposition |
| 3 | [`recursion/generate_parentheses`](../algorithms/recursion/generate_parentheses.md) | Recursion under a constraint |
| 4 | [`backtracking/subsets`](../algorithms/backtracking/subsets.md) | The choose / explore / unchoose skeleton |
| 5 | [`backtracking/permutations`](../algorithms/backtracking/permutations.md) | Used-set bookkeeping |
| 6 | [`backtracking/combination_sum`](../algorithms/backtracking/combination_sum.md) | Reuse elements + pruning |
| 7 | [`recursion/letter_combinations_phone`](../algorithms/recursion/letter_combinations_phone.md) | Cartesian-product backtracking |
| 8 | [`backtracking/n_queens`](../algorithms/backtracking/n_queens.md) | Constraint pruning at scale |
| 9 | [`dp/climbing_stairs`](../algorithms/dp/climbing_stairs.md) | Turn a recurrence into 1D DP |
| 10 | [`dp/coin_change`](../algorithms/dp/coin_change.md) | Unbounded DP, minimize cost |
| 11 | [`dp/knapsack`](../algorithms/dp/knapsack.md) | 0/1 DP, space-optimized |
| 12 | [`dp/longest_increasing_subseq`](../algorithms/dp/longest_increasing_subseq.md) | DP + binary search |
| 13 | [`dp/longest_common_subseq`](../algorithms/dp/longest_common_subseq.md) | 2D DP over two strings |
| 14 | [`dp/edit_distance`](../algorithms/dp/edit_distance.md) | 2D DP with three transitions |
| 15 | [`dp/constraint_satisfaction`](../algorithms/dp/constraint_satisfaction.md) | DP under explicit constraints |
| 16 | [`dp/traveling_salesman_dp`](../algorithms/dp/traveling_salesman_dp.md) | Bitmask DP (capstone) |

??? note "Drill commands (run in order)"
    ```bash
    just challenge recursion pow_x_n
    just challenge recursion tower_of_hanoi
    just challenge recursion generate_parentheses
    just challenge backtracking subsets
    just challenge backtracking permutations
    just challenge backtracking combination_sum
    just challenge recursion letter_combinations_phone
    just challenge backtracking n_queens
    just challenge dp climbing_stairs
    just challenge dp coin_change
    just challenge dp knapsack
    just challenge dp longest_increasing_subseq
    just challenge dp longest_common_subseq
    just challenge dp edit_distance
    just challenge dp constraint_satisfaction
    just challenge dp traveling_salesman_dp
    ```

!!! example "Greedy coda — when greedy beats DP"
    Some optimization prompts have no overlapping subproblems and a local choice
    is provably optimal. Contrast DP with
    [`greedy/merge_intervals`](../algorithms/greedy/merge_intervals.md),
    [`greedy/jump_game`](../algorithms/greedy/jump_game.md), and
    [`greedy/interval_scheduling`](../algorithms/greedy/interval_scheduling.md).
    Also drill [`recursion/flatten_nested_list`](../algorithms/recursion/flatten_nested_list.md)
    for recursion over nested structure.

---

## Path 4 · Systems & CS Fundamentals

!!! abstract "Goal"
    Build the data structures that systems are made of — search, sort, heaps,
    lists, bits — then read the appendix theory that explains why they perform
    the way they do.

**Prerequisites:** Path 1; comfortable [reading code](../practice/index.md); skim
the [system-design](../reference/06-system-design.md) and
[interview-day](../reference/07-interview-day-guide.md) sheets.

!!! tip "Why this order"
    Drill the building-block structures first, then study the appendix concepts
    (hashing internals, amortized analysis, concurrency, recursion→iteration,
    numeric pitfalls) against the very drills that exhibit them.

| # | Problem | What it teaches |
|---|---------|-----------------|
| 1 | [`searching/binary_search`](../algorithms/searching/binary_search.md) | Loop-invariant discipline |
| 2 | [`searching/find_minimum_rotated`](../algorithms/searching/find_minimum_rotated.md) | Binary search on a pivot |
| 3 | [`searching/search_rotated_array`](../algorithms/searching/search_rotated_array.md) | Binary search on transformed input |
| 4 | [`sorting/quickselect`](../algorithms/sorting/quickselect.md) | Partition-based selection (expected O(n)) |
| 5 | [`sorting/merge_sort_inversions`](../algorithms/sorting/merge_sort_inversions.md) | Divide-and-conquer + counting |
| 6 | [`heaps/kth_largest`](../algorithms/heaps/kth_largest.md) | Heap of size k |
| 7 | [`heaps/merge_k_sorted_lists`](../algorithms/heaps/merge_k_sorted_lists.md) | k-way merge with a heap |
| 8 | [`heaps/task_scheduler`](../algorithms/heaps/task_scheduler.md) | Heap + greedy scheduling |
| 9 | [`linked_lists/reverse_linked_list`](../algorithms/linked_lists/reverse_linked_list.md) | Pointer surgery |
| 10 | [`linked_lists/merge_two_sorted`](../algorithms/linked_lists/merge_two_sorted.md) | Merge on linked nodes |
| 11 | [`linked_lists/lru_cache`](../algorithms/linked_lists/lru_cache.md) | Design: hash map + doubly linked list |
| 12 | [`bit_manipulation/single_number`](../algorithms/bit_manipulation/single_number.md) | XOR identities |
| 13 | [`bit_manipulation/counting_bits`](../algorithms/bit_manipulation/counting_bits.md) | DP over bit patterns |
| 14 | [`bit_manipulation/reverse_bits`](../algorithms/bit_manipulation/reverse_bits.md) | Fixed-width bit operations |

??? note "Drill commands (run in order)"
    ```bash
    just challenge searching binary_search
    just challenge searching find_minimum_rotated
    just challenge searching search_rotated_array
    just challenge sorting quickselect
    just challenge sorting merge_sort_inversions
    just challenge heaps kth_largest
    just challenge heaps merge_k_sorted_lists
    just challenge heaps task_scheduler
    just challenge linked_lists reverse_linked_list
    just challenge linked_lists merge_two_sorted
    just challenge linked_lists lru_cache
    just challenge bit_manipulation single_number
    just challenge bit_manipulation counting_bits
    just challenge bit_manipulation reverse_bits
    ```

### Appendix reading (study, don't drill)

These topics ship in the printable [packet](../index.md#printable-packet)
(rendered from `reference-sheets/appendix-topics.json`). Pair each with the drill
that makes it concrete:

| Appendix topic | Read it alongside |
|----------------|-------------------|
| Hash Table Internals | `arrays/two_sum`, `arrays/group_anagrams`, `linked_lists/lru_cache` |
| Amortized Analysis | `stacks_queues/daily_temperatures`, `sorting/quickselect`, dynamic arrays |
| Concurrency & Parallelism Primitives | `heaps/task_scheduler` |
| Recursion to Iteration Conversion | `recursion/tower_of_hanoi`, `recursion/pow_x_n`, `recursion/flatten_nested_list` |
| Fixed-Width & Numeric Pitfalls | `bit_manipulation/reverse_bits`, `bit_manipulation/single_number`, `strings/string_to_integer_atoi` |

---

## Pacing a path

How you spread the drills matters more than how fast you finish. Pick the cadence
that fits your timeline.

=== "2-week sprint"

    - **Days 1-4:** Path 1 end to end; re-drill any red ones the next morning.
    - **Days 5-9:** One of Path 2 or Path 3 (whichever your loop weighs more).
    - **Days 10-12:** The other half of that path + the greedy/spatial extensions.
    - **Days 13-14:** Path 4 building blocks + skim the appendix table.

=== "4-week deep"

    - **Week 1:** Path 1, plus the string and `patterns/sliding_window` extensions.
    - **Week 2:** Path 2 (trees → graphs → weighted → MST/flow).
    - **Week 3:** Path 3 (recursion → backtracking → DP → bitmask) + greedy coda.
    - **Week 4:** Path 4 structures, then read every appendix topic against its drill.

=== "Daily maintenance"

    Once a path is green, keep it warm: `just challenge` two or three problems a
    day across paths and track streaks with `just challenge-progress`. Spaced
    re-drilling beats one-time completion.

!!! note "Spaced repetition"
    A problem only counts when you can re-implement it cold. Use
    `just solution <topic> <problem>` sparingly — peeking resets the clock on that
    drill. Cleared everything? The [cross-reference guide](../reference/08-cross-reference-guide.md)
    maps each pattern back to its implementation for review.
