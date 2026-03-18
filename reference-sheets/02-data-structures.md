# Data Structures Reference (Page 1 of 2)

## Python Built-in Types: Operations & Big-O

### list (dynamic array)
| Operation | Avg | Worst | Notes |
|-----------|-----|-------|-------|
| `a[i]` | O(1) | O(1) | index |
| `a[i] = x` | O(1) | O(1) | assign |
| `a.append(x)` | O(1) | O(n) | amortized O(1) |
| `a.pop()` | O(1) | O(1) | pop from end |
| `a.pop(i)` | O(n) | O(n) | shift elements |
| `a.insert(i,x)` | O(n) | O(n) | shift elements |
| `del a[i]` | O(n) | O(n) | shift elements |
| `x in a` | O(n) | O(n) | linear scan |
| `a.sort()` | O(n log n) | O(n log n) | Timsort |
| `a[i:j]` | O(j-i) | O(j-i) | slice copy |
| `a.extend(b)` | O(k) | O(k) | k = len(b) |
| `len(a)` | O(1) | O(1) | |
| `a.reverse()` | O(n) | O(n) | in-place |
| `a + b` | O(n+m) | O(n+m) | creates new list |
| `a * k` | O(nk) | O(nk) | creates new list |

### dict (hash map)
| Operation | Avg | Worst | Notes |
|-----------|-----|-------|-------|
| `d[k]` | O(1) | O(n) | get |
| `d[k] = v` | O(1) | O(n) | set |
| `del d[k]` | O(1) | O(n) | delete |
| `k in d` | O(1) | O(n) | membership |
| `d.get(k, default)` | O(1) | O(n) | safe get |
| `d.keys/values/items` | O(1) | O(1) | view objects |
| `len(d)` | O(1) | O(1) | |
| `d.pop(k)` | O(1) | O(n) | |
| `d.setdefault(k,v)` | O(1) | O(n) | get or set |
| `d1 \| d2` | O(n+m) | | merge (3.9+) |

**Note**: dict preserves insertion order (Python 3.7+). Worst case O(n) from hash collisions (rare).

### set (hash set)
| Operation | Avg | Worst |
|-----------|-----|-------|
| `s.add(x)` | O(1) | O(n) |
| `s.remove(x)` | O(1) | O(n) |
| `s.discard(x)` | O(1) | O(n) |
| `x in s` | O(1) | O(n) |
| `s \| t` (union) | O(n+m) | |
| `s & t` (intersect) | O(min(n,m)) | |
| `s - t` (difference) | O(n) | |
| `s ^ t` (sym diff) | O(n+m) | |
| `s <= t` (subset) | O(n) | |

```python
s = {1, 2, 3}
s.add(4); s.remove(4)       # remove raises KeyError if missing
s.discard(4)                 # no error if missing
s.pop()                      # remove/return arbitrary element
frozenset({1,2,3})           # immutable, hashable (usable as dict key)
```

### tuple
- Immutable, hashable (usable as dict keys/set elements if contents are hashable)
- `O(1)` index, `O(n)` search, `O(n)` iteration
- Unpacking: `a, b, *rest = (1, 2, 3, 4, 5)`

---

## Array/List Patterns

### Two Pointers (sorted array or opposite ends)
```python
# Pair sum in sorted array
def two_sum_sorted(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == target: return [lo, hi]
        elif s < target: lo += 1
        else: hi -= 1
    return []

# Remove duplicates in-place (sorted)
def remove_dupes(a):
    if not a: return 0
    w = 1  # write pointer
    for r in range(1, len(a)):
        if a[r] != a[r-1]:
            a[w] = a[r]; w += 1
    return w
```

### Sliding Window
```python
# Fixed size window: max sum of subarray of size k
def max_sum_k(a, k):
    s = sum(a[:k])
    best = s
    for i in range(k, len(a)):
        s += a[i] - a[i-k]
        best = max(best, s)
    return best

# Variable size: smallest subarray with sum >= target
def min_subarray(a, target):
    lo = total = 0
    best = float('inf')
    for hi in range(len(a)):
        total += a[hi]
        while total >= target:
            best = min(best, hi - lo + 1)
            total -= a[lo]; lo += 1
    return best if best != float('inf') else 0
```

### Prefix Sum
```python
# Build prefix sum
pre = [0] * (len(a) + 1)
for i in range(len(a)):
    pre[i+1] = pre[i] + a[i]
# Sum of a[i..j] inclusive = pre[j+1] - pre[i]

# 2D Prefix Sum
m, n = len(grid), len(grid[0])
pre = [[0]*(n+1) for _ in range(m+1)]
for i in range(m):
    for j in range(n):
        pre[i+1][j+1] = grid[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j]
# Sum of submatrix (r1,c1) to (r2,c2) inclusive:
# pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]
```

---

## Stack / Queue

```python
# Stack (LIFO) - use list
stack = []
stack.append(x)              # push O(1)
stack.pop()                  # pop  O(1)
stack[-1]                    # peek O(1)

# Queue (FIFO) - use deque (NOT list.pop(0) which is O(n))
from collections import deque
q = deque()
q.append(x)                 # enqueue O(1)
q.popleft()                 # dequeue O(1)
q[0]                         # peek    O(1)

# Monotonic stack: next greater element
def next_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []               # stores indices
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res
```

---

# Data Structures Reference (Page 2 of 2)

## Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Dummy head pattern (simplifies edge cases)
dummy = ListNode(0)
dummy.next = head
# ... manipulate list ...
return dummy.next

# Reverse linked list
def reverse(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Find middle (slow/fast pointers)
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle node (2nd middle if even length)

# Detect cycle
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast: return True
    return False

# Find cycle start
def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

## Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Inorder (left, root, right) - BST gives sorted order
def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Iterative inorder (useful pattern)
def inorder_iter(root):
    res, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res

# Level-order (BFS)
def level_order(root):
    if not root: return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
```

### Trie
```python
class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for c in word:
            if c not in node.children:
                node.children[c] = Trie()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.is_end

    def starts_with(self, prefix):
        node = self
        for c in prefix:
            if c not in node.children: return False
            node = node.children[c]
        return True
```

## Graph Representations

```python
# Adjacency list (most common) - dict of lists
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)          # undirected

# Adjacency list from n nodes, 0-indexed
graph = [[] for _ in range(n)]
for u, v in edges:
    graph[u].append(v)

# Weighted adjacency list
graph = defaultdict(list)
for u, v, w in edges:
    graph[u].append((v, w))

# Adjacency matrix (dense graphs or need O(1) edge lookup)
adj = [[0]*n for _ in range(n)]
for u, v in edges:
    adj[u][v] = 1
    adj[v][u] = 1               # undirected

# Edge list (for Union-Find / Kruskal's)
edges = [(weight, u, v), ...]
edges.sort()                     # sort by weight
```

## Hash Map / Set Patterns

```python
# Two Sum (unsorted): value -> index
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        comp = target - x
        if comp in seen: return [seen[comp], i]
        seen[x] = i

# Group anagrams: sorted string as key
groups = defaultdict(list)
for s in strs:
    groups[tuple(sorted(s))].append(s)

# Subarray sum equals k (prefix sum + hash map)
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}               # prefix_sum -> count of occurrences
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

# Longest substring without repeating chars
def length_of_longest(s):
    seen = {}
    lo = best = 0
    for hi, c in enumerate(s):
        if c in seen and seen[c] >= lo:
            lo = seen[c] + 1
        seen[c] = hi
        best = max(best, hi - lo + 1)
    return best
```
