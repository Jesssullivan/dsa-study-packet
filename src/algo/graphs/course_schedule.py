"""Determine if all courses can be finished (cycle detection).

Problem:
    There are numCourses courses labeled 0..numCourses-1. Given a list
    of prerequisite pairs [course, prereq], determine if it is possible
    to finish all courses (i.e., the prerequisite graph is a DAG).

Approach:
    BFS topological sort (Kahn's algorithm). If the resulting order
    contains fewer than numCourses nodes, a cycle exists.

When to use:
    Cycle detection in a directed graph — "can all tasks be completed?",
    "is the dependency graph a DAG?". Topological sort that checks for
    leftover nodes. See also: topological_sort for the ordering itself.

Complexity:
    Time:  O(V + E)
    Space: O(V + E)
"""

from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Return True if all courses can be completed.

    >>> can_finish(2, [[1, 0]])
    True
    >>> can_finish(2, [[1, 0], [0, 1]])
    False
    """
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    queue: deque[int] = deque(i for i in range(num_courses) if in_degree[i] == 0)
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited == num_courses


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """Return a valid course order, or [] if impossible.

    >>> find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    [0, 1, 2, 3]
    """
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1

    queue: deque[int] = deque(i for i in range(num_courses) if in_degree[i] == 0)
    order: list[int] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != num_courses:
        return []
    return order
