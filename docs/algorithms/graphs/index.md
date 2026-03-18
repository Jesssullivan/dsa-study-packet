---
title: Graphs
---

# Graphs

| Problem | Complexity | Key Pattern |
|---------|-----------|-------------|
| [A Star Search](a_star_search.md) | `O(E log V) with a good heuristic (grid: E ~ 4V)` | Shortest path when you have a good heuristic (estimated distance to goal). |
| [Bellman Ford](bellman_ford.md) | `O(V * E)` | Shortest paths with negative edge weights — currency arbitrage |
| [Clone Graph](clone_graph.md) | `O(V + E)` | Graph deep copy — "clone graph", "copy linked structure with cycles". |
| [Course Schedule](course_schedule.md) | `O(V + E)` | Cycle detection in a directed graph — "can all tasks be completed?", |
| [Dijkstra](dijkstra.md) | `O((V + E) log V)` | Shortest path with NON-NEGATIVE weights. Flight routing, network latency, |
| [Geohash Grid](geohash_grid.md) | `---` | Spatial indexing for proximity queries — "find nearby points", |
| [Kd Tree](kd_tree.md) | `---` | Nearest neighbor in multi-dimensional space — "closest point", |
| [Minimum Spanning Tree](minimum_spanning_tree.md) | `---` | Minimum cost to connect all nodes — cable/road/pipeline routing, |
| [Network Delay Time](network_delay_time.md) | `O((V + E) log V)` | "Can a signal/message reach all nodes, and how long?" — broadcast |
| [Network Flow](network_flow.md) | `O(V * E^2)` | Maximum throughput — "max bandwidth", "maximum matching", "supply |
| [Number Of Islands](number_of_islands.md) | `O(m * n) — each cell visited at most once` | Connected components / flood fill — "count islands", "count regions", |
| [Topological Sort](topological_sort.md) | `O(V + E)` | Dependency resolution — "build order", "task scheduling with prereqs", |
| [Word Ladder](word_ladder.md) | `O(n * m^2) where n = |word_list|, m = word length` | BFS for shortest transformation sequence — "minimum edits", "fewest |
