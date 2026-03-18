"""Pow(x, n) — compute x raised to the power n using fast exponentiation.

Problem:
    Implement pow(x, n), which calculates x raised to the power n
    (i.e., x^n). Handle negative exponents.

Approach:
    Fast exponentiation (exponentiation by squaring). If n is even,
    pow(x, n) = pow(x*x, n//2). If n is odd, pow(x, n) = x * pow(x, n-1).
    For negative n, compute pow(1/x, -n).

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
        return my_pow(1.0 / x, -n)
    if n == 0:
        return 1.0
    if n % 2 == 0:
        return my_pow(x * x, n // 2)
    return x * my_pow(x, n - 1)
