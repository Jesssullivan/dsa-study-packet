"""Hypothesis property-based testing patterns — the tutorial.

This test file IS the tutorial.  Each section teaches one Hypothesis
concept through runnable, commented code.  The systems-under-test
(``SortedList`` and ``BoundedCounter``) live in
``concepts.hypothesis_patterns``.

Sections
--------
1. ``@composite`` strategy — build complex test data step by step
2. ``RuleBasedStateMachine`` — stateful testing with an oracle
3. ``@example`` — reproduce known edge cases deterministically
4. ``@settings`` — control test intensity
5. ``st.builds`` — auto-generate dataclass instances
6. ``st.recursive`` — generate nested/tree-like structures

References
----------
* Hypothesis docs   — https://hypothesis.readthedocs.io/en/latest/
* Stateful testing  — https://hypothesis.readthedocs.io/en/latest/stateful.html
* Composite         — https://hypothesis.readthedocs.io/en/latest/data.html#composite-strategies
* Settings          — https://hypothesis.readthedocs.io/en/latest/settings.html
"""

import pytest
from hypothesis import example, given, settings
from hypothesis import strategies as st
from hypothesis.stateful import (
    RuleBasedStateMachine,
    invariant,
    rule,
    run_state_machine_as_test,
)

from concepts.hypothesis_patterns import BoundedCounter, SortedList

# =========================================================================== #
# 1. @composite — build complex test data step by step
# =========================================================================== #
# ``@st.composite`` lets you write a strategy as a regular function.
# Inside, you call ``draw()`` to pull values from other strategies.
# This is perfect when your test data has inter-dependent constraints
# (e.g., "a SortedList that already contains N random elements").
#
# The function receives a special ``draw`` callable as its first
# argument — it's injected by Hypothesis, NOT something you provide.
# https://hypothesis.readthedocs.io/en/latest/data.html#composite-strategies


@st.composite
def sorted_list_with_elements(
    draw: st.DrawFn,
    *,
    min_elements: int = 0,
    max_elements: int = 20,
) -> SortedList:
    """Strategy that builds a SortedList pre-filled with random ints.

    Usage in a test::

        @given(sl=sorted_list_with_elements(min_elements=1))
        def test_something(sl: SortedList) -> None: ...
    """
    # First, draw a list of integers.
    elements = draw(
        st.lists(
            st.integers(min_value=-100, max_value=100),
            min_size=min_elements,
            max_size=max_elements,
        )
    )
    # Then imperatively build the SortedList.
    sl = SortedList()
    for elem in elements:
        sl.insert(elem)
    return sl


class TestCompositeStrategy:
    """Demonstrate ``@composite`` with SortedList."""

    @given(sl=sorted_list_with_elements(min_elements=1))
    def test_composite_list_is_sorted(self, sl: SortedList) -> None:
        """Any SortedList produced by the composite strategy is sorted."""
        data = sl.to_list()
        assert data == sorted(data)

    @given(sl=sorted_list_with_elements(), val=st.integers(-100, 100))
    def test_insert_preserves_sorted(self, sl: SortedList, val: int) -> None:
        """Inserting into a composite-built list preserves sort order."""
        sl.insert(val)
        data = sl.to_list()
        assert data == sorted(data)


# =========================================================================== #
# 2. RuleBasedStateMachine — stateful testing with an oracle
# =========================================================================== #
# Stateful testing explores *sequences* of operations.  Hypothesis
# generates random method-call sequences and checks that invariants
# hold after every step.
#
# The "oracle" pattern: maintain a *reference model* (here, a plain
# sorted Python list) alongside the system-under-test and assert that
# they agree after every operation.
#
# Key components:
#   - ``rule()``: a possible action (with strategies for arguments)
#   - ``@invariant``: checked after EVERY rule execution
#   - ``run_state_machine_as_test()``: run the machine from a pytest test
# https://hypothesis.readthedocs.io/en/latest/stateful.html


