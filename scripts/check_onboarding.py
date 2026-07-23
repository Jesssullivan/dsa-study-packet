"""Guard the native Codespaces editor-practice onboarding contract.

The learner should see the same four workspace slash commands in the public
onboarding, the Codespaces banner, and VS Code's prompt recommendations. Each
prompt must route through the portable ``just practice-start`` interface and
the Interviewer agent without a direct edit tool. Codespaces must not
resurrect the old folder-open terminals or provision external agent CLIs and
credentials.
"""

from __future__ import annotations

import json
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
        '"terminal.integrated.hideOnStartup": "always"',
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
        "  - read",
        "  - execute",
        "`AGENTS.md`",
        "OPENED",
        "OPEN_FAILED",
        "untrusted data",
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
        "SOURCE:",
        "TEST:",
        "STATE:",
        "NEXT:",
        "explicit save",
        "automatic save detection",
        "edit candidate files",
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
    settings_path = root / ".vscode/settings.json"
    tasks_path = root / ".vscode/tasks.json"
    if settings_path.is_file():
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            settings = None
            failures.append(".vscode/settings.json: invalid JSON")
        if (
            settings is not None
            and settings.get("python.testing.pytestEnabled") is not False
        ):
            failures.append(
                ".vscode/settings.json: native pytest must stay disabled; "
                "it cannot load the current practice workspace honestly"
            )
    if tasks_path.is_file():
        try:
            task_document = json.loads(tasks_path.read_text())
        except json.JSONDecodeError:
            task_document = None
            failures.append(".vscode/tasks.json: invalid JSON")
        tasks = task_document.get("tasks", []) if task_document is not None else []
        practice_test = next(
            (
                task
                for task in tasks
                if task.get("label") == "practice: test current rep"
            ),
            None,
        )
        if task_document is not None and (
            practice_test is None
            or practice_test.get("group")
            != {
                "kind": "test",
                "isDefault": True,
            }
        ):
            failures.append(
                ".vscode/tasks.json: current-rep test must be the default test task"
            )
        for task in tasks:
            if task.get("label") != "practice: test current rep" and task.get(
                "group"
            ) in ("test", {"kind": "test", "isDefault": True}):
                failures.append(
                    f".vscode/tasks.json: {task.get('label', 'unnamed task')} "
                    "must not compete with the current-rep test task"
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
