---
title: Reverse Bits
---

# Reverse Bits

## Problem

Given a 32-bit unsigned integer, return the integer obtained by
reversing all 32 bits.

## Approach

Bit-by-bit: extract the lowest bit of n, shift result left, OR
the bit in, and shift n right. Repeat 32 times.
Also includes a divide-and-conquer approach that swaps groups of
bits using masks.

## When to Use

Bit-level transformation — "reverse bits", "swap nibbles/bytes",
"bit-reversal permutation" (used in FFT). Divide-and-conquer mask
approach is constant-time. Also: endianness conversion.

## Complexity

| | |
|---|---|
| **Time** | `O(1)  (fixed 32 iterations)` |
| **Space** | `O(1)` |

## Implementation

=== "Solution"

    ::: algo.bit_manipulation.reverse_bits
        options:
          show_source: true

=== "Tests"

    ```python title="tests/bit_manipulation/test_reverse_bits.py"
    --8<-- "tests/bit_manipulation/test_reverse_bits.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge bit_manipulation reverse_bits`

        Then implement the functions to make all tests pass.
        Use `just study bit_manipulation` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.bit_manipulation.reverse_bits
            options:
              show_source: true
