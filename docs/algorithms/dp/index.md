---
title: Dynamic Programming
---

# Dynamic Programming

| Problem | Complexity | Key Pattern |
|---------|-----------|-------------|
| [Climbing Stairs](climbing_stairs.md) | `O(n)` | Counting paths / Fibonacci family — "how many ways to reach step N", |
| [Coin Change](coin_change.md) | `O(amount * len(coins))` | Classic "minimum cost to reach target" DP. Any problem where you choose |
| [Constraint Satisfaction](constraint_satisfaction.md) | `Exponential worst case, but constraint propagation prunes` | Puzzle solving, scheduling, configuration — "Sudoku", "N-Queens via |
| [Edit Distance](edit_distance.md) | `O(m * n)` | String similarity / diff algorithms — "minimum edits", "Levenshtein |
| [Knapsack](knapsack.md) | `O(n * W)` | Resource allocation with constraints — "maximize value under weight |
| [Longest Common Subseq](longest_common_subseq.md) | `O(m * n)` | Diff / alignment — "longest common subsequence", "diff two files", |
| [Longest Increasing Subseq](longest_increasing_subseq.md) | `O(n log n)` | Patience sorting / longest chain — "longest increasing subsequence", |
| [Traveling Salesman Dp](traveling_salesman_dp.md) | `O(n^2 * 2^n)` | Visit-all-nodes optimization — "shortest route visiting every city", |
