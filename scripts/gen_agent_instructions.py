"""Fan the AGENTS.md persona region out to GitHub Copilot instruction files.

AGENTS.md is the single source of truth for the resident-interviewer persona.
Copilot reads its own files, so we generate two of them from the persona region
(between the `<!-- BEGIN:persona -->` / `<!-- END:persona -->` markers):

  - `.github/copilot-instructions.md` — repo-wide Copilot instructions.
  - `.github/agents/interviewer.agent.md` — a Copilot custom agent Copilot can
    offer for practice / mock-interview requests.

Both outputs are deterministic: no timestamps, stable ordering, trailing
newline. Edit the persona in AGENTS.md, then run `just gen-agents`;
`scripts/check_agent_instructions.py` guards against drift.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
COPILOT_INSTRUCTIONS = ROOT / ".github" / "copilot-instructions.md"
INTERVIEWER_AGENT = ROOT / ".github" / "agents" / "interviewer.agent.md"

BEGIN_MARKER = "<!-- BEGIN:persona -->"
END_MARKER = "<!-- END:persona -->"

HEADER = (
    "<!-- GENERATED from AGENTS.md persona region "
    "— edit there, then run: just gen-agents -->"
)

# One orientation sentence so a cold Copilot session knows what the repo is
# before it reads the persona.
ORIENTATION = (
    "This repository is a public, company-neutral technical-interview study "
    "packet whose purpose is a repeatable practice day that trains confident, "
    "non-panicked reasoning-out-loud under observation."
)

# Kept free of any colon-space or trailing hash so it stays a valid YAML plain
# scalar. Written to make Copilot surface the agent for interview practice asks.
AGENT_DESCRIPTION = (
    "Resident interviewer for kind, realistic mock technical-interview "
    "practice — select this agent to run a practice rep, conduct a mock or "
    "timed whiteboard interview, do interview practice, or interview the "
    "candidate."
)


class PersonaMarkerError(RuntimeError):
    """Raised when the AGENTS.md persona markers are missing or duplicated."""


def extract_persona(text: str) -> str:
    """Return the persona body between the markers, verbatim.

    Leading and trailing blank lines are trimmed so the output stays stable
    regardless of spacing around the markers. Interior text is untouched.
    """
    lines = text.splitlines()
    begins = [i for i, line in enumerate(lines) if line.strip() == BEGIN_MARKER]
    ends = [i for i, line in enumerate(lines) if line.strip() == END_MARKER]

    if len(begins) != 1 or len(ends) != 1:
        raise PersonaMarkerError(
            f"expected exactly one {BEGIN_MARKER} and one {END_MARKER} in "
            f"{AGENTS.relative_to(ROOT).as_posix()}; found "
            f"{len(begins)} begin and {len(ends)} end marker(s)"
        )
    begin, end = begins[0], ends[0]
    if begin >= end:
        raise PersonaMarkerError(
            f"{BEGIN_MARKER} must appear before {END_MARKER} in "
            f"{AGENTS.relative_to(ROOT).as_posix()}"
        )

    body = lines[begin + 1 : end]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    if not body:
        raise PersonaMarkerError("persona region is empty")
    return "\n".join(body)


def render_copilot_instructions(persona: str) -> str:
    return "\n".join([HEADER, "", ORIENTATION, "", persona]) + "\n"


def render_interviewer_agent(persona: str) -> str:
    frontmatter = "\n".join(
        [
            "---",
            "name: Interviewer",
            f"description: {AGENT_DESCRIPTION}",
            "---",
        ]
    )
    return "\n".join([frontmatter, "", HEADER, "", persona]) + "\n"


def generated_files() -> dict[Path, str]:
    """Map each output path to its deterministic content."""
    persona = extract_persona(AGENTS.read_text())
    return {
        COPILOT_INSTRUCTIONS: render_copilot_instructions(persona),
        INTERVIEWER_AGENT: render_interviewer_agent(persona),
    }


def main() -> int:
    try:
        files = generated_files()
    except PersonaMarkerError as exc:
        print(f"gen_agent_instructions: {exc}", file=sys.stderr)
        return 1

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    rels = ", ".join(
        sorted(path.relative_to(ROOT).as_posix() for path in files)
    )
    print(f"Generated persona fan-out from AGENTS.md: {rels}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
