# Python Standard Library Cheat Sheet (Page 1 of 2)

## `collections`

### Counter
```python
from collections import Counter
c = Counter("abracadabra")       # Counter({'a':5,'b':2,'r':2,'c':1,'d':1})
c.most_common(2)                 # [('a',5),('b',2)]
c['z']                           # 0 (missing keys return 0)
c.update("aaa")                  # add counts
c.subtract(Counter("a"))         # subtract counts
c1 + c2                          # combine counts (drops zero/neg)
c1 - c2                          # subtract (drops zero/neg)
c1 & c2                          # min of each count
c1 | c2                          # max of each count
list(c.elements())               # iterator of elements repeated by count
+c                               # drop zero/negative counts
```

### defaultdict
```python
from collections import defaultdict
g = defaultdict(list)            # missing key -> []
g[0].append(1)                   # no KeyError
d = defaultdict(int)             # missing key -> 0
d = defaultdict(set)             # missing key -> set()
d = defaultdict(lambda: float('inf'))
```

### deque
```python
from collections import deque
dq = deque([1,2,3], maxlen=5)   # optional maxlen (auto-evicts)
dq.append(4)                    # right append    O(1)
dq.appendleft(0)                # left append     O(1)
dq.pop()                        # right pop       O(1)
dq.popleft()                    # left pop        O(1)
dq.rotate(1)                    # rotate right: [3,1,2]
dq.rotate(-1)                   # rotate left:  [2,3,1]
dq.extend([5,6])                # right extend
dq.extendleft([5,6])            # left extend (reverses order)
```

### OrderedDict
```python
from collections import OrderedDict
od = OrderedDict()
od['a'] = 1; od['b'] = 2
od.move_to_end('a')             # move to end
od.move_to_end('a', last=False) # move to front
od.popitem(last=True)           # pop from end (LIFO)
od.popitem(last=False)          # pop from front (FIFO)
# LRU cache pattern: move_to_end on access, popitem(last=False) to evict
```

### ChainMap
```python
from collections import ChainMap
defaults = {'color': 'red', 'size': 10}
overrides = {'color': 'blue'}
cm = ChainMap(overrides, defaults)
cm['color']   # 'blue' (first found wins)
cm['size']    # 10
cm.maps       # [overrides, defaults] - mutable list
```

---

## `itertools`

```python
import itertools as it

# COMBINATORIC
it.product('AB','xy')          # Ax Ay Bx By (cartesian product)
it.product(range(3), repeat=2) # 00 01 02 10 11 12 20 21 22
it.permutations('ABC', 2)      # AB AC BA BC CA CB  (n!/(n-r)!)
it.combinations('ABC', 2)      # AB AC BC           (nCr)
it.combinations_with_replacement('ABC', 2)  # AA AB AC BB BC CC

# INFINITE
it.count(10, 2)                # 10, 12, 14, 16, ...
it.cycle('AB')                 # A, B, A, B, ...
it.repeat(5, 3)                # 5, 5, 5

# TERMINATING
it.chain([1,2], [3,4])         # 1, 2, 3, 4  (flatten one level)
it.chain.from_iterable([[1,2],[3,4]])  # same
it.accumulate([1,2,3,4])       # 1, 3, 6, 10  (running sum)
it.accumulate([3,1,4], max)    # 3, 3, 4      (running max)
it.accumulate([3,1,4], min)    # 3, 1, 1      (running min)

list(it.groupby('AAABBC'))     # [(A,[A,A,A]),(B,[B,B]),(C,[C])]
# MUST sort first if groups aren't contiguous

it.islice(range(100), 5)       # first 5 elements
it.islice(range(100), 2, 8, 2) # [2, 4, 6] (start, stop, step)
it.takewhile(lambda x: x<5, [1,3,6,2])  # [1, 3]
it.dropwhile(lambda x: x<5, [1,3,6,2])  # [6, 2]
it.starmap(pow, [(2,3),(3,2)]) # [8, 9]
it.compress('ABCDE', [1,0,1,0,1])  # A, C, E
it.filterfalse(lambda x: x%2, range(10))  # 0,2,4,6,8
it.zip_longest([1,2],[3,4,5], fillvalue=0) # (1,3),(2,4),(0,5)
it.pairwise([1,2,3,4])         # (1,2),(2,3),(3,4)  # Python 3.10+
it.batched('ABCDEFG', 3)       # ABC DEF G          # Python 3.12+
```

---

## `functools`

```python
from functools import lru_cache, cache, reduce, partial

@lru_cache(maxsize=None)        # unbounded memoization
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

@cache                          # Python 3.9+, same as lru_cache(maxsize=None)
def expensive(x, y): ...

# WARNING: lru_cache args must be HASHABLE (no lists/dicts/sets)
# Convert: tuple(lst), frozenset(s), tuple(sorted(d.items()))

reduce(lambda a, b: a + b, [1,2,3,4])  # 10
reduce(lambda a, b: a * b, [1,2,3,4])  # 24
reduce(lambda a, b: a + b, [1,2,3], 100)  # 106 (with initial)

add5 = partial(lambda x, y: x + y, 5)
add5(3)  # 8

# singledispatch: generic function overloading by first arg type
from functools import singledispatch
@singledispatch
def process(arg): print(f"default: {arg}")
@process.register(int)
def _(arg): print(f"int: {arg}")
```

---

# Python Standard Library Cheat Sheet (Page 2 of 2)

## `heapq` (min-heap only)

