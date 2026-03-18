# Problem Decomposition: Real-Time Vehicle Tracking System

## Problem Statement

Design a real-time vehicle tracking system that ingests GPS position updates
from 100,000 vehicles, stores their trajectories, and supports queries like
"find all vehicles within 5 km of a point" and "show me vehicle X's route
for the last 2 hours."

---

## Your Task

Break this problem down using the structure below. Spend 15-20 minutes
thinking through each section before looking at the hints at the bottom.

---

## 1. Clarifying Questions (list 5-8 you'd ask the interviewer)

-
-
-
-
-

## 2. Inputs

| Input | Format | Source | Update Frequency |
|---|---|---|---|
| | | | |
| | | | |

## 3. Outputs / Queries Supported

| Query | Expected Latency | Access Pattern |
|---|---|---|
| | | |
| | | |

## 4. Constraints

- Number of vehicles:
- Position update frequency:
- Query latency requirement:
- Data retention:
- Availability requirement:

## 5. Sub-Problems

1.
2.
3.
4.
5.

## 6. Data Structures

| Sub-Problem | Data Structure | Why |
|---|---|---|
| | | |
| | | |

## 7. Storage Design

| Data | Store | Schema/Key Design | Why |
|---|---|---|---|
| | | | |
| | | | |

## 8. Tradeoffs

| Decision | Option A | Option B | Your Choice & Why |
|---|---|---|---|
| | | | |
| | | | |

## 9. Architecture Sketch

```
[Component A] ---> [Component B] ---> [Component C]
```

## 10. Scaling Considerations

- What happens at 1M vehicles?
- What if query volume is 10x read-heavy?
- How do you handle a vehicle that goes offline for hours then sends a burst?

---

## Hints (don't read until you've filled in the above)

<details>
<summary>Clarifying Questions</summary>

- What's the GPS update frequency? (every 1s, 5s, 30s?)
- Do we need historical trajectories or just current position?
- What's the geographic scope? (city, country, global?)
- How precise does the proximity query need to be? (exact vs approximate)
- Are there real-time alerting requirements? (geofence entry/exit)
- What's the read-to-write ratio?
- Do we need to support replay of historical routes?
- Is there a map visualization component?
</details>

<details>
<summary>Sub-Problems</summary>

1. **Ingestion** -- receive and validate high-throughput GPS updates (Kafka/Kinesis)
2. **Current position store** -- maintain latest position per vehicle for proximity queries (Redis with geospatial index or DynamoDB)
3. **Trajectory store** -- append-only time-series of positions (TimescaleDB, InfluxDB, or S3 + partitioned Parquet)
4. **Proximity query service** -- "find vehicles near point X" using geospatial index (Redis GEORADIUS, PostGIS, or in-memory H3 index)
5. **Route query service** -- "show vehicle X's route from time A to B" (range query on time-series store)
</details>

<details>
<summary>Key Data Structures</summary>

- **Geohash/H3 index** for spatial partitioning of current positions
- **Time-partitioned tables** for trajectory storage (partition by hour/day)
- **In-memory geospatial index** (R-tree or grid) for low-latency proximity queries
- **Write-ahead log** (Kafka topic) for durability before processing
</details>

<details>
<summary>Back-of-Envelope Math</summary>

- 100K vehicles x 1 update/sec = 100K writes/sec
- Each update: ~100 bytes (vehicle_id, lat, lon, timestamp, speed, heading)
- Write throughput: ~10 MB/sec
- Daily storage: ~864 GB raw (compress to ~200 GB with columnar format)
- Proximity query: need sub-100ms; geospatial index on current positions only
</details>
