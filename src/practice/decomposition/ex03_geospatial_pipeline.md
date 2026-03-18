# Problem Decomposition: Geospatial Data Pipeline

## Problem Statement

Design a data pipeline that ingests 100+ geospatial data sources (ADS-B
aircraft positions, AIS ship positions, weather grids, satellite imagery,
airspace boundaries) into a unified data store that supports real-time
queries and historical analysis. Data freshness requirement: most sources
must be queryable within 30 seconds of receipt.

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

## 2. Data Sources Inventory

| Source Type | Example | Format | Volume | Frequency |
|---|---|---|---|---|
| | | | | |
| | | | | |

## 3. Outputs / Consumers

| Consumer | Query Pattern | Latency Requirement |
|---|---|---|
| | | |
| | | |

## 4. Constraints

- Number of sources:
- Total ingest rate:
- Freshness (source to queryable):
- Retention policy:
- Availability / uptime:

## 5. Sub-Problems

1.
2.
3.
4.
5.
6.

## 6. Data Model

How do you represent heterogeneous geospatial data in a unified way?

| Entity | Key Fields | Geometry Type | Temporal? |
|---|---|---|---|
| | | | |
| | | | |

## 7. Pipeline Stages

```
[Stage 1: ???] -> [Stage 2: ???] -> [Stage 3: ???] -> [Stage 4: ???]
```

Describe what each stage does, what technology you'd use, and why.

## 8. Tradeoffs

| Decision | Option A | Option B | Your Choice & Why |
|---|---|---|---|
| | | | |
| | | | |

## 9. Architecture Sketch

```
[Sources] ---> [???] ---> [???] ---> [???] ---> [Consumers]
```

## 10. Failure Modes

| Failure | Impact | Mitigation |
|---|---|---|
| Source goes down | | |
| Pipeline backlog | | |
| Storage full | | |
| Schema change in source | | |

---

## Hints (don't read until you've filled in the above)

<details>
<summary>Clarifying Questions</summary>

- What are the source formats? (JSON, Protobuf, CSV, binary, GRIB for weather?)
- Do all sources have the same coordinate system? (WGS84 or do we need transforms?)
- What's the query interface? (SQL, REST API, WebSocket for streaming?)
- Do we need to join across source types? (e.g., "aircraft within a weather polygon")
- Is there a schema registry or can sources change format without notice?
- What's the durability requirement? (can we lose 1 minute of data?)
- Do we need exactly-once semantics or is at-least-once with dedup acceptable?
- Who manages the source connectors? (us or the data providers?)
</details>

<details>
<summary>Sub-Problems</summary>

1. **Source connectors** -- adapters per source type (poll-based for APIs, push-based for streams, file watchers for drops)
2. **Schema normalization** -- convert heterogeneous formats into a common internal model (standardize coordinates, timestamps, identifiers)
3. **Stream processing** -- validate, enrich, deduplicate, and route events (Kafka Streams, Flink, or Beam)
4. **Spatial indexing** -- index ingested data for fast geo-queries (H3 for aggregation, R-tree for polygons, geohash for point lookups)
5. **Hot storage** -- recent data for real-time queries (PostGIS, Redis, or DynamoDB with geo index)
6. **Cold storage** -- historical data for analysis (S3 + Parquet partitioned by time and H3 cell, queryable via Athena/Trino)
</details>

<details>
<summary>Pipeline Architecture</summary>

```
[100+ Sources]
    |
    v
[Source Connectors] -- one per source, handles auth/format/retry
    |
    v
[Kafka Topics] -- partitioned by source type or geo region
    |
    v
[Stream Processor (Flink/Beam)] -- normalize, validate, enrich, dedup
    |
    +---> [Hot Store (PostGIS/Redis)] -- real-time queries, 24-48h retention
    |
    +---> [Cold Store (S3 + Parquet)] -- historical, partitioned by time + H3
    |
    +---> [Event Bus (Kafka/SNS)] -- notify downstream consumers of new data
```
</details>

<details>
<summary>Back-of-Envelope Math</summary>

- ADS-B: ~10K aircraft in US airspace, 1 update/sec = 10K events/sec
- AIS: ~50K ships, 1 update/10sec = 5K events/sec
- Weather grids: CONUS grid at 3km resolution, 4 updates/hour = bursty, ~100MB/update
- Total: ~50K events/sec sustained, bursty to 200K on weather updates
- Daily storage: ~50K * 86400 * 200B = ~860 GB/day raw events
- Hot store: 48h window = ~1.7 TB in PostGIS (with indexes, ~3-4 TB)
- Cold store: compress to ~200 GB/day in Parquet, ~6 TB/month
</details>
