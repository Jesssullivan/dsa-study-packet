"""
================================================================================
ALGORITHM & DATA STRUCTURE INTERVIEW STUDY GUIDE
================================================================================
Target: Backend-Focused Full-Stack Engineer @ target employer (Aviation/Air Traffic Domain)

Difficulty ratings:
  [E] = Easy   — Expected to solve in <10 min, warm-up level
  [M] = Medium — Core interview questions, 15-25 min
  [H] = Hard   — Differentiators, 25-40 min

Each section covers:
  1. Must-know problems with descriptions
  2. Key patterns & techniques
  3. Python idioms
  4. Complexity notes
================================================================================
"""

# ==============================================================================
# 1. ARRAYS & HASHING
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Two Sum                  — Find two indices whose values sum to target.
                               Hash map: store complement -> index as you iterate.

[E] Contains Duplicate       — Return True if any value appears twice.
                               set() and check membership.

[M] Group Anagrams           — Group strings that are anagrams of each other.
                               Sort each string as key, or use Counter as key.

[M] Top K Frequent Elements  — Return the k most frequent elements.
                               Counter + heap, or bucket sort by frequency.

[M] Product of Array Except  — Product of all elements except self, no division.
    Self                       Two-pass: prefix products then suffix products.

[M] Valid Sudoku             — Check if a 9x9 board is valid (no repeats in
                               row/col/box). Sets for each row, col, and 3x3 box.

[M] Encode and Decode        — Design encode/decode for list of strings.
    Strings                    Length-prefix: "4#word" format.

[M] Longest Consecutive      — Length of longest consecutive element sequence.
    Sequence                   Put all in set, only start counting from numbers
                               where (n-1) not in set. O(n).

[H] First Missing Positive   — Find smallest missing positive int in O(n) time,
                               O(1) space. Cyclic sort: place each num at index
                               num-1.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Hash map for O(1) lookup / counting / grouping
- Frequency counting with collections.Counter
- Bucket sort when frequency is bounded
- Cyclic sort for "missing/duplicate in range [1,n]" problems
- Tuple of sorted string or frozenset as hashable group key

PYTHON IDIOMS:
──────────────
    from collections import Counter, defaultdict

    # Two Sum — single pass hash map
    def two_sum(nums, target):
        seen = {}
        for i, n in enumerate(nums):
            comp = target - n
            if comp in seen:
                return [seen[comp], i]
            seen[n] = i

    # Group Anagrams — sorted-string key
    def group_anagrams(strs):
        groups = defaultdict(list)
        for s in strs:
            groups[tuple(sorted(s))].append(s)
        return list(groups.values())

    # Top K Frequent — bucket sort O(n)
    def top_k_frequent(nums, k):
        count = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)
        result = []
        for i in range(len(buckets) - 1, -1, -1):
            result.extend(buckets[i])
            if len(result) >= k:
                return result[:k]

    # Longest Consecutive Sequence — set-based O(n)
    def longest_consecutive(nums):
        num_set = set(nums)
        best = 0
        for n in num_set:
            if n - 1 not in num_set:       # start of a sequence
                length = 0
                while n + length in num_set:
                    length += 1
                best = max(best, length)
        return best

COMPLEXITY NOTES:
─────────────────
- Hash map ops: O(1) average, O(n) worst (rare with good hash)
- Counter construction: O(n)
- Sorting-based grouping: O(n * k log k) where k = string length
- Bucket sort: O(n) when range is bounded
"""


# ==============================================================================
# 2. TWO POINTERS
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Valid Palindrome          — Ignore non-alphanumeric, case-insensitive check.
                                Two pointers from both ends, skip non-alnum.

[M] Two Sum II (sorted)       — Input array is sorted. Left/right pointer,
                                shrink based on sum comparison.

[M] 3Sum                      — Find all unique triplets summing to zero.
                                Sort + fix one element + two-pointer on rest.
                                Skip duplicates carefully.

[M] Container With Most Water — Max area between two vertical lines.
                                Left/right pointers, move the shorter side.

[M] Trapping Rain Water       — Total water trapped between bars.
                                Two pointers with left_max / right_max tracking,
                                or prefix/suffix max arrays.

[H] Trapping Rain Water       — The two-pointer approach is preferred:
    (optimal)                   move the pointer with the smaller max inward.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Sorted array → two pointers from ends (converging)
- Opposite ends for palindrome / pair-sum
- Same direction for fast/slow or partitioning
- Fix one element and reduce to 2Sum for 3Sum
- Duplicate skipping: while l < r and nums[l] == nums[l-1]: l += 1

PYTHON IDIOMS:
──────────────
    # 3Sum — sort + two pointers, O(n^2)
    def three_sum(nums):
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # skip duplicate fixed element
            lo, hi = i + 1, len(nums) - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1
                elif total > 0:
                    hi -= 1
                else:
                    result.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
        return result

    # Container With Most Water — O(n)
    def max_area(height):
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            best = max(best, min(height[lo], height[hi]) * (hi - lo))
            if height[lo] < height[hi]:
                lo += 1
            else:
                hi -= 1
        return best

    # Trapping Rain Water — two pointers O(n) time O(1) space
    def trap(height):
        lo, hi = 0, len(height) - 1
        lo_max = hi_max = water = 0
        while lo < hi:
            if height[lo] < height[hi]:
                lo_max = max(lo_max, height[lo])
                water += lo_max - height[lo]
                lo += 1
            else:
                hi_max = max(hi_max, height[hi])
                water += hi_max - height[hi]
                hi -= 1
        return water

COMPLEXITY NOTES:
─────────────────
- Two pointer on sorted array: O(n)
- 3Sum: O(n^2) — can't do better in general
- Container/trapping: O(n) time, O(1) space with two pointers
"""


# ==============================================================================
# 3. SLIDING WINDOW
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Best Time to Buy and     — Single pass, track min price so far, update
    Sell Stock                  max profit. Technically a sliding window of size
                                variable that tracks a running minimum.

[M] Longest Substring Without — Expand right pointer, shrink left when
    Repeating Characters        duplicate found. Use set or dict for char positions.

[M] Longest Repeating         — Sliding window. Track most-frequent char count
    Character Replacement       in window. Shrink when (window_len - max_freq) > k.

[M] Permutation in String     — Fixed-size window of len(s1), compare frequency
                                counts. Slide and update counts incrementally.

[H] Minimum Window Substring  — Variable window. Expand right to satisfy all
                                chars, shrink left to minimize. Use Counter for
                                "need" and "have" tracking.

[H] Sliding Window Maximum    — Max in each window of size k. Use monotonic
                                deque (decreasing). O(n).

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Fixed window: size k, slide by adding right / removing left
- Variable window: expand right, shrink left when condition violated
- Frequency map + "valid" counter for substring matching problems
- Monotonic deque for min/max in window

PYTHON IDIOMS:
──────────────
    from collections import Counter, deque

    # Longest Substring Without Repeating Characters — O(n)
    def length_of_longest_substring(s):
        seen = {}
        left = best = 0
        for right, ch in enumerate(s):
            if ch in seen and seen[ch] >= left:
                left = seen[ch] + 1
            seen[ch] = right
            best = max(best, right - left + 1)
        return best

    # Minimum Window Substring — O(n)
    def min_window(s, t):
        need = Counter(t)
        missing = len(t)            # total chars still needed
        left = start = end = 0
        for right, ch in enumerate(s, 1):       # right is 1-indexed
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            if missing == 0:                     # window is valid
                while need[s[left]] < 0:         # shrink from left
                    need[s[left]] += 1
                    left += 1
                if not end or right - left < end - start:
                    start, end = left, right
                need[s[left]] += 1               # invalidate window
                missing += 1
                left += 1
        return s[start:end]

    # Sliding Window Maximum — monotonic deque O(n)
    def max_sliding_window(nums, k):
        dq = deque()  # stores indices, front = max
        result = []
        for i, n in enumerate(nums):
            while dq and nums[dq[-1]] <= n:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:     # remove out-of-window
                dq.popleft()
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result

