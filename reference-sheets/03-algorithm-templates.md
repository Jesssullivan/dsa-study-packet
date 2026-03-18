# Algorithm Templates (Page 1 of 4)

## Binary Search (3 Variants)

### Variant 1: Find exact value
```python
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if a[mid] == target:   return mid
        elif a[mid] < target:  lo = mid + 1
        else:                  hi = mid - 1
    return -1  # not found
```

### Variant 2: Find leftmost (first) position where condition is True
```python
# Find smallest index where condition(a[i]) is True
# Precondition: a is partitioned: [F,F,F,...,T,T,T]
def bisect_left_cond(a, target):
    lo, hi = 0, len(a)       # NOTE: hi = len(a), not len(a)-1
    while lo < hi:            # NOTE: lo < hi, not lo <= hi
        mid = lo + (hi - lo) // 2
        if a[mid] < target:   # condition: a[mid] >= target
            lo = mid + 1
        else:
            hi = mid
    return lo                 # first index where a[i] >= target

# Use cases: lower bound, first occurrence, minimum value satisfying condition
```

### Variant 3: Find rightmost (last) position where condition is True
```python
# Find largest index where condition is True
# Precondition: a is partitioned: [T,T,T,...,F,F,F]
def bisect_right_cond(a, target):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] <= target:  # condition: a[mid] <= target
            lo = mid + 1
        else:
            hi = mid
    return lo - 1             # last index where a[i] <= target

# Use cases: upper bound, last occurrence, maximum value satisfying condition
```

### Binary Search on Answer (Minimize/Maximize)
```python
# "What is the minimum X such that feasible(X) is True?"
# feasible goes: [F, F, F, ..., T, T, T]
def min_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# "What is the maximum X such that feasible(X) is True?"
# feasible goes: [T, T, T, ..., F, F, F]
def max_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # NOTE: round up to avoid infinite loop
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

# Float binary search
def float_bs(lo, hi, eps=1e-9):
    for _ in range(100):       # 100 iterations gives ~10^-30 precision
        mid = (lo + hi) / 2
        if feasible(mid): hi = mid
        else: lo = mid
    return lo
```

---

## BFS / DFS Templates

### BFS on Graph (shortest path in unweighted graph)
```python
from collections import deque

def bfs(graph, start, target):
    q = deque([start])
    visited = {start}
    dist = 0
    while q:
        for _ in range(len(q)):     # process level by level
            node = q.popleft()
            if node == target:
                return dist
            for nei in graph[node]:
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)
        dist += 1
    return -1  # not reachable
```

### BFS on Grid
```python
def bfs_grid(grid, sr, sc):
    m, n = len(grid), len(grid[0])
    q = deque([(sr, sc)])
    visited = {(sr, sc)}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    dist = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr,nc) not in visited and grid[nr][nc] != '#':
                    visited.add((nr, nc))
                    q.append((nr, nc))
        dist += 1
    return dist
```

### Multi-source BFS
```python
# Start BFS from all sources simultaneously (e.g., "rotting oranges")
q = deque()
for r in range(m):
    for c in range(n):
        if grid[r][c] == SOURCE:
            q.append((r, c))
            visited.add((r, c))
# Then standard BFS loop
```

### DFS on Graph (recursive)
```python
def dfs(graph, node, visited):
    visited.add(node)
    for nei in graph[node]:
        if nei not in visited:
            dfs(graph, nei, visited)
```

### DFS on Graph (iterative)
```python
def dfs_iter(graph, start):
    stack = [start]
    visited = {start}
    while stack:
        node = stack.pop()
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                stack.append(nei)
```

### DFS on Tree (common patterns)
```python
# Height of tree
def height(root):
    if not root: return 0
    return 1 + max(height(root.left), height(root.right))

# Path sum (root to leaf)
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:  # leaf
        return target == root.val
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))

# Lowest Common Ancestor
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right: return root
    return left or right
```

---

# Algorithm Templates (Page 2 of 4)

## Topological Sort

### Kahn's Algorithm (BFS, gives one valid ordering)
```python
from collections import deque, defaultdict

def topo_sort_kahn(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:          # u -> v
        graph[u].append(v)
        indegree[v] += 1

    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    if len(order) != n:
        return []               # cycle detected
    return order
```

### DFS-based Topological Sort
```python
def topo_sort_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order = []
    has_cycle = False

    def dfs(u):
        nonlocal has_cycle
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                has_cycle = True; return
            if color[v] == WHITE:
                dfs(v)
        color[u] = BLACK
        order.append(u)

    for i in range(n):
        if color[i] == WHITE:
            dfs(i)
    if has_cycle: return []
    return order[::-1]          # reverse post-order
```

