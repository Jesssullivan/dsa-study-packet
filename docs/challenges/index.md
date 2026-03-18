---
title: Daily Drill
---

# Daily Drill

42 core algorithms. All of them. Every day. Seven days.

Challenge mode strips each implementation, leaving the signature and docstring.
You re-implement from scratch and run tests to verify.

---

## How It Works

```bash
just challenge <topic> <problem>  # strip solution → you implement
just study <topic>                # watch mode — re-runs tests on save
just solution <topic> <problem>   # restore if stuck
just challenge-done <t> <p>       # mark complete
just challenge-progress           # see stats
```

---

## The 42

Copy-paste the full block to strip all 42 at once, or work topic by topic.

### Arrays (3)

```bash
just challenge arrays two_sum
just challenge arrays group_anagrams
just challenge arrays product_except_self
```

### Two Pointers (2)

```bash
just challenge two_pointers three_sum
just challenge two_pointers trapping_rain_water
```

### Sliding Window (2)

```bash
just challenge sliding_window min_window_substring
just challenge sliding_window longest_substring_no_repeat
```

### Stacks & Queues (2)

```bash
just challenge stacks_queues valid_parentheses
just challenge stacks_queues daily_temperatures
```

### Searching (2)

```bash
just challenge searching binary_search
just challenge searching search_rotated_array
```

### Linked Lists (2)

```bash
just challenge linked_lists reverse_linked_list
just challenge linked_lists lru_cache
```

### Trees (3)

```bash
just challenge trees validate_bst
just challenge trees level_order_traversal
just challenge trees trie
```

### Graphs (7)

```bash
just challenge graphs number_of_islands
just challenge graphs topological_sort
just challenge graphs course_schedule
just challenge graphs dijkstra
just challenge graphs a_star_search
just challenge graphs bellman_ford
just challenge graphs minimum_spanning_tree
```

### Dynamic Programming (5)

```bash
just challenge dp coin_change
just challenge dp edit_distance
just challenge dp knapsack
just challenge dp longest_increasing_subseq
just challenge dp longest_common_subseq
```

### Heaps (2)

```bash
just challenge heaps kth_largest
just challenge heaps merge_k_sorted_lists
```

### Backtracking (3)

```bash
just challenge backtracking subsets
just challenge backtracking combination_sum
just challenge backtracking n_queens
```

### Greedy (2)

```bash
just challenge greedy merge_intervals
just challenge greedy jump_game
```

### Strings (2)

```bash
just challenge strings valid_palindrome
just challenge strings longest_palindromic_substring
```

### Recursion (2)

```bash
just challenge recursion generate_parentheses
just challenge recursion flatten_nested_list
```

### Bit Manipulation (1)

```bash
just challenge bit_manipulation single_number
```

### Sorting (1)

```bash
just challenge sorting quickselect
```

---

## Tracking

After each pass, mark status:

| Mark | Meaning |
|------|---------|
| :white_check_mark: | From memory, under 25 min |
| :warning: | Needed a hint or slow |
| :x: | Could not solve |

Re-drill all :warning: and :x: problems first the next day.

```bash
just challenge-progress
```

---

## Extended Practice

The remaining 27 implementations are in the repo for deeper study:

- **graphs**: clone_graph, word_ladder, network_delay_time, network_flow, geohash_grid, kd_tree
- **dp**: climbing_stairs, traveling_salesman_dp, constraint_satisfaction
- **arrays**: top_k_frequent
- **two_pointers**: container_with_most_water
- **stacks_queues**: min_stack
- **searching**: find_minimum_rotated
- **linked_lists**: merge_two_sorted
- **trees**: max_depth, invert_tree
- **heaps**: task_scheduler
- **backtracking**: permutations
- **greedy**: interval_scheduling
- **strings**: valid_anagram, longest_common_prefix, string_to_integer_atoi
- **recursion**: pow_x_n, letter_combinations_phone, tower_of_hanoi
- **bit_manipulation**: counting_bits, reverse_bits
- **sorting**: merge_sort_inversions
- **patterns**: sliding_window (max_sum_subarray)

Use `just challenge <topic> <problem>` on any of these the same way.

---

## Tips

- Talk out loud while solving — practice interview communication
- 25 min per problem is interview pace
- If you can't identify the pattern in 3 min, check the [decision tree](../guide/when-to-use-what.md)
