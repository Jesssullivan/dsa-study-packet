# 14-Day Whiteboard Ramp

The day-by-day plan for the two weeks before a whiteboarding / live-coding
interview, and **the only place the daily loop and calendar live**. The method
(CLARP, panic first-aid, scripts, rubric) is
[sheet 10](10-whiteboard-performance-protocol.md). Each day is a focused
four-hour block. **Record every rep.**

## Print this stack (the physical desk)

- **The booklet** (`booklet.pdf`) — decision trees + one algorithm per page.
- **Sheets 01, 03, 05** — stdlib, algorithm templates, pattern triggers (open every day).
- **Sheet 10** — the method (read it fully on Day 1).
- **Sheet 07** — interview-day logistics (Week 2).
- **This sheet (11)** — check off a row a day.

## The daily loop (board ↔ IDE)

1. **Pick**: `just study-spaced 1` → today's drill.
2. **Present cold**: `just interview <topic> <problem>` — prints the problem
   statement only (no approach, no complexity) and strips the solution.
3. **Board**: phone recording ON. Stand. Run **CLARP out loud** (sheet 10 §2),
   start to finish, no editor.
4. **IDE**: implement your board solution in the stripped file; `just study
   <topic>` until tests pass. Say out loud where the typed version differed
   from the board version, and why.
5. **Score**: watch 2 min of tape, grade the sheet-10 §5 rubric, log it:
   `just rep "<topic>/<problem> C2 L1 A2 R1 P2 <one fix>"`.
6. **Mark**: `just challenge-done <topic> <problem>` (feeds spaced repetition).

## Four-hour allocation

| Time | Work |
|------|------|
| 0:00-0:10 | Arrival ritual: breathing + worry dump + reappraisal + choose first draw |
| 0:10-1:40 | Two cold board reps, 35 min each, camera on |
| 1:40-2:40 | IDE implementation + tests for both reps |
| 2:40-3:10 | Tape review + rubric + one logged fix per rep |
| 3:10-3:40 | Targeted refresher for the miss, not passive browsing |
| 3:40-4:00 | Spaced-repetition closeout + tomorrow's first miss queued |

## Example cycle (fill in your own dates)

> This run: **Day 1 = Sun Jul 5, 2026**, interviews ≈ Jul 20. Adjust the anchor;
> the shape holds for any two-week window.

## Week 1 — build the reflex (correctness + narration)

| Day | Focus | Drills (`just interview`) | Sheets open | Watching |
|-----|-------|---------------------------|-------------|----------|
| **1** | Read sheet 10 cover-to-cover, then easy arrays | `arrays two_sum`, `arrays group_anagrams` | 10, 03, 01 | camera |
| **2** | Arrays + stacks/queues | `arrays product_except_self`, `stacks_queues valid_parentheses`, `stacks_queues daily_temperatures` | 03, 05, 01 | camera |
| **3** | Sliding window + binary search — **practice a deliberate blank + recovery (sheet 10 §3)** | `sliding_window longest_substring_no_repeat`, `searching binary_search`, `searching search_rotated_array` | 03, 05 | camera |
| **4** | BFS/DFS + linked lists | `graphs number_of_islands`, `graphs course_schedule`, `linked_lists reverse_linked_list` | 03, 02 | camera |
| **5** | Trees + heaps — **first human rep** | `trees validate_bst`, `trees level_order_traversal`, `heaps kth_largest` | 02, 03 | **person** |
| **6** | Trees/trie + shore up your weakest rubric row | `trees trie`, 2 review draws | 08, 02 | person |
| **7** | **Rest** (or one light review rep). Rest is training. | — | — | — |

## Week 2 — pressure + breadth (collaboration + hard cases)

| Day | Focus | Drills (`just interview`) | Sheets open | Watching |
|-----|-------|---------------------------|-------------|----------|
| **8** | Graphs (heaviest topic — most reps) | `graphs dijkstra`, `graphs topological_sort`, `graphs bellman_ford` | 03, 06 | person interrupts with "why?" |
| **9** | Dynamic programming | `dp coin_change`, `dp edit_distance`, `dp knapsack`, `dp longest_increasing_subseq` | 03 | person interrupts |
| **10** | Mixed cold draws, full 35-min mock format. If your targets differ by language, hand-write one solution in each (scratch file, `c++ -std=c++20 -Wall`). | `just study-spaced 3` | 07, 05 | camera |
| **11** | Backtracking + greedy + strings | `backtracking subsets`, `backtracking n_queens`, `greedy merge_intervals`, `strings valid_palindrome` | 03, 05 | person |
| **12** | **Full mock panel** — back-to-back problems, on camera, with a person | 3 cold draws | 07, 10 (§7 card) | **person** |
| **13** | Taper. Re-watch your **best** tapes (not worst) to lock in the felt sense of a good rep. Light reps only. | 1 easy draw | 10 (§7) | camera |
| **14** | Rest. Arrive rested, not crammed. Read the sheet-10 §7 panic card + sheet 07. Practice the board-dump only. | — | 10 (§7), 07 | — |

**The target is not a perfect score — it's +1 on your weakest rubric row each
day.** Fourteen days of +1 is a transformed interview. You've got this.
