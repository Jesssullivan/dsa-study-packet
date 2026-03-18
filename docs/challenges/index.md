---
title: Daily Challenges
---

# Daily Challenges

Self-test your algorithm knowledge with the challenge system. Each challenge strips the implementation from a problem file, leaving only the function signature and docstring for you to re-implement from memory.

---

## How It Works

```bash
# Start a challenge -- opens the problem with implementation stripped
just challenge graphs dijkstra

# Check your solution against the test suite
just solution graphs dijkstra

# Run tests for a specific topic
just practice graphs

# Watch mode -- re-runs tests on save
just study dp
```

1. `just challenge <topic> <problem>` strips the implementation and opens the file
2. You re-implement the function from the signature and docstring alone
3. `just solution <topic> <problem>` restores the original and runs tests
4. Compare your solution against the reference implementation

---

## Daily Routine

Follow this routine each study day:

1. **Warm-up** (10 min) -- 1 easy problem to build confidence
2. **Core** (60 min) -- 2 medium problems, 30 min each
3. **Review** (20 min) -- re-implement yesterday's core problems from memory
4. **Reference** (15 min) -- study one section of a [reference sheet](../reference/index.md)

---

## 7-Day Challenge Plan

Cover all 69 implementations in one week. Each day focuses on related topics.

### Day 1: Arrays + Two Pointers + Sliding Window (9 problems)

**Arrays** (4 problems):

```bash
just challenge arrays two_sum
just challenge arrays group_anagrams
just challenge arrays product_except_self
just challenge arrays top_k_frequent
```

**Two Pointers** (3 problems):

```bash
just challenge two_pointers three_sum
just challenge two_pointers container_with_most_water
just challenge two_pointers trapping_rain_water
```

**Sliding Window** (2 problems):

```bash
just challenge sliding_window longest_substring_no_repeat
just challenge sliding_window min_window_substring
```

---

### Day 2: Stacks/Queues + Searching + Strings (11 problems)

**Stacks & Queues** (3 problems):

```bash
just challenge stacks_queues valid_parentheses
just challenge stacks_queues min_stack
just challenge stacks_queues daily_temperatures
```

**Searching** (3 problems):

```bash
just challenge searching binary_search
just challenge searching search_rotated_array
just challenge searching find_minimum_rotated
```

**Strings** (5 problems):

```bash
just challenge strings longest_palindrome
just challenge strings valid_anagram
just challenge strings longest_common_prefix
just challenge strings string_to_integer
just challenge strings count_and_say
```

---

### Day 3: Linked Lists + Trees (8 problems)

**Linked Lists** (3 problems):

```bash
just challenge linked_lists reverse_linked_list
just challenge linked_lists merge_two_sorted
just challenge linked_lists lru_cache
```

**Trees** (5 problems):

```bash
just challenge trees max_depth
just challenge trees invert_tree
just challenge trees validate_bst
just challenge trees level_order_traversal
just challenge trees serialize_deserialize
```

---

### Day 4: Graphs (13 problems)

```bash
just challenge graphs number_of_islands
just challenge graphs clone_graph
just challenge graphs topological_sort
just challenge graphs course_schedule
just challenge graphs dijkstra
just challenge graphs network_delay_time
just challenge graphs word_ladder
just challenge graphs a_star_search
just challenge graphs bellman_ford
just challenge graphs minimum_spanning_tree
just challenge graphs network_flow
just challenge graphs geohash_grid
just challenge graphs kd_tree
```

---

### Day 5: Dynamic Programming (8 problems)

```bash
just challenge dp climbing_stairs
just challenge dp coin_change
just challenge dp longest_increasing_subseq
just challenge dp edit_distance
just challenge dp knapsack
just challenge dp longest_common_subseq
just challenge dp traveling_salesman_dp
just challenge dp constraint_satisfaction
```

---

### Day 6: Heaps + Backtracking + Greedy (10 problems)

**Heaps** (3 problems):

```bash
just challenge heaps kth_largest
just challenge heaps merge_k_sorted_lists
just challenge heaps task_scheduler
```

**Backtracking** (4 problems):

```bash
just challenge backtracking subsets
just challenge backtracking permutations
just challenge backtracking combination_sum
just challenge backtracking n_queens
```

**Greedy** (3 problems):

```bash
just challenge greedy merge_intervals
just challenge greedy jump_game
just challenge greedy interval_scheduling
```

---

### Day 7: Recursion + Bit Manipulation + Sorting + Review (10 problems)

**Bit Manipulation** (3 problems):

```bash
just challenge bit_manipulation single_number
just challenge bit_manipulation counting_bits
just challenge bit_manipulation reverse_bits
```

**Sorting** (2 problems):

```bash
just challenge sorting quickselect
just challenge sorting merge_sort_inversions
```

**Review** -- redo your 5 weakest problems from Days 1-6 timed (25 min each):

```bash
# Pick your weakest 5 and time yourself
just challenge <topic> <problem>
```

---

## Progress Tracking

After each day, note which problems you solved cleanly vs. needed hints:

| Status | Meaning |
|--------|---------|
| :white_check_mark: | Solved from memory in under 25 min |
| :warning: | Solved but needed a hint or took too long |
| :x: | Could not solve -- review tomorrow |

Re-attempt all :warning: and :x: problems the next day during the review phase.

---

## Tips

- **Talk out loud** while solving -- practice the interview communication pattern
- **Write tests first** if you get stuck -- tests clarify the problem
- **Time yourself** -- 25 min per medium problem is the interview pace
- Use the [decision tree](../guide/when-to-use-what.md) if you cannot identify the pattern within 3 minutes
