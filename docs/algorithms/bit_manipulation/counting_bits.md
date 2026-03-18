---
title: Counting Bits
---

# Counting Bits

## Problem

Given an integer n, return an array of length n+1 where the i-th
element is the number of 1-bits in the binary representation of i.

## Approach

DP recurrence: dp[i] = dp[i >> 1] + (i & 1).
The number of set bits in i equals the bits in i//2 plus whether
the least significant bit is set.

## When to Use

DP on binary representation — "count set bits for 0..n", "Hamming
weight table". Recurrence dp[i] = dp[i>>1] + (i&1) builds on
previously computed values. Also: popcount lookup tables.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(n)` |

## Implementation

=== "Solution"

    ::: algo.bit_manipulation.counting_bits
        options:
          show_source: true

=== "Tests"

    ```python title="tests/bit_manipulation/test_counting_bits.py"
    --8<-- "tests/bit_manipulation/test_counting_bits.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge bit_manipulation counting_bits`

        Then implement the functions to make all tests pass.
        Use `just study bit_manipulation` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.bit_manipulation.counting_bits
            options:
              show_source: true
