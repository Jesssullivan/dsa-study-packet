# 4-Week Study Plan

Target: Senior Full-Stack (Backend) Algorithm Interview at target employer.

## Daily Routine

Each day follows the same structure:

1. **Warm-up** (10 min): 1 easy problem -- build confidence, get fingers moving.
2. **Core** (60 min): 2 medium problems, 30 min each -- the meat of interview prep.
3. **Review** (20 min): Re-implement yesterday's core problems from memory.
4. **Reference** (15 min): Study one section of a reference sheet.

---

## Week 1: Arrays, Hashing, Two Pointers, Sliding Window, Binary Search

Focus: Build speed on the bread-and-butter patterns.

### Day 1 (Mon) -- Arrays & Hashing Fundamentals
- Warm-up: `src/algo/arrays/two_sum.py`
- Core 1: `src/algo/arrays/group_anagrams.py`
- Core 2: `src/algo/arrays/product_except_self.py`
- Reference: `01-python-stdlib.md` -- collections, itertools

### Day 2 (Tue) -- Arrays & Hashing Continued
- Warm-up: Contains Duplicate (scaffold: `just new arrays contains_duplicate`)
- Core 1: `src/algo/arrays/top_k_frequent.py`
- Core 2: Encode/Decode Strings (`just new arrays encode_decode_strings`)
- Review: Re-implement group_anagrams, product_except_self
- Reference: `02-data-structures.md` -- hash maps, sets

### Day 3 (Wed) -- Two Pointers
- Warm-up: Valid Palindrome (`just new two_pointers valid_palindrome`)
- Core 1: `src/algo/two_pointers/three_sum.py`
- Core 2: `src/algo/two_pointers/container_with_most_water.py`
- Review: Re-implement top_k_frequent
- Reference: `05-common-patterns.md` -- two pointer patterns

### Day 4 (Thu) -- Two Pointers Advanced
- Warm-up: Two Sum II (sorted input) (`just new two_pointers two_sum_ii`)
- Core 1: `src/algo/two_pointers/trapping_rain_water.py`
- Core 2: 4Sum (`just new two_pointers four_sum`)
- Review: Re-implement three_sum, container_with_most_water
- Reference: `03-algorithm-templates.md` -- two pointer templates

### Day 5 (Fri) -- Sliding Window
- Warm-up: Best Time to Buy/Sell Stock (`just new sliding_window buy_sell_stock`)
- Core 1: `src/algo/sliding_window/longest_substring_no_repeat.py`
- Core 2: `src/algo/sliding_window/min_window_substring.py`
- Review: Re-implement trapping_rain_water
- Reference: `03-algorithm-templates.md` -- sliding window templates

### Day 6 (Sat) -- Binary Search
- Warm-up: Binary Search (`just new searching binary_search`)
- Core 1: Search in Rotated Sorted Array (`just new searching search_rotated`)
- Core 2: Find Minimum in Rotated Array (`just new searching min_rotated`)
- Review: Re-implement longest_substring_no_repeat, min_window_substring
- Reference: `04-big-o-complexity.md` -- log(n) patterns

### Day 7 (Sun) -- Week 1 Review
- Re-do the 2 hardest problems from the week without references.
- Timed: 25 min each, simulating interview conditions.
- Review any reference sheet sections that felt weak.

---

## Week 2: Trees, Graphs, Linked Lists, Stacks/Queues

Focus: Recursive thinking and graph traversal patterns.

### Day 8 (Mon) -- Binary Trees Basics
- Warm-up: Invert Binary Tree (`just new trees invert_tree`)
- Core 1: Max Depth of Binary Tree (`just new trees max_depth`)
- Core 2: Level Order Traversal (`just new trees level_order`)
- Reference: `02-data-structures.md` -- tree representations

### Day 9 (Tue) -- Binary Trees Continued
- Warm-up: Same Tree (`just new trees same_tree`)
- Core 1: Validate BST (`just new trees validate_bst`)
- Core 2: Lowest Common Ancestor (`just new trees lowest_common_ancestor`)
- Review: Re-implement invert_tree, level_order
- Reference: `03-algorithm-templates.md` -- DFS/BFS templates

### Day 10 (Wed) -- Binary Trees Advanced
- Warm-up: Subtree of Another Tree (`just new trees subtree_of_another`)
- Core 1: Binary Tree Right Side View (`just new trees right_side_view`)
- Core 2: Serialize/Deserialize Binary Tree (`just new trees serialize_tree`)
- Review: Re-implement validate_bst, lowest_common_ancestor
- Reference: `05-common-patterns.md` -- tree patterns

### Day 11 (Thu) -- Graphs Fundamentals
- Warm-up: `src/algo/graphs/number_of_islands.py`
- Core 1: `src/algo/graphs/clone_graph.py`
- Core 2: Course Schedule (`just new graphs course_schedule`)
- Review: Re-implement right_side_view, serialize_tree
- Reference: `02-data-structures.md` -- adjacency list, adjacency matrix

