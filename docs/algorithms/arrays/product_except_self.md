---
title: Product Except Self
---

# Product Except Self

## Problem

Given an integer array, return an array where each element is the
product of all other elements. Do not use division.

## Approach

Two-pass prefix/suffix products. First pass builds prefix products
left-to-right, second pass multiplies in suffix products right-to-left.
Uses the output array itself to store prefix, then folds in suffix
with a running variable.

## When to Use

Prefix/suffix accumulation without division — product, sum, or any
associative operation where you need "everything except index i".
Also: running totals, range queries without a segment tree.

## Complexity

| | |
|---|---|
| **Time** | `O(n)` |
| **Space** | `O(1)  (output array not counted)` |

## Implementation

=== "Solution"

    ::: algo.arrays.product_except_self
        options:
          show_source: true

=== "Tests"

    ```python title="tests/arrays/test_product_except_self.py"
    --8<-- "tests/arrays/test_product_except_self.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge arrays product_except_self`

        Then implement the functions to make all tests pass.
        Use `just study arrays` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.arrays.product_except_self
            options:
              show_source: true
