"""CI guard: fail if the first-run onboarding surfaces drift out of agreement.

A learner's first ten minutes touch a handful of files — the README, the
Codespaces WELCOME, the devcontainer banner + launch script + secret
declarations, and the `just doctor` preflight. They must tell one story: the
same first line to say, the same interviewer-secret names, the same one-time
setup pointers. This guard is the single source of truth for that agreement.
It does not generate the surfaces; it just refuses to let them drift apart.

Edit a surface, keep it in step with the rest (and with the SURFACES table
below); where a surface genuinely lacks a string it should carry, fix the
surface rather than weaken its row.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The one line a learner says to start a rep — identical across every surface.
THE_LINE = "Start my first practice rep."

# The interviewer-secret environment variables, named identically everywhere
# they appear so a learner who sets one can grep for it and trust the match.
SECRET_VARS = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "OPENAI_API_KEY")

# Relative file -> the substrings it MUST contain. Verified against the tree.
SURFACES: dict[str, tuple[str, ...]] = {
    "README.md": (THE_LINE, *SECRET_VARS, "WELCOME.md"),
    "WELCOME.md": (
        THE_LINE,
        *SECRET_VARS,
        "claude setup-token",
        "github.com/settings/codespaces",
    ),
    ".devcontainer/welcome.sh": (THE_LINE, *SECRET_VARS),
    ".devcontainer/launch-agent.sh": (
        THE_LINE,
        "CLAUDE_CODE_OAUTH_TOKEN",
        "ANTHROPIC_API_KEY",
    ),
    ".devcontainer/devcontainer.json": SECRET_VARS,
    "scripts/doctor.py": (THE_LINE, "ANTHROPIC_API_KEY", "OPENAI_API_KEY"),
}

REMEDY = (
    "onboarding drift — these surfaces must agree; "
    "see scripts/check_onboarding.py SURFACES"
)


def check(root: Path) -> list[str]:
    """Return one "file: missing ..." line per surface/substring that drifted.

    Testable against any tree that mirrors the repo layout: only the SURFACES
    entries under ``root`` are consulted, so a temporary copy works.
    """
    failures: list[str] = []
    for rel, required in SURFACES.items():
        path = root / rel
        if not path.exists():
            failures.append(f"{rel}: missing file")
            continue
        text = path.read_text()
        failures.extend(f'{rel}: missing "{needle}"' for needle in required if needle not in text)
    return failures


def main() -> int:
    failures = check(ROOT)
    if failures:
        print("Onboarding drift (first-run surfaces disagree):", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        print(f"  {REMEDY}", file=sys.stderr)
        return 1
    print(f"Onboarding guard passed; {len(SURFACES)} first-run surfaces agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
