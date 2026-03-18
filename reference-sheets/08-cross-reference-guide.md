# Cross-Reference Guide — When to Use What

> **Purpose:** Master lookup for mapping problem descriptions, patterns, and real-world
> scenarios to specific implementations in this repo. Start here when facing a new problem.

---

## Section 1: Problem Pattern → Implementation Map

### Arrays & Hashing

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Find two values that sum to X" | Hash map lookup | `src/algo/arrays/two_sum.py` | O(n) |
| "Group items by property" | Hash map grouping | `src/algo/arrays/group_anagrams.py` | O(n*k log k) |
| "Top K / most frequent" | Bucket sort or heap | `src/algo/arrays/top_k_frequent.py` | O(n) |
| "Product without self" | Prefix/suffix arrays | `src/algo/arrays/product_except_self.py` | O(n) |

### Two Pointers

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Three values sum to zero" | Sort + two pointers | `src/algo/two_pointers/three_sum.py` | O(n^2) |
| "Maximum area / container" | Two pointers converging | `src/algo/two_pointers/container_with_most_water.py` | O(n) |
| "Water trapped between bars" | Two pointers + max tracking | `src/algo/two_pointers/trapping_rain_water.py` | O(n) |

### Sliding Window

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Minimum window containing chars" | Variable sliding window | `src/algo/sliding_window/min_window_substring.py` | O(n) |
| "Longest substring without repeat" | Sliding window + hash | `src/algo/sliding_window/longest_substring_no_repeat.py` | O(n) |

### Stacks & Queues

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Valid brackets/parentheses" | Stack matching | `src/algo/stacks_queues/valid_parentheses.py` | O(n) |
| "Min/max in O(1)" | Auxiliary stack | `src/algo/stacks_queues/min_stack.py` | O(1) |
| "Next greater/warmer element" | Monotonic stack | `src/algo/stacks_queues/daily_temperatures.py` | O(n) |

### Binary Search

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Find target in sorted array" | Binary search | `src/algo/searching/binary_search.py` | O(log n) |
| "Search in rotated array" | Modified binary search | `src/algo/searching/search_rotated_array.py` | O(log n) |
| "Find min in rotated array" | Binary search variant | `src/algo/searching/find_minimum_rotated.py` | O(log n) |

### Linked Lists

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Reverse a linked list" | Pointer manipulation | `src/algo/linked_lists/reverse_linked_list.py` | O(n) |
| "Merge sorted lists" | Two-pointer merge | `src/algo/linked_lists/merge_two_sorted.py` | O(n+m) |
| "Cache with eviction" | Hash map + doubly linked list | `src/algo/linked_lists/lru_cache.py` | O(1) |

### Trees

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Tree depth / height" | DFS recursion | `src/algo/trees/max_depth.py` | O(n) |
| "Mirror / flip tree" | Recursive swap | `src/algo/trees/invert_tree.py` | O(n) |
| "Is it a valid BST?" | DFS with bounds | `src/algo/trees/validate_bst.py` | O(n) |
| "Level-by-level traversal" | BFS with deque | `src/algo/trees/level_order_traversal.py` | O(n) |

