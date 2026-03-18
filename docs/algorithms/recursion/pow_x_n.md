---
title: Pow X N
---

# Pow X N

## Problem

Implement pow(x, n), which calculates x raised to the power n
(i.e., x^n). Handle negative exponents.

## Approach

Fast exponentiation (exponentiation by squaring). If n is even,
pow(x, n) = pow(x*x, n//2). If n is odd, pow(x, n) = x * pow(x, n-1).
For negative n, compute pow(1/x, -n).

## When to Use

Any "repeated operation" that can be halved — exponentiation, matrix
power, modular arithmetic. Foundation of divide-and-conquer thinking.

## Complexity

| | |
|---|---|
| **Time** | `O(log n)` |
| **Space** | `O(log n) — recursion stack` |

## Implementation

=== "Solution"

    ::: algo.recursion.pow_x_n
        options:
          show_source: true

=== "Tests"

    ```python title="tests/recursion/test_pow_x_n.py"
    --8<-- "tests/recursion/test_pow_x_n.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge recursion pow_x_n`

        Then implement the functions to make all tests pass.
        Use `just study recursion` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.recursion.pow_x_n
            options:
              show_source: true
