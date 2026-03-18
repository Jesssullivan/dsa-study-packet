# Common Patterns Quick Reference (1 page)

## Problem Type -> Algorithm Mapping

| Problem Signal | Pattern / Algorithm |
|---|---|
| **"Find shortest path" (unweighted)** | BFS |
| **"Find shortest path" (weighted, non-neg)** | Dijkstra |
| **"Find shortest path" (negative weights)** | Bellman-Ford |
| **"All pairs shortest path"** | Floyd-Warshall |
| **"Connected components"** | DFS/BFS or Union-Find |
| **"Detect cycle" (directed)** | DFS with coloring (white/gray/black) |
| **"Detect cycle" (undirected)** | Union-Find or DFS with parent tracking |
| **"Ordering with dependencies"** | Topological Sort |
| **"Minimum spanning tree"** | Kruskal's (sparse) or Prim's (dense) |
| **"Find in sorted array"** | Binary Search |
| **"Minimum/maximum X that satisfies Y"** | Binary Search on Answer |
| **"Kth smallest/largest"** | Heap (O(n log k)) or Quick Select (O(n) avg) |
| **"Top K elements"** | Heap of size k |
| **"Median of stream"** | Two heaps (max-heap + min-heap) |
| **"Merge K sorted"** | Min-heap of size k |
| **"Subarray with sum/property"** | Prefix sum + hash map |
| **"Contiguous subarray optimization"** | Sliding window or Kadane's |
| **"Substring matching/anagrams"** | Sliding window + counter |
| **"Longest substring with condition"** | Sliding window (variable) |
| **"All subsets/combinations"** | Backtracking or bitmask DP |
| **"All permutations"** | Backtracking |
| **"Constraint satisfaction"** | Backtracking with pruning |
| **"Count ways" / "min cost"** | Dynamic Programming |
| **"String comparison/edit"** | 2D DP (LCS, edit distance) |
| **"Longest increasing subsequence"** | DP + binary search O(n log n) |
| **"Interval scheduling"** | Sort + greedy or sweep line |
| **"Overlapping intervals"** | Sort by start, merge |
| **"Maximum in sliding window"** | Monotonic deque |
| **"Next greater/smaller element"** | Monotonic stack |
| **"Histogram largest rectangle"** | Monotonic stack |
| **"Word search / prefix matching"** | Trie |
| **"Autocomplete"** | Trie + DFS |
| **"Disjoint groups / merging"** | Union-Find |

---

## Red Flags & Hints in Problem Descriptions

| Keyword / Hint | Think... |
|---|---|
| "sorted array" | Binary search, two pointers |
| "O(log n)" required | Binary search |
| "minimum number of steps" | BFS (unweighted shortest path) |
| "contiguous subarray" | Sliding window, prefix sum, Kadane's |
| "at most K distinct" | Sliding window with counter |
| "palindrome" | Two pointers (expand from center), DP |
| "parentheses / brackets" | Stack |
| "evaluate expression" | Stack (two stacks: operators + operands) |
| "matrix traversal" | BFS/DFS on grid |
| "island counting" | BFS/DFS or Union-Find on grid |
| "tree diameter/depth" | DFS (post-order) |
| "serialize / level-order" | BFS |
| "lowest common ancestor" | DFS with recursion |
| "number of ways" | DP (usually) |
| "can you partition into..." | DP (subset sum variant) |
| "maximum profit" | DP or greedy |
| "buy and sell stock" | State machine DP or Kadane's |
| "robber / no adjacent" | DP: dp[i] = max(dp[i-1], dp[i-2]+val) |
| "word break / segmentation" | DP + hash set, or Trie |
| "design" / "implement" | Choose right data structure, think API |
| "stream" / "online" | Heap, balanced BST, or amortized structure |
| "frequency" / "mode" | Counter / hash map |
| "graph" not explicitly stated | Build graph from relationships, then BFS/DFS |

---

## Decision Framework: When Stuck

```
1. What is the INPUT SIZE?
   -> Determines max acceptable time complexity (see Big-O sheet)

2. What is the OUTPUT?
   -> Boolean: search/decision -> binary search, DFS, DP
   -> Single value: optimization -> DP, greedy, binary search on answer
   -> All solutions: enumeration -> backtracking
   -> Ordering: topological sort, sort + greedy

3. Can I SORT the input?
   -> Often unlocks two pointers, binary search, greedy

4. Can I use a HASH MAP?
   -> Trade space for time: O(n) lookup instead of O(n) scan

5. Is there OPTIMAL SUBSTRUCTURE + OVERLAPPING SUBPROBLEMS?
   -> Yes: Dynamic Programming
   -> Optimal substructure only: Greedy (prove greedy choice works)

6. Does the problem have a GRAPH structure?
   -> Explicit or implicit graph -> BFS/DFS/Dijkstra

7. Am I choosing from INTERVALS or EVENTS?
   -> Sort by end time (scheduling), sort by start (merging), sweep line
```

---

## Gotchas & Common Mistakes

| Mistake | Fix |
|---|---|
| `list.pop(0)` in a loop | Use `collections.deque.popleft()` -> O(1) |
| `s += char` in a loop | Use `parts.append(char)`, then `''.join(parts)` |
| Mutable default arg `def f(a=[])` | Use `def f(a=None): a = a or []` |
| Modifying list while iterating | Iterate over a copy or use indices |
| Integer overflow | Python has arbitrary precision ints (no overflow) |
| Float precision | Use `math.isclose()` or integer math when possible |
| Off-by-one in binary search | Check: `lo <= hi` vs `lo < hi`, `hi = n` vs `hi = n-1` |
| Forgetting to copy in backtracking | `result.append(path[:])` not `result.append(path)` |
| `@lru_cache` with mutable args | Convert lists to tuples first |
| DFS hitting recursion limit | `sys.setrecursionlimit(10**6)` or use iterative |
| Dijkstra with negative weights | Use Bellman-Ford instead |
| BFS without marking visited early | Mark when ENQUEUING, not when dequeuing |
| Graph: forgetting self-loops/multi-edges | Check problem constraints |
| Sorting stability assumptions | Python sort IS stable (Timsort) |
| `//` with negative numbers | `-7 // 2 = -4` in Python (floors toward -inf), use `int(-7/2) = -3` for truncation toward zero |
