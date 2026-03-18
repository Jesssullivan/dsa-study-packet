---
title: Course Schedule
---

# Course Schedule

## Problem

There are numCourses courses labeled 0..numCourses-1. Given a list
of prerequisite pairs [course, prereq], determine if it is possible
to finish all courses (i.e., the prerequisite graph is a DAG).

## Approach

BFS topological sort (Kahn's algorithm). If the resulting order
contains fewer than numCourses nodes, a cycle exists.

## When to Use

Cycle detection in a directed graph — "can all tasks be completed?",
"is the dependency graph a DAG?". Topological sort that checks for
leftover nodes. See also: topological_sort for the ordering itself.

## Complexity

| | |
|---|---|
| **Time** | `O(V + E)` |
| **Space** | `O(V + E)` |

## Implementation

=== "Solution"

    ::: algo.graphs.course_schedule
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_course_schedule.py"
    --8<-- "tests/graphs/test_course_schedule.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs course_schedule`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.course_schedule
            options:
              show_source: true
