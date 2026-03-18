---
title: Trapping Rain Water
---

# Trapping Rain Water

## Problem

Given n non-negative integers representing an elevation map where
the width of each bar is 1, compute how much water can be trapped
after raining.

## Approach

Two pointers from both ends. Track left_max and right_max. Move
the pointer on the side with the smaller max inward. Water at each
position is (current_side_max - height[pointer]).

## When to Use

Bounded accumulation between barriers — water trapping, histogram
area, or any problem where capacity at each position depends on the
max values to its left and right. Also: elevation profile analysis.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.two_pointers.trapping_rain_water
        options:
          show_source: true

=== "Tests"

    ```python title="tests/two_pointers/test_trapping_rain_water.py"
    --8<-- "tests/two_pointers/test_trapping_rain_water.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge two_pointers trapping_rain_water`

        Then implement the functions to make all tests pass.
        Use `just study two_pointers` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.two_pointers.trapping_rain_water
            options:
              show_source: true
