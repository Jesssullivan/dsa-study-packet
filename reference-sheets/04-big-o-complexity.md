# Big-O Complexity Reference (1 page)

## Common Time Complexities (fastest to slowest)

| Notation | Name | Example | n=10^6 ops |
|----------|------|---------|------------|
| O(1) | Constant | Hash lookup, array index | 1 |
| O(log n) | Logarithmic | Binary search | 20 |
| O(sqrt(n)) | Square root | Trial division | 1000 |
| O(n) | Linear | Linear scan, counting sort | 10^6 |
| O(n log n) | Linearithmic | Merge sort, heap sort | 2x10^7 |
| O(n^2) | Quadratic | Nested loops, bubble sort | 10^12 BAD |
| O(n^3) | Cubic | Floyd-Warshall, matrix mult | 10^18 BAD |
| O(2^n) | Exponential | Subsets, brute force | heat death |
| O(n!) | Factorial | Permutations | heat death |

**Rule of thumb**: ~10^8 simple operations per second in Python. For n=10^6, need O(n log n) or better.

| n limit | Target complexity |
|---------|-------------------|
| n <= 10 | O(n!) or O(2^n) |
| n <= 20 | O(2^n) |
| n <= 25 | O(2^(n/2)) |
| n <= 100 | O(n^3) |
| n <= 1000 | O(n^2) |
| n <= 10^5 | O(n log n) |
| n <= 10^6 | O(n) or O(n log n) |
| n <= 10^8 | O(n) |
| n > 10^8 | O(log n) or O(1) |

---

## Python Built-in Operation Costs

### list
| Operation | Time |
|-----------|------|
| `a[i]`, `a[i]=x`, `len`, `append`, `pop()` | O(1) |
| `pop(i)`, `insert(i,x)`, `del a[i]`, `x in a`, `index` | O(n) |
| `sort` | O(n log n) |
| `a[i:j]`, `extend(k items)` | O(j-i), O(k) |
| `a + b` | O(n+m) |

### dict / set
| Operation | Average |
|-----------|---------|
| `get`, `set`, `del`, `in`, `add`, `remove` | O(1) |
| `union`, `intersection`, `difference` | O(n+m), O(min), O(n) |
| `iteration` | O(n) |

### str
| Operation | Time |
|-----------|------|
| `s[i]`, `len` | O(1) |
| `s + t`, `s[i:j]`, `in`, `find`, `replace`, `split`, `join` | O(n) |
| **Danger**: `s += c` in loop = O(n^2) total. Use `''.join(parts)` |

### deque
| Operation | Time |
|-----------|------|
| `append`, `appendleft`, `pop`, `popleft` | O(1) |
| `a[i]` (random access) | O(n) |

---

## Sorting Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable | Notes |
|-----------|------|---------|-------|-------|--------|-------|
| **Timsort** (Python) | O(n) | O(n log n) | O(n log n) | O(n) | Yes | Python's `sorted()`/`list.sort()` |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Divide & conquer |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No | Randomized pivot avoids worst |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | In-place but not cache-friendly |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | k = range of values |
| Radix Sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes | d = digits, k = base |
| Bucket Sort | O(n+k) | O(n+k) | O(n^2) | O(n+k) | Yes | Uniform distribution |

---

## Graph Algorithm Complexities

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| BFS / DFS | O(V+E) | O(V) | Adj list; O(V^2) with adj matrix |
| Topological Sort | O(V+E) | O(V) | DAG only |
| Dijkstra (binary heap) | O((V+E) log V) | O(V) | Non-negative weights |
| Dijkstra (Fibonacci heap) | O(E + V log V) | O(V) | Theoretical, rarely used |
| Bellman-Ford | O(VE) | O(V) | Handles negative weights |
| Floyd-Warshall | O(V^3) | O(V^2) | All pairs |
| Kruskal's MST | O(E log E) | O(V) | With Union-Find |
| Prim's MST | O((V+E) log V) | O(V) | With binary heap |
| Union-Find (ops) | O(alpha(n)) ~ O(1) | O(n) | Per operation, amortized |

---

## Space Complexity Rules of Thumb

| Structure / Operation | Space |
|-----------------------|-------|
| Recursion depth d | O(d) stack frames |
| DFS on tree | O(h) where h = height (O(log n) balanced, O(n) skewed) |
| BFS on tree | O(w) where w = max width (up to O(n/2) = O(n)) |
| BFS on graph | O(V) for visited set + queue |
| Hash map of n items | O(n) |
| 2D DP table n x m | O(nm) -- optimize to O(min(n,m)) with rolling array |
| Adjacency list | O(V+E) |
| Adjacency matrix | O(V^2) |
| Sorting (Timsort) | O(n) auxiliary |
| Heap | O(n) to store, O(1) auxiliary for operations |
| Trie of k words, avg len L | O(k * L) worst case |

### Recursion Stack Depth
- Python default recursion limit: **1000**
- Increase with: `import sys; sys.setrecursionlimit(10**6)`
- Better: convert to iterative with explicit stack for deep recursion

### Common Space Optimizations
- **DP rolling array**: O(nm) -> O(m) when row i depends only on row i-1
- **Bit manipulation**: Use int as bitset (Python ints are arbitrary precision)
- **In-place modification**: Mark visited in grid with sentinel value
- **Generator/iterator**: Process stream without storing all in memory
