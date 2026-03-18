---
title: Min Window Substring
---

# Min Window Substring

## Problem

Given strings s and t, find the minimum window substring of s
that contains all characters of t (including duplicates).
Return "" if no such window exists.

## Approach

Variable-size sliding window with Counter for "need" and "have"
tracking. Expand the right pointer to include characters, shrink
the left pointer to minimize the window once all characters are
satisfied.

## When to Use

Minimum window containing all required elements — "smallest substring
with all chars", "shortest subarray covering set". Expand right to
satisfy, shrink left to minimize. Streaming log/event filtering.

## Complexity

| | |
|---|---|
| **Time** | `O(n) where n = len(s) -- each character visited at most twice` |
| **Space** | `O(k) where k = number of unique characters in t` |

## Implementation

=== "Solution"

    ::: algo.sliding_window.min_window_substring
        options:
          show_source: true

=== "Tests"

    ```python title="tests/sliding_window/test_min_window_substring.py"
    --8<-- "tests/sliding_window/test_min_window_substring.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge sliding_window min_window_substring`

        Then implement the functions to make all tests pass.
        Use `just study sliding_window` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.sliding_window.min_window_substring
            options:
              show_source: true
