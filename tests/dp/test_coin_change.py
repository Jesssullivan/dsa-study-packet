"""Tests for coin change."""

from hypothesis import given
from hypothesis import strategies as st

from algo.dp.coin_change import coin_change


class TestCoinChange:
    def test_basic(self) -> None:
        assert coin_change([1, 5, 10, 25], 30) == 2

    def test_standard_example(self) -> None:
        assert coin_change([1, 2, 5], 11) == 3

    def test_impossible(self) -> None:
        assert coin_change([2], 3) == -1

    def test_zero_amount(self) -> None:
        assert coin_change([1], 0) == 0

    def test_single_coin_exact(self) -> None:
        assert coin_change([3], 9) == 3

    def test_large_denomination(self) -> None:
        assert coin_change([1, 2, 5], 100) == 20


def _coin_change_bfs(coins: list[int], amount: int) -> int:
    """Independent oracle: minimum coins via breadth-first search over sums.

    BFS explores reachable sums level by level; the level at which *amount*
    is first reached is exactly the minimum number of coins. Returns -1 when
    *amount* is unreachable. Uses only positive denominations.
    """
    if amount == 0:
        return 0
    positive = [c for c in coins if c > 0]
    seen = {0}
    frontier = {0}
    steps = 0
    while frontier:
        steps += 1
        nxt: set[int] = set()
        for s in frontier:
            for c in positive:
                t = s + c
                if t == amount:
                    return steps
                if t < amount and t not in seen:
                    seen.add(t)
                    nxt.add(t)
        frontier = nxt
    return -1


@given(
    coins=st.lists(
        st.integers(min_value=1, max_value=20),
        min_size=1,
        max_size=6,
        unique=True,
    ),
    amount=st.integers(min_value=0, max_value=60),
)
def test_coin_change_matches_bfs_oracle(coins: list[int], amount: int) -> None:
    """coin_change must equal an independent BFS shortest-coins oracle."""
    assert coin_change(coins, amount) == _coin_change_bfs(coins, amount)


@given(
    coins=st.lists(
        st.integers(min_value=1, max_value=20),
        min_size=1,
        max_size=6,
        unique=True,
    ),
    amount=st.integers(min_value=0, max_value=60),
)
def test_coin_change_minus_one_iff_unmakeable(coins: list[int], amount: int) -> None:
    """Result is -1 exactly when *amount* is not a non-negative coin combination."""
    reachable = [False] * (amount + 1)
    reachable[0] = True
    for a in range(1, amount + 1):
        reachable[a] = any(c <= a and reachable[a - c] for c in coins)
    assert (coin_change(coins, amount) == -1) == (not reachable[amount])


@given(
    coins=st.lists(
        st.integers(min_value=1, max_value=20),
        min_size=1,
        max_size=6,
        unique=True,
    ),
    amount=st.integers(min_value=1, max_value=60),
)
def test_coin_change_count_bounds(coins: list[int], amount: int) -> None:
    """When makeable: at least ceil(amount/max_coin) and at most *amount* coins."""
    result = coin_change(coins, amount)
    if result != -1:
        assert result * max(coins) >= amount
        assert result <= amount
