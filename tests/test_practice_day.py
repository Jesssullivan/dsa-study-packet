"""Anti-drift guards for the sheet-11 practice-day conductor."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS))

import catalog  # type: ignore[import-not-found]  # noqa: E402
import practice_day  # type: ignore[import-not-found]  # noqa: E402


def test_catalog_counts_current_core_and_sheets() -> None:
    assert catalog.core_count() == 43
    assert catalog.reference_sheet_count() == 11


def test_day_12_is_full_mock_panel_from_sheet_11() -> None:
    day = practice_day.load_days()[12]
    assert "Observed live-coding mock" in day.focus
    assert "3 cold draws" in day.drills
    assert day.watching == "person"


def test_command_cell_draws_three_real_problems() -> None:
    draws = practice_day.cold_draws(practice_day.load_days()[10])

    assert len(draws) == 3
    assert all(topic != "just" for topic, _, _ in draws)


def test_day_12_render_uses_spaced_repetition_draws() -> None:
    rendered = practice_day.render_day(12)
    assert "Stop condition" in rendered
    assert "just practice-start clarp" in rendered
    assert "just practice-next" in rendered
    assert "just practice-test" in rendered
    assert "just practice-finish" in rendered
    assert "just challenge-done" not in rendered


def test_rest_days_do_not_draw_or_start_reps() -> None:
    for day_number in (7, 14):
        day = practice_day.load_days()[day_number]
        rendered = practice_day.render_day(day_number)

        assert practice_day.cold_draws(day) == []
        assert "No draws today" in rendered
        assert "just practice-" not in rendered
        assert "never auto-draw" in rendered
        assert "Four-hour block" not in rendered
        assert "Editor reps" not in rendered
        assert "log the reps" not in rendered
        assert "run this block" not in rendered
        assert "take the scheduled rest, then stop" in rendered
