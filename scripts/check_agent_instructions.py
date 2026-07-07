"""CI guard: fail if the generated Copilot files drift from the AGENTS.md persona.

AGENTS.md is the single source of truth for the resident-interviewer persona.
`scripts/gen_agent_instructions.py` fans it out to the Copilot instruction
files; this guard regenerates the expected content in memory and compares it to
what is committed. Any mismatch (or a missing output) is drift — regenerate with
`just gen-agents` and commit the result.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_agent_instructions import ROOT, PersonaMarkerError, generated_files


def main() -> int:
    try:
        files = generated_files()
    except PersonaMarkerError as exc:
        print(f"Agent instruction guard failed: {exc}", file=sys.stderr)
        return 1

    stale: list[str] = []
    for path, expected in files.items():
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            stale.append(f"{rel}: missing (never generated)")
        elif path.read_text() != expected:
            stale.append(f"{rel}: out of date")

    if stale:
        print(
            "Agent instruction drift (generated files disagree with the "
            "AGENTS.md persona):",
            file=sys.stderr,
        )
        for entry in stale:
            print(f"  {entry}", file=sys.stderr)
        print("  run: just gen-agents", file=sys.stderr)
        return 1

    rels = ", ".join(sorted(path.relative_to(ROOT).as_posix() for path in files))
    print(f"Agent instruction guard passed; generated files match AGENTS.md: {rels}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