class SortedListMachine(RuleBasedStateMachine):
    """Stateful test: SortedList vs sorted() as oracle."""

    def __init__(self) -> None:
        super().__init__()
        # System-under-test.
        self.sl = SortedList()
        # Reference oracle — a plain Python list we keep sorted manually.
        self.oracle: list[int] = []

    @rule(val=st.integers(-50, 50))
    def add_element(self, val: int) -> None:
        """Insert an element into both the SUT and oracle."""
        self.sl.insert(val)
        # For the oracle, just append and sort — simple but correct.
        self.oracle.append(val)
        self.oracle.sort()

    @rule(val=st.integers(-50, 50))
    def remove_element(self, val: int) -> None:
        """Attempt to remove an element from both SUT and oracle.

        If the element doesn't exist, both should raise ValueError.
        """
        if val in self.oracle:
            self.sl.remove(val)
            self.oracle.remove(val)
        else:
            with pytest.raises(ValueError):
                self.sl.remove(val)

    @invariant()
    def check_sorted_invariant(self) -> None:
        """After every rule, the SUT list must match the oracle."""
        assert self.sl.to_list() == self.oracle


# Run the state machine as a standard pytest test.
# ``run_state_machine_as_test`` generates random sequences of rule
# calls and checks all invariants after each step.


def test_sorted_list_state_machine() -> None:
    run_state_machine_as_test(SortedListMachine)


# =========================================================================== #
# 3. @example — reproduce known edge cases deterministically
# =========================================================================== #
# ``@example`` forces Hypothesis to run your test with a specific input
# in addition to the random ones.  This is useful for:
#   - Regression tests for bugs you've found
#   - Known tricky edge cases (empty inputs, boundary values)
# https://hypothesis.readthedocs.io/en/latest/reproducing.html


class TestExampleDecorator:
    """Using ``@example`` to pin specific inputs."""

    @given(val=st.integers(-100, 100))
    @example(val=0)  # Edge case: zero
    @example(val=-100)  # Edge case: lower bound
    @example(val=100)  # Edge case: upper bound
    def test_insert_then_search_finds_it(self, val: int) -> None:
        """After inserting a value, search must find it."""
        sl = SortedList()
        sl.insert(val)
        assert sl.search(val)

    def test_remove_from_empty_raises(self) -> None:
        """Known edge case: removing from an empty SortedList."""
        sl = SortedList()
        with pytest.raises(ValueError):
            sl.remove(42)


# =========================================================================== #
# 4. @settings — control test intensity
# =========================================================================== #
# ``@settings`` lets you tune Hypothesis parameters per-test:
#   - ``max_examples``: how many random inputs to generate
#   - ``deadline``: max time per example in milliseconds (None=no limit)
#   - ``suppress_health_check``: skip health checks that don't apply
#
# You can also define named profiles for CI vs. local dev.
# https://hypothesis.readthedocs.io/en/latest/settings.html


class TestSettingsProfiles:
    """Demonstrate ``@settings`` for controlling test intensity."""

    @settings(max_examples=500)
    @given(sl=sorted_list_with_elements(), val=st.integers(-100, 100))
    def test_high_intensity_insert(self, sl: SortedList, val: int) -> None:
        """Run 500 examples instead of the default for extra confidence."""
        sl.insert(val)
        data = sl.to_list()
        assert data == sorted(data)

    @settings(max_examples=10)
    @given(sl=sorted_list_with_elements())
    def test_low_intensity_smoke(self, sl: SortedList) -> None:
        """Quick smoke test — only 10 examples."""
        assert sl.to_list() == sorted(sl.to_list())


# =========================================================================== #
# 5. st.builds — auto-generate dataclass instances
# =========================================================================== #
# ``st.builds`` calls a constructor with strategy-generated arguments.
# For dataclasses, this means you provide a strategy for each field
# and Hypothesis fills them in.
#
# This is much cleaner than writing ``@composite`` when the
# construction is just "call __init__ with random args".
# https://hypothesis.readthedocs.io/en/latest/data.html#st-builds


