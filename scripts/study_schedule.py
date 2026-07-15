"""Spaced-repetition drill scheduler.

Ranks the core problem set by review urgency from .challenges/progress.md:
never-attempted
problems come first, then those longest since their last review. Prints the next
problems as isolated CLARP editor reps; swap the paradigm argument for REACTO,
UMPIRE, or plain comments without changing the draw.

Usage:
    python scripts/study_schedule.py [N]   # default 5
"""

from __future__ import annotations

import contextlib
import re
import sys
from collections import deque
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
            m = re.match(
                r"- \[x\] ([a-z0-9_]+/[a-z0-9_]+)\s*(?:\u2014|:)?\s*(.*)",
                line,
            )
            if m:
                done[m.group(1)] = m.group(2).strip()
    return done


def _days_since(datestr: str) -> int:
    try:
        d = datetime.strptime(datestr.strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return _NEVER - 1  # unparseable -> treat as very stale (just below never)
    return (date.today() - d).days


def _interleave_topics(entries: list[QueueEntry]) -> list[QueueEntry]:
    """Round-robin equal-urgency entries without reordering within a topic."""
    by_topic: dict[str, deque[QueueEntry]] = {}
    for entry in entries:
        by_topic.setdefault(entry[1], deque()).append(entry)

    interleaved: list[QueueEntry] = []
    while by_topic:
        exhausted: list[str] = []
        for topic, topic_entries in by_topic.items():
            interleaved.append(topic_entries.popleft())
            if not topic_entries:
                exhausted.append(topic)
        for topic in exhausted:
            del by_topic[topic]
    return interleaved


def ranked_queue(progress: Path = PROGRESS) -> list[QueueEntry]:
    """Return drills by urgency, interleaving topics within each tie bucket."""
    done = _completed(progress)
    buckets: dict[int, list[QueueEntry]] = {}
    for topic, problems in CORE_42.items():
        for problem in problems:
            key = f"{topic}/{problem}"
            urgency = _NEVER if key not in done else _days_since(done[key])
            buckets.setdefault(urgency, []).append((urgency, topic, problem))

    ranked: list[QueueEntry] = []
    for urgency in sorted(buckets, reverse=True):
        ranked.extend(_interleave_topics(buckets[urgency]))
    return ranked


def format_queue(count: int = 5, progress: Path = PROGRESS) -> str:
    """Render the next spaced-repetition drills as shell commands."""
    ranked = ranked_queue(progress)
    total = len(ranked)
    drilled = sum(1 for u, _, _ in ranked if u != _NEVER)
    lines = [f"# Spaced-repetition queue: {drilled}/{total} attempted", ""]
    for urgency, topic, problem in ranked[:count]:
        tag = "new" if urgency == _NEVER else f"{urgency}d since review"
        lines.append(f"just practice-start clarp {topic} {problem}    # {tag}")
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
