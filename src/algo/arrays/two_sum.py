"""Two Sum — find two indices whose values sum to target.

Problem:
    Given an array of integers and a target, return the indices of the
    two numbers that add up to the target. Each input has exactly one
    solution and you may not use the same element twice.

Approach:
    Single-pass hash map. For each element, compute the complement
    (target - current). If the complement is already in the map, return
    both indices. Otherwise store current value -> index.

When to use:
    Any problem asking "find pair with property X" — hash map for O(1) lookups.
    Also: complement problems, two-number sum/difference/product.

Complexity:
    Time:  O(n)
    Space: O(n)
"""

"""Two Sum - find two incidences whose value sums to the target, if possible

Intended usage:
>>> two_sum([<1,2,3,4,...>], target) 

my plan:

I'll create simple, single pass hash map iterating through the input Seq

This relationship is called a compliment

"""

from collections.abc import Sequence


def two_sum(input: Sequence[int], target: int) -> tuple[int, int]:
    hash_map: dict[int, int] = {}

    for i, n in enumerate(input):
        compliment = target - n
        if compliment in hash_map:
            return hash_map[compliment], i

    # if we don't find the compliment:
    msg = "no compliment found"
    raise ValueError(msg)