# Strategy that generates valid BoundedCounter instances.
# We ensure min_val <= max_val by drawing min first, then drawing max
# from [min, min+100].
@st.composite
def bounded_counters(draw: st.DrawFn) -> BoundedCounter:
    """Strategy that generates valid BoundedCounter instances."""
    min_val = draw(st.integers(min_value=-50, max_value=50))
    max_val = draw(st.integers(min_value=min_val, max_value=min_val + 100))
    return BoundedCounter(min_val=min_val, max_val=max_val)


class TestStBuilds:
    """Demonstrate ``st.builds`` / ``@composite`` for dataclass instances."""

    @given(bc=bounded_counters())
    def test_counter_starts_at_min(self, bc: BoundedCounter) -> None:
        """Counter always starts at min_val."""
        assert bc.value == bc.min_val

    @given(bc=bounded_counters())
    def test_increment_then_decrement_roundtrips(self, bc: BoundedCounter) -> None:
        """If there's room to increment, inc then dec returns to start."""
        if bc.min_val < bc.max_val:
            start = bc.value
            bc.increment()
            bc.decrement()
            assert bc.value == start

    @given(bc=bounded_counters())
    def test_cannot_exceed_max(self, bc: BoundedCounter) -> None:
        """Incrementing to max and then once more must raise."""
        # Fill the counter to max.
        while bc.value < bc.max_val:
            bc.increment()
        assert bc.value == bc.max_val
        with pytest.raises(ValueError):
            bc.increment()

    @given(bc=bounded_counters())
    def test_cannot_go_below_min(self, bc: BoundedCounter) -> None:
        """Counter starts at min, so decrementing immediately must raise."""
        with pytest.raises(ValueError):
            bc.decrement()


# =========================================================================== #
# 6. st.recursive — generate nested / tree-like structures
# =========================================================================== #
# ``st.recursive`` builds recursive data structures.  You provide:
#   - ``base``: strategy for leaf values
#   - ``extend``: function that takes a strategy and wraps it one level
#
# Hypothesis controls the recursion depth automatically.
# https://hypothesis.readthedocs.io/en/latest/data.html#recursive-data


# Define a recursive JSON-like structure type for clarity.
type JsonLike = int | str | list[JsonLike] | dict[str, JsonLike]

# Strategy: generate tree-like nested dicts/lists of primitives.
json_like: st.SearchStrategy[JsonLike] = st.recursive(
    # Base case: leaf nodes are ints or short strings.
    base=st.one_of(st.integers(-100, 100), st.text(max_size=10)),
    # Extend: wrap leaves in lists or dicts to add nesting.
    extend=lambda inner: st.one_of(
        st.lists(inner, max_size=5),
        st.dictionaries(
            keys=st.text(min_size=1, max_size=5),
            values=inner,
            max_size=5,
        ),
    ),
    # Max nesting depth.
    max_leaves=30,
)


class TestRecursiveStructures:
    """Demonstrate ``st.recursive`` for tree-like data."""

    @given(data=json_like)
    def test_json_like_is_valid_type(self, data: JsonLike) -> None:
        """Every generated value is one of the allowed types."""
        assert isinstance(data, int | str | list | dict)

    @given(data=json_like)
    def test_can_count_leaves(self, data: JsonLike) -> None:
        """We can recursively traverse any generated structure."""

        def count_leaves(node: JsonLike) -> int:
            """Count leaf (int/str) nodes in a nested structure."""
            if isinstance(node, int | str):
                return 1
            if isinstance(node, list):
                return sum(count_leaves(child) for child in node)
            # dict
            return sum(count_leaves(v) for v in node.values())

        # Should not raise — the structure is always well-formed.
        result = count_leaves(data)
        assert result >= 0
