"""Tests for the native Codespaces onboarding drift guard."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_onboarding import (  # type: ignore[import-not-found]
    FORBIDDEN,
    SLASH_COMMANDS,
    SURFACES,
    check,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _mirror_surfaces(dst: Path) -> None:
    """Copy every guarded surface from the real repo into a temporary tree."""
    for rel in set(SURFACES) | set(FORBIDDEN):
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / rel, out)


def test_real_repo_surfaces_agree() -> None:
    assert check(REPO_ROOT) == []


def test_removed_slash_command_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    victim = tmp_path / "README.md"
    command = SLASH_COMMANDS[0]
    victim.write_text(victim.read_text().replace(command, ""))

    failures = check(tmp_path)

    assert f'README.md: missing "{command}"' in failures
    assert all(failure.startswith("README.md:") for failure in failures)


def test_folder_open_launcher_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    victim = tmp_path / ".vscode/tasks.json"
    victim.write_text(victim.read_text() + '\n"runOn": "folderOpen"\n')

    assert any(
        failure.startswith(".vscode/tasks.json: contains forbidden")
        and "folderOpen" in failure
        for failure in check(tmp_path)
    )


def test_prompt_level_tools_override_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    victim = tmp_path / ".github/prompts/reacto.prompt.md"
    victim.write_text(victim.read_text() + "\ntools:\n  - edit/editFiles\n")

    assert '.github/prompts/reacto.prompt.md: contains forbidden "\ntools:"' in check(
        tmp_path
    )


def test_missing_surface_file_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    (tmp_path / ".github/prompts/comments.prompt.md").unlink()

    assert ".github/prompts/comments.prompt.md: missing file" in check(tmp_path)
