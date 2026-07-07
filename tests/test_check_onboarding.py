"""Tests for the onboarding-surface drift guard."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_onboarding import (  # type: ignore[import-not-found]
    SURFACES,
    THE_LINE,
    check,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _mirror_surfaces(dst: Path) -> None:
    """Copy every guarded surface from the real repo into a temporary tree."""
    for rel in SURFACES:
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / rel, out)


def test_real_repo_surfaces_agree() -> None:
    # The invariant CI enforces: today's tree must have no onboarding drift.
    assert check(REPO_ROOT) == []


def test_removed_line_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    victim = tmp_path / "README.md"
    victim.write_text(victim.read_text().replace(THE_LINE, ""))

    failures = check(tmp_path)

    assert any(f.startswith("README.md:") and THE_LINE in f for f in failures)
    # Only the mutated surface drifts; every other surface still agrees.
    assert all(f.startswith("README.md:") for f in failures)


def test_removed_secret_var_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    victim = tmp_path / ".devcontainer/devcontainer.json"
    victim.write_text(victim.read_text().replace("OPENAI_API_KEY", "REDACTED"))

    assert '.devcontainer/devcontainer.json: missing "OPENAI_API_KEY"' in check(
        tmp_path
    )


def test_missing_surface_file_is_caught(tmp_path: Path) -> None:
    _mirror_surfaces(tmp_path)
    (tmp_path / "scripts/doctor.py").unlink()

    assert "scripts/doctor.py: missing file" in check(tmp_path)