```python
import heapq
h = []
heapq.heappush(h, 5)            # push element             O(log n)
heapq.heappush(h, (1, 'task'))  # push tuple (priority, value)
val = heapq.heappop(h)          # pop smallest              O(log n)
h[0]                             # peek at smallest          O(1)
heapq.heapify(lst)               # convert list to heap      O(n)
heapq.heapreplace(h, val)       # pop then push (more efficient)
heapq.heappushpop(h, val)       # push then pop (more efficient)
heapq.nlargest(3, lst)          # 3 largest                 O(n log k)
heapq.nsmallest(3, lst)         # 3 smallest                O(n log k)
heapq.nlargest(3, lst, key=lambda x: x[1])  # with key func
heapq.merge(*sorted_iters)     # merge sorted iterables    O(n log k)

# MAX HEAP: negate values
heapq.heappush(h, -val)         # push negated
-heapq.heappop(h)               # pop and negate back

# Custom objects: use tuple (priority, tiebreaker, object)
# or implement __lt__ on your class
```

## `bisect` (binary search on sorted lists)

```python
import bisect
a = [1, 3, 3, 5, 7]
bisect.bisect_left(a, 3)        # 1  (leftmost insertion point)
bisect.bisect_right(a, 3)       # 3  (rightmost insertion point)
bisect.bisect(a, 3)             # 3  (alias for bisect_right)
bisect.insort_left(a, 4)        # insert maintaining sort   O(n)
bisect.insort_right(a, 4)       # insert maintaining sort   O(n)

# Find index of value (exact match)
i = bisect.bisect_left(a, x)
found = i < len(a) and a[i] == x

# Find leftmost value >= x
i = bisect.bisect_left(a, x)    # a[i] >= x (or i == len(a))

# Find rightmost value <= x
i = bisect.bisect_right(a, x) - 1  # a[i] <= x (or i == -1)

# Count occurrences of x in sorted list
lo = bisect.bisect_left(a, x)
hi = bisect.bisect_right(a, x)
count = hi - lo
```

## `math`

```python
import math
math.gcd(12, 8)                  # 4
math.lcm(4, 6)                   # 12  (Python 3.9+)
math.gcd(12, 8, 6)               # 2   (multi-arg, Python 3.9+)
math.comb(5, 2)                   # 10  (5 choose 2, i.e., nCr)
math.perm(5, 2)                   # 20  (nPr)
math.factorial(5)                 # 120
math.inf                          # positive infinity
-math.inf                         # negative infinity
math.ceil(3.2)                    # 4
math.floor(3.8)                   # 3
math.log(8, 2)                    # 3.0
math.log2(8)                      # 3.0  (more precise than log(x,2))
math.log10(1000)                  # 3.0
math.sqrt(16)                     # 4.0
math.isqrt(10)                    # 3    (integer sqrt, Python 3.8+)
math.pow(2, 10)                   # 1024.0 (float)
math.prod([1,2,3,4])             # 24   (Python 3.8+)
math.copysign(1, -3)              # -1.0
math.isinf(x), math.isnan(x)
```

## String Methods Quick Reference

```python
s = "hello world"
s.split()                    # ['hello', 'world']
s.split(',', maxsplit=1)     # split on comma, max 1 split
s.rsplit(',', 1)             # split from right
s.strip()                    # strip whitespace both sides
s.lstrip('h')                # strip from left
s.rstrip('d')                # strip from right
s.replace('l', 'L', 1)      # replace first occurrence
s.find('lo')                 # 3 (index, or -1 if not found)
s.index('lo')                # 3 (raises ValueError if not found)
s.rfind('l')                 # 9 (rightmost)
s.count('l')                 # 3
s.startswith('he')           # True
s.endswith(('d','s'))        # True (tuple of suffixes)
s.isalpha(), s.isdigit(), s.isalnum()
s.upper(), s.lower(), s.title(), s.capitalize(), s.swapcase()
s.zfill(15)                  # '0000hello world'
','.join(['a','b','c'])      # 'a,b,c'
s.partition(' ')             # ('hello', ' ', 'world')
s.rpartition(' ')            # ('hello', ' ', 'world')
chr(97)                      # 'a'
ord('a')                     # 97
```

## `sorted()` and Sorting

```python
sorted(lst)                              # ascending
sorted(lst, reverse=True)               # descending
sorted(lst, key=lambda x: x[1])         # by second element
sorted(lst, key=lambda x: (-x[0], x[1]))# primary desc, secondary asc
sorted(s, key=str.lower)                # case-insensitive

# Custom comparator (cmp_to_key)
from functools import cmp_to_key
def compare(a, b):            # return negative/zero/positive
    return (a > b) - (a < b)  # standard 3-way compare
sorted(lst, key=cmp_to_key(compare))

# Stable sort: equal elements keep original order
# list.sort() is in-place, sorted() returns new list
# Both use Timsort: O(n log n) worst, O(n) when nearly sorted

# Sort dict by value
sorted(d.items(), key=lambda x: x[1])
```

## Useful Built-ins Reminder

```python
zip(a, b)                    # pair elements, stops at shorter
enumerate(lst, start=0)      # (index, value) pairs
map(fn, iterable)            # apply fn to each element
filter(fn, iterable)         # keep elements where fn is truthy
any(iterable)                # True if any truthy
all(iterable)                # True if all truthy
min(a, key=..., default=...) # min with key func and default
max(a, key=..., default=...) # max with key func and default
sum(iterable, start=0)       # sum with optional start
abs(-5)                       # 5
divmod(17, 5)                 # (3, 2)  (quotient, remainder)
pow(2, 10, MOD)              # modular exponentiation (fast)
isinstance(x, (int, float))  # type check
float('inf'), float('-inf')
int('1010', 2)               # 10  (binary string to int)
bin(10)                       # '0b1010'
bin(10).count('1')            # popcount = 2
```
