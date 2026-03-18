---
title: Jump Game
---

# Jump Game

## Approach

I:  Track the farthest reachable index. If current index exceeds
    farthest, return False.
II: BFS-style greedy. Track current window end and farthest
    reachable. Increment jumps when reaching the window end.

## When to Use

Reachability analysis — "can you reach the end?", "minimum hops to
reach target". Track farthest reachable index greedily.
Also: network hop-count analysis, coverage verification.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.greedy.jump_game
        options:
          show_source: true

=== "Tests"

    ```python title="tests/greedy/test_jump_game.py"
    --8<-- "tests/greedy/test_jump_game.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge greedy jump_game`

        Then implement the functions to make all tests pass.
        Use `just study greedy` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.greedy.jump_game
            options:
              show_source: true
