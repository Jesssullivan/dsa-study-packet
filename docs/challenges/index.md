---
title: Practice Drills
---

# Practice Drills

Let the review queue choose the next problem, or select one when you know the
skill you want to isolate. One rep should produce one useful correction, not a
larger solve count.

## Start in the editor

Choose a comment format in Copilot Chat:

```text
/reacto
/clarp
/umpire
/comments
```

No arguments are needed. To select a drill, add its topic and name, such as
`/clarp graphs dijkstra`. The direct terminal equivalent is:

```bash
just practice-start clarp graphs dijkstra
```

Fill the comments in your source file, save, and remove the `THINKING GATE`
yourself. Then implement and add cases in your test file. Use `/continue` or
`just practice-next` for one next instruction.

```bash
just practice-test
just practice-repl
just practice-finish "one fix"
```

## Core 43

The core set covers common patterns across sessions. `just catalog` prints all
editor-practice targets and marks each Core or Extra. Add natural names to
search; ambiguous words such as `anagram` and `prime` keep every valid choice.

| Topic | Problems |
|-------|----------|
| Arrays | `two_sum`, `group_anagrams`, `product_except_self`, `top_k_frequent` |
| Two pointers | `three_sum`, `trapping_rain_water` |
| Sliding window | `min_window_substring`, `longest_substring_no_repeat` |
| Stacks and queues | `valid_parentheses`, `daily_temperatures` |
| Searching | `binary_search`, `search_rotated_array` |
| Linked lists | `reverse_linked_list`, `lru_cache` |
| Trees | `validate_bst`, `level_order_traversal`, `trie` |
| Graphs | `number_of_islands`, `topological_sort`, `course_schedule`, `dijkstra`, `a_star_search`, `bellman_ford`, `minimum_spanning_tree` |
| Dynamic programming | `coin_change`, `edit_distance`, `knapsack`, `longest_increasing_subseq`, `longest_common_subseq` |
| Heaps | `kth_largest`, `merge_k_sorted_lists` |
| Backtracking | `subsets`, `combination_sum`, `n_queens` |
| Greedy | `merge_intervals`, `jump_game` |
| Strings | `valid_palindrome`, `longest_palindromic_substring` |
| Recursion | `generate_parentheses`, `flatten_nested_list` |
| Bit manipulation | `single_number` |
| Sorting | `quickselect` |
| Math | `sieve_of_eratosthenes` |

Choose by the signal you want to improve: restating the problem, selecting an
example, recognizing a pattern, implementing cleanly, testing, or explaining
complexity. The [decision tree](../guide/when-to-use-what.md) helps with
pattern selection. Inspect the [algorithm library](../algorithms/index.md)
after the rep reaches a natural stopping point.

## More practice

The repository includes additional problems in the same topic directories.
Any entry from `just catalog` can start with `just practice-start`. Use the
[learning paths](../guide/learning-paths.md) when you want a curated order, or
[Advanced Exercises](../practice/index.md) for code reading and open-ended
decomposition.

Untimed conversation and timed board-style reps can use the same catalog. The
editor workspace is the default surface, not the only valid one.
