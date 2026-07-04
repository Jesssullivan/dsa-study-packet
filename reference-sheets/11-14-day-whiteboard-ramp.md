# 14-Day Whiteboard Ramp

A day-by-day plan for the two weeks before a whiteboarding / live-coding /
"talk me through it" interview. It turns the protocol in
[sheet 10](10-whiteboard-performance-protocol.md) into a concrete daily
checklist: *on this day, stand at the board, do these drills, with these printed
sheets open.* Each day is ≈2–3 hours. **Record every rep.**

The knowledge substrate is the Core 42 (`scripts/study_schedule.py`); this sheet
adds the **performance** rep — standing, out loud, on camera — on top of it.

## Print this stack (the physical desk)

- **The booklet** (`booklet.pdf`) — decision trees + one algorithm per page.
- **Sheets 01, 03, 05** — stdlib, algorithm templates, pattern triggers (open every day).
- **Sheet 10** — the performance & panic protocol (read it fully on Day 1).
- **Sheet 07** — interview-day logistics (Week 2).
- **This sheet (11)** — check off a row a day.

## Example cycle (fill in your own dates)

> This run: **Day 1 = Sun Jul 5, 2026**, interviews ≈ Jul 20. Adjust the anchor;
> the shape holds for any two-week window.

## Week 1 — build the reflex (correctness + narration)

| Day | Focus | Drills (`just challenge`) | Sheets open | Watching |
|-----|-------|---------------------------|-------------|----------|
| **1** | Read sheet 10 cover-to-cover, then easy arrays | `arrays two_sum`, `arrays group_anagrams` | 10, 03, 01 | camera |
| **2** | Arrays + stacks/queues | `arrays product_except_self`, `stacks_queues valid_parentheses`, `stacks_queues daily_temperatures` | 03, 05, 01 | camera |
| **3** | Sliding window + binary search — **practice a deliberate blank + recovery (§3)** | `sliding_window longest_substring_no_repeat`, `searching binary_search`, `searching search_rotated_array` | 03, 05 | camera |
| **4** | BFS/DFS + linked lists | `graphs islands`, `graphs course_schedule`, `linked_lists reverse_linked_list` | 03, 02 | camera |
| **5** | Trees + heaps — **first human rep** | `trees validate_bst`, `trees level_order_traversal`, `heaps kth_largest` | 02, 03 | **person** |
| **6** | Trees/trie + shore up your weakest row on the rubric | `trees trie`, 2 review draws | 08, 02 | person |
| **7** | **Rest** (or one light review rep). Rest is training. | — | — | — |

## Week 2 — pressure + breadth (collaboration + hard cases)

| Day | Focus | Drills (`just challenge`) | Sheets open | Watching |
|-----|-------|---------------------------|-------------|----------|
| **8** | Graphs (heaviest topic — most reps) | `graphs dijkstra`, `graphs topo_sort`, `graphs bellman_ford` | 03, 06 | person interrupts with "why?" |
| **9** | Dynamic programming | `dp coin_change`, `dp edit_distance`, `dp knapsack`, `dp LIS` | 03 | person interrupts |
| **10** | Mixed cold draws, full 35-min mock format. If targets differ by language, write one solution in each. | `study_schedule.py 3` | 07, 05 | camera |
| **11** | Backtracking + greedy + strings | `backtracking subsets`, `backtracking n_queens`, `greedy merge_intervals`, `strings valid_palindrome` | 03, 05 | person |
| **12** | **Full mock panel** — back-to-back problems, on camera, with a person | 3 cold draws | 07, 10 (§8 card) | **person** |
| **13** | Taper. Re-watch your **best** tapes (not worst) to lock in the felt sense of a good rep. Light reps only. | 1 easy draw | 10 (§8) | camera |
| **14** | Rest. Arrive rested, not crammed. Read the §8 one-page panic card + sheet 07. Practice the board-dump only. | — | 10 (§8), 07 | — |

## Each day, in order

1. `uv run python scripts/study_schedule.py 1` — get the next drill.
2. Phone recording **on**. Stand at the board.
3. Run **CLARP out loud** (sheet 10 §2), start to finish, no editor.
4. Type it into `just challenge <topic> <problem>` to check against tests.
5. Watch 2 minutes of tape. Score the §5 rubric. Note **one** fix for tomorrow.

**The target is not a perfect score — it's +1 on your weakest rubric row each
day.** Fourteen days of +1 is a transformed interview. You've got this.
