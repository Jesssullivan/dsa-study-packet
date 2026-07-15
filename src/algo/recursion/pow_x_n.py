"""Pow(x, n) — compute x raised to the power n using fast exponentiation.

Problem:
    Implement pow(x, n), which calculates x raised to the power n
    (i.e., x^n). Handle negative exponents.

Approach:
    my_pow: fast exponentiation (exponentiation by squaring), recursive.
    If n is even, pow(x, n) = pow(x*x, n//2). If n is odd,
    pow(x, n) = x * pow(x, n-1). For negative n, compute pow(1/x, -n).
    my_pow_iterative is the alternate: the same squaring trick unrolled
    into a loop that walks n's bits, using O(1) space instead of O(log n)
    recursion depth.

When to use:
    Any "repeated operation" that can be halved — exponentiation, matrix
    power, modular arithmetic. Foundation of divide-and-conquer thinking.

Complexity:
    Time:  O(log n)
    Space: O(log n) — recursion stack
"""


def my_pow(x: float, n: int) -> float:
    """Compute x raised to the power n via fast exponentiation.

    >>> my_pow(2.0, 10)
    1024.0
    >>> my_pow(2.0, -2)
    0.25
    >>> my_pow(0.0, 0)
    1.0
    """
    if n < 0:
        # inverting the base here means x == 0 raises ZeroDivisionError,
        # matching the real mathematical domain (0 ** negative is undefined)
        return my_pow(1.0 / x, -n)
    if n == 0:
        return 1.0
    if n % 2 == 0:
        # squaring x while halving n keeps total work at O(log n) calls
        return my_pow(x * x, n // 2)
    return x * my_pow(x, n - 1)


# --- iterative alternate: same squaring trick, O(1) space ---
def my_pow_iterative(x: float, n: int) -> float:
    """Compute x raised to the power n via iterative fast exponentiation.

    >>> my_pow_iterative(2.0, 10)
    1024.0
    >>> my_pow_iterative(2.0, -2)
    0.25
    >>> my_pow_iterative(0.0, 0)
    1.0
    """
    if n < 0:
        x = 1.0 / x
        n = -n

    result = 1.0
    while n > 0:
        if n % 2 == 1:
            result *= x
        x *= x
        n //= 2
    return result
