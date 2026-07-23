"""Working-tree edge cases for the public-boundary guard."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_public_boundary as guard  # type: ignore[import-not-found]


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def public_repo(tmp_path: Path, monkeypatch: object) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Boundary Test")
    git(tmp_path, "config", "user.email", "boundary@example.invalid")
    # Disposable fixture commits must not inherit a developer's global signing
    # policy or open pinentry. This changes only the temporary repository.
    git(tmp_path, "config", "commit.gpgsign", "false")
    victim = tmp_path / "tracked.txt"
    victim.write_text("public content\n")
    git(tmp_path, "add", "tracked.txt")
    git(tmp_path, "commit", "-qm", "initial")
    monkeypatch.setattr(guard, "ROOT", tmp_path)  # type: ignore[attr-defined]
    return victim


def secret() -> str:
    # Keep the guard's own test source free of a token-shaped literal.
    return "gh" + "p_" + ("A" * 24)


def test_pending_tracked_deletion_has_no_content_to_scan(tmp_path: Path) -> None:
    assert guard.read_text(tmp_path / "deleted-file") is None


def test_staged_secret_is_scanned_after_working_tree_deletion(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    victim = public_repo(tmp_path, monkeypatch)
    victim.write_text(secret() + "\n")
    git(tmp_path, "add", "tracked.txt")
    victim.unlink()

    assert guard.main() == 1
    assert "tracked.txt:1: GitHub token" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_staged_secret_is_scanned_when_working_tree_is_clean(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    victim = public_repo(tmp_path, monkeypatch)
    victim.write_text(secret() + "\n")
    git(tmp_path, "add", "tracked.txt")
    victim.write_text("public content\n")

    assert guard.main() == 1
    assert "tracked.txt:1: GitHub token" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_unstaged_secret_is_scanned_when_index_is_clean(
    tmp_path: Path, monkeypatch: object, capsys: object
) -> None:
    victim = public_repo(tmp_path, monkeypatch)
    victim.write_text(secret() + "\n")

    assert guard.main() == 1
    assert "tracked.txt:1: GitHub token" in capsys.readouterr().err  # type: ignore[attr-defined]
