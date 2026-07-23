"""Semantic checks for the native Codespaces/Copilot practice surface."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

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


def _write_executable(path: Path, text: str) -> None:
    path.write_text(text)
    path.chmod(0o755)


def _fake_tool(path: Path, name: str, version: str) -> None:
    _write_executable(path, f"#!/bin/sh\nprintf '%s\\n' '{name} {version}'\n")


def _fake_release_commands(path: Path) -> None:
    _write_executable(
        path / "uname",
        """#!/bin/sh
case "${1:-}" in
  -s) printf '%s\n' "${FAKE_UNAME_S:-Linux}" ;;
  -m) printf '%s\n' "${FAKE_UNAME_M:-x86_64}" ;;
  *) exit 2 ;;
esac
""",
    )
    _write_executable(
        path / "curl",
        """#!/bin/sh
output=
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o) output="$2"; shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$output" ] || exit 2
mkdir -p "$(dirname "$output")"
: > "$output"
touch "$HOME/curl-called"
""",
    )
    _write_executable(
        path / "sha256sum",
        """#!/bin/sh
cat > "$HOME/checksum-input"
exit "${FAKE_CHECKSUM_EXIT:-0}"
""",
    )
    _write_executable(
        path / "tar",
        """#!/bin/sh
archive=
destination=
while [ "$#" -gt 0 ]; do
  case "$1" in
    -C) destination="$2"; shift 2 ;;
    -*) shift ;;
    *) archive="$1"; shift ;;
  esac
done
[ -n "$archive" ] && [ -n "$destination" ] || exit 2
name="$(basename "$archive")"
write_tool() {
  target="$1"
  label="$2"
  version="$3"
  mkdir -p "$(dirname "$target")"
  printf '#!/bin/sh\nprintf "%%s\\n" "%s %s"\n' "$label" "$version" > "$target"
  chmod +x "$target"
}
case "$name" in
  uv-*.tar.gz)
    directory="${name%.tar.gz}"
    write_tool "$destination/$directory/uv" uv \
      "${FAKE_UV_INSTALL_VERSION:-0.11.27}"
    ;;
  just-*.tar.gz)
    write_tool "$destination/just" just \
      "${FAKE_JUST_INSTALL_VERSION:-1.40.0}"
    ;;
  watchexec-*.tar.xz)
    directory="${name%.tar.xz}"
    write_tool "$destination/$directory/watchexec" watchexec \
      "${FAKE_WATCHEXEC_INSTALL_VERSION:-2.3.2}"
    ;;
  *) exit 2 ;;
