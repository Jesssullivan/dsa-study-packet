---
title: Lru Cache
---

# Lru Cache

## Problem

Design a data structure that follows the Least Recently Used (LRU)
eviction policy, supporting get and put in O(1) time.

## Approach

OrderedDict version: move accessed keys to end; pop from front on evict.
Manual version: doubly linked list + hash map for O(1) removal/insertion.

## When to Use

O(1) cache with eviction — "design LRU/LFU cache", bounded-memory
caching with recency tracking. Pattern: hash map + doubly linked list.
Aviation: caching decoded METAR/TAF data, recent flight plan lookups.

## Complexity

| | |
|---|---|
| **Time** | `O(1) for both get and put` |
| **Space** | `O(capacity)` |

## Implementation

=== "Solution"

    ::: algo.linked_lists.lru_cache
        options:
          show_source: true

=== "Tests"

    ```python title="tests/linked_lists/test_lru_cache.py"
    --8<-- "tests/linked_lists/test_lru_cache.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge linked_lists lru_cache`

        Then implement the functions to make all tests pass.
        Use `just study linked_lists` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.linked_lists.lru_cache
            options:
              show_source: true
