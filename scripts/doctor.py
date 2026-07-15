"""Preflight: report editor-practice toolchain readiness, with hints.

Runs on the system interpreter on purpose (`just doctor` calls python3, not
`uv run`) so it still works when the venv is broken. That is when you need a
doctor. Exits 1 only if a core tool (uv, just, git) is missing; everything
else is informational.
"""

from __future__ import annotations

import os
import shutil
import sys

CORE = (
    ("uv", "installs python + deps; https://astral.sh/uv"),
    ("just", "runs every recipe; https://just.systems"),
    ("git", "loads immutable practice source from the checkout's committed HEAD"),
)
LOOP = (
    ("watchexec", "'just practice-watch'; test/repl loop works without it"),
    ("code", "opens candidate source + test tabs; paths print if absent"),
)
INTERVIEWERS = (
    ("claude", "optional manual CLI; built-in Copilot is the Codespaces default"),
    ("codex", "optional manual CLI; built-in Copilot is the Codespaces default"),
    (
        "gemini",
        "npm i -g @google/gemini-cli; reads AGENTS.md via .gemini/settings.json",
    ),
)
PUBLISHING = (
    ("pandoc", "'just pdf-all' reference-sheet PDFs (optional)"),
    ("tectonic", "'just packet' booklet PDF (optional)"),
    ("bazelisk", "'just remote-*' cache-first builds (optional)"),
)


def report(title: str, tools: tuple[tuple[str, str], ...]) -> list[str]:
    print(title)
    missing = []
    for name, hint in tools:
        found = shutil.which(name)
        mark = "ok" if found else "--"
        print(f"  {name:<10} {mark:<4} {hint}")
        if not found:
            missing.append(name)
    return missing


def main() -> int:
    print(f"doctor: python {sys.version.split()[0]} at {sys.executable}")
    print()
    core_missing = report("Core", CORE)
    report("Practice loop", LOOP)
    print("Interviewers")
    if os.environ.get("CODESPACES"):
        print("  copilot    ok   built into Codespaces (Chat in the sidebar)")
    else:
        print(
            "  copilot    --   install GitHub Copilot Chat in VS Code, or use a CLI below"
        )
    for name, hint in INTERVIEWERS:
        mark = "ok" if shutil.which(name) else "--"
        print(f"  {name:<10} {mark:<4} {hint}")
    report("Publishing (optional)", PUBLISHING)
    print()
    if os.path.isdir(".venv"):
        print("venv: .venv present; 'uv run pytest -q' should work")
    else:
        print("venv: missing; run 'uv sync --extra dev' first")
    if core_missing:
        print(f"MISSING core tools: {', '.join(core_missing)}", file=sys.stderr)
        return 1
    print(
        "Core toolchain ok. Start with /reacto in Chat or 'just practice-start reacto'."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
