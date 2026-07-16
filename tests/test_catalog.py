"""Tests for exact practice-target discovery."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import catalog  # type: ignore[import-not-found]  # noqa: E402
from core42 import (  # type: ignore[import-not-found]  # noqa: E402
    CORE_42,
    PRACTICE_TARGETS,
)


def _slugs(query: str) -> list[str]:
    return [entry.slug for entry in catalog.matching_entries(query)]


def test_full_catalog_is_the_practice_registry_and_marks_core_status() -> None:
    entries = catalog.catalog_entries()
    core = {
        (topic, problem) for topic, problems in CORE_42.items() for problem in problems
    }

    assert len(entries) == 72
    assert {entry.key for entry in entries} == set(PRACTICE_TARGETS)
    assert {entry.key for entry in entries if entry.core} == core
    assert all(entry.summary for entry in entries)
    assert all(
        "\N{EM DASH}" not in entry.summary and "\N{EN DASH}" not in entry.summary
        for entry in entries
    )

    rendered = catalog.render_catalog()
    assert "Editor-practice targets: 72 problems" in rendered
    assert "- arrays/two_sum | Core |" in rendered
    assert "- math/is_prime | Extra |" in rendered


@pytest.mark.parametrize("query", ["2 sum", "two-sum", "two_sum"])
def test_two_sum_aliases_return_one_exact_pair(query: str) -> None:
    assert _slugs(query) == ["arrays/two_sum"]


def test_specific_and_bare_anagram_aliases_preserve_ambiguity() -> None:
    assert _slugs("valid anagram") == ["strings/valid_anagram"]
    assert _slugs("group anagrams") == ["arrays/group_anagrams"]
    assert _slugs("anagram") == [
        "strings/valid_anagram",
        "arrays/group_anagrams",
    ]


def test_multi_query_preserves_request_order_and_every_ambiguous_meaning() -> None:
    rendered = catalog.render_query("anagram, 2 sum and prime")
    expected = [
        "CHOOSE: strings/valid_anagram",
        "CHOOSE: arrays/group_anagrams",
        "MATCH: arrays/two_sum",
        "CHOOSE: math/is_prime",
        "CHOOSE: math/sieve_of_eratosthenes",
    ]

    positions = [rendered.index(value) for value in expected]
    assert positions == sorted(positions)
    assert rendered.count("QUERY:") == 3
    assert rendered.count("STATE: CHOOSE") == 1


def test_conversational_request_prefix_does_not_become_a_fake_problem() -> None:
    groups = catalog.search_catalog(
        "lets work on some basics, anagram, 2 sum and prime"
    )

    assert [group.query for group in groups] == ["anagram", "2 sum", "prime"]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("let's practice two sum", ["two sum"]),
        ("I want to practice prime", ["prime"]),
        ("practice anagram, 2 sum", ["anagram", "2 sum"]),
    ],
)
def test_conversational_filler_is_removed_from_each_phrase(
    query: str, expected: list[str]
) -> None:
    assert [group.query for group in catalog.search_catalog(query)] == expected


def test_ready_guidance_preserves_the_already_selected_mode() -> None:
    rendered = catalog.render_query("two sum")

    assert "practice-start comments" not in rendered
    assert "STATE: READY" in rendered
    assert "START: arrays/two_sum" in rendered
    assert "QUEUE:" not in rendered
    assert "start START with the selected mode" in rendered


def test_query_is_ready_only_when_every_phrase_is_an_exact_match() -> None:
    rendered = catalog.render_query("valid anagram and two-sum and is prime")

    assert rendered.count("STATE: READY") == 1
    assert "STATE: CHOOSE" not in rendered
    assert rendered.count("MATCH:") == 3
    assert rendered.count("START:") == 1
    assert "START: strings/valid_anagram" in rendered
    assert rendered.splitlines().count("QUEUE: arrays/two_sum") == 1
    assert rendered.splitlines().count("QUEUE: math/is_prime") == 1
    assert rendered.count("NEXT:") == 1


def test_prime_query_distinguishes_one_check_from_a_prime_table() -> None:
    entries = catalog.matching_entries("prime")

    assert [entry.slug for entry in entries] == [
        "math/is_prime",
        "math/sieve_of_eratosthenes",
    ]
    assert "return whether n is prime" in entries[0].summary
    assert "return every prime number" in entries[1].summary


@pytest.mark.parametrize("query", ["prime", "prime number", "prime numbers"])
def test_ambiguous_prime_phrases_never_silently_choose_a_rep(query: str) -> None:
    rendered = catalog.render_query(query)

    assert "STATE: CHOOSE" in rendered
    assert "CHOOSE: math/is_prime" in rendered
    assert "CHOOSE: math/sieve_of_eratosthenes" in rendered
    assert "START:" not in rendered


@pytest.mark.parametrize(
    "query",
    [
        "check if a number is prime",
        "check whether a number is prime",
        "is number prime",
        "primality",
    ],
)
def test_single_number_prime_phrases_choose_the_predicate(query: str) -> None:
    rendered = catalog.render_query(query)

    assert "STATE: READY" in rendered
    assert "START: math/is_prime" in rendered
    assert "math/sieve_of_eratosthenes" not in rendered


@pytest.mark.parametrize("query", ["plime", "unknown puzzle"])
def test_unknown_queries_have_a_distinct_retry_state(query: str) -> None:
    rendered = catalog.render_query(query)

    assert "STATE: NOT_FOUND" in rendered
    assert "STATE: CHOOSE" not in rendered
    assert "CHOOSE:" not in rendered
    assert "START:" not in rendered
    assert "NEXT: revise each unmatched name" in rendered


def test_catalog_state_always_has_the_action_its_state_promises() -> None:
    ready = catalog.render_query("valid anagram, two sum")
    choose = catalog.render_query("anagram")
    not_found = catalog.render_query("plime")

    assert ready.count("START:") == 1
    assert "QUEUE: arrays/two_sum" in ready
    assert "CHOOSE:" in choose
    assert "START:" not in choose
    assert "STATE: NOT_FOUND" in not_found
    assert "START:" not in not_found


def test_unknown_pair_guidance_uses_matches_and_next_not_paths() -> None:
    rendered = catalog.selection_error("strings", "anagram")

    assert "unknown practice target: strings/anagram" in rendered
    assert "MATCH: strings/valid_anagram" in rendered
    assert "MATCH: arrays/group_anagrams" in rendered
    assert 'NEXT: run `just catalog "anagram"`' in rendered
    assert "tests/" not in rendered
    assert "src/" not in rendered