esac
""",
    )


def _setup_env(
    tmp_path: Path,
    *,
    uv_version: str = "0.11.27",
    just_version: str = "1.40.0",
    watchexec_version: str = "2.3.2",
) -> tuple[dict[str, str], Path]:
    home = tmp_path / "home"
    system_bin = tmp_path / "system-bin"
    home.mkdir()
    system_bin.mkdir()
    _fake_tool(system_bin / "uv", "uv", uv_version)
    _fake_tool(system_bin / "just", "just", just_version)
    _fake_tool(system_bin / "watchexec", "watchexec", watchexec_version)
    _fake_release_commands(system_bin)
    env = os.environ | {
        "HOME": str(home),
        "PATH": f"{system_bin}{os.pathsep}{os.environ['PATH']}",
    }
    return env, home


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
    assert "@sha256:" in config["image"]
    assert config["remoteEnv"]["PATH"].startswith("/home/vscode/.local/bin:")


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


def test_setup_verifies_declared_tool_versions() -> None:
    setup = (ROOT / ".devcontainer/setup.sh").read_text()
    for tool, variable in (
        ("uv", "UV_VERSION"),
        ("just", "JUST_VERSION"),
        ("watchexec", "WATCHEXEC_VERSION"),
    ):
        assert f'has_version {tool} "${variable}"' in setup
    assert 'require_version uv "$UV_VERSION"' in setup
    assert 'require_version just "$JUST_VERSION"' in setup
    assert "install.sh" not in setup
    assert "sha256sum --check --status" in setup
    assert setup.count("_SHA256_X86_64=") == 3
    assert setup.count("_SHA256_AARCH64=") == 3


def test_setup_accepts_matching_tools_without_downloading(tmp_path: Path) -> None:
    env, home = _setup_env(tmp_path, uv_version="0.11.27")
    system_bin = Path(env["PATH"].split(os.pathsep, 1)[0])
    _write_executable(system_bin / "curl", "#!/bin/sh\nexit 97\n")

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert not (home / "curl-called").exists()


def test_setup_forgets_hashed_old_tool_after_install(tmp_path: Path) -> None:
    env, home = _setup_env(tmp_path, uv_version="0.0.0")

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert (home / "curl-called").is_file()
    assert (home / "checksum-input").read_text().split()[0] == (
        "5d5594af1530c7c31e46a8cc0a35ceb4d28f3890049efe2149ac53c9ad121493"
    )
    installed = subprocess.run(
        [str(home / ".local/bin/uv"), "--version"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert installed.stdout.strip() == "uv 0.11.27"


def test_setup_fails_when_installer_leaves_wrong_version(tmp_path: Path) -> None:
    env, _ = _setup_env(tmp_path, uv_version="0.0.0")
    env["FAKE_UV_INSTALL_VERSION"] = "0.0.1"

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode != 0
    assert "uv install did not provide declared version 0.11.27" in proc.stderr


def test_setup_forgets_hashed_old_just_after_install(tmp_path: Path) -> None:
    env, _ = _setup_env(tmp_path, just_version="0.0.0")

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr


def test_setup_rejects_an_archive_with_wrong_digest(tmp_path: Path) -> None:
    env, home = _setup_env(tmp_path, uv_version="0.0.0")
    env["FAKE_CHECKSUM_EXIT"] = "1"

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode != 0
    assert "uv install did not provide declared version 0.11.27" in proc.stderr
    assert not (home / ".local/bin/uv").exists()


def test_setup_selects_arm64_release_digest(tmp_path: Path) -> None:
    env, home = _setup_env(tmp_path, uv_version="0.0.0")
    env["FAKE_UNAME_M"] = "aarch64"

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert (home / "checksum-input").read_text().split()[0] == (
        "b0b1909a7e5caf2ec0cbe2649f5171050c26d85efb65d9d4de2cfe754dc14ea3"
    )


def test_setup_rejects_unknown_release_architecture(tmp_path: Path) -> None:
    env, _ = _setup_env(tmp_path, uv_version="0.0.0")
    env["FAKE_UNAME_M"] = "riscv64"

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode != 0
    assert "unsupported Codespaces architecture: riscv64" in proc.stderr


def test_setup_keeps_watchexec_optional_when_install_fails(tmp_path: Path) -> None:
    env, _ = _setup_env(tmp_path, watchexec_version="0.0.0")
    system_bin = Path(env["PATH"].split(os.pathsep, 1)[0])
    _write_executable(system_bin / "curl", "#!/bin/sh\nexit 97\n")

    proc = subprocess.run(
        ["bash", ".devcontainer/setup.sh", "--tools"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0
    assert "watch mode unavailable" in proc.stderr


def test_devcontainer_workflow_uses_pinned_actions_and_login_free_path() -> None:
    workflow = (ROOT / ".github/workflows/devcontainer.yml").read_text()
    assert "export PATH=" not in workflow
    assert "bash --noprofile --norc" in workflow
    assert "# RESTATE:" not in workflow
    for prompt in (
        "Write what this function should return",
        "Work one ordinary example and one edge case",
        "Note the simplest correct plan",
    ):
        assert prompt in workflow
    assert "NEXT: Add 1 more ordinary reasoning comment above the gate" in workflow
    action_refs = [
        line.strip().removeprefix("- uses: ").split(" #", 1)[0]
        for line in workflow.splitlines()
        if line.strip().startswith("- uses: ")
    ]
    assert action_refs
    for action_ref in action_refs:
        revision = action_ref.rsplit("@", 1)[1]
        assert len(revision) == 40
        assert all(character in "0123456789abcdef" for character in revision)


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


@pytest.mark.parametrize(
    ("topic", "problem"),
    [("lru_cache", ""), ("", "lru_cache")],
)
def test_practice_open_recipe_forwards_exact_pairs_and_guides_partial_names(
    topic: str,
    problem: str,
) -> None:
    exact = subprocess.run(
        ["just", "--dry-run", "practice-open", "linked_lists", "lru_cache"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert exact.returncode == 0, exact.stderr
    exact_output = exact.stdout + exact.stderr
    assert "topic='linked_lists'" in exact_output
    assert "problem='lru_cache'" in exact_output
    assert 'practice_workspace.py open "$topic" "$problem"' in exact_output

    partial = subprocess.run(
        ["just", "practice-open", topic, problem],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert partial.returncode == 2
    assert 'NEXT: just catalog "lru_cache"' in partial.stdout


def test_all_interviewer_surfaces_prioritize_safe_file_open_intent() -> None:
    for relative in (
        "AGENTS.md",
        ".claude/skills/interviewer/SKILL.md",
        ".github/agents/interviewer.agent.md",
        ".github/copilot-instructions.md",
    ):
        text = " ".join((ROOT / relative).read_text().split())
        assert "just practice-open topic problem" in text
        assert "reference tests" in text
        assert "before placement" in text
        assert "`START` immediately" in text
        assert "Discuss without the editor" not in text
        assert "otherwise run `just practice-open topic problem`" in text
        assert "never `QUEUE`" in text
        assert "takes priority" in text
        assert "`PRACTICE:" in text
        assert "before relaying the prompt" in text


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