## Shortest Path Algorithms

### Dijkstra's (non-negative weights, single source)
```python
import heapq

def dijkstra(graph, src, n):
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]             # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:         # skip outdated entries
            continue
        for v, w in graph[u]:   # (neighbor, weight)
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist                 # dist[i] = shortest dist from src to i
# Time: O((V+E) log V)  Space: O(V+E)
```

### Bellman-Ford (handles negative weights, detects negative cycles)
```python
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(n - 1):       # relax n-1 times
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None          # negative cycle exists

    return dist
# Time: O(VE)  Space: O(V)
```

### Floyd-Warshall (all pairs shortest path)
```python
def floyd_warshall(n, edges):
    dist = [[float('inf')]*n for _ in range(n)]
    for i in range(n): dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):           # intermediate vertex
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
# Time: O(V^3)  Space: O(V^2)
```

## Union-Find (Disjoint Set Union)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False          # already connected
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True                        # newly connected

    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Time: O(alpha(n)) per operation ~ O(1) amortized
# Use cases: connected components, cycle detection, Kruskal's MST
```

---

# Algorithm Templates (Page 3 of 4)

## Sliding Window

### Fixed Size
```python
def fixed_window(a, k):
    # Process window [0, k)
    window_state = ...  # initialize with a[0:k]
    best = evaluate(window_state)
    for i in range(k, len(a)):
        # Add a[i] (entering element)
        # Remove a[i-k] (leaving element)
        best = max(best, evaluate(window_state))
    return best
```

### Variable Size (Shrinkable)
```python
# Longest/largest window satisfying some condition
def variable_window(a):
    lo = 0
    best = 0
    for hi in range(len(a)):
        # Expand: add a[hi] to window state
        while not valid():        # window invalid
            # Shrink: remove a[lo] from window state
            lo += 1
        best = max(best, hi - lo + 1)
    return best

# Shortest window satisfying some condition
def shortest_window(a, target):
    lo = 0
    best = float('inf')
    for hi in range(len(a)):
        # Expand: add a[hi] to window state
        while valid():            # window valid -- try to shrink
            best = min(best, hi - lo + 1)
            # Shrink: remove a[lo] from window state
            lo += 1
    return best
```

### Sliding Window with Counter (string pattern problems)
```python
from collections import Counter
def find_anagrams(s, p):
    if len(p) > len(s): return []
    pc = Counter(p)
    sc = Counter(s[:len(p)])
    res = []
    if sc == pc: res.append(0)
    for i in range(len(p), len(s)):
        sc[s[i]] += 1                  # add right
        left = s[i - len(p)]
        sc[left] -= 1                  # remove left
        if sc[left] == 0: del sc[left]
        if sc == pc: res.append(i - len(p) + 1)
    return res
```

## Two Pointers Patterns

```python
# Pattern 1: Opposite ends (sorted array)
lo, hi = 0, len(a) - 1
while lo < hi:
    # Use a[lo] and a[hi]
    # Move lo right or hi left based on condition

# Pattern 2: Same direction (fast/slow for linked list)
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

# Pattern 3: Merge two sorted arrays
i = j = 0
while i < len(a) and j < len(b):
    if a[i] <= b[j]:
        result.append(a[i]); i += 1
    else:
        result.append(b[j]); j += 1
# Append remaining: result.extend(a[i:]) + result.extend(b[j:])

# Pattern 4: Partition (Dutch National Flag / 3-way partition)
lo, mid, hi = 0, 0, len(a) - 1
while mid <= hi:
    if a[mid] < pivot:
        a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
    elif a[mid] > pivot:
        a[mid], a[hi] = a[hi], a[mid]; hi -= 1
    else:
        mid += 1
```

## Backtracking Template

```python
def backtrack(candidates, path, result, start):
    if is_solution(path):
        result.append(path[:])        # make a copy!
        return
    for i in range(start, len(candidates)):
        # Optional: skip duplicates
        if i > start and candidates[i] == candidates[i-1]:
            continue
        # Optional: pruning
        if not is_valid(candidates[i], path):
            continue
        path.append(candidates[i])     # choose
        backtrack(candidates, path, result, i + 1)  # explore
        # NOTE: use i (not i+1) if elements can be reused
        path.pop()                     # un-choose

result = []
candidates.sort()                      # sort if skipping duplicates
backtrack(candidates, [], result, 0)
```

### Common Backtracking Problems
```python
# Subsets (power set)
def subsets(nums):
    res = []
    def bt(start, path):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return res

