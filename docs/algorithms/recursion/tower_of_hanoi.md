---
title: Tower Of Hanoi
---

# Tower Of Hanoi

## Problem

Move n disks from a source peg to a target peg using an auxiliary
peg. Only one disk may be moved at a time, and a larger disk may
never be placed on top of a smaller one.

## Approach

Classic recursion: move n-1 disks from source to auxiliary, move
the largest disk from source to target, then move n-1 disks from
auxiliary to target. Base case: n == 0 (do nothing).

## When to Use

Pure recursive decomposition — the canonical example. Demonstrates
how recursion breaks problems into identical sub-problems. Also:
understanding call stack depth and O(2^n) explosion.

## Complexity

| | |
|---|---|
| **Time** | `O(2^n) — number of moves` |
| **Space** | `O(n) — recursion depth` |

## Implementation

=== "Solution"

    ::: algo.recursion.tower_of_hanoi
        options:
          show_source: true

=== "Tests"

    ```python title="tests/recursion/test_tower_of_hanoi.py"
    --8<-- "tests/recursion/test_tower_of_hanoi.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge recursion tower_of_hanoi`

        Then implement the functions to make all tests pass.
        Use `just study recursion` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.recursion.tower_of_hanoi
            options:
              show_source: true
