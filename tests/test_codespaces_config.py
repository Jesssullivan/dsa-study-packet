"""Semantic checks for the native Codespaces/Copilot practice surface."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARADIGMS = ("reacto", "clarp", "umpire", "comments")
PROMPTS = (*PARADIGMS, "continue")
AGENT_TOOLS = {
    "read/readFile",
    "execute/runInTerminal",
    "execute/getTerminalOutput",
}


def _json(relative: str) -> object:
    return json.loads((ROOT / relative).read_text())


def _frontmatter(path: Path) -> list[str]:
    text = path.read_text()
    assert text.startswith("---\n")
    return text.split("---\n", 2)[1].splitlines()


def test_devcontainer_runs_each_lifecycle_phase_once() -> None:
    config = _json(".devcontainer/devcontainer.json")
    assert isinstance(config, dict)
    assert config["onCreateCommand"].endswith("setup.sh --tools")
    assert config["updateContentCommand"].endswith("setup.sh --sync")
    assert config["postCreateCommand"].endswith("setup.sh --seed")
    assert config["waitFor"] == "updateContentCommand"
    lifecycle = (
        config["onCreateCommand"],
        config["updateContentCommand"],
        config["postCreateCommand"],
    )
    assert len(set(lifecycle)) == 3


def test_devcontainer_uses_native_copilot_without_external_cli_provisioning() -> None:
    config = _json(".devcontainer/devcontainer.json")
    assert isinstance(config, dict)
    customizations = config["customizations"]
    assert isinstance(customizations, dict)
    vscode = customizations["vscode"]
    assert isinstance(vscode, dict)
    extensions = set(vscode["extensions"])
    assert {"GitHub.copilot", "GitHub.copilot-chat"} <= extensions
    assert not any("anthropic" in extension.lower() for extension in extensions)
    assert "features" not in config
    assert "secrets" not in config
    assert "postAttachCommand" not in config


def test_workspace_recommends_prompts_but_disables_inline_completion() -> None:
    settings = _json(".vscode/settings.json")
    assert isinstance(settings, dict)
    assert settings["chat.useAgentsMdFile"] is True
    assert settings["github.copilot.chat.codeGeneration.useInstructionFiles"] is False
    assert settings["chat.promptFilesRecommendations"] == dict.fromkeys(PROMPTS, True)
    assert settings["github.copilot.enable"] == {"*": False}
    assert settings["github.copilot.nextEditSuggestions.enabled"] is False
    assert "chat.disableAIFeatures" not in settings


def test_workspace_tasks_are_explicit_and_never_run_on_folder_open() -> None:
    tasks = _json(".vscode/tasks.json")
    assert isinstance(tasks, dict)
    serialized = json.dumps(tasks)
    assert "folderOpen" not in serialized
    assert ".devcontainer/launch-agent.sh" not in serialized
    commands = {task.get("command") for task in tasks["tasks"]}
    assert {
        "just practice-start ${input:practiceParadigm}",
        "just practice-next",
        "just practice-test",
        "just practice-watch",
        "just practice-open",
        "just practice-repl",
    } <= commands
    finish = next(
        task
        for task in tasks["tasks"]
        if task["label"] == "practice: finish current rep"
    )
    assert finish["type"] == "process"
    assert finish["command"] == "just"
    assert finish["args"] == ["practice-finish", "${input:practiceFinishNote}"]


def test_slash_prompts_route_to_the_interviewer_and_portable_recipe() -> None:
    prompt_dir = ROOT / ".github/prompts"
    assert {
        path.stem.removesuffix(".prompt") for path in prompt_dir.glob("*.prompt.md")
    } == set(PROMPTS)
    for paradigm in PARADIGMS:
        path = prompt_dir / f"{paradigm}.prompt.md"
        frontmatter = _frontmatter(path)
        assert f"name: {paradigm}" in frontmatter
        assert "agent: 'Interviewer'" in frontmatter
        assert not any(line.startswith("tools:") for line in frontmatter)
        assert f"just practice-start {paradigm}" in path.read_text()

    continuation = prompt_dir / "continue.prompt.md"
    continuation_frontmatter = _frontmatter(continuation)
    assert "name: continue" in continuation_frontmatter
    assert "agent: 'Interviewer'" in continuation_frontmatter
    assert not any(line.startswith("tools:") for line in continuation_frontmatter)
    continuation_text = continuation.read_text()
    assert "just practice-next" in continuation_text
    assert "practice-status" not in continuation_text
    assert "practice-current" not in continuation_text
    assert "`STATE:` and `NEXT:`" in continuation_text
    assert "Never edit the candidate workspace" in continuation_text


def test_interviewer_agent_has_no_direct_edit_tool() -> None:
    path = ROOT / ".github/agents/interviewer.agent.md"
    frontmatter = _frontmatter(path)
    assert "target: vscode" in frontmatter
    tools_index = frontmatter.index("tools:")
    tools = {
        line.removeprefix("  - ")
        for line in frontmatter[tools_index + 1 :]
        if line.startswith("  - ")
    }
    assert tools == AGENT_TOOLS
    assert "AGENTS.md" in path.read_text()
    assert "not a security boundary" in path.read_text()
