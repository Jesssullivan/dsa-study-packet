"""Jump Game — can you reach the last index? / minimum jumps.

Problem (I):
    Given an array where each element is the max jump length from that
    position, determine if you can reach the last index.

Problem (II):
    Return the minimum number of jumps to reach the last index.
    Assume the answer always exists.

Approach:
    I:  Track the farthest reachable index. If current index exceeds
        farthest, return False.
    II: BFS-style greedy. Track current window end and farthest
        reachable. Increment jumps when reaching the window end.

When to use:
    Reachability analysis — "can you reach the end?", "minimum hops to
    reach target". Track farthest reachable index greedily.
    Also: network hop-count analysis, coverage verification.

Complexity:
    Time:  O(n)
    Space: O(1)
"""

from collections.abc import Sequence


def can_jump(nums: Sequence[int]) -> bool:
    """Return True if the last index is reachable.

    >>> can_jump([2, 3, 1, 1, 4])
    True
    >>> can_jump([3, 2, 1, 0, 4])
    False
    """
    farthest = 0
    for i, n in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + n)
    return True


def jump_game_ii(nums: Sequence[int]) -> int:
    """Return the minimum number of jumps to reach the last index.

    >>> jump_game_ii([2, 3, 1, 1, 4])
    2
    >>> jump_game_ii([1])
    0
    """
    if len(nums) <= 1:
        return 0

    jumps = 0
    cur_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= len(nums) - 1:
                break

    return jumps
