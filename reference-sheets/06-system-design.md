# System Design Reference Sheet

## Load Balancing

| Strategy | How It Works | Best For |
|---|---|---|
| Round Robin | Rotate through servers sequentially | Homogeneous servers, stateless services |
| Weighted Round Robin | Rotate with weights per server capacity | Heterogeneous servers |
| Least Connections | Route to server with fewest active connections | Long-lived connections, varying request cost |
| Consistent Hashing | Hash key to ring position; route to next node | Caches, sharded datastores, minimize reshuffling |
| IP Hash | Hash client IP to pin to a server | Session affinity without sticky cookies |

**Consistent hashing** detail: virtual nodes (vnodes) spread load more evenly. Adding/removing a node only moves `K/N` keys on average.

## Caching Patterns

| Pattern | Flow | Tradeoff |
|---|---|---|
| **Cache-aside** (lazy) | App checks cache -> miss -> read DB -> populate cache | Simple; stale reads possible |
| **Write-through** | App writes cache + DB together | Strong consistency; higher write latency |
| **Write-behind** (write-back) | App writes cache; cache async-writes DB | Low write latency; risk of data loss |
| **Read-through** | Cache itself fetches from DB on miss | Cleaner app code; cache becomes a dependency |

Key knobs:
- **TTL**: balance freshness vs hit rate. Short TTL = more DB hits. Long TTL = stale data.
- **Eviction**: LRU (most common), LFU (frequency-based), FIFO.
- **Cache stampede**: use locking or probabilistic early expiration.
- **Invalidation**: event-driven (pub/sub on writes) or TTL-based.

## Message Queues

### Kafka
- Append-only log, partitioned by topic.
- Consumer groups for parallel processing; each partition consumed by one consumer per group.
- Retention-based (not delete-on-consume); enables replay.
- Use case: high-throughput event streaming, audit logs, real-time pipelines.

### SQS
- Fully managed, no partition management.
- Standard queue: at-least-once, best-effort ordering.
- FIFO queue: exactly-once, strict ordering (lower throughput).
- Visibility timeout: message invisible to other consumers while being processed.

### Dead Letter Queues (DLQ)
- Route messages that fail processing N times.
- Always set `maxReceiveCount`. Monitor DLQ depth as an alert.
- Reprocess: move DLQ messages back to main queue after fixing the consumer.

## Database Design

### SQL vs NoSQL Tradeoffs

| | SQL (Postgres, MySQL) | NoSQL (DynamoDB, Mongo, Cassandra) |
|---|---|---|
| Schema | Rigid, enforced | Flexible, schema-on-read |
| Joins | Native | Manual (denormalize or app-side) |
| Transactions | ACID | Varies (eventual consistency common) |
| Scale model | Vertical first; read replicas | Horizontal (partition/shard natively) |
| Best for | Complex queries, relationships | High write throughput, simple access patterns |

### Sharding Strategies
- **Range-based**: shard by key range (e.g., A-M, N-Z). Risk: hot shards.
- **Hash-based**: hash(key) % N. Even distribution; range queries require scatter-gather.
- **Directory-based**: lookup table maps key to shard. Flexible; lookup is a bottleneck.

### Replication
- **Leader-follower**: one writer, N readers. Simple; replication lag on reads.
- **Multi-leader**: multiple writers. Good for geo-distributed; conflict resolution needed.
- **Leaderless** (Dynamo-style): quorum reads/writes (R + W > N). Tunable consistency.

## Distributed Systems Patterns

### CAP Theorem
Pick two of three: **Consistency**, **Availability**, **Partition tolerance**.
In practice, partitions happen, so choose CP (reject requests during partition)
or AP (serve stale data during partition).

### Consensus
- **Raft**: leader election + log replication. Understandable. Used in etcd, Consul.
- **Paxos**: more general, harder to implement.
- Use case: metadata stores, config management, leader election.

### Eventual Consistency
- Writes propagate asynchronously; reads may see stale data.
- Conflict resolution: last-writer-wins (LWW), vector clocks, CRDTs.
- Read-your-writes: route reads to the same replica that handled the write.

