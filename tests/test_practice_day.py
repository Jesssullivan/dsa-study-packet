"""Anti-drift guards for the sheet-11 practice-day conductor."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS))

import catalog  # type: ignore[import-not-found]  # noqa: E402
import practice_day  # type: ignore[import-not-found]  # noqa: E402


def test_catalog_counts_current_core_and_sheets() -> None:
    assert catalog.core_count() == 42
    assert catalog.reference_sheet_count() == 11


def test_day_12_is_full_mock_panel_from_sheet_11() -> None:
    day = practice_day.load_days()[12]
    assert "Full mock panel" in day.focus
    assert "3 cold draws" in day.drills
    assert day.watching == "person"


def test_day_12_render_uses_spaced_repetition_draws() -> None:
    rendered = practice_day.render_day(12)
    assert "Stop condition" in rendered
    assert "just interview" in rendered
    assert "just challenge-done" in rendered
