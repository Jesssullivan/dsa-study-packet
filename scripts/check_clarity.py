"""Guard concise, low-ambiguity agent and onboarding surfaces.

Run with the repository root by default, or pass another root to inspect a
fixture or checkout::

    python scripts/check_clarity.py [ROOT]
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SURFACE_BUDGETS: dict[str, int] = {
    "AGENTS.md": 1000,
    "CLAUDE.md": 80,
    ".claude/skills/interviewer/SKILL.md": 500,
    ".claude/skills/practice-day/SKILL.md": 500,
    ".github/agents/interviewer.agent.md": 180,
    ".github/copilot-instructions.md": 1000,
    ".github/prompts/reacto.prompt.md": 90,
    ".github/prompts/clarp.prompt.md": 90,
    ".github/prompts/umpire.prompt.md": 90,
    ".github/prompts/comments.prompt.md": 90,
    ".github/prompts/continue.prompt.md": 90,
    ".devcontainer/welcome.sh": 300,
    "README.md": 650,
    "WELCOME.md": 300,
    "docs/index.md": 400,
    "docs/guide/getting-started.md": 850,
    "docs/challenges/index.md": 550,
    "docs/guide/local-practice.md": 500,
    "docs/guide/learning-paths.md": 1500,
    "docs/guide/source-of-truth.md": 1500,
    "docs/practice/index.md": 450,
    "reference-sheets/11-14-day-whiteboard-ramp.md": 1000,
}

EM_DASH = "\u2014"
PRACTICE_DAY_SKILL = ".claude/skills/practice-day/SKILL.md"
UNRESOLVED_STRINGS: dict[str, str] = {
    "study-spaced N": "replace N with a concrete draw count or a command that draws internally",
    "C_ L_ A_ R_ P_": "replace score blanks with concrete input or an atomic closeout command",
}


def word_count(text: str) -> int:
    """Count whitespace-delimited words, matching the guard's documented budgets."""
    return len(text.split())


def frontmatter_description(text: str) -> str | None:
    """Return a single-line Markdown frontmatter description when present."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("description:"):
            return line.removeprefix("description:").strip()
    return None


def check(root: Path) -> list[str]:
    """Return one actionable failure per clarity contract violation."""
    failures: list[str] = []
    for relative, budget in SURFACE_BUDGETS.items():
        path = root / relative
        if not path.is_file():
            failures.append(f"{relative}: missing clarity-guarded surface")
            continue

        text = path.read_text()
        words = word_count(text)
        if words > budget:
            failures.append(
                f"{relative}: {words} words exceeds the {budget}-word budget; "
                f"cut at least {words - budget} word(s)"
            )

        em_dash_count = text.count(EM_DASH)
        if em_dash_count:
            failures.append(
                f"{relative}: contains {em_dash_count} U+2014 em dash character(s); "
                "replace them with commas, colons, parentheses, or hyphens"
            )

        for unresolved, remedy in UNRESOLVED_STRINGS.items():
            if unresolved in text:
                failures.append(
                    f'{relative}: contains unresolved instruction "{unresolved}"; {remedy}'
                )

        if relative == PRACTICE_DAY_SKILL:
            description = frontmatter_description(text)
            if description is not None and "let's practice" in description.casefold():
                failures.append(
                    f'{relative}: description claims generic "let\'s practice"; '
                    "reserve this skill for an explicit practice day or full block"
                )

    return failures


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args(argv)

    failures = check(args.root.resolve())
    if failures:
        print("Clarity guard failed:")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print(
        f"Clarity guard passed; {len(SURFACE_BUDGETS)} surfaces are within "
        "their word budgets and contain no ambiguous control text."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