### Day 12 (Fri) -- Graphs Advanced
- Warm-up: Pacific Atlantic Water Flow (`just new graphs pacific_atlantic`)
- Core 1: Graph Valid Tree (`just new graphs valid_tree`)
- Core 2: Word Ladder (`just new graphs word_ladder`)
- Review: Re-implement clone_graph, course_schedule
- Reference: `03-algorithm-templates.md` -- graph traversal templates

### Day 13 (Sat) -- Linked Lists & Stacks/Queues
- Warm-up: `src/algo/linked_lists/reverse_linked_list.py`
- Core 1: `src/algo/linked_lists/merge_two_sorted.py`
- Core 2: `src/algo/stacks_queues/valid_parentheses.py`
- Review: Re-implement valid_tree, word_ladder
- Reference: `02-data-structures.md` -- linked list, stack, queue ops

### Day 14 (Sun) -- Week 2 Review
- Warm-up: `src/algo/linked_lists/lru_cache.py` (combines multiple patterns)
- Re-do the 2 hardest problems from the week without references.
- Review: `05-common-patterns.md` -- graph/tree patterns summary.

---

## Week 3: DP, Backtracking, Greedy, Heaps

Focus: The patterns that separate medium from hard.

### Day 15 (Mon) -- DP 1D
- Warm-up: Climbing Stairs (`just new dp climbing_stairs`)
- Core 1: House Robber (`just new dp house_robber`)
- Core 2: Longest Increasing Subsequence (`just new dp longest_increasing_subseq`)
- Reference: `03-algorithm-templates.md` -- DP templates

### Day 16 (Tue) -- DP 2D
- Warm-up: Unique Paths (`just new dp unique_paths`)
- Core 1: Coin Change (`just new dp coin_change`)
- Core 2: Longest Common Subsequence (`just new dp longest_common_subseq`)
- Review: Re-implement house_robber, longest_increasing_subseq
- Reference: `05-common-patterns.md` -- DP state transition patterns

### Day 17 (Wed) -- DP Advanced
- Warm-up: Decode Ways (`just new dp decode_ways`)
- Core 1: Word Break (`just new dp word_break`)
- Core 2: Edit Distance (`just new dp edit_distance`)
- Review: Re-implement coin_change, longest_common_subseq
- Reference: `04-big-o-complexity.md` -- DP time/space analysis

### Day 18 (Thu) -- Backtracking
- Warm-up: Subsets (`just new backtracking subsets`)
- Core 1: Combination Sum (`just new backtracking combination_sum`)
- Core 2: Permutations (`just new backtracking permutations`)
- Review: Re-implement word_break, edit_distance
- Reference: `03-algorithm-templates.md` -- backtracking template

### Day 19 (Fri) -- Greedy & Intervals
- Warm-up: Maximum Subarray (`just new greedy max_subarray`)
- Core 1: Merge Intervals (`just new greedy merge_intervals`)
- Core 2: Non-Overlapping Intervals (`just new greedy non_overlapping_intervals`)
- Review: Re-implement combination_sum, permutations
- Reference: `05-common-patterns.md` -- greedy patterns, interval tricks

### Day 20 (Sat) -- Heaps & Priority Queues
- Warm-up: Kth Largest Element (`just new heaps kth_largest`)
- Core 1: Top K Frequent Elements (heap approach) (`just new heaps top_k_heap`)
- Core 2: Find Median from Data Stream (`just new heaps median_stream`)
- Review: Re-implement merge_intervals, non_overlapping_intervals
- Reference: `02-data-structures.md` -- heapq, SortedContainers

### Day 21 (Sun) -- Week 3 Review
- Re-do the 2 hardest DP problems timed (25 min each).
- Re-implement one backtracking and one greedy problem from memory.
- Review: all algorithm templates one more time.

---

## Week 4: domain, Code Reading, System Design, Mocks

Focus: Shift from LeetCode to interview-specific prep.

### Day 22 (Mon) -- domain: Graphs & Pathfinding
- Warm-up: Dijkstra's Shortest Path (`just new graphs dijkstra`)
- Core 1: A* Search (`just new graphs a_star`)
- Core 2: Network Delay Time (`just new graphs network_delay`)
- Reference: `06-system-design.md` -- geospatial indexing section
- Concept: `src/concepts/t_strings.py` -- PEP 750 template strings (15 min)

### Day 23 (Tue) -- domain: Geospatial & Streaming
- Warm-up: K Closest Points to Origin (`just new heaps k_closest_points`)
- Core 1: Design Hit Counter (`just new stacks_queues hit_counter`)
- Core 2: Sliding Window Maximum (`just new heaps sliding_window_max`)
- Review: Re-implement dijkstra, a_star
- Reference: `06-system-design.md` -- stream processing, caching
- Concept: `src/concepts/advanced_typing.py` -- modern type system (15 min)

