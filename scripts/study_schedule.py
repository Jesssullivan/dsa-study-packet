"""Spaced-repetition drill scheduler.

Ranks the Core 42 by review urgency from .challenges/progress.md: never-attempted
problems come first, then those longest since their last review. Prints the next
problems to drill with their `just interview` commands (cold present — the
ladder's default; `just challenge` remains the learning-mode alternative).

Usage:
    python scripts/study_schedule.py [N]   # default 5
"""

from __future__ import annotations

import contextlib
import re
import sys
from datetime import date, datetime
from pathlib import Path

from core42 import CORE_42

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / ".challenges" / "progress.md"
_NEVER = 10**7


QueueEntry = tuple[int, str, str]


def _completed(progress: Path = PROGRESS) -> dict[str, str]:
    done: dict[str, str] = {}
    if progress.exists():
        for line in progress.read_text().splitlines():
            m = re.match(r"- \[x\] (\S+/\S+)\s*—?\s*(.*)", line)
            if m:
                done[m.group(1)] = m.group(2).strip()
    return done


def _days_since(datestr: str) -> int:
    try:
        d = datetime.strptime(datestr.strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return _NEVER - 1  # unparseable -> treat as very stale (just below never)
    return (date.today() - d).days


def ranked_queue(progress: Path = PROGRESS) -> list[QueueEntry]:
    """Return drills ranked by review urgency."""
    done = _completed(progress)
    ranked: list[QueueEntry] = []
    for topic, problems in CORE_42.items():
        for problem in problems:
            key = f"{topic}/{problem}"
            urgency = _NEVER if key not in done else _days_since(done[key])
            ranked.append((urgency, topic, problem))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked


def format_queue(count: int = 5, progress: Path = PROGRESS) -> str:
    """Render the next spaced-repetition drills as shell commands."""
    ranked = ranked_queue(progress)
    total = len(ranked)
    drilled = sum(1 for u, _, _ in ranked if u != _NEVER)
    lines = [f"# Spaced-repetition queue — {drilled}/{total} attempted", ""]
    for urgency, topic, problem in ranked[:count]:
        tag = "new" if urgency == _NEVER else f"{urgency}d since review"
        lines.append(f"just interview {topic} {problem}    # {tag}")
    return "\n".join(lines)


def main() -> int:
    count = 5
    if len(sys.argv) > 1:
        with contextlib.suppress(ValueError):
            count = max(1, int(sys.argv[1]))

    print(format_queue(count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
