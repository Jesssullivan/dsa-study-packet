"""Tower of Hanoi — move n disks between pegs.

Problem:
    Move n disks from a source peg to a target peg using an auxiliary
    peg. Only one disk may be moved at a time, and a larger disk may
    never be placed on top of a smaller one.

Approach:
    Classic recursion: move n-1 disks from source to auxiliary, move
    the largest disk from source to target, then move n-1 disks from
    auxiliary to target. Base case: n == 0 (do nothing).

When to use:
    Pure recursive decomposition — the canonical example. Demonstrates
    how recursion breaks problems into identical sub-problems. Also:
    understanding call stack depth and O(2^n) explosion.

Complexity:
    Time:  O(2^n) — number of moves
    Space: O(n) — recursion depth
"""


def tower_of_hanoi(
    n: int,
    source: str = "A",
    target: str = "C",
    auxiliary: str = "B",
) -> list[tuple[str, str]]:
    """Solve Tower of Hanoi for *n* disks, returning moves as (from, to) tuples.

    >>> tower_of_hanoi(1)
    [('A', 'C')]
    >>> tower_of_hanoi(2)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    """
    moves: list[tuple[str, str]] = []

    def solve(disks: int, src: str, tgt: str, aux: str) -> None:
        if disks == 0:
            return
        solve(disks - 1, src, aux, tgt)
        moves.append((src, tgt))
        solve(disks - 1, aux, tgt, src)

    solve(n, source, target, auxiliary)
    return moves
