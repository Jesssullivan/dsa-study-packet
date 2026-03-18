"""Reverse Bits — reverse the bits of a 32-bit unsigned integer.

Problem:
    Given a 32-bit unsigned integer, return the integer obtained by
    reversing all 32 bits.

Approach:
    Bit-by-bit: extract the lowest bit of n, shift result left, OR
    the bit in, and shift n right. Repeat 32 times.
    Also includes a divide-and-conquer approach that swaps groups of
    bits using masks.

When to use:
    Bit-level transformation — "reverse bits", "swap nibbles/bytes",
    "bit-reversal permutation" (used in FFT). Divide-and-conquer mask
    approach is constant-time. Also: endianness conversion.

Complexity:
    Time:  O(1)  (fixed 32 iterations)
    Space: O(1)
"""

UINT32_BITS = 32


def reverse_bits(n: int) -> int:
    """Reverse the bits of a 32-bit unsigned integer.

    >>> reverse_bits(0b00000010100101000001111010011100)
    964176192
    >>> bin(reverse_bits(0b00000010100101000001111010011100))
    '0b111001011110000010100101000000'
    """
    result = 0
    for _ in range(UINT32_BITS):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def reverse_bits_divide_conquer(n: int) -> int:
    """Reverse bits using divide-and-conquer with bitmasks.

    >>> reverse_bits_divide_conquer(0b00000010100101000001111010011100)
    964176192
    """
    n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    return ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
