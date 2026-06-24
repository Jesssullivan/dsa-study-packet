# Interview Day Guide

Practical, printable reference for technical interview day.

---

## What to Print & Bring

**Printed Materials** (in this order on your desk):

1. `07-interview-day-guide.md` (this sheet) -- top of stack for quick pattern lookup
2. `01-python-stdlib.md` -- collections, heapq, itertools, bisect
3. `03-algorithm-templates.md` -- sliding window, binary search, BFS/DFS, DP, backtracking
4. `05-common-patterns.md` -- pattern recognition triggers
5. `04-big-o-complexity.md` -- complexity verification
6. `06-system-design.md` -- for system design round (L7+)
7. RESEARCH.md first page, if available (organization overview, mission, products, tech stack)

**Physical Items**:
- Notepad + pen (for sketching graphs, trees, state transitions)
- Water bottle
- Charger plugged in

---

## Pre-Interview Warmup (30 min before)

1. **Solve 1 easy problem** (10 min) -- `src/algo/arrays/two_sum.py` or `src/algo/stacks_queues/valid_parentheses.py`. Gets your brain in coding mode.
2. **Quick review** (10 min) -- skim reference sheet 01 (Python stdlib) + 03 (algorithm templates). Focus on function signatures, not reading every line.
3. **Body prep** (10 min) -- stretch, hydrate, 3 deep breaths. Use the bathroom. Close Slack/email. Set phone to DND.

---

## Browser Tabs to Open

Open these before the interview starts:

| Tab | URL | Purpose |
|-----|-----|---------|
| 1 | <https://docs.python.org/3/library/collections.html> | Counter, defaultdict, deque |
| 2 | <https://docs.python.org/3/library/heapq.html> | heappush, heappop, nlargest, nsmallest |
| 3 | <https://docs.python.org/3/library/itertools.html> | combinations, permutations, accumulate |
| 4 | <https://docs.python.org/3/library/bisect.html> | bisect_left, bisect_right, insort |
| 5 | <https://www.bigocheatsheet.com/> | Data structure & sorting complexities |
| 6 | <https://visualgo.net/> | Algorithm visualization (graphs, sorting, trees) |
| 7 | <https://docs.python.org/3/library/typing.html> | Type hints reference |
| 8 | Target organization/product pages | Mission, product, and leadership context |

---

## Interview Flow & Prep by Round

### Stage 1: Pre-screen

Headhunter chats with CTO and hiring manager based on FOSS contributions, PR experience, etc.
No prep needed -- this is about your existing body of work.

### Stage 2: Hiring manager interview

Role fit, experience, expectations. Be ready to discuss your background, why
the organization, and what you bring.

### Stage 3: Engineering lead interview

Technical depth, architecture thinking, team dynamics.
**Print sheet on desk**: 06 (system design) for reference.

### Stage 4: Backend algo deep dive (1-3 hrs)

**Tabs**: 1-5 for quick stdlib lookups and complexity verification.
**Print sheets on desk**: 01, 03, 04, 05.

**Approach for each problem**:
1. Read the problem fully -- twice. Underline constraints.
2. State your approach out loud before coding.
3. Write clean code with type hints.
4. Test with the given examples + one edge case.
5. State time and space complexity.

Think out loud the entire time. Silence = lost signal.

### Stage 5: Frontend / cross-team engineering deep dive (1-3 hrs)

**Tabs**: None needed (they show you code).
**Print sheet on desk**: 01 for stdlib reference, 05 for common patterns.

**5-step framework for code review**:
1. **Read slowly** -- skim signatures and docstrings first, then trace one path.
2. **Identify the "smell"** -- nested loops, missing error handling, N+1 queries, unbounded cache.
3. **Trace with concrete input** -- pick a small input and walk through the code line by line.
4. **Name the pattern/antipattern** -- "This is an N+1 query pattern" or "This cache has no eviction policy."
5. **Propose fix with complexity analysis** -- "Replace the nested loop with a hash map lookup, O(n^2) -> O(n)."

