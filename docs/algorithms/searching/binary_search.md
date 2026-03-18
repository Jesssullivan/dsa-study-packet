---
title: Binary Search
---

# Binary Search

## Problem

Given a sorted array of integers and a target value, return the
index of the target if found, otherwise return -1.

## Approach

Both iterative and recursive implementations. Maintain lo/hi
bounds; compute mid = lo + (hi - lo) // 2 to avoid overflow.

### Algorithm Flow

```mermaid
flowchart TD
    A["lo = 0, hi = n - 1"] --> B{"lo <= hi?"}
    B -- No --> C["return -1<br/>(not found)"]
    B -- Yes --> D["mid = lo + (hi - lo) // 2"]
    D --> E{"nums[mid] == target?"}
    E -- Yes --> F["return mid"]
    E -- No --> G{"nums[mid] < target?"}
    G -- Yes --> H["lo = mid + 1<br/>(search right half)"]
    G -- No --> I["hi = mid - 1<br/>(search left half)"]
    H --> B
    I --> B

    style A fill:#7c3aed,color:#fff
    style F fill:#059669,color:#fff
    style C fill:#dc2626,color:#fff
```

## When to Use

Sorted array lookup or any monotonic predicate search — "find target",
"first/last occurrence", "search insert position". Foundation for
bisect-based optimizations. Aviation: altitude/waypoint lookup tables.

## Complexity

| | |
|---|---|
| **Time** | `O(log n)` |
| **Space** | `O(1) iterative, O(log n) recursive (call stack)` |

## Implementation

=== "Solution"

    ::: algo.searching.binary_search
        options:
          show_source: true

=== "Tests"

    ```python title="tests/searching/test_binary_search.py"
    --8<-- "tests/searching/test_binary_search.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge searching binary_search`

        Then implement the functions to make all tests pass.
        Use `just study searching` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.searching.binary_search
            options:
              show_source: true