### Other Patterns
- **Circuit breaker**: fail fast when downstream is unhealthy. States: closed -> open -> half-open.
- **Bulkhead**: isolate failures by partitioning resources (thread pools, connections).
- **Saga**: distributed transaction as a sequence of local transactions + compensating actions.
- **Idempotency**: design operations so retries are safe. Use idempotency keys.

## Domain-relevant: Real-Time & Geospatial

### Real-Time Data Ingestion
- **Pattern**: Source -> Message broker (Kafka) -> Stream processor -> Store + Serve
- **Backpressure**: if consumer can't keep up, use bounded queues + drop/sample policy.
- **Exactly-once**: Kafka transactions + idempotent producers; or dedup at consumer.
- **Fan-out**: one event triggers multiple consumers (Kafka consumer groups, SNS -> SQS).

### Geospatial Indexing

| Structure | How It Works | Best For |
|---|---|---|
| **R-tree** | Bounding rectangles in a balanced tree | Range queries, nearest neighbor on polygons |
| **Geohash** | Encode lat/lng to a string; prefix = coarser area | Proximity search via prefix matching; easy to shard |
| **H3** (Uber) | Hexagonal hierarchical grid over the globe | Uniform area cells; good for aggregation and analysis |
| **Quad-tree** | Recursively subdivide 2D space into 4 quadrants | Point data, adaptive resolution |
| **KD-tree** | Binary tree splitting on alternating dimensions | Nearest-neighbor in low dimensions |

PostGIS: Postgres extension for geospatial. Supports R-tree indexes (GiST), ST_Distance, ST_Within, ST_Intersects.

### Stream Processing
- **Windowing**: tumbling (fixed, non-overlapping), sliding (overlapping), session (gap-based).
- **Watermarks**: track event-time progress; handle late-arriving data.
- **Frameworks**: Apache Flink (true streaming), Spark Structured Streaming (micro-batch), Kafka Streams (library, no cluster).

## API Design

### REST vs gRPC

| | REST | gRPC |
|---|---|---|
| Format | JSON (text) | Protobuf (binary) |
| Transport | HTTP/1.1 or 2 | HTTP/2 (multiplexed) |
| Streaming | Limited (SSE, WebSocket) | Native bidirectional streaming |
| Tooling | Universal (curl, browser) | Needs codegen; harder to debug |
| Best for | Public APIs, web clients | Internal microservices, low-latency |

### Pagination
- **Offset-based**: `?page=3&size=20`. Simple; skips rows on every request (slow at depth).
- **Cursor-based**: `?cursor=abc123&size=20`. Encode last-seen ID/timestamp. Stable under inserts.
- **Keyset**: `WHERE id > last_id ORDER BY id LIMIT 20`. Most efficient for SQL.

### Rate Limiting
- **Token bucket**: tokens refill at fixed rate; request costs 1 token. Allows bursts.
- **Sliding window log**: store timestamps; count in window. Precise; memory-heavy.
- **Sliding window counter**: combine fixed window counts with interpolation. Good tradeoff.
- Implement at API gateway (Kong, AWS API Gateway) or app level (Redis + Lua script).

## Monitoring & Observability

### Three Pillars

| Pillar | What | Tools |
|---|---|---|
| **Metrics** | Numeric time-series (latency p99, error rate, throughput) | Prometheus, Grafana, CloudWatch |
| **Logs** | Structured event records | ELK (Elasticsearch + Logstash + Kibana), Loki |
| **Traces** | Request flow across services | Jaeger, Zipkin, AWS X-Ray, OpenTelemetry |

### Key Metrics (RED Method)
- **Rate**: requests per second.
- **Errors**: error count or error rate.
- **Duration**: latency distribution (p50, p95, p99).

### Alerting
- Alert on symptoms (high error rate), not causes (CPU usage).
- Use multi-window, multi-burn-rate alerts to avoid flapping.
- Runbooks: every alert should link to a doc explaining what to check and how to mitigate.

### SLIs/SLOs/SLAs
- **SLI** (indicator): measured metric (e.g., "99.2% of requests < 200ms").
- **SLO** (objective): target for the SLI (e.g., "99.9% availability per month").
- **SLA** (agreement): contractual promise with consequences for breach.
- **Error budget**: 100% - SLO = budget for experimentation/deploys.
