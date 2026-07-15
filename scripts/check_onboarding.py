"""Guard the native Codespaces editor-practice onboarding contract.

The learner should see the same four workspace slash commands in the public
onboarding, the Codespaces banner, and VS Code's prompt recommendations. Each
prompt must route through the portable ``just practice-start`` interface and
the Interviewer agent without a direct edit tool. Codespaces must not
resurrect the old folder-open terminals or provision external agent CLIs and
credentials.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BRAND = "The DSA Woodshed"
PARADIGMS = ("reacto", "clarp", "umpire", "comments")
SLASH_COMMANDS = tuple(f"/{name}" for name in PARADIGMS)

# Relative file -> substrings it must contain.
SURFACES: dict[str, tuple[str, ...]] = {
    "README.md": (
        BRAND,
        *SLASH_COMMANDS,
        "just practice-start",
        "just practice-next",
        "just practice-finish",
    ),
    "WELCOME.md": (
        *SLASH_COMMANDS,
        "just practice-start",
        "just practice-next",
        "just practice-finish",
    ),
    ".devcontainer/welcome.sh": (
        BRAND,
        *SLASH_COMMANDS,
        "/continue",
        "just practice-start",
        "just practice-next",
        "just practice-finish",
    ),
    ".devcontainer/devcontainer.json": (
        "GitHub.copilot-chat",
        "setup.sh --tools",
        "setup.sh --sync",
        "setup.sh --seed",
    ),
    ".devcontainer/setup.sh": ("--tools", "--sync", "--seed"),
    ".vscode/settings.json": (
        "chat.useAgentsMdFile",
        "github.copilot.chat.codeGeneration.useInstructionFiles",
        "chat.promptFilesRecommendations",
        "github.copilot.enable",
        "github.copilot.nextEditSuggestions.enabled",
        *PARADIGMS,
        "continue",
    ),
    ".vscode/tasks.json": (
        "practice-start",
        "practice-next",
        "practice-test",
        "practice-watch",
        "practice-repl",
        "practice-open",
        "practice-finish",
    ),
    ".github/agents/interviewer.agent.md": (
        "target: vscode",
        "read/readFile",
        "execute/runInTerminal",
        "execute/getTerminalOutput",
        "`AGENTS.md`",
        "just practice-next",
    ),
    **{
        f".github/prompts/{name}.prompt.md": (
            f"name: {name}",
            "agent: 'Interviewer'",
            f"just practice-start {name}",
        )
        for name in PARADIGMS
    },
    ".github/prompts/continue.prompt.md": (
        "name: continue",
        "agent: 'Interviewer'",
        "just practice-next",
        "STATE:",
        "NEXT:",
        "Never edit the candidate workspace",
    ),
}

# Relative file -> substrings that would restore superseded startup behavior
# or escape the read/execute-only interviewer boundary.
FORBIDDEN: dict[str, tuple[str, ...]] = {
    ".devcontainer/devcontainer.json": (
        "anthropic.claude-code",
        "ANTHROPIC_API_KEY",
        "CLAUDE_CODE_OAUTH_TOKEN",
        "OPENAI_API_KEY",
    ),
    ".devcontainer/setup.sh": (
        "npm install -g @openai/codex",
        "seed_claude_json",
        "codex login",
    ),
    ".vscode/tasks.json": (
        '"runOn": "folderOpen"',
        ".devcontainer/launch-agent.sh",
        "exec bash",
    ),
    ".github/agents/interviewer.agent.md": (
        "edit/editFiles",
        "edit/createFile",
        "edit/applyPatch",
    ),
    **{f".github/prompts/{name}.prompt.md": ("\ntools:",) for name in PARADIGMS},
    ".github/prompts/continue.prompt.md": ("\ntools:",),
}

REMEDY = (
    "Codespaces onboarding drift: keep slash prompts, the portable just "
    "interface, and native no-auto-terminal startup in agreement; see "
    "scripts/check_onboarding.py"
)


def check(root: Path) -> list[str]:
    """Return one actionable line per missing or forbidden contract string."""
    failures: list[str] = []
    files = set(SURFACES) | set(FORBIDDEN)
    for rel in sorted(files):
        path = root / rel
        if not path.exists():
            failures.append(f"{rel}: missing file")
            continue
        text = path.read_text()
        failures.extend(
            f'{rel}: missing "{needle}"'
            for needle in SURFACES.get(rel, ())
            if needle not in text
        )
        failures.extend(
            f'{rel}: contains forbidden "{needle}"'
            for needle in FORBIDDEN.get(rel, ())
            if needle in text
        )
    return failures


def main() -> int:
    failures = check(ROOT)
    if failures:
        print("Codespaces onboarding drift:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        print(f"  {REMEDY}", file=sys.stderr)
        return 1
    print(f"Onboarding guard passed; {len(SURFACES)} native surfaces agree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