COMPLEXITY NOTES:
─────────────────
- All sliding window problems: O(n) time
- Space: O(min(n, alphabet_size)) for character problems
- Monotonic deque: O(n) time, O(k) space
"""


# ==============================================================================
# 4. STACK
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Valid Parentheses         — Push opening, pop on closing, check match.
                                Stack must be empty at end.

[M] Min Stack                 — Stack that supports getMin() in O(1).
                                Store (value, current_min) pairs, or maintain a
                                parallel min stack.

[M] Evaluate Reverse Polish   — Push numbers, pop two on operator, push result.
    Notation

[M] Daily Temperatures        — Next warmer day for each. Monotonic decreasing
                                stack of indices. Pop when current > stack top.

[M] Generate Parentheses      — Generate all valid combos of n pairs.
                                Backtracking with open/close counts, but the
                                "stack" idea is the validity check.

[H] Largest Rectangle in      — Monotonic stack: for each bar, find the nearest
    Histogram                   smaller bar on left and right. Area = height *
                                (right_bound - left_bound - 1).

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Matching brackets/delimiters → stack
- "Next greater/smaller element" → monotonic stack
- Monotonic increasing stack: finds next smaller element
- Monotonic decreasing stack: finds next greater element
- Stack for expression evaluation (postfix, infix with precedence)

PYTHON IDIOMS:
──────────────
    # Valid Parentheses
    def is_valid(s):
        stack = []
        match = {')': '(', ']': '[', '}': '{'}
        for ch in s:
            if ch in match:
                if not stack or stack[-1] != match[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)
        return not stack

    # Daily Temperatures — monotonic stack O(n)
    def daily_temperatures(temps):
        result = [0] * len(temps)
        stack = []  # stack of indices, decreasing temps
        for i, t in enumerate(temps):
            while stack and temps[stack[-1]] < t:
                j = stack.pop()
                result[j] = i - j
            stack.append(i)
        return result

    # Largest Rectangle in Histogram — O(n)
    def largest_rectangle(heights):
        stack = []  # increasing heights (index, height)
        max_area = 0
        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                idx, height = stack.pop()
                max_area = max(max_area, height * (i - idx))
                start = idx
            stack.append((start, h))
        for idx, height in stack:
            max_area = max(max_area, height * (len(heights) - idx))
        return max_area

COMPLEXITY NOTES:
─────────────────
- All monotonic stack problems: O(n) — each element pushed/popped once
- Min Stack: O(1) for all operations, O(n) extra space
"""


# ==============================================================================
# 5. BINARY SEARCH
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Binary Search             — Classic search in sorted array.
                                lo, hi, mid = lo + (hi - lo) // 2.

[M] Search in Rotated Sorted  — Determine which half is sorted, then decide
    Array                       which half to search. Handle duplicates variant.

[M] Find Minimum in Rotated   — Binary search: if nums[mid] > nums[hi], min is
    Sorted Array                in right half, else left half.

[M] Koko Eating Bananas       — Binary search on answer (eating speed).
                                Feasibility check: can she finish in h hours?

[M] Search a 2D Matrix        — Treat as 1D sorted array. Or start from
                                top-right corner: go left if too big, down if
                                too small.

[H] Median of Two Sorted      — Binary search on partition of smaller array.
    Arrays                      Ensure left partitions of both arrays form the
                                correct lower half. O(log(min(m,n))).

[H] Find in Sorted Array      — Binary search for leftmost and rightmost
    (first/last position)       occurrence. Two separate searches with
                                condition tweaks.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Classic: lo <= hi, return exact match
- Bisect left/right: find insertion point or boundary
- Search on answer: binary search over the solution space with feasibility check
- Invariant: always maintain the answer within [lo, hi]
- Template: decide lo = mid + 1 vs hi = mid based on which side could hold answer

