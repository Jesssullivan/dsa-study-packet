---
title: Longest Substring No Repeat
---

# Longest Substring No Repeat

## Problem

Given a string s, find the length of the longest substring
without repeating characters.

## Approach

Sliding window with a dict tracking the last-seen index of each
character. When a duplicate is found within the current window,
jump the left pointer past the previous occurrence.

## When to Use

Longest valid window — "longest substring/subarray without repeats",
"maximum window satisfying constraint". Expand right, contract left
only when the window becomes invalid. Streaming uniqueness checks.

## Complexity

| | |
|---|---|
| **Time** | `O(n) -- single pass through the string` |
| **Space** | `O(min(n, alphabet_size)) for the last-seen dict` |

## Implementation

=== "Solution"

    ::: algo.sliding_window.longest_substring_no_repeat
        options:
          show_source: true

=== "Tests"

    ```python title="tests/sliding_window/test_longest_substring_no_repeat.py"
    --8<-- "tests/sliding_window/test_longest_substring_no_repeat.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge sliding_window longest_substring_no_repeat`

        Then implement the functions to make all tests pass.
        Use `just study sliding_window` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.sliding_window.longest_substring_no_repeat
            options:
              show_source: true