### Day 24 (Wed) -- Code Reading Practice
- Work through `src/practice/code_reading/ex01_caching_service.py`
- Work through `src/practice/code_reading/ex02_flight_data_pipeline.py`
- Work through `src/practice/code_reading/ex03_rate_limiter.py`
- For each: identify all issues, propose fixes, estimate complexity impact.
- Reference: `06-system-design.md` -- caching patterns, message queues
- Concept: `src/concepts/hypothesis_patterns.py` -- property-based testing (15 min)

### Day 25 (Thu) -- Problem Decomposition Practice
- Work through `src/practice/decomposition/ex01_flight_route_optimizer.md`
- Work through `src/practice/decomposition/ex02_vehicle_tracking.md`
- Practice: talk through each decomposition out loud (record yourself).
- Reference: `06-system-design.md` -- distributed systems, API design
- Concept: `src/concepts/fft_dct.py` -- signal processing fundamentals (15 min)

### Day 26 (Fri) -- System Design Deep Dive
- Work through `src/practice/decomposition/ex03_geospatial_pipeline.md`
- Practice system design: "Design a real-time flight tracking API"
- Practice system design: "Design a weather data ingestion pipeline"
- Reference: `06-system-design.md` -- full review
- Concept: `src/concepts/modern_flask.py` -- Flask 3.x patterns (15 min)

### Day 27 (Sat) -- Mock Interview Day
- Morning: Timed algorithm round (75 min, 3 problems, no references).
  Pick 3 unsolved mediums from any topic.
- Afternoon: Practice "Practical Problem Solving" with a partner or
  rubber duck. Walk through one code reading exercise explaining your
  reasoning out loud.
- Evening: Practice one problem decomposition exercise on a whiteboard.
- Concept: `src/concepts/validation.py` -- Pydantic/Zod validation patterns (15 min)

### Day 28 (Sun) -- Final Review
- Review all reference sheets one last time.
- Re-do your 3 weakest problems.
- Prepare questions for the CEO chat (company direction, team culture,
  how domain platform is evolving).
- Rest. Sleep well.

### Week 4: Concept Module Integration

Each day in Week 4 includes a 15-minute concept module session. These cover
production-level Python topics that may surface in the practical problem solving
or system design rounds. Run `just test-concepts` to verify your understanding,
or `just study-concept` for watch mode.

| Day | Module | File | Topic |
|-----|--------|------|-------|
| 22 | T-Strings | `src/concepts/t_strings.py` | PEP 750 template strings -- lazy interpolation, safe SQL/HTML templating |
| 23 | Advanced Typing | `src/concepts/advanced_typing.py` | Modern type system -- Protocol, TypeVar, ParamSpec, TypeGuard |
| 24 | Hypothesis Patterns | `src/concepts/hypothesis_patterns.py` | Property-based testing -- strategies, @given, @composite, stateful testing |
| 25 | FFT / DCT | `src/concepts/fft_dct.py` | Signal processing -- FFT, inverse FFT, DCT, frequency analysis |
| 26 | Modern Flask | `src/concepts/modern_flask.py` | Flask 3.x -- async views, class-based views, nested blueprints |
| 27 | Validation | `src/concepts/validation.py` | Pydantic v2 -- model validators, discriminated unions, serialization |

---

## Practical Problem Solving Round -- Prep Strategy

This round simulates a code review / debugging session. The interviewer shows
you unfamiliar code and asks you to analyze it.

### What They're Evaluating
- Can you read and understand code you didn't write?
- Can you identify performance bottlenecks?
- Can you spot bugs and edge cases?
- Can you suggest improvements with clear reasoning?
- Do you communicate your thought process clearly?

### How to Practice
1. **Read open-source code** -- pick a Python library you use, read a module cold.
2. **Use the code_reading exercises** in `src/practice/code_reading/`.
3. **Practice narrating** -- say out loud what you observe as you read.
4. **Build a checklist** to scan for:
   - Time complexity of loops (nested = red flag)
   - Memory usage (loading all data, no streaming)
   - Error handling (missing try/except, no validation)
   - Thread safety (shared mutable state, no locks)
   - I/O patterns (N+1 queries, synchronous blocking calls)
   - Cache behavior (no eviction, no TTL, unbounded growth)
5. **Suggest fixes in priority order** -- biggest impact first.

### Framework for Analyzing Unfamiliar Code
1. **Skim** -- read function signatures and docstrings first.
2. **Trace** -- pick one execution path and follow it end to end.
3. **Question** -- "What happens when input is empty? Very large? Malformed?"
4. **Measure** -- estimate time/space complexity of the hot path.
5. **Propose** -- suggest 2-3 improvements ranked by impact.