PYTHON IDIOMS:
──────────────
    import bisect

    # Classic binary search
    def binary_search(nums, target):
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    # Search on answer: Koko Eating Bananas
    def min_eating_speed(piles, h):
        lo, hi = 1, max(piles)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            hours = sum((p + mid - 1) // mid for p in piles)  # ceil division
            if hours <= h:
                hi = mid       # mid might be the answer, search lower
            else:
                lo = mid + 1   # mid too slow, need faster
        return lo

    # bisect module for insertion point
    # bisect.bisect_left(a, x)  — leftmost position to insert x
    # bisect.bisect_right(a, x) — rightmost position to insert x

    # Median of Two Sorted Arrays — O(log(min(m,n)))
    def find_median_sorted_arrays(nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2
            j = (m + n + 1) // 2 - i
            left1  = nums1[i - 1] if i > 0 else float('-inf')
            right1 = nums1[i]     if i < m else float('inf')
            left2  = nums2[j - 1] if j > 0 else float('-inf')
            right2 = nums2[j]     if j < n else float('inf')
            if left1 <= right2 and left2 <= right1:
                if (m + n) % 2:
                    return max(left1, left2)
                return (max(left1, left2) + min(right1, right2)) / 2
            elif left1 > right2:
                hi = i - 1
            else:
                lo = i + 1

COMPLEXITY NOTES:
─────────────────
- Classic binary search: O(log n) time, O(1) space
- Search on answer: O(n * log(range)) — n for feasibility check, log(range) searches
- Median of two sorted: O(log(min(m,n)))
"""


# ==============================================================================
# 6. LINKED LISTS
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Reverse Linked List       — Iterative: prev/curr pointers. Recursive: reverse
                                rest, then point next node back.

[E] Merge Two Sorted Lists    — Dummy head, compare and advance. Classic merge.

[E] Linked List Cycle         — Floyd's: slow (1 step) + fast (2 steps). If they
                                meet, cycle exists.

[M] Linked List Cycle II      — After detection, reset one pointer to head, both
                                move 1 step. They meet at cycle start.

[M] Remove Nth Node From End  — Two pointers, gap of n. When fast hits end,
                                slow is at the node before the target.

[M] Reorder List              — Find middle (slow/fast), reverse second half,
                                interleave the two halves.

[M] Add Two Numbers           — Numbers stored in reverse. Traverse both,
                                sum digits + carry.

[M] Copy List with Random     — Hash map: old node -> new node. Two passes.
    Pointer                     Or interleave technique for O(1) space.

[H] Merge K Sorted Lists      — Min-heap of (value, index, node). Pop min, push
                                its next. O(n log k).

[H] LRU Cache                 — Hash map + doubly linked list. O(1) get and put.
                                OrderedDict shortcut in Python.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Dummy head node to simplify edge cases (empty list, single node)
- Slow/fast pointers: find middle, detect cycle
- Reverse in place: prev, curr, next pointer dance
- Sentinel nodes for cleaner merge/insert logic

PYTHON IDIOMS:
──────────────
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next

    # Reverse Linked List — iterative O(n)
    def reverse_list(head):
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev = head
            head = nxt
        return prev

    # Detect cycle start — Floyd's algorithm
    def detect_cycle(head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                slow = head
                while slow is not fast:
                    slow = slow.next
                    fast = fast.next
                return slow
        return None

    # LRU Cache — OrderedDict shortcut
    from collections import OrderedDict

    class LRUCache:
        def __init__(self, capacity):
            self.cache = OrderedDict()
            self.cap = capacity

        def get(self, key):
            if key not in self.cache:
                return -1
            self.cache.move_to_end(key)
            return self.cache[key]

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.cap:
                self.cache.popitem(last=False)

    # LRU Cache — manual doubly linked list (what interviewers want to see)
    class DNode:
        def __init__(self, key=0, val=0):
            self.key, self.val = key, val
            self.prev = self.next = None

    class LRUCacheManual:
        def __init__(self, capacity):
            self.cap = capacity
            self.cache = {}
            self.head, self.tail = DNode(), DNode()  # sentinels
            self.head.next = self.tail
            self.tail.prev = self.head

        def _remove(self, node):
            node.prev.next = node.next
            node.next.prev = node.prev

        def _add_to_front(self, node):
            node.next = self.head.next
            node.prev = self.head
            self.head.next.prev = node
            self.head.next = node

        def get(self, key):
            if key not in self.cache:
                return -1
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val

        def put(self, key, value):
            if key in self.cache:
                self._remove(self.cache[key])
            node = DNode(key, value)
            self.cache[key] = node
            self._add_to_front(node)
            if len(self.cache) > self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]

COMPLEXITY NOTES:
─────────────────
- Reverse, merge, cycle detect: O(n) time, O(1) space
- Merge K sorted: O(n log k) where n = total nodes, k = number of lists
- LRU Cache: O(1) for both get and put
"""


# ==============================================================================
# 7. TREES
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Invert Binary Tree        — Swap left/right children recursively.

[E] Maximum Depth             — max(depth(left), depth(right)) + 1. Or BFS
                                counting levels.

[E] Same Tree / Subtree       — Recursive comparison of structure and values.

[M] Level Order Traversal     — BFS with deque. Process level by level using
                                len(queue) to know level boundaries.

[M] Validate BST              — Inorder traversal should be strictly increasing.
                                Or recursive with (low, high) bounds.

[M] Lowest Common Ancestor    — If both targets in left subtree, recurse left.
    (BST and Binary Tree)       If split, current node is LCA.
                                BST version: use value comparisons.

[M] Kth Smallest in BST       — Inorder traversal, return kth element. Or
                                augment tree with subtree sizes.

[M] Binary Tree Right Side    — BFS, take last element of each level. Or DFS
    View                        with depth tracking.

[H] Serialize / Deserialize   — Preorder with "null" markers. Deserialize with
    Binary Tree                 queue/iterator.

[H] Binary Tree Maximum       — At each node, max path = node.val + max(0, left)
    Path Sum                    + max(0, right). Track global max. Return
                                node.val + max(0, max(left, right)) upward.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- DFS: preorder (root-left-right), inorder (left-root-right), postorder
- BFS: level-order with deque
- Recursive structure: base case (None) → combine children results
- BST property: inorder gives sorted order
- Path problems: track "path through node" vs "path ending at node"

PYTHON IDIOMS:
──────────────
    from collections import deque

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    # Level Order Traversal — BFS
    def level_order(root):
        if not root:
            return []
        result, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level)
        return result

    # Validate BST — recursive bounds
    def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
        if not root:
            return True
        if not (lo < root.val < hi):
            return False
        return (is_valid_bst(root.left, lo, root.val) and
                is_valid_bst(root.right, root.val, hi))

    # Serialize / Deserialize — preorder with None markers
    def serialize(root):
        vals = []
        def dfs(node):
            if not node:
                vals.append('#')
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(vals)

    def deserialize(data):
        vals = iter(data.split(','))
        def dfs():
            v = next(vals)
            if v == '#':
                return None
            node = TreeNode(int(v))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()

    # Maximum Path Sum
    def max_path_sum(root):
        best = [float('-inf')]
        def dfs(node):
            if not node:
                return 0
            left = max(0, dfs(node.left))
            right = max(0, dfs(node.right))
            best[0] = max(best[0], node.val + left + right)  # path through node
            return node.val + max(left, right)  # path ending at node (going up)
        dfs(root)
        return best[0]

COMPLEXITY NOTES:
─────────────────
- Most tree problems: O(n) time, O(h) space where h = height
- Balanced tree: h = log n. Worst case (skewed): h = n
- BFS space: O(w) where w = max width (up to n/2 at last level)
"""


# ==============================================================================
# 8. TRIES
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Implement Trie            — insert, search, startsWith. Each node has
                                children dict and is_end flag.

[M] Design Add and Search     — Trie + DFS for wildcard '.' matching.
    Words

[H] Word Search II            — Build trie from word list. DFS on board, walk
                                trie simultaneously. Prune branches when found.

[M] Replace Words             — Trie of roots. For each word, find shortest
                                prefix in trie.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Trie = prefix tree. Each edge is a character.
- O(L) insert/search where L = word length
- Use defaultdict(TrieNode) or dict for children
- Word Search II: trie + board DFS avoids re-searching for each word

PYTHON IDIOMS:
──────────────
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False

    class Trie:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word):
            node = self.root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

        def search(self, word):
            node = self._find(word)
            return node is not None and node.is_end

        def starts_with(self, prefix):
            return self._find(prefix) is not None

        def _find(self, prefix):
            node = self.root
            for ch in prefix:
                if ch not in node.children:
                    return None
                node = node.children[ch]
            return node

    # Word Search II — trie + board DFS
    def find_words(board, words):
        trie = Trie()
        for w in words:
            trie.insert(w)

        rows, cols = len(board), len(board[0])
        result = set()

        def dfs(r, c, node, path):
            ch = board[r][c]
            if ch not in node.children:
                return
            node = node.children[ch]
            path += ch
            if node.is_end:
                result.add(path)
            board[r][c] = '#'  # mark visited
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(nr, nc, node, path)
            board[r][c] = ch   # unmark

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, trie.root, '')
        return list(result)

COMPLEXITY NOTES:
─────────────────
- Trie insert/search: O(L) per operation, L = word length
- Space: O(total characters across all words)
- Word Search II: O(m * n * 4^L) worst case, but trie pruning makes it fast
"""


# ==============================================================================
# 9. HEAP / PRIORITY QUEUE
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Kth Largest Element       — Min-heap of size k. Or quickselect for O(n) avg.

[M] Last Stone Weight          — Max-heap (negate values in Python). Smash two
                                largest repeatedly.

[M] K Closest Points to       — Max-heap of size k by distance, or quickselect.
    Origin

[M] Task Scheduler             — Greedy + heap. Process most-frequent tasks first.
                                Use cooldown queue for waiting tasks.

[H] Merge K Sorted Lists      — Min-heap of (value, list_index, node). Pop min,
                                push next from same list.

[H] Find Median from Data     — Two heaps: max-heap for lower half, min-heap for
    Stream                      upper half. Balance sizes. Median from tops.

[H] IPO (maximize capital)    — Sort by cost. Greedily pick highest-profit
                                affordable project. Two heaps or sort + heap.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Python heapq is a MIN-heap. Negate values for max-heap.
- "Top K" or "Kth" → heap of size k
- "Merge K sorted" → heap of size k (one element per source)
- Two heaps for running median (max-heap left, min-heap right)
- Lazy deletion: mark items as deleted, skip them when popped

PYTHON IDIOMS:
──────────────
    import heapq

    # Kth Largest Element — min-heap of size k, O(n log k)
    def find_kth_largest(nums, k):
        heap = nums[:k]
        heapq.heapify(heap)     # O(k)
        for n in nums[k:]:
            if n > heap[0]:
                heapq.heapreplace(heap, n)  # pop + push in one step
        return heap[0]

    # Also: heapq.nlargest(k, nums) — convenient but O(n log k)
    # Also: heapq.nsmallest(k, nums)

    # Task Scheduler — O(n log 26) = O(n)
    def least_interval(tasks, n):
        counts = list(Counter(tasks).values())
        max_heap = [-c for c in counts]
        heapq.heapify(max_heap)
        time = 0
        cooldown = deque()  # (available_time, neg_count)
        while max_heap or cooldown:
            time += 1
            if max_heap:
                cnt = heapq.heappop(max_heap) + 1  # do one task (cnt is negative)
                if cnt:
                    cooldown.append((time + n, cnt))
            if cooldown and cooldown[0][0] == time:
                heapq.heappush(max_heap, cooldown.popleft()[1])
        return time

    # Find Median from Data Stream — two heaps
    class MedianFinder:
        def __init__(self):
            self.lo = []  # max-heap (negated) — lower half
            self.hi = []  # min-heap — upper half

        def add_num(self, num):
            heapq.heappush(self.lo, -num)
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
            if len(self.hi) > len(self.lo):
                heapq.heappush(self.lo, -heapq.heappop(self.hi))

        def find_median(self):
            if len(self.lo) > len(self.hi):
                return -self.lo[0]
            return (-self.lo[0] + self.hi[0]) / 2

COMPLEXITY NOTES:
─────────────────
- heapify: O(n)
- push/pop: O(log n)
- Kth largest with heap: O(n log k)
- Merge K sorted: O(n log k)
- Median stream: O(log n) per add, O(1) per find
"""


# ==============================================================================
# 10. BACKTRACKING
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Subsets                   — For each element, include or exclude.
                                Backtracking tree has 2^n leaves.

[M] Subsets II (with dups)    — Sort first, skip duplicates at same recursion level.

[M] Combinations (n choose k) — Backtrack, stop when len(path) == k.

[M] Permutations              — Swap or "used" boolean array. n! permutations.

[M] Combination Sum           — Candidates can be reused. Backtrack with
                                remaining target. Start from current index (not 0)
                                to avoid duplicates.

[M] Word Search               — DFS on grid, mark visited cells, backtrack.

[H] N-Queens                  — Place queens row by row. Track columns and both
                                diagonals with sets. O(n!) states to explore.

[H] Sudoku Solver             — Fill empty cells, try 1-9, validate, backtrack.
                                Constraint propagation for optimization.

[M] Palindrome Partitioning   — Try all cut points. If prefix is palindrome,
                                recurse on suffix.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Template: choose → explore → unchoose
- Prune early: skip invalid branches before recursing
- Sort to handle duplicates: skip if nums[i] == nums[i-1] and not used
- For combinations/subsets: use start index to avoid re-picking earlier elements
- For permutations: use "used" set or swap-based approach

PYTHON IDIOMS:
──────────────
    # Subsets — iterative or backtracking
    def subsets(nums):
        result = []
        def backtrack(start, path):
            result.append(path[:])      # snapshot
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()             # unchoose
        backtrack(0, [])
        return result

    # Combination Sum — reuse allowed
    def combination_sum(candidates, target):
        result = []
        def backtrack(start, path, remaining):
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break               # prune (requires sorted candidates)
                path.append(candidates[i])
                backtrack(i, path, remaining - candidates[i])  # i, not i+1
                path.pop()
        candidates.sort()
        backtrack(0, [], target)
        return result

    # N-Queens
    def solve_n_queens(n):
        result = []
        cols = set()
        pos_diag = set()  # (r + c) is constant on / diagonals
        neg_diag = set()  # (r - c) is constant on \\ diagonals

        def backtrack(r, queens):
            if r == n:
                board = []
                for _, c in sorted(queens):
                    board.append('.' * c + 'Q' + '.' * (n - c - 1))
                result.append(board)
                return
            for c in range(n):
                if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                    continue
                cols.add(c)
                pos_diag.add(r + c)
                neg_diag.add(r - c)
                backtrack(r + 1, queens + [(r, c)])
                cols.remove(c)
                pos_diag.remove(r + c)
                neg_diag.remove(r - c)

        backtrack(0, [])
        return result

COMPLEXITY NOTES:
─────────────────
- Subsets: O(2^n) subsets, O(n) per subset → O(n * 2^n)
- Permutations: O(n!)
- Combination Sum: exponential, depends on target/candidates
- N-Queens: O(n!) with pruning
"""


# ==============================================================================
# 11. GRAPHS
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Number of Islands         — DFS/BFS from each '1', mark visited. Count
                                connected components.

[M] Clone Graph               — BFS/DFS with hash map: old node -> clone node.
                                Copy neighbors as you traverse.

[M] Pacific Atlantic Water    — DFS/BFS from ocean borders inward. Intersect
    Flow                        reachable sets from both oceans.

[M] Course Schedule            — Topological sort. Detect cycle in directed graph.
    (I and II)                  Kahn's (BFS with in-degree) or DFS with states.

[M] Rotting Oranges            — Multi-source BFS from all rotten oranges
                                simultaneously. Track time = levels of BFS.

[M] Graph Valid Tree           — n-1 edges + connected (union-find or DFS).

[H] Word Ladder                — BFS shortest path. Nodes = words, edges = 1-char
                                difference. Use wildcard patterns for neighbors.

[H] Alien Dictionary           — Topological sort on character ordering derived
                                from sorted word list.

[H] Cheapest Flights within   — Modified Dijkstra or Bellman-Ford with at most
    K Stops                     k+1 edges.

[H] Network Delay Time        — Dijkstra's from source. Answer = max of all
                                shortest distances.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- BFS: shortest path in unweighted graph, level-order processing
- DFS: cycle detection, connected components, path finding
- Topological sort: DAG ordering. Kahn's (BFS + in-degree) or DFS + post-order
- Union-Find: connected components, cycle detection in undirected graph
- Dijkstra: shortest path with non-negative weights
- Bellman-Ford: shortest path with negative weights, or edge-count constraint

PYTHON IDIOMS:
──────────────
    from collections import deque, defaultdict
    import heapq

    # Number of Islands — BFS
    def num_islands(grid):
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    queue = deque([(r, c)])
                    grid[r][c] = '0'
                    while queue:
                        cr, cc = queue.popleft()
                        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                            nr, nc = cr + dr, cc + dc
                            if (0 <= nr < rows and 0 <= nc < cols
                                    and grid[nr][nc] == '1'):
                                grid[nr][nc] = '0'
                                queue.append((nr, nc))
        return count

    # Topological Sort — Kahn's Algorithm (BFS)
    def course_schedule(num_courses, prerequisites):
        graph = defaultdict(list)
        in_degree = [0] * num_courses
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return order if len(order) == num_courses else []

    # Dijkstra's Algorithm — O((V + E) log V)
    def network_delay_time(times, n, k):
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        dist = {}
        heap = [(0, k)]
        while heap:
            d, u = heapq.heappop(heap)
            if u in dist:
                continue
            dist[u] = d
            for v, w in graph[u]:
                if v not in dist:
                    heapq.heappush(heap, (d + w, v))
        return max(dist.values()) if len(dist) == n else -1

    # Union-Find with path compression and union by rank
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
            if px == py:
                return False
            if self.rank[px] < self.rank[py]:
                px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
            self.components -= 1
            return True

COMPLEXITY NOTES:
─────────────────
- BFS/DFS: O(V + E)
- Dijkstra with binary heap: O((V + E) log V)
- Bellman-Ford: O(V * E)
- Topological sort: O(V + E)
- Union-Find: near O(1) amortized per operation (inverse Ackermann)
"""


# ==============================================================================
# 12. DYNAMIC PROGRAMMING
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Climbing Stairs           — dp[i] = dp[i-1] + dp[i-2]. Fibonacci variant.
                                O(1) space with two variables.

[E] Min Cost Climbing Stairs  — dp[i] = cost[i] + min(dp[i-1], dp[i-2]).

[M] House Robber              — dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
                                Can't rob adjacent houses.

[M] House Robber II (circular) — Run House Robber on nums[1:] and nums[:-1],
                                take the max.

[M] Coin Change               — dp[amount] = min coins. dp[a] = min(dp[a],
                                dp[a - coin] + 1) for each coin. BFS also works.

[M] Longest Increasing        — O(n^2): dp[i] = max(dp[j] + 1) for j < i where
    Subsequence                 nums[j] < nums[i].
                                O(n log n): patience sorting with bisect.

[M] Word Break                — dp[i] = True if s[:i] can be segmented.
                                dp[i] = any(dp[j] and s[j:i] in wordSet).

[M] Unique Paths              — dp[r][c] = dp[r-1][c] + dp[r][c-1]. Grid DP.

[M] Longest Common            — 2D DP: if s1[i]==s2[j], dp[i][j] = dp[i-1][j-1]+1
    Subsequence                 else max(dp[i-1][j], dp[i][j-1]).

[H] 0/1 Knapsack              — dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] +
                                val[i]). Space optimize to 1D (iterate w
                                backwards).

[H] Edit Distance             — dp[i][j] = min(insert, delete, replace).
                                Classic 2D DP.

[H] Longest Valid             — Stack-based or DP. dp[i] = length of longest
    Parentheses                 valid ending at i.

[H] Regular Expression        — dp[i][j] = does s[:i] match p[:j].
    Matching                    Handle '.' and '*' cases.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Identify subproblem: what state do I need? (index, remaining capacity, etc.)
- Top-down (memoization) vs bottom-up (tabulation)
- State reduction: often only need previous row/column → O(n) space
- Common patterns:
  * Linear DP: dp[i] depends on dp[i-1], dp[i-2], etc.
  * Grid DP: dp[r][c] depends on neighbors
  * Interval DP: dp[i][j] for subarray/substring [i..j]
  * Knapsack: dp[i][w] with items and capacity
  * String matching: dp[i][j] for prefixes of two strings

PYTHON IDIOMS:
──────────────
    from functools import lru_cache

    # Coin Change — bottom-up O(amount * len(coins))
    def coin_change(coins, amount):
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1

    # LIS — O(n log n) with patience sorting
    def length_of_lis(nums):
        tails = []  # tails[i] = smallest tail of increasing subseq of length i+1
        for n in nums:
            pos = bisect.bisect_left(tails, n)
            if pos == len(tails):
                tails.append(n)
            else:
                tails[pos] = n
        return len(tails)

    # LCS — top-down with memoization
    def longest_common_subsequence(text1, text2):
        @lru_cache(maxsize=None)
        def dp(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            if text1[i] == text2[j]:
                return 1 + dp(i + 1, j + 1)
            return max(dp(i + 1, j), dp(i, j + 1))
        return dp(0, 0)

    # 0/1 Knapsack — 1D space optimization
    def knapsack(weights, values, capacity):
        dp = [0] * (capacity + 1)
        for w, v in zip(weights, values):
            for c in range(capacity, w - 1, -1):  # backwards to avoid reuse
                dp[c] = max(dp[c], dp[c - w] + v)
        return dp[capacity]

    # Edit Distance — O(m * n)
    def min_distance(word1, word2):
        m, n = len(word1), len(word2)
        dp = list(range(n + 1))
        for i in range(1, m + 1):
            prev = dp[0]
            dp[0] = i
            for j in range(1, n + 1):
                temp = dp[j]
                if word1[i-1] == word2[j-1]:
                    dp[j] = prev
                else:
                    dp[j] = 1 + min(prev, dp[j], dp[j-1])
                prev = temp
        return dp[n]

COMPLEXITY NOTES:
─────────────────
- Most 1D DP: O(n) or O(n^2)
- Most 2D DP (strings, grid): O(m * n)
- Knapsack: O(n * W) — pseudo-polynomial
- LIS with binary search: O(n log n)
- Space optimization: often reducible from O(m*n) to O(min(m,n))
"""


# ==============================================================================
# 13. GREEDY
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Jump Game                 — Track farthest reachable index. If current index
                                > farthest, return False.

[M] Jump Game II              — BFS-style greedy. Track current end and farthest.
                                Increment jumps when reaching current end.

[M] Merge Intervals           — Sort by start. Merge overlapping intervals.

[M] Non-overlapping Intervals — Sort by end time. Greedily keep earliest-ending
    (interval scheduling)       non-overlapping intervals. Count removed ones.

[M] Gas Station               — If total gas >= total cost, solution exists.
                                Track running surplus, reset start when it goes
                                negative.

[M] Hand of Straights         — Sort, greedily form groups of W consecutive.
                                Use Counter, decrement as you form groups.

[H] Partition Labels           — Last occurrence of each char. Extend partition
                                end to max last occurrence seen so far.

[M] Valid Parenthesis String  — Track range of possible open-paren counts
    (with *)                    (lo, hi). '*' can be '(', ')', or ''.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Greedy works when local optimal choice leads to global optimal
- Sorting is often the first step (by start, end, deadline, ratio)
- Interval problems: sort by start or end depending on the goal
- Exchange argument: prove greedy is optimal by showing any swap doesn't improve
- Activity selection: sort by finish time, greedily pick non-overlapping

PYTHON IDIOMS:
──────────────
    # Merge Intervals — O(n log n)
    def merge_intervals(intervals):
        intervals.sort()
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged

    # Jump Game II — greedy BFS O(n)
    def jump(nums):
        jumps = cur_end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == cur_end:
                jumps += 1
                cur_end = farthest
        return jumps

    # Non-overlapping Intervals (min removals) — O(n log n)
    def erase_overlap_intervals(intervals):
        intervals.sort(key=lambda x: x[1])  # sort by END time
        end = float('-inf')
        removals = 0
        for s, e in intervals:
            if s >= end:
                end = e        # keep this interval
            else:
                removals += 1  # remove (overlaps with previous kept)
        return removals

COMPLEXITY NOTES:
─────────────────
- Most greedy: O(n log n) due to sorting, O(n) for the greedy pass
- Jump Game: O(n) — no sorting needed
"""


# ==============================================================================
# 14. BIT MANIPULATION
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[E] Single Number             — XOR all elements. Duplicates cancel: a ^ a = 0.

[E] Number of 1 Bits          — n & (n-1) clears lowest set bit. Count iterations.
                                Or bin(n).count('1') in Python.

[E] Counting Bits             — dp[i] = dp[i >> 1] + (i & 1). Build array 0..n.

[M] Reverse Bits              — Shift and OR, 32 iterations.

[M] Missing Number            — XOR all indices and values. Or sum formula:
                                n*(n+1)/2 - sum(nums).

[M] Sum of Two Integers       — Add without +: a ^ b for sum without carry,
    (no + operator)             (a & b) << 1 for carry. Repeat until no carry.
                                (Tricky in Python due to arbitrary precision.)

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- XOR properties: a ^ 0 = a, a ^ a = 0, commutative, associative
- n & (n-1): clears lowest set bit
- n & (-n): isolates lowest set bit
- Check bit i: n & (1 << i)
- Set bit i: n | (1 << i)
- Clear bit i: n & ~(1 << i)

PYTHON IDIOMS:
──────────────
    # Single Number — O(n) time O(1) space
    def single_number(nums):
        result = 0
        for n in nums:
            result ^= n
        return result

    # Counting Bits — O(n)
    def counting_bits(n):
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # Number of 1 bits — Brian Kernighan's algorithm
    def hamming_weight(n):
        count = 0
        while n:
            n &= n - 1  # clear lowest set bit
            count += 1
        return count

COMPLEXITY NOTES:
─────────────────
- XOR scan: O(n) time, O(1) space
- Bit counting: O(number of set bits), at most O(log n)
"""


# ==============================================================================
# 15. MATH & GEOMETRY
# ==============================================================================
"""
MUST-KNOW PROBLEMS:
───────────────────
[M] Rotate Image              — Transpose matrix, then reverse each row.
                                90-degree clockwise rotation in-place.

[M] Spiral Matrix              — Simulate spiral traversal with four boundaries
                                (top, bottom, left, right). Shrink after each
                                direction.

[M] Set Matrix Zeroes          — Use first row/col as markers. Two passes:
                                mark, then zero. Handle first row/col separately.

[M] Pow(x, n)                 — Fast exponentiation. x^n = (x^(n/2))^2.
                                Handle negative n. O(log n).

[E] Happy Number              — Sum of squares of digits repeatedly. Detect
                                cycle with slow/fast pointers or set.

[E] Plus One                  — Handle carry from least significant digit.

[M] Multiply Strings          — Grade-school multiplication digit by digit.
                                Result array of length m + n.

KEY PATTERNS & TECHNIQUES:
──────────────────────────
- Matrix rotation: transpose + reverse (clockwise), or reverse + transpose (CCW)
- Spiral: boundary tracking with four pointers
- Fast power: repeated squaring O(log n)
- Cycle detection in mathematical sequences: Floyd's or set

PYTHON IDIOMS:
──────────────
    # Rotate Image 90 CW — in place
    def rotate(matrix):
        n = len(matrix)
        # Transpose
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Reverse rows
        for row in matrix:
            row.reverse()

    # Spiral Matrix
    def spiral_order(matrix):
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):        # right
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):        # down
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):  # left
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):  # up
                    result.append(matrix[r][left])
                left += 1
        return result

    # Fast Power — O(log n)
    def my_pow(x, n):
        if n < 0:
            x, n = 1/x, -n
        result = 1
        while n:
            if n & 1:
                result *= x
            x *= x
            n >>= 1
        return result

COMPLEXITY NOTES:
─────────────────
- Rotate/spiral: O(m * n)
- Fast power: O(log n)
- Set matrix zeroes: O(m * n) time, O(1) extra space with in-place markers
"""


# ==============================================================================
# 16. SYSTEM DESIGN ALGORITHMS
# ==============================================================================
"""
These appear in system design rounds but you should know the algorithmic details.

MUST-KNOW TOPICS:
─────────────────

[M] CONSISTENT HASHING
    - Problem: Distribute keys across N servers, minimize remapping on add/remove.
    - Approach: Hash both keys and servers onto a ring [0, 2^32). Key maps to
      next server clockwise. Virtual nodes for balance.
    - Remapping: Only K/N keys move on server change (vs K total with mod hashing).
    - Libraries: hashring, uhashring (Python)

[M] RATE LIMITING ALGORITHMS
    - Token Bucket: Bucket holds tokens, refilled at rate r. Each request
      consumes a token. Allows bursts up to bucket capacity.
    - Sliding Window Log: Store timestamps of requests. Count those within
      the window. Precise but memory-heavy.
    - Sliding Window Counter: Approximate. Weighted count from current and
      previous window. Memory-efficient.
    - Fixed Window: Count requests per time window. Edge case: burst at
      window boundary allows 2x rate.
    - Leaky Bucket: Requests enter a FIFO queue processed at fixed rate.
      Smooths bursts but adds latency.

[H] LRU CACHE
    - HashMap + Doubly Linked List (see Linked Lists section above).
    - get/put both O(1). Move accessed item to front. Evict from tail.

[H] LFU CACHE
    - HashMap + frequency buckets (each bucket is a doubly linked list).
    - Track min frequency. On access, move item to freq+1 bucket.
    - On eviction, remove LRU item from min-frequency bucket.

[M] BLOOM FILTER
    - Probabilistic set membership. k hash functions, m-bit array.
    - Insert: set bits at h1(x), h2(x), ..., hk(x).
    - Query: check all k bits. False positives possible, no false negatives.
    - Optimal k = (m/n) * ln(2). False positive rate ~ (1 - e^(-kn/m))^k.

[M] SKIP LIST
    - Probabilistic alternative to balanced BSTs. Multiple levels of linked lists.
    - O(log n) search, insert, delete on average.
    - Used in Redis sorted sets.

[H] MERKLE TREE
    - Binary tree of hashes. Leaf = hash(data block). Internal = hash(left + right).
    - Efficiently verify data integrity. Used in Git, blockchain, anti-entropy.
    - O(log n) to verify a single block.

[M] LOAD BALANCING ALGORITHMS
    - Round Robin: Cycle through servers. Simple, no state.
    - Weighted Round Robin: Servers have weights proportional to capacity.
    - Least Connections: Route to server with fewest active connections.
    - Consistent Hashing: See above. Good for caches.
    - IP Hash: Hash client IP to server. Ensures session stickiness.
    - Random: Simple but surprisingly effective at scale.

PYTHON IDIOMS:
──────────────
    # Token Bucket Rate Limiter
    import time

    class TokenBucket:
        def __init__(self, rate, capacity):
            self.rate = rate            # tokens per second
            self.capacity = capacity
            self.tokens = capacity
            self.last_refill = time.monotonic()

        def allow(self):
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    # Sliding Window Counter Rate Limiter
    class SlidingWindowCounter:
        def __init__(self, limit, window_secs):
            self.limit = limit
            self.window = window_secs
            self.prev_count = 0
            self.curr_count = 0
            self.curr_start = time.monotonic()

        def allow(self):
            now = time.monotonic()
            elapsed = now - self.curr_start
            if elapsed >= self.window:
                self.prev_count = self.curr_count
                self.curr_count = 0
                self.curr_start = now
                elapsed = 0
            weight = 1 - (elapsed / self.window)
            estimate = self.prev_count * weight + self.curr_count
            if estimate < self.limit:
                self.curr_count += 1
                return True
            return False

    # Bloom Filter
    import hashlib

    class BloomFilter:
        def __init__(self, size, num_hashes):
            self.size = size
            self.num_hashes = num_hashes
            self.bits = [False] * size

        def _hashes(self, item):
            for i in range(self.num_hashes):
                h = int(hashlib.sha256(
                    f"{item}{i}".encode()).hexdigest(), 16)
                yield h % self.size

        def add(self, item):
            for h in self._hashes(item):
                self.bits[h] = True

        def might_contain(self, item):
            return all(self.bits[h] for h in self._hashes(item))

    # LFU Cache
    from collections import defaultdict, OrderedDict

    class LFUCache:
        def __init__(self, capacity):
            self.cap = capacity
            self.key_val = {}
            self.key_freq = {}
            self.freq_keys = defaultdict(OrderedDict)
            self.min_freq = 0

        def get(self, key):
            if key not in self.key_val:
                return -1
            self._increment_freq(key)
            return self.key_val[key]

        def put(self, key, value):
            if self.cap <= 0:
                return
            if key in self.key_val:
                self.key_val[key] = value
                self._increment_freq(key)
                return
            if len(self.key_val) >= self.cap:
                # Evict LRU item from min-frequency bucket
                evict_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
                del self.key_val[evict_key]
                del self.key_freq[evict_key]
            self.key_val[key] = value
            self.key_freq[key] = 1
            self.freq_keys[1][key] = None
            self.min_freq = 1

        def _increment_freq(self, key):
            freq = self.key_freq[key]
            del self.freq_keys[freq][key]
            if not self.freq_keys[freq] and self.min_freq == freq:
                self.min_freq += 1
            self.key_freq[key] = freq + 1
            self.freq_keys[freq + 1][key] = None
"""


# ==============================================================================
# 17. BACKEND-SPECIFIC: DATABASE QUERY OPTIMIZATION
# ==============================================================================
"""
ALGORITHMS AND CONCEPTS:
────────────────────────

[M] B-TREE / B+-TREE INDEX
    - B+-tree: all values in leaves, internal nodes are routing keys.
    - O(log_B n) lookups where B = branching factor (typically 100-500).
    - Clustered index: data rows stored in index order (one per table).
    - Non-clustered: separate structure pointing to data rows.
    - Covering index: index contains all columns needed by query → no table lookup.

[M] HASH INDEX
    - O(1) exact-match lookup. No range queries.
    - Used for in-memory hash joins, hash partitioning.

[M] QUERY EXECUTION PLANS
    - Nested Loop Join: O(m * n). Good for small inner table or indexed inner.
    - Hash Join: O(m + n). Build hash table on smaller relation, probe with larger.
    - Sort-Merge Join: O(m log m + n log n). Good when both inputs sorted.
    - Index Scan vs Table Scan: optimizer chooses based on selectivity.
    - Key concept: selectivity. High selectivity (few rows) → use index.
      Low selectivity (many rows) → full scan is faster.

[M] QUERY OPTIMIZATION TECHNIQUES
    - Push predicates down (filter early).
    - Use covering indexes to avoid table lookups.
    - Avoid SELECT *. Specify needed columns.
    - EXPLAIN / EXPLAIN ANALYZE to read query plans.
    - Denormalization for read-heavy workloads.
    - Materialized views for expensive aggregations.
    - Partition pruning: time-based or hash partitioning.

[H] TRANSACTION ISOLATION & CONCURRENCY
    - MVCC (Multi-Version Concurrency Control): readers don't block writers.
      Each transaction sees a snapshot.
    - Two-Phase Locking (2PL): acquire locks in growing phase, release in
      shrinking phase. Guarantees serializability.
    - Optimistic Concurrency: proceed without locks, validate at commit.
      Good for low-contention workloads.
    - Isolation levels: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ,
      SERIALIZABLE. Trade consistency for concurrency.

PYTHON IDIOMS (SQLAlchemy / raw SQL):
─────────────────────────────────────
    # Efficient bulk operations
    # BAD: N+1 query problem
    for user in session.query(User).all():
        print(user.orders)  # each triggers a separate query

    # GOOD: eager loading
    users = session.query(User).options(joinedload(User.orders)).all()

    # GOOD: subquery load
    users = session.query(User).options(subqueryload(User.orders)).all()

    # Index hints in raw SQL
    # CREATE INDEX idx_flights_origin_time ON flights(origin, departure_time);
    # SELECT * FROM flights WHERE origin = 'BOS' AND departure_time > '2026-03-17'
    # ORDER BY departure_time LIMIT 100;

    # Pagination: keyset pagination (cursor-based) > OFFSET
    # BAD:  SELECT * FROM flights ORDER BY id LIMIT 20 OFFSET 10000;
    # GOOD: SELECT * FROM flights WHERE id > :last_seen_id ORDER BY id LIMIT 20;
"""


# ==============================================================================
# 18. BACKEND-SPECIFIC: CACHING employerATEGIES
# ==============================================================================
"""
ALGORITHMS AND CONCEPTS:
────────────────────────

[M] CACHE EVICTION POLICIES
    - LRU (Least Recently Used): Evict the item not accessed for longest.
      Implemented with OrderedDict or hash map + doubly linked list.
    - LFU (Least Frequently Used): Evict the least-accessed item. Track
      frequency buckets. See Section 16 for implementation.
    - TTL (Time To Live): Items expire after a fixed duration. Background
      cleanup or lazy expiration (check on access).
    - FIFO: First in, first out. Simple but doesn't consider access patterns.
    - ARC (Adaptive Replacement Cache): Balances recency and frequency
      dynamically. Used in ZFS.

[M] CACHE PATTERNS
    - Cache-Aside (Lazy Loading): App checks cache first. On miss, fetch
      from DB, populate cache. Most common pattern.
    - Write-Through: Write to cache and DB simultaneously. Strong consistency
      but higher write latency.
    - Write-Behind (Write-Back): Write to cache, asynchronously flush to DB.
      Better write performance but risk of data loss.
    - Read-Through: Cache itself fetches from DB on miss. Cleaner app code.
    - Cache Stampede Prevention: Locking (only one thread fetches), probabilistic
      early expiration, stale-while-revalidate.

[H] DISTRIBUTED CACHING
    - Consistent hashing for key distribution across cache nodes.
    - Replication for availability. Read replicas.
    - Cache invalidation: hardest problem in CS.
      - Event-driven: publish invalidation events (Kafka, Redis pub/sub).
      - TTL-based: accept slight staleness.
      - Version-based: cache key includes version number.

PYTHON IDIOMS:
──────────────
    from functools import lru_cache
    import time

    # Python's built-in LRU cache
    @lru_cache(maxsize=1024)
    def expensive_computation(key):
        return compute(key)

    # TTL cache decorator
    def ttl_cache(ttl_seconds, maxsize=128):
        def decorator(func):
            cache = {}
            def wrapper(*args):
                now = time.monotonic()
                if args in cache:
                    result, timestamp = cache[args]
                    if now - timestamp < ttl_seconds:
                        return result
                result = func(*args)
                cache[args] = (result, now)
                # Evict expired entries periodically
                if len(cache) > maxsize * 2:
                    expired = [k for k, (_, ts) in cache.items()
                               if now - ts >= ttl_seconds]
                    for k in expired:
                        del cache[k]
                return result
            return wrapper
        return decorator

    # Redis-based caching pattern (pseudocode)
    import redis
    import json

    r = redis.Redis()

    def get_flight(flight_id):
        # Cache-aside pattern
        cache_key = f"flight:{flight_id}"
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
        flight = db.query(Flight).get(flight_id)  # DB fetch
        r.setex(cache_key, 300, json.dumps(flight.to_dict()))  # TTL 5 min
        return flight.to_dict()
"""


# ==============================================================================
# 19. BACKEND-SPECIFIC: LOAD BALANCING ALGORITHMS
# ==============================================================================
"""
ALGORITHMS:
───────────

[E] ROUND ROBIN
    - Cycle through servers 0, 1, 2, ..., N-1, 0, 1, ...
    - Simple. No awareness of server load or capacity.
    - Implementation: counter % N.

[M] WEIGHTED ROUND ROBIN
    - Servers assigned weights. Higher weight = more requests.
    - Server with weight 3 gets 3x requests vs weight 1.
    - Smooth Weighted Round Robin (Nginx): avoids bursty distribution.

[M] LEAST CONNECTIONS
    - Route to server with fewest active connections.
    - Better for variable request processing times.
    - Requires tracking active connection count per server.

[M] CONSISTENT HASHING (covered in Section 16)

[M] POWER OF TWO CHOICES
    - Pick two servers at random, route to the one with fewer connections.
    - Simple yet surprisingly effective (exponential improvement over random).
    - Used in modern load balancers.

[H] WEIGHTED LEAST CONNECTIONS
    - Combines weights and connection counts.
    - Score = active_connections / weight. Pick lowest score.

PYTHON IDIOMS:
──────────────
    import random
    import itertools

    class RoundRobinLB:
        def __init__(self, servers):
            self.servers = servers
            self.cycle = itertools.cycle(servers)

        def next_server(self):
            return next(self.cycle)

    class WeightedRoundRobinLB:
        \"\"\"Smooth Weighted Round Robin (Nginx algorithm)\"\"\"
        def __init__(self, servers_weights):
            # servers_weights: [(server, weight), ...]
            self.servers = [s for s, _ in servers_weights]
            self.weights = [w for _, w in servers_weights]
            self.current_weights = [0] * len(self.servers)
            self.total_weight = sum(self.weights)

        def next_server(self):
            # Increment all by their weight
            for i in range(len(self.servers)):
                self.current_weights[i] += self.weights[i]
            # Pick highest current weight
            idx = self.current_weights.index(max(self.current_weights))
            # Decrease selected by total weight
            self.current_weights[idx] -= self.total_weight
            return self.servers[idx]

    class LeastConnectionsLB:
        def __init__(self, servers):
            self.connections = {s: 0 for s in servers}

        def next_server(self):
            server = min(self.connections, key=self.connections.get)
            self.connections[server] += 1
            return server

        def release(self, server):
            self.connections[server] -= 1

    class PowerOfTwoChoicesLB:
        def __init__(self, servers):
            self.connections = {s: 0 for s in servers}
            self.servers = servers

        def next_server(self):
            a, b = random.sample(self.servers, 2)
            server = a if self.connections[a] <= self.connections[b] else b
            self.connections[server] += 1
            return server

        def release(self, server):
            self.connections[server] -= 1
"""


# ==============================================================================
# 20. BACKEND-SPECIFIC: ROUTING & PATHFINDING (Aviation Domain)
# ==============================================================================
"""
ALGORITHMS:
───────────

[M] DIJKSTRA'S ALGORITHM
    - Shortest path from single source with non-negative weights.
    - O((V + E) log V) with binary heap.
    - Aviation use: cheapest route between airports considering cost/time.
    - See Section 11 (Graphs) for implementation.

[H] A* SEARCH
    - Dijkstra + heuristic. f(n) = g(n) + h(n).
    - g(n) = actual cost from start. h(n) = estimated cost to goal.
    - Heuristic must be admissible (never overestimate) for optimality.
    - Aviation use: route planning with great-circle distance heuristic.

[M] BELLMAN-FORD
    - Handles negative edge weights. O(V * E).
    - Can detect negative cycles.
    - Aviation use: rare, but useful if route costs can be negative (subsidies).

[H] FLOYD-WARSHALL
    - All-pairs shortest paths. O(V^3). Works with negative weights (no neg cycles).
    - Aviation use: precompute all airport-to-airport shortest paths.

[M] MINIMUM SPANNING TREE (Kruskal / Prim)
    - Kruskal: sort edges, union-find to avoid cycles. O(E log E).
    - Prim: grow tree from start vertex using min-heap. O(E log V).
    - Aviation use: minimum-cost network connecting all airports.

[H] NETWORK FLOW (Ford-Fulkerson / Edmonds-Karp)
    - Maximum flow through a network. Edmonds-Karp: BFS for augmenting paths,
      O(V * E^2).
    - Aviation use: maximum throughput through airspace sectors, gate assignment.

PYTHON IDIOMS:
──────────────
    import heapq
    from math import radians, sin, cos, asin, sqrt

    # A* Search
    def a_star(graph, start, goal, heuristic):
        open_set = [(heuristic(start, goal), 0, start)]  # (f, g, node)
        g_score = {start: 0}
        came_from = {}

        while open_set:
            f, g, current = heapq.heappop(open_set)
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1], g

            if g > g_score.get(current, float('inf')):
                continue

            for neighbor, weight in graph[current]:
                tentative_g = g + weight
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    came_from[neighbor] = current
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))

        return None, float('inf')  # no path

    # Great-circle distance heuristic (Haversine formula)
    def haversine(coord1, coord2):
        \"\"\"Distance in km between two (lat, lon) points.\"\"\"
        lat1, lon1 = map(radians, coord1)
        lat2, lon2 = map(radians, coord2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        return 2 * 6371 * asin(sqrt(a))  # Earth radius in km

    # Kruskal's MST — O(E log E)
    def kruskal(n, edges):
        \"\"\"edges = [(weight, u, v), ...]\"\"\"
        edges.sort()
        uf = UnionFind(n)  # from Section 11
        mst = []
        total = 0
        for w, u, v in edges:
            if uf.find(u) != uf.find(v):
                uf.union(u, v)
                mst.append((u, v, w))
                total += w
        return mst, total

    # Bellman-Ford — O(V * E)
    def bellman_ford(n, edges, src):
        dist = [float('inf')] * n
        dist[src] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        # Detect negative cycle
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                raise ValueError("Negative cycle detected")
        return dist
"""


# ==============================================================================
# 21. BACKEND-SPECIFIC: OPTIMIZATION ALGORITHMS
# ==============================================================================
"""
ALGORITHMS:
───────────

[H] LINEAR PROGRAMMING
    - Optimize linear objective subject to linear constraints.
    - Simplex method: traverse vertices of feasible polytope.
    - Aviation use: crew scheduling, fuel optimization, gate assignment.
    - Python: scipy.optimize.linprog, PuLP, OR-Tools.

[H] CONemployerAINT SATISFACTION (CSP)
    - Variables with domains, subject to constraints.
    - Backtracking + constraint propagation.
    - Arc consistency (AC-3): prune domains early.
    - Aviation use: scheduling (crew, gates, runways), conflict resolution.

[M] GREEDY SCHEDULING
    - Job scheduling with deadlines, priorities, durations.
    - Earliest Deadline First (EDF): schedule by deadline.
    - Shortest Job First (SJF): minimize average wait time.
    - Priority scheduling with preemption.
    - Aviation use: runway scheduling, departure sequencing.

[H] GENETIC ALGORITHMS / SIMULATED ANNEALING
    - Metaheuristics for NP-hard optimization.
    - GA: population + selection + crossover + mutation.
    - SA: random perturbations, accept worse solutions with decreasing probability.
    - Aviation use: airspace sectorization, long-term scheduling.

PYTHON IDIOMS:
──────────────
    # Linear Programming with scipy
    from scipy.optimize import linprog

    # Minimize c^T * x subject to A_ub * x <= b_ub
    # Example: minimize fuel cost for route allocation
    def optimize_routes():
        c = [10, 15, 20]       # cost per route
        A_ub = [[-1, 0, 0],    # constraints
                [0, -1, 0],
                [1, 1, 1]]
        b_ub = [-1, -1, 10]    # min 1 flight per route, max 10 total
        bounds = [(0, None)] * 3
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        return result.x

    # Constraint Satisfaction — backtracking with AC-3
    def solve_csp(variables, domains, constraints):
        assignment = {}

        def is_consistent(var, val, assignment):
            for constraint in constraints:
                if not constraint(var, val, assignment):
                    return False
            return True

        def backtrack(assignment):
            if len(assignment) == len(variables):
                return assignment.copy()
            var = select_unassigned(variables, assignment, domains)
            for val in order_domain_values(var, domains):
                if is_consistent(var, val, assignment):
                    assignment[var] = val
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    del assignment[var]
            return None

        return backtrack(assignment)

    # Job Scheduling — Earliest Deadline First
    def schedule_jobs(jobs):
        \"\"\"jobs = [(deadline, duration, profit), ...]\"\"\"
        # Sort by deadline
        jobs.sort()
        schedule = []
        current_time = 0
        for deadline, duration, profit in jobs:
            if current_time + duration <= deadline:
                schedule.append((current_time, duration, profit))
                current_time += duration
        return schedule
"""


# ==============================================================================
# 22. BACKEND-SPECIFIC: GEOSPATIAL ALGORITHMS (Aviation Domain)
# ==============================================================================
"""
ALGORITHMS:
───────────

[M] HAVERSINE / GREAT-CIRCLE DISTANCE
    - Distance between two (lat, lon) points on a sphere.
    - See Section 20 for implementation.
    - Aviation use: distance between airports, fuel estimation.

[M] GEOHASHING
    - Encode (lat, lon) into a string. Nearby points share prefixes.
    - Enables proximity queries with prefix matching.
    - Resolution: longer hash = more precision.
    - Aviation use: sector lookup, nearby airport search.

[H] R-TREE / K-D TREE (Spatial Indexing)
    - R-tree: bounding rectangles, B-tree-like for spatial data.
      Good for range queries ("all flights in this sector").
    - K-D tree: binary space partitioning. Alternates split dimension.
      O(log n) nearest neighbor. Build O(n log n).
    - Aviation use: airspace sector lookup, conflict detection.

[M] POINT-IN-POLYGON
    - Ray casting: count intersections of ray from point to infinity.
      Odd = inside, even = outside.
    - Aviation use: is aircraft in restricted airspace? Sector containment.

[H] CONVEX HULL
    - Graham scan O(n log n) or Andrew's monotone chain.
    - Aviation use: bounding regions, airspace boundaries.

[M] QUADTREE
    - Recursively divide 2D space into 4 quadrants.
    - Good for variable-density spatial data.
    - Aviation use: radar coverage, flight density mapping.

PYTHON IDIOMS:
──────────────
    from scipy.spatial import KDTree, ConvexHull
    import numpy as np

    # K-D Tree for nearest airport lookup
    def build_airport_index(airports):
        \"\"\"airports = [(lat, lon, code), ...]\"\"\"
        coords = np.array([(a[0], a[1]) for a in airports])
        tree = KDTree(coords)
        return tree, airports

    def find_nearest_airports(tree, airports, lat, lon, k=5):
        distances, indices = tree.query([lat, lon], k=k)
        return [(airports[i][2], distances[j])
                for j, i in enumerate(indices)]

    # Geohash encoding
    def geohash_encode(lat, lon, precision=8):
        \"\"\"Encode lat/lon to geohash string.\"\"\"
        base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
        lat_range = [-90.0, 90.0]
        lon_range = [-180.0, 180.0]
        bits = 0
        hash_str = []
        is_lon = True

        while len(hash_str) < precision:
            if is_lon:
                mid = (lon_range[0] + lon_range[1]) / 2
                if lon >= mid:
                    bits = bits * 2 + 1
                    lon_range[0] = mid
                else:
                    bits = bits * 2
                    lon_range[1] = mid
            else:
                mid = (lat_range[0] + lat_range[1]) / 2
                if lat >= mid:
                    bits = bits * 2 + 1
                    lat_range[0] = mid
                else:
                    bits = bits * 2
                    lat_range[1] = mid
            is_lon = not is_lon

            if len(bin(bits)) - 2 == 5:  # 5 bits accumulated
                hash_str.append(base32[bits])
                bits = 0

        return ''.join(hash_str)

    # Point-in-Polygon — ray casting
    def point_in_polygon(point, polygon):
        \"\"\"point = (x, y), polygon = [(x1,y1), (x2,y2), ...]\"\"\"
        x, y = point
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y) and
                    x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    # Sector-based flight lookup (aviation)
    # Given sectors as polygons and flights as (lat, lon) points:
    def assign_flights_to_sectors(flights, sectors):
        \"\"\"
        flights = [(flight_id, lat, lon), ...]
        sectors = [(sector_id, [(lat, lon), ...]), ...]  # polygon vertices
        \"\"\"
        assignments = {}
        for fid, flat, flon in flights:
            for sid, polygon in sectors:
                if point_in_polygon((flon, flat), polygon):
                    assignments[fid] = sid
                    break
        return assignments
"""


# ==============================================================================
# QUICK REFERENCE: COMPLEXITY CHEAT SHEET
# ==============================================================================
"""
DATA STRUCTURE OPERATIONS:
──────────────────────────
Structure          | Access | Search | Insert | Delete | Notes
─────────────────────────────────────────────────────────────
Array              | O(1)   | O(n)   | O(n)   | O(n)   | O(1) append amortized
Hash Table         | -      | O(1)*  | O(1)*  | O(1)*  | *average case
Binary Search Tree | O(h)   | O(h)   | O(h)   | O(h)   | h=log n balanced
Heap               | O(1)†  | O(n)   | O(logn) | O(logn) | †peek only
Trie               | -      | O(L)   | O(L)   | O(L)   | L = key length
Skip List          | O(logn)| O(logn)| O(logn)| O(logn)| probabilistic

SORTING ALGORITHMS:
───────────────────
Algorithm      | Best     | Average  | Worst    | Space  | Stable
────────────────────────────────────────────────────────────────
Quick Sort     | O(nlogn) | O(nlogn) | O(n^2)   | O(logn) | No
Merge Sort     | O(nlogn) | O(nlogn) | O(nlogn) | O(n)    | Yes
Heap Sort      | O(nlogn) | O(nlogn) | O(nlogn) | O(1)    | No
Tim Sort*      | O(n)     | O(nlogn) | O(nlogn) | O(n)    | Yes
Counting Sort  | O(n+k)   | O(n+k)   | O(n+k)   | O(k)    | Yes
Radix Sort     | O(d*n)   | O(d*n)   | O(d*n)   | O(n+k)  | Yes

* Python's built-in sort. Hybrid merge+insertion sort.

GRAPH ALGORITHMS:
─────────────────
Algorithm        | Time          | Space  | Use Case
─────────────────────────────────────────────────────────
BFS              | O(V + E)      | O(V)   | Shortest path (unweighted)
DFS              | O(V + E)      | O(V)   | Connected components, cycle detect
Dijkstra         | O((V+E)logV)  | O(V)   | Shortest path (non-neg weights)
Bellman-Ford     | O(V * E)      | O(V)   | Shortest path (neg weights ok)
Floyd-Warshall   | O(V^3)        | O(V^2) | All-pairs shortest path
Kruskal          | O(E log E)    | O(V)   | MST
Prim             | O(E log V)    | O(V)   | MST (dense graphs)
Topological Sort | O(V + E)      | O(V)   | DAG ordering
A*               | O(E)          | O(V)   | Shortest path with heuristic

PYTHON-SPECIFIC PERFORMANCE NOTES:
───────────────────────────────────
- list.append(): O(1) amortized
- list.pop(0): O(n) — use collections.deque.popleft() for O(1)
- 'x in list': O(n) — use 'x in set' for O(1)
- dict/set: O(1) average for lookup, insert, delete
- sorted(): O(n log n) — Timsort, stable
- heapq: min-heap only. Negate for max-heap.
- collections.Counter: O(n) construction, O(1) lookup
- bisect module: O(log n) for sorted list operations
- functools.lru_cache: O(1) memoized function lookup
"""


# ==============================================================================
# STUDY PLAN: PRIORITY ORDER
# ==============================================================================
"""
TIER 1 — MUST KNOW (covers ~60% of coding interviews):
──────────────────────────────────────────────────────
  1. Arrays & Hashing (Two Sum, Group Anagrams, Top K)
  2. Two Pointers (3Sum, Container With Most Water)
  3. Sliding Window (Longest Substring, Min Window Substring)
  4. Binary Search (Rotated Array, Search on Answer)
  5. Linked Lists (Reverse, Merge, LRU Cache)
  6. Trees (Level Order, Validate BST, Max Path Sum)
  7. Graphs (Islands, Topological Sort, Dijkstra)
  8. Dynamic Programming (Coin Change, LIS, LCS, Knapsack)

TIER 2 — HIGH VALUE (covers next ~25%):
───────────────────────────────────────
  9. Stack (Monotonic stack, Valid Parentheses)
 10. Heap (Merge K Sorted, Running Median)
 11. Backtracking (Subsets, Permutations, N-Queens)
 12. Greedy (Merge Intervals, Jump Game)

TIER 3 — GOOD TO KNOW (remaining ~15%):
────────────────────────────────────────
 13. Tries (Implement Trie, Word Search II)
 14. Bit Manipulation (Single Number, Counting Bits)
 15. Math & Geometry (Rotate Image, Spiral Matrix)

BACKEND-SPECIFIC (for system design & domain rounds):
─────────────────────────────────────────────────────
 16. Caching (LRU/LFU implementation, cache patterns)
 17. Load Balancing (Round Robin, Least Connections, Consistent Hashing)
 18. Database Query Optimization (Indexes, Join types, MVCC)
 19. Routing/Pathfinding (A*, Dijkstra — especially for aviation domain)
 20. Geospatial (Haversine, Geohashing, K-D trees — aviation domain)
 21. System Design Algorithms (Bloom filter, Rate limiting, Skip list)
"""
