"""Print the generated study-packet catalog.

This is the compact, executable replacement for hand-maintained counts in docs.
"""

from __future__ import annotations

from pathlib import Path

from core42 import CORE_42

ROOT = Path(__file__).resolve().parent.parent


def _topic_title(topic: str) -> str:
    return topic.replace("_", " ")


def core_count() -> int:
    return sum(len(problems) for problems in CORE_42.values())


def implementation_count() -> int:
    return sum(
        1
        for path in (ROOT / "src" / "algo").glob("*/*.py")
        if path.name != "__init__.py"
    )


def concept_count() -> int:
    return sum(
        1
        for path in (ROOT / "src" / "concepts").glob("*.py")
        if path.name != "__init__.py"
    )


def reference_sheet_count() -> int:
    return len(list((ROOT / "reference-sheets").glob("[0-9][0-9]-*.md")))


def render_catalog() -> str:
    lines = [
        "# Study packet catalog",
        "",
        f"- Core drill set: {core_count()} problems",
        f"- Algorithm implementations: {implementation_count()}",
        f"- Concept modules: {concept_count()}",
        f"- Reference sheets: {reference_sheet_count()}",
        "",
        "## Core drill set",
        "",
    ]
    for topic, problems in CORE_42.items():
        drills = ", ".join(problems)
        lines.append(f"- {_topic_title(topic)} ({len(problems)}): {drills}")
    return "\n".join(lines)


def main() -> int:
    print(render_catalog())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