**Problem decomposition framework**:
1. Restate the problem in your own words. Confirm understanding.
2. Identify sub-problems. Draw a diagram (use your notepad).
3. Map each sub-problem to a known algorithm or data structure.
4. Define interfaces between components.
5. Discuss tradeoffs: time vs space, accuracy vs speed, complexity vs maintainability.

### Stage 6: On-site intensive (6-8 hrs)

All-day in-person. Multiple rounds covering algorithms, system design, code reading, and collaboration.

**System design framework** (30 min per round):
- 5 min: **Requirements** -- functional + non-functional. Ask clarifying questions. Estimate scale (QPS, data volume, latency target).
- 5 min: **High-level design** -- draw boxes and arrows. Identify core components.
- 15 min: **Deep-dive components** -- pick 2-3 to detail. Schema, APIs, data flow, failure modes.
- 5 min: **Tradeoffs** -- consistency vs availability, cost vs performance. Name alternatives you considered.

### Stage 7: Executive or bar-raiser interview

**Tab**: 8 (target organization/product pages).

Prepare 3-4 questions showing genuine interest:
- "How is the mission evolving across operational domains?"
- "What's the biggest technical challenge the engineering team is tackling right now?"
- "How does the team balance mission needs, reliability, and product velocity?"
- "Which constraints shape engineering decisions most: latency, security, scale, certification, or operator workflow?"

Mission, judgment, team fit. Be authentic, curious, and concise.

### Stage 8: Offer & negotiation

No prep in this guide -- but know your numbers and priorities going in.

---

## Quick-Access Patterns Checklist

When you see a trigger word in the problem statement, reach for the corresponding pattern:

| Trigger | Pattern | Template Location |
|---------|---------|-------------------|
| "subarray", "substring", "contiguous" | Sliding window | ref 03 SS3 |
| "sorted array", "search", "minimize maximum" | Binary search | ref 03 SS1 |
| "shortest path", "level by level", "minimum steps" | BFS | ref 03 SS2 |
| "connected components", "group", "union" | DFS / Union-Find | ref 03 SS2, SS6 |
| "k-th largest/smallest", "top k", "closest k" | Heap | ref 02 SS(heap) |
| "pairs that sum to", "two values" | Two pointers / hash map | ref 05 SS2 |
| "overlapping intervals", "merge ranges" | Merge intervals / sort by start | ref 05 SS(intervals) |
| "all combinations", "all subsets", "generate" | Backtracking | ref 03 SS5 |
| "maximum/minimum cost", "number of ways" | Dynamic programming | ref 03 SS4 |
| "dependency order", "prerequisites", "schedule" | Topological sort | ref 03 SS(topo) |
| "prefix", "autocomplete", "word search" | Trie | ref 02 SS(trie) |
| "next greater", "previous smaller", "monotonic" | Monotonic stack | ref 05 SS(stack) |
| "sliding window maximum/minimum" | Monotonic deque | ref 05 SS(deque) |
| "cycle detection", "linked list middle" | Fast & slow pointers | ref 05 SS(pointers) |
| "palindrome", "parentheses matching" | Stack | ref 02 SS(stack) |

---

## Emergency Debug Checklist

When you're stuck during a coding round:

| Symptom | Check |
|---------|-------|
| **Off-by-one error** | Check loop bounds: `< n` vs `<= n`. Check index ranges: 0-indexed vs 1-indexed. |
| **Wrong answer** | Trace with the simplest possible input (n=1 or n=2). |
| **Time limit exceeded (TLE)** | Look for O(n^2) that can become O(n log n) or O(n). Common fix: replace inner loop with hash map or binary search. |
| **Can't think of approach** | Ask: "What data structure gives me O(1) lookup?" (hash map). "Can I sort first?" "Can I use a seen set?" |
| **Still stuck** | Simplify: solve for a smaller version first. Build from brute force, then optimize. |
| **Recursive solution has bugs** | Check base cases first. Draw the recursion tree for n=3. |
| **Memory limit exceeded** | Are you storing all results? Can you stream / use constant space? Iterative DP instead of memoization? |

**Golden rule**: If stuck for more than 3 minutes, talk to your interviewer. Say: "I'm considering X and Y approaches. X has this tradeoff, Y has that. I'm leaning toward X because..." They want to help.
