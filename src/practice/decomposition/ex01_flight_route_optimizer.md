# Problem Decomposition: Flight Route Optimizer

## Problem Statement

Design a flight route optimizer that finds fuel-efficient routes between
airports given real-time weather constraints. The system should re-optimize
when weather conditions change significantly.

---

## Your Task

˚
---

## 1. Clarifying Questions (list 5-8 you'd ask the interviewer)

-
-
-
-
-

## 2. Inputs

| Input | Format | Source | Update Frequency |
|-------|--------|--------|------------------|
|       |        |        |                  |
|       |        |        |                  |

## 3. Outputs

| Output | Format | Consumer |
|--------|--------|----------|
|        |        |          |
|        |        |          |

## 4. Constraints

- Latency requirement:
- Throughput requirement:
- Data freshness:
- Accuracy tolerance:

## 5. Sub-Problems (break the big problem into 3-5 smaller ones)

1.
2.
3.
4.
5.

## 6. Data Structures

| Sub-Problem | Data Structure | Why |
|-------------|----------------|-----|
|             |                |     |
|             |                |     |

## 7. Algorithms

| Sub-Problem | Algorithm | Time Complexity | Space Complexity |
|-------------|-----------|-----------------|------------------|
|             |           |                 |                  |
|             |           |                 |                  |

## 8. Tradeoffs

| Decision | Option A | Option B | Your Choice & Why |
|----------|----------|----------|-------------------|
|          |          |          |                   |
|          |          |          |                   |

## 9. Architecture Sketch

Describe the high-level components and how they interact:

```
[Component A] ---> [Component B] ---> [Component C]
```

## 10. What Would You Build First? (MVP)

-

---

## Hints (don't read until you've filled in the above)

<details>
<summary>Clarifying Questions</summary>

- How many airports/routes? (domestic vs international, 500 vs 5000 airports)
- What weather data is available? (wind, turbulence, icing, visibility)
- How often do routes need re-optimization? (every minute? on weather change?)
- Single aircraft or fleet-wide optimization?
- What does "fuel-efficient" mean? (minimum fuel, minimum time, or a weighted combo?)
- Are there hard constraints? (no-fly zones, altitude restrictions, ATC routing)
- What's the acceptable compute time for a single route optimization?
- Is there a human in the loop or is it fully automated?

</details>

<details>
<summary>Sub-Problems</summary>

1. **Airspace graph construction** -- model waypoints as nodes, airways as edges with cost = f(fuel, time, weather risk)
2. **Weather data integration** -- ingest and index weather grid data for fast lookup by 3D coordinate
3. **Cost function design** -- combine fuel burn, time, turbulence risk, wind advantage into a single edge weight
4. **Pathfinding** -- A* or Dijkstra with the cost function, respecting altitude and airspace constraints
5. **Re-optimization trigger** -- detect when weather changes enough to invalidate the current route

</details>

<details>
<summary>Key Algorithms</summary>

- **A*** with a great-circle distance heuristic for pathfinding
- **R-tree or H3 index** for fast weather data lookup by spatial coordinate
- **Weighted graph** with dynamic edge costs (recomputed when weather updates)
- **Priority queue (min-heap)** for A* frontier

</details>