### Graphs

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Connected components / islands" | BFS/DFS flood fill | `src/algo/graphs/number_of_islands.py` | O(m*n) |
| "Deep copy a graph" | BFS/DFS + visited map | `src/algo/graphs/clone_graph.py` | O(V+E) |
| "Dependency ordering" | Topological sort (Kahn's) | `src/algo/graphs/topological_sort.py` | O(V+E) |
| "Can finish all tasks? (cycles)" | Topological sort / DFS | `src/algo/graphs/course_schedule.py` | O(V+E) |
| "Shortest path (positive weights)" | Dijkstra's algorithm | `src/algo/graphs/dijkstra.py` | O((V+E) log V) |
| "Signal delay to all nodes" | Dijkstra variant | `src/algo/graphs/network_delay_time.py` | O((V+E) log V) |
| "Shortest transformation chain" | BFS level-by-level | `src/algo/graphs/word_ladder.py` | O(n*m^2) |
| "Grid pathfinding with heuristic" | A* search | `src/algo/graphs/a_star_search.py` | O(E log V) |
| "Shortest path (negative weights)" | Bellman-Ford | `src/algo/graphs/bellman_ford.py` | O(V*E) |
| "Minimum cost to connect all" | Kruskal's / Prim's | `src/algo/graphs/minimum_spanning_tree.py` | O(E log E) |
| "Maximum flow through network" | Edmonds-Karp | `src/algo/graphs/network_flow.py` | O(V*E^2) |
| "Spatial proximity queries" | Geohash encoding | `src/algo/graphs/geohash_grid.py` | O(precision) |
| "Nearest neighbor in k dimensions" | KD-tree | `src/algo/graphs/kd_tree.py` | O(log n) avg |

### Dynamic Programming

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Count ways to reach target" | DP (Fibonacci-like) | `src/algo/dp/climbing_stairs.py` | O(n) |
| "Minimum cost to reach amount" | DP (bottom-up) | `src/algo/dp/coin_change.py` | O(amount*coins) |
| "Longest increasing subsequence" | DP + binary search | `src/algo/dp/longest_increasing_subseq.py` | O(n log n) |
| "String edit distance" | 2D DP | `src/algo/dp/edit_distance.py` | O(m*n) |
| "0/1 Knapsack" | DP (1D optimized) | `src/algo/dp/knapsack.py` | O(n*W) |
| "Longest common subsequence" | 2D DP | `src/algo/dp/longest_common_subseq.py` | O(m*n) |
| "Shortest route visiting all cities" | Bitmask DP (TSP) | `src/algo/dp/traveling_salesman_dp.py` | O(n^2 * 2^n) |
| "Constraint satisfaction (Sudoku)" | Backtracking + propagation | `src/algo/dp/constraint_satisfaction.py` | varies |

### Heaps

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Kth largest element" | Min-heap of size k | `src/algo/heaps/kth_largest.py` | O(n log k) |
| "Merge k sorted lists" | Heap merge | `src/algo/heaps/merge_k_sorted_lists.py` | O(n log k) |
| "Task scheduling with cooldown" | Max-heap + queue | `src/algo/heaps/task_scheduler.py` | O(n) |

### Backtracking

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Generate all subsets" | Backtracking | `src/algo/backtracking/subsets.py` | O(n * 2^n) |
| "Generate all permutations" | Backtracking | `src/algo/backtracking/permutations.py` | O(n * n!) |
| "Combinations summing to target" | Backtracking (w/ reuse) | `src/algo/backtracking/combination_sum.py` | O(2^target) |
| "N queens placement" | Backtracking + pruning | `src/algo/backtracking/n_queens.py` | O(n!) |

### Greedy

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Merge overlapping intervals" | Sort + merge | `src/algo/greedy/merge_intervals.py` | O(n log n) |
| "Can reach end? Min jumps?" | Greedy max-reach | `src/algo/greedy/jump_game.py` | O(n) |
| "Max non-overlapping intervals" | Greedy by end time | `src/algo/greedy/interval_scheduling.py` | O(n log n) |

### Bit Manipulation

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Find unique element (others x2)" | XOR all | `src/algo/bit_manipulation/single_number.py` | O(n) |
| "Count set bits 0..n" | DP: dp[i] = dp[i>>1] + (i&1) | `src/algo/bit_manipulation/counting_bits.py` | O(n) |
| "Reverse bits of integer" | Bit-by-bit or D&C | `src/algo/bit_manipulation/reverse_bits.py` | O(1) |

### Sorting

| When You See... | Use This Pattern | Implementation | Complexity |
|---|---|---|---|
| "Find kth smallest" | Quickselect | `src/algo/sorting/quickselect.py` | O(n) avg |
| "Count inversions" | Merge sort variant | `src/algo/sorting/merge_sort_inversions.py` | O(n log n) |

---

## Section 2: Data Structure Selection Guide

| Need | Use | Why | Example Implementations |
|---|---|---|---|
| O(1) lookup by key | `dict` / hash map | Hash-based amortized O(1) | `two_sum.py`, `group_anagrams.py` |
| O(1) membership test | `set` | Hash-based | `number_of_islands.py` (visited set) |
| Ordered iteration | sorted `list` | Timsort O(n log n) | `three_sum.py` (sort first) |
| FIFO queue | `collections.deque` | O(1) appendleft/popleft | BFS in `level_order_traversal.py`, `word_ladder.py` |
| Priority queue | `heapq` | O(log n) push/pop | `dijkstra.py`, `kth_largest.py`, `merge_k_sorted_lists.py` |
| Stack (LIFO) | `list` with append/pop | O(1) amortized | `valid_parentheses.py`, `daily_temperatures.py` |
| Sorted container | `bisect` module | O(log n) search | `longest_increasing_subseq.py`, `hypothesis_patterns.py` |
| Disjoint sets | Union-Find class | ~O(alpha(n)) amortized | `minimum_spanning_tree.py` |
| Spatial index | KD-tree / geohash | O(log n) nearest neighbor | `kd_tree.py`, `geohash_grid.py` |
| Cache with eviction | OrderedDict / DLL+dict | O(1) get, put, evict | `lru_cache.py` |

### When to pick what

```
Need key -> value?          --> dict
Need "is X in the set?"     --> set
Need min/max repeatedly?    --> heapq
Need FIFO?                  --> collections.deque
Need LIFO?                  --> list (append/pop)
Need sorted insert + search --> bisect / SortedList
Need merge/find groups?     --> Union-Find
Need nearest in 2D/3D?      --> KD-tree or geohash
```

---

## Section 3: Concept Modules -- When to Study Each

| Concept Module | Study When... | Key Functions / Classes | Cross-References |
|---|---|---|---|
| `t_strings.py` | Learning Python 3.14 features, preventing injection | `sql_safe()`, `html_safe()`, `structured_log()`, `render()` | PEP 750, ref sheet 03 (Python 3.14) |
| `advanced_typing.py` | Writing typed Python, understanding Protocol vs ABC | `Drawable` Protocol, `Stack[T]`, `Container[T]`, `@overload`, `TypeGuard` | PEP 544/612/647/695/696, ref sheet 03 |
| `hypothesis_patterns.py` | Learning property-based testing, finding edge cases | `SortedList`, `BoundedCounter` | Hypothesis docs, ref sheet 03, `tests/concepts/test_hypothesis_patterns.py` |
| `fft_dct.py` | Signal processing, frequency analysis, sensor data | `compute_fft()`, `filter_signal()`, `compute_dct()`, `spectral_analysis()` | target employer: ADS-B signals, weather radar |
| `modern_flask.py` | Web API patterns, app factory, testing | `create_app()`, `api_bp` Blueprint, `ValidationError` | System design round, API questions |
| `validation.py` | Data validation, API boundaries, Pydantic v2 vs Zod | `User` model, `Address`, `Shape` discriminated union, `serialize_user()` | Practical problem solving round |

### Concept -> Algorithm connections

- **t_strings** demonstrate the *template pattern* -- same concept as parameterized queries in `sql_safe()`, analogous to how DP builds solutions from templates
- **advanced_typing** shows `Stack[T]` -- the same LIFO structure used in `valid_parentheses.py` and `daily_temperatures.py`
- **hypothesis_patterns** uses `bisect` -- the same binary search strategy in `longest_increasing_subseq.py`
- **fft_dct** is pure signal processing -- relevant when target employer interview asks about sensor data pipelines
- **modern_flask** is the API layer -- pairs with `validation.py` for full request lifecycle
- **validation** with Pydantic is the runtime counterpart to `advanced_typing`'s static type system

---

## Section 4: domain Problem Mapping

| target employer Domain Challenge | Relevant Algorithms | Implementations |
|---|---|---|
| Flight route optimization | A*, Dijkstra, Bellman-Ford | `graphs/a_star_search.py`, `graphs/dijkstra.py`, `graphs/bellman_ford.py` |
| Airspace network planning | MST, Network flow | `graphs/minimum_spanning_tree.py`, `graphs/network_flow.py` |
| Weather-constrained routing | Constraint satisfaction, TSP | `dp/constraint_satisfaction.py`, `dp/traveling_salesman_dp.py` |
| Geospatial indexing (airports, waypoints) | Geohash, KD-tree | `graphs/geohash_grid.py`, `graphs/kd_tree.py` |
| Real-time data streaming | Sliding window, heaps | `sliding_window/`, `heaps/task_scheduler.py` |
| Sensor signal processing (ADS-B, radar) | FFT, DCT, filtering | `concepts/fft_dct.py` |
| Dependency scheduling (builds, deploys) | Topological sort, course schedule | `graphs/topological_sort.py`, `graphs/course_schedule.py` |
| API design & validation | Flask, Pydantic | `concepts/modern_flask.py`, `concepts/validation.py` |
| Data pipeline optimization | Merge intervals, scheduling | `greedy/merge_intervals.py`, `greedy/interval_scheduling.py` |
| Cache design (session, config) | LRU cache | `linked_lists/lru_cache.py` |
| Network capacity planning | Max flow, MST | `graphs/network_flow.py`, `graphs/minimum_spanning_tree.py` |
| Task prioritization with constraints | Heap + cooldown, greedy | `heaps/task_scheduler.py`, `greedy/jump_game.py` |

### How to frame algorithm answers for target employer

When asked about an aviation/aerospace domain problem, connect to fundamentals:

1. **"How would you route aircraft around weather?"**
   - Model airspace as weighted graph, weather cells as infinite-weight edges
   - A* with great-circle heuristic (`a_star_search.py`)
   - Bellman-Ford if fuel costs can be negative via tailwinds (`bellman_ford.py`)

2. **"Design a system to track nearby aircraft"**
   - Geohash grid for O(1) cell lookup (`geohash_grid.py`)
   - KD-tree for exact nearest-neighbor queries (`kd_tree.py`)
   - Sliding window on streaming position updates (`sliding_window/`)

3. **"Schedule maintenance tasks with dependencies"**
   - Topological sort for ordering (`topological_sort.py`)
   - Course schedule pattern for cycle detection (`course_schedule.py`)
   - Interval scheduling for time-slot allocation (`interval_scheduling.py`)

---

## Section 5: Quick Decision Tree

```
START: What does the problem ask for?
|
+-- "Find / search for something"
|   |
|   +-- Input is sorted?
|   |   +-- YES --> Binary search (searching/binary_search.py)
|   |   |           Rotated? --> search_rotated_array.py, find_minimum_rotated.py
|   |   +-- NO  --> Hash map O(n) lookup (arrays/two_sum.py pattern)
|   |
|   +-- Find in a graph?
|       +-- Unweighted shortest path --> BFS (graphs/number_of_islands.py pattern)
|       +-- Weighted, positive       --> Dijkstra (graphs/dijkstra.py)
|       +-- Weighted, negative       --> Bellman-Ford (graphs/bellman_ford.py)
|       +-- With heuristic           --> A* (graphs/a_star_search.py)
|
+-- "Optimize a value" (min cost, max profit, count ways)
|   |
|   +-- Overlapping subproblems?
|   |   +-- YES --> Dynamic programming (dp/)
|   |   |          1D: climbing_stairs.py, coin_change.py
|   |   |          2D: edit_distance.py, longest_common_subseq.py
|   |   |          Bitmask: traveling_salesman_dp.py
|   |   +-- NO  --> Greedy (prove greedy choice property)
|   |               merge_intervals.py, jump_game.py, interval_scheduling.py
|   |
|   +-- Need top-K or priority ordering?
|       +-- Kth element     --> Heap (heaps/kth_largest.py) or Quickselect (sorting/quickselect.py)
|       +-- Merge K streams --> Heap merge (heaps/merge_k_sorted_lists.py)
|
+-- "Generate all / enumerate"
|   |
|   +-- All subsets          --> Backtracking (backtracking/subsets.py)
|   +-- All permutations     --> Backtracking (backtracking/permutations.py)
|   +-- Combinations to sum  --> Backtracking with reuse (backtracking/combination_sum.py)
|   +-- Placement with rules --> Backtracking + pruning (backtracking/n_queens.py)
|
+-- "Process a sequence" (subarray, substring)
|   |
|   +-- Contiguous subarray/substring?
|   |   +-- YES --> Sliding window (sliding_window/)
|   |   |          Fixed size:    pattern in patterns/sliding_window.py
|   |   |          Variable size: min_window_substring.py, longest_substring_no_repeat.py
|   |   +-- NO  --> Subsequence: DP (dp/longest_increasing_subseq.py, longest_common_subseq.py)
|   |
|   +-- Next greater/smaller element? --> Monotonic stack (stacks_queues/daily_temperatures.py)
|   +-- Valid nesting?                --> Stack (stacks_queues/valid_parentheses.py)
|
+-- "Graph structure" (explicit or implicit)
|   |
|   +-- Connected components  --> DFS/BFS (graphs/number_of_islands.py) or Union-Find
|   +-- Dependency ordering   --> Topological sort (graphs/topological_sort.py)
|   +-- Cycle detection       --> Course schedule pattern (graphs/course_schedule.py)
|   +-- Clone / copy          --> BFS/DFS + visited map (graphs/clone_graph.py)
|   +-- Minimum spanning tree --> Kruskal's (graphs/minimum_spanning_tree.py)
|   +-- Maximum flow          --> Edmonds-Karp (graphs/network_flow.py)
|
+-- "Design a data structure"
    |
    +-- O(1) access + eviction --> LRU Cache (linked_lists/lru_cache.py)
    +-- O(1) min/max retrieval --> Min Stack (stacks_queues/min_stack.py)
    +-- Sorted insert + search --> SortedList with bisect (concepts/hypothesis_patterns.py)
    +-- Generic typed container -> Stack[T] (concepts/advanced_typing.py)
```

---

## Section 6: Complexity Quick-Reference by Category

Use this to sanity-check your solution's complexity during an interview.

### O(1) solutions
| Problem | Implementation |
|---|---|
| Min stack operations | `stacks_queues/min_stack.py` |
| LRU cache get/put | `linked_lists/lru_cache.py` |
| Reverse bits | `bit_manipulation/reverse_bits.py` |

### O(n) solutions
| Problem | Implementation |
|---|---|
| Two sum | `arrays/two_sum.py` |
| Product except self | `arrays/product_except_self.py` |
| Top K frequent | `arrays/top_k_frequent.py` |
| Container with most water | `two_pointers/container_with_most_water.py` |
| Trapping rain water | `two_pointers/trapping_rain_water.py` |
| Min window substring | `sliding_window/min_window_substring.py` |
| Longest substring no repeat | `sliding_window/longest_substring_no_repeat.py` |
| Valid parentheses | `stacks_queues/valid_parentheses.py` |
| Daily temperatures | `stacks_queues/daily_temperatures.py` |
| Reverse linked list | `linked_lists/reverse_linked_list.py` |
| Max depth of tree | `trees/max_depth.py` |
| Invert tree | `trees/invert_tree.py` |
| Validate BST | `trees/validate_bst.py` |
| Level order traversal | `trees/level_order_traversal.py` |
| Climbing stairs | `dp/climbing_stairs.py` |
| Single number | `bit_manipulation/single_number.py` |
| Counting bits | `bit_manipulation/counting_bits.py` |
| Task scheduler | `heaps/task_scheduler.py` |
| Jump game | `greedy/jump_game.py` |
| Quickselect (average) | `sorting/quickselect.py` |

### O(n log n) solutions
| Problem | Implementation |
|---|---|
| Three sum | `two_pointers/three_sum.py` (sort dominates, then O(n^2) scan) |
| Longest increasing subseq | `dp/longest_increasing_subseq.py` |
| Merge intervals | `greedy/merge_intervals.py` |
| Interval scheduling | `greedy/interval_scheduling.py` |
| Merge sort inversions | `sorting/merge_sort_inversions.py` |

### O(log n) solutions
| Problem | Implementation |
|---|---|
| Binary search | `searching/binary_search.py` |
| Search rotated array | `searching/search_rotated_array.py` |
| Find minimum rotated | `searching/find_minimum_rotated.py` |

### O(V+E) graph solutions
| Problem | Implementation |
|---|---|
| Clone graph | `graphs/clone_graph.py` |
| Topological sort | `graphs/topological_sort.py` |
| Course schedule | `graphs/course_schedule.py` |

### O((V+E) log V) graph solutions
| Problem | Implementation |
|---|---|
| Dijkstra | `graphs/dijkstra.py` |
| Network delay time | `graphs/network_delay_time.py` |
| A* search | `graphs/a_star_search.py` |

### Exponential solutions (backtracking)
| Problem | Implementation |
|---|---|
| Subsets O(n * 2^n) | `backtracking/subsets.py` |
| Permutations O(n * n!) | `backtracking/permutations.py` |
| Combination sum O(2^target) | `backtracking/combination_sum.py` |
| N queens O(n!) | `backtracking/n_queens.py` |
| TSP O(n^2 * 2^n) | `dp/traveling_salesman_dp.py` |

---

## Section 7: Pattern Recognition Cheat Sheet

When you read a problem statement, look for these keywords and jump to the right section.

| Keyword in Problem | First Thing to Try | If That Fails |
|---|---|---|
| "sorted" | Binary search, two pointers | -- |
| "contiguous subarray" | Sliding window | Prefix sums, Kadane's |
| "substring" | Sliding window + hash map | DP |
| "parentheses" / "brackets" | Stack | -- |
| "next greater" / "next warmer" | Monotonic stack | -- |
| "shortest path" | BFS (unweighted), Dijkstra (weighted) | Bellman-Ford (negative), A* (heuristic) |
| "connected" / "island" / "region" | DFS/BFS flood fill, Union-Find | -- |
| "dependency" / "prerequisite" | Topological sort | -- |
| "cycle" | DFS coloring (directed), Union-Find (undirected) | -- |
| "minimum cost" / "count ways" | Dynamic programming | -- |
| "all subsets" / "all combinations" | Backtracking | Bitmask enumeration |
| "merge" / "overlapping intervals" | Sort + greedy sweep | -- |
| "kth largest" / "top k" | Heap of size k | Quickselect |
| "design" / "implement" | Choose data structures, define API | -- |
| "cache" / "eviction" | LRU = hash map + doubly linked list | -- |
| "stream" / "online" | Heap, sliding window | -- |
| "frequency" / "how many times" | Hash map / Counter | -- |
| "edit distance" / "transform" | 2D DP | BFS (word_ladder) |
| "knapsack" / "subset sum" | DP (1D or 2D) | -- |
| "schedule tasks" | Heap + greedy | Topological sort if deps |
| "maximum flow" | Edmonds-Karp / Ford-Fulkerson | -- |
| "nearest point" / "proximity" | KD-tree, geohash | -- |
| "visit all cities/nodes" | TSP bitmask DP | -- |
| "XOR" / "single unique" | Bit manipulation | -- |

---

## Section 8: Study Order Recommendations

### If you have 2 hours (crunch mode)

1. Skim this decision tree (Section 5) -- internalize the branching
2. Review `arrays/two_sum.py` (hash map pattern)
3. Review `sliding_window/min_window_substring.py` (window pattern)
4. Review `dp/coin_change.py` (DP template)
5. Review `graphs/dijkstra.py` (graph traversal)
6. Review `backtracking/subsets.py` (enumeration template)

### If you have 1 day

Add to the above:
- All of Section 1 (scan for recognition, don't memorize)
- `trees/validate_bst.py` + `level_order_traversal.py`
- `greedy/merge_intervals.py`
- `linked_lists/lru_cache.py`
- `concepts/modern_flask.py` + `concepts/validation.py`

### If you have 1 week

Work through every implementation in order:
1. Arrays & hashing (day 1)
2. Two pointers + sliding window (day 2)
3. Stacks, searching, linked lists (day 3)
4. Trees + graphs (day 4)
5. DP + backtracking (day 5)
6. Heaps, greedy, bit manipulation, sorting (day 6)
7. Concept modules + target employer domain mapping (day 7)

---

## Cross-Reference to Other Sheets

| Sheet | Use it for... |
|---|---|
| `01-python-stdlib.md` | Python built-in functions, data types, standard library |
| `02-data-structures.md` | Detailed data structure theory and operations |
| `03-algorithm-templates.md` | Pseudocode templates for each algorithm family |
| `03-python-314-and-modern-patterns.md` | Python 3.14 features, t-strings, typing, Hypothesis |
| `04-big-o-complexity.md` | Complexity analysis, input size -> acceptable complexity |
| `05-common-patterns.md` | Problem signal -> pattern mapping (compact version) |
| `06-system-design.md` | System design interview framework |
| `07-interview-day-guide.md` | Day-of logistics, communication framework, timing |
| **08-cross-reference-guide.md** | You are here -- the master lookup |