# Permutations
def permutations(nums):
    res = []
    def bt(path, used):
        if len(path) == len(nums):
            res.append(path[:]); return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            bt(path, used)
            path.pop()
            used[i] = False
    bt([], [False]*len(nums))
    return res

# N-Queens (constraint satisfaction)
def n_queens(n):
    res = []
    cols, diag1, diag2 = set(), set(), set()
    def bt(r, board):
        if r == n:
            res.append([''.join(row) for row in board]); return
        for c in range(n):
            if c in cols or r-c in diag1 or r+c in diag2: continue
            cols.add(c); diag1.add(r-c); diag2.add(r+c)
            board[r][c] = 'Q'
            bt(r+1, board)
            board[r][c] = '.'
            cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)
    bt(0, [['.']*n for _ in range(n)])
    return res
```

---

# Algorithm Templates (Page 4 of 4)

## Dynamic Programming Patterns

### Top-Down (Memoization)
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    if base_case(state): return base_value
    result = initial_value
    for choice in choices(state):
        result = combine(result, dp(next_state(state, choice)))
    return result
# Remember: args must be hashable. Use tuples, not lists.
```

### Bottom-Up (Tabulation)
```python
# 1D DP
dp = [0] * (n + 1)
dp[0] = base_value
for i in range(1, n + 1):
    dp[i] = recurrence(dp, i)
return dp[n]

# 2D DP
dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        dp[i][j] = recurrence(dp, i, j)
return dp[n][m]
```

### Classic DP Problems

```python
# Fibonacci: dp[i] = dp[i-1] + dp[i-2]

# Climbing stairs: dp[i] = dp[i-1] + dp[i-2]

# Coin change (minimum coins): dp[i] = min(dp[i-coin]+1) for coin in coins
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# 0/1 Knapsack
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            dp[i][w] = dp[i-1][w]                     # skip item
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                    dp[i-1][w-weights[i-1]] + values[i-1])  # take item
    return dp[n][W]

# LCS (Longest Common Subsequence)
def lcs(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# LIS (Longest Increasing Subsequence) - O(n log n)
import bisect
def lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

# Edit Distance
def edit_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

### DP Space Optimization (rolling array)
```python
# When dp[i] only depends on dp[i-1], use two rows or a single row
prev = [0] * (m + 1)
curr = [0] * (m + 1)
for i in range(1, n + 1):
    for j in range(1, m + 1):
        curr[j] = recurrence(prev, curr, j)
    prev, curr = curr, [0] * (m + 1)
```

## Monotonic Stack / Queue

```python
# Monotonic decreasing stack: find next greater element
# Also used for: largest rectangle in histogram, trapping rain water
def largest_rectangle(heights):
    stack = []                      # indices of increasing heights
    max_area = 0
    heights.append(0)               # sentinel
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area

# Monotonic deque: sliding window maximum
def max_sliding_window(nums, k):
    dq = deque()                    # indices of decreasing values
    res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                # maintain decreasing order
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()           # remove out-of-window
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

## Quick Select (kth smallest, average O(n))

```python
import random
def quick_select(nums, k):         # k is 1-indexed
    pivot = random.choice(nums)
    lo = [x for x in nums if x < pivot]
    eq = [x for x in nums if x == pivot]
    hi = [x for x in nums if x > pivot]

    if k <= len(lo):
        return quick_select(lo, k)
    elif k <= len(lo) + len(eq):
        return pivot
    else:
        return quick_select(hi, k - len(lo) - len(eq))
# Average O(n), worst O(n^2). Randomized pivot makes worst case rare.
```

## Merge Sort / Count Inversions

```python
def merge_sort_count(arr):
    if len(arr) <= 1: return arr, 0
    mid = len(arr) // 2
    left, l_inv = merge_sort_count(arr[:mid])
    right, r_inv = merge_sort_count(arr[mid:])
    merged, split_inv = merge_count(left, right)
    return merged, l_inv + r_inv + split_inv

def merge_count(left, right):
    i = j = inv = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            inv += len(left) - i    # all remaining left elements are inversions
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv
```

## Kruskal's MST (with Union-Find)

```python
def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # sort by weight
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    for u, v, w in edges:
        if uf.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1: break
    return mst_weight, mst_edges
```

## Interval Problems

```python
# Merge overlapping intervals
def merge_intervals(intervals):
    intervals.sort()
    merged = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged

# Minimum meeting rooms (sweep line)
def min_rooms(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))    # start
        events.append((e, -1))   # end
    events.sort()
    curr = best = 0
    for _, delta in events:
        curr += delta
        best = max(best, curr)
    return best
```
