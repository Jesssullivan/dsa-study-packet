"""Print one sheet-11 practice day as an executable block."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from catalog import core_count, reference_sheet_count
from study_schedule import _NEVER, ranked_queue

ROOT = Path(__file__).resolve().parent.parent
RAMP = ROOT / "reference-sheets" / "11-14-day-whiteboard-ramp.md"


@dataclass(frozen=True)
class PracticeDay:
    day: int
    focus: str
    drills: str
    sheets: str
    watching: str


def _clean_md(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    text = text.replace("<br/>", " / ").replace("<br>", " / ")
    return re.sub(r"\s+", " ", text).strip()


def _raw_table_cells(line: str) -> list[str]:
    if not line.startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_cells(line: str) -> list[str]:
    return [_clean_md(cell) for cell in _raw_table_cells(line)]


def load_days(path: Path = RAMP) -> dict[int, PracticeDay]:
    days: dict[int, PracticeDay] = {}
    for line in path.read_text().splitlines():
        raw_cells = _raw_table_cells(line)
        cells = [_clean_md(cell) for cell in raw_cells]
        if len(cells) < 5:
            continue
        day_match = re.fullmatch(r"\d+", cells[0])
        if day_match is None:
            continue
        day = int(cells[0])
        days[day] = PracticeDay(
            day=day,
            focus=cells[1],
            drills=raw_cells[2],
            sheets=cells[3],
            watching=cells[4],
        )
    return days


def load_allocation(path: Path = RAMP) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    in_section = False
    for line in path.read_text().splitlines():
        if line.startswith("## Four-hour allocation"):
            in_section = True
            continue
        if not in_section:
            continue
        cells = _table_cells(line)
        if len(cells) != 2:
            if rows:
                break
            continue
        if cells[0].lower() == "time" or set(cells[0]) == {"-"}:
            continue
        rows.append((cells[0], cells[1]))
    return rows


def _literal_drills(day: PracticeDay) -> list[tuple[str, str]]:
    drills: list[tuple[str, str]] = []
    for topic, problem in re.findall(r"`([a-z_]+)\s+([a-z_]+)`", day.drills):
        drills.append((topic, problem))
    return drills


def cold_draws(day: PracticeDay) -> list[tuple[str, str, str]]:
    """Return concrete cold draw commands for a practice day."""
    literal = _literal_drills(day)
    if literal:
        return [(topic, problem, "sheet 11") for topic, problem in literal]

    count_match = re.search(r"(\d+)\s+cold draws?", day.drills)
    count = int(count_match.group(1)) if count_match else 1
    draws: list[tuple[str, str, str]] = []
    for urgency, topic, problem in ranked_queue()[:count]:
        tag = "new" if urgency == _NEVER else f"{urgency}d since review"
        draws.append((topic, problem, tag))
    return draws


def render_day(day_number: int) -> str:
    days = load_days()
    if day_number not in days:
        valid = ", ".join(str(day) for day in sorted(days))
        raise SystemExit(f"unknown practice day {day_number}; valid days: {valid}")

    day = days[day_number]
    lines = [
        f"# Practice Day {day.day} — {date.today().isoformat()}",
        "",
        "Stop condition: run this block, log the reps, then stop building.",
        "",
        f"- Catalog now: {core_count()} core drills, {reference_sheet_count()} reference sheets",
        f"- Focus: {day.focus}",
        f"- Observer: {day.watching}",
        f"- Sheets open: {day.sheets}",
        "",
        "## Four-hour block",
        "",
    ]
    for slot, work in load_allocation():
        lines.append(f"- {slot}: {work}")

    lines += [
        "",
        "## Cold draws",
        "",
    ]
    for index, (topic, problem, tag) in enumerate(cold_draws(day), start=1):
        lines.append(f"{index}. `just interview {topic} {problem}`  # {tag}")

    if day.day == 12:
        lines += [
            "",
            "Day 12 rule: run the draws back-to-back with the observer. If the",
            "block gets tight, complete the first two through IDE verification and",
            "use the third as board-only panel pressure plus rubric scoring.",
        ]

    lines += [
        "",
        "## Closeout",
        "",
        "- After each board rep: 2 min tape review, score C/L/A/R/P, log one fix.",
        "- Then run `just study <topic>` and `just challenge-done <topic> <problem>`.",
        "- No passive playlist. One targeted refresher only if a rep exposed the miss.",
    ]
    return "\n".join(lines)


def main() -> int:
    day = 12
    if len(sys.argv) > 1:
        day = int(sys.argv[1])
    print(render_day(day))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
