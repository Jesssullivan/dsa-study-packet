"""String to Integer (atoi) — convert a string to a 32-bit signed integer.

Problem:
    Implement atoi which converts a string to a 32-bit signed integer.
    Handle leading whitespace, an optional +/- sign, consecutive digits,
    and clamp the result to [-2^31, 2^31 - 1].

Approach:
    Linear scan with state tracking: skip whitespace, read optional sign,
    accumulate digits, clamp on overflow. Stop at first non-digit after
    sign processing.

When to use:
    Parsing problems, state machine patterns. Tests attention to edge
    cases (whitespace, signs, overflow, trailing non-digits).

Complexity:
    Time:  O(n)
    Space: O(1)
"""

INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def my_atoi(s: str) -> int:
    """Convert string *s* to a 32-bit signed integer.

    >>> my_atoi("42")
    42
    >>> my_atoi("   -42")
    -42
    >>> my_atoi("4193 with words")
    4193
    >>> my_atoi("-91283472332")
    -2147483648
    """
    n = len(s)
    i = 0

    # skip leading whitespace
    while i < n and s[i] == " ":
        i += 1

    if i == n:
        return 0

    # read optional sign
    sign = 1
    if s[i] in ("+", "-"):
        if s[i] == "-":
            sign = -1
        i += 1

    # accumulate digits
    result = 0
    while i < n and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1

    result *= sign

    # clamp to 32-bit signed range
    if result < INT_MIN:
        return INT_MIN
    if result > INT_MAX:
        return INT_MAX
    return result
