"""Regression tests for topic-interleaved spaced-repetition draws."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS))

import study_schedule  # type: ignore[import-not-found]  # noqa: E402


def test_empty_queue_interleaves_topics_instead_of_front_loading_arrays(
    tmp_path: Path,
) -> None:
    missing_progress = tmp_path / "progress.md"

    ranked = study_schedule.ranked_queue(missing_progress)

    expected_topics = list(study_schedule.CORE_42)[:5]
    assert [topic for _, topic, _ in ranked[:5]] == expected_topics
    assert all(urgency == study_schedule._NEVER for urgency, _, _ in ranked)
    assert ranked == study_schedule.ranked_queue(missing_progress)


def test_higher_urgency_bucket_finishes_before_lower_bucket(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        study_schedule,
        "CORE_42",
        {
            "arrays": ["arrays_old", "arrays_recent"],
            "trees": ["trees_old", "trees_recent"],
        },
    )
    monkeypatch.setattr(
        study_schedule,
        "_days_since",
        lambda label: {"old": 30, "recent": 2}[label],
    )
    progress = tmp_path / "progress.md"
    progress.write_text(
        "\n".join(
            [
                "- [x] arrays/arrays_old: old",
                "- [x] arrays/arrays_recent recent",
                "- [x] trees/trees_old \u2014 old",
                "- [x] trees/trees_recent: recent",
            ]
        )
    )

    assert study_schedule.ranked_queue(progress) == [
        (30, "arrays", "arrays_old"),
        (30, "trees", "trees_old"),
        (2, "arrays", "arrays_recent"),
        (2, "trees", "trees_recent"),
    ]


def test_equal_urgency_round_robin_preserves_problem_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        study_schedule,
        "CORE_42",
        {
            "arrays": ["a1", "a2", "a3"],
            "trees": ["t1", "t2"],
            "graphs": ["g1"],
        },
    )

    assert study_schedule.ranked_queue(tmp_path / "missing.md") == [
        (study_schedule._NEVER, "arrays", "a1"),
        (study_schedule._NEVER, "trees", "t1"),
        (study_schedule._NEVER, "graphs", "g1"),
        (study_schedule._NEVER, "arrays", "a2"),
        (study_schedule._NEVER, "trees", "t2"),
        (study_schedule._NEVER, "arrays", "a3"),
    ]


def test_formatted_draw_uses_isolated_editor_entry_point(tmp_path: Path) -> None:
    rendered = study_schedule.format_queue(1, tmp_path / "missing.md")

    assert "just practice-start clarp arrays two_sum" in rendered
    assert "just interview" not in rendered
