---
title: Task Scheduler
---

# Task Scheduler

## Problem

Given a list of tasks (characters) and a cooldown period n, find the
minimum number of intervals needed to execute all tasks. The same task
must wait at least n intervals before being executed again.

## Approach

Use a max-heap (negated counts) to always schedule the most frequent
task first. After executing a task, place it in a cooldown queue with
the time it becomes available. When that time arrives, push it back
onto the heap.

## When to Use

Scheduling with cooldown constraints — "minimum time to complete all
tasks with cooldown", "CPU scheduling", "rate-limited job execution".
Max-heap ensures the most frequent task is scheduled first.
Aviation: runway scheduling with minimum separation times.

## Complexity

| | |
|---|---|
| **Time** | `O(t) where t = total intervals (bounded by len(tasks) * (n+1))` |
| **Space** | `O(1) — at most 26 distinct task types` |

## Implementation

=== "Solution"

    ::: algo.heaps.task_scheduler
        options:
          show_source: true

=== "Tests"

    ```python title="tests/heaps/test_task_scheduler.py"
    --8<-- "tests/heaps/test_task_scheduler.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge heaps task_scheduler`

        Then implement the functions to make all tests pass.
        Use `just study heaps` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.heaps.task_scheduler
            options:
              show_source: true
