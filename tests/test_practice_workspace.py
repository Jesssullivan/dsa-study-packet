"""Tests for the isolated, editor-first practice workspace."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import practice_workspace as practice  # type: ignore[import-not-found]  # noqa: E402

SOURCE = '''"""arrays / {problem}

Problem:
    Return the sum of the values.

Approach:
    This committed explanation must not reach the cold workspace.
"""


def solve(values: list[int]) -> int:
    """Return the sum."""
    secret = sum(values)
    return secret
'''


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def practice_repo(tmp_path: Path) -> Path:
    _write(tmp_path / ".gitignore", ".challenges/\n")
    _write(tmp_path / "src/algo/__init__.py", "")
    _write(tmp_path / "src/algo/arrays/__init__.py", "")
    for problem in ("first", "second"):
        _write(
            tmp_path / f"src/algo/arrays/{problem}.py",
            SOURCE.format(problem=problem),
        )
        _write(
            tmp_path / f"tests/arrays/test_{problem}.py",
            (
                f"from algo.arrays.{problem} import solve\n\n\n"
                f"def test_{problem}() -> None:\n"
                "    assert solve([1, 2, 3]) == 6\n"
            ),
        )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "-c",
            "commit.gpgSign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-qm",
            "fixture",
        ],
        cwd=tmp_path,
        check=True,
    )
    return tmp_path


@pytest.mark.parametrize("paradigm_name", tuple(practice.PARADIGMS))
def test_each_paradigm_has_one_ordered_thinking_gate(paradigm_name: str) -> None:
    paradigm = practice.PARADIGMS[paradigm_name]
    rendered = practice.render_candidate(SOURCE.format(problem="first"), paradigm)
    lines = [line.strip() for line in rendered.splitlines()]
    expected = [
        *paradigm.seeds[: paradigm.lock_after],
        practice.PRACTICE_LOCK,
        *paradigm.seeds[paradigm.lock_after :],
    ]
    start = lines.index(paradigm.seeds[0])

    assert lines[start : start + len(expected)] == expected
    assert rendered.count(practice.PRACTICE_LOCK) == 1
    assert all(rendered.count(seed) == 1 for seed in paradigm.seeds)
    assert "secret = sum(values)" not in rendered


def test_workspace_is_created_without_mutating_tracked_source(
    practice_repo: Path,
) -> None:
    tracked = practice_repo / "src/algo/arrays/first.py"
    before = tracked.read_text()

    metadata, action, archived = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )

    workspace = practice_repo / ".challenges/workspace"
    candidate = workspace / "first.py"
    assert action == "created"
    assert archived is None
    assert tracked.read_text() == before
    assert candidate.is_file()
    assert practice.PRACTICE_LOCK in candidate.read_text()
    assert "secret = sum(values)" not in candidate.read_text()
    assert metadata["source"] == ".challenges/workspace/first.py"
    assert metadata["candidate_test"] == (
        ".challenges/workspace/test_first_candidate.py"
    )
    assert (
        "# from algo.arrays.first import solve"
        in (workspace / "test_first_candidate.py").read_text()
    )
    assert (workspace / "practice_plugin.py").is_file()
    assert (workspace / "repl.py").is_file()
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=practice_repo,
        text=True,
        capture_output=True,
        check=True,
    )
    assert status.stdout == ""


def test_present_reads_committed_statement_without_creating_workspace(
    practice_repo: Path,
) -> None:
    tracked = practice_repo / "src/algo/arrays/first.py"
    tracked.write_text('"""Working-tree notes must not leak."""\n')

    statement = practice.present_problem(practice_repo, "arrays", "first")

    assert "arrays / first" in statement
    assert "Problem:" in statement
    assert "Approach:" not in statement
    assert "Working-tree notes" not in statement
    assert not (practice_repo / ".challenges/workspace").exists()


def test_problem_selection_rejects_half_an_explicit_pair(practice_repo: Path) -> None:
    with pytest.raises(practice.PracticeError, match="provide both topic and problem"):
        practice.select_problem(practice_repo, "arrays", None)


def test_reference_reads_committed_solution_without_restoring_tracked_file(
    practice_repo: Path,
) -> None:
    tracked = practice_repo / "src/algo/arrays/first.py"
    tracked.write_text('"""Candidate work in progress."""\n')

    reference = practice.reference_solution(practice_repo, "arrays", "first")

    assert "secret = sum(values)" in reference
    assert "Candidate work in progress" not in reference
    assert tracked.read_text() == '"""Candidate work in progress."""\n'


def test_same_session_resumes_without_overwriting_candidate_work(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    candidate_test = practice_repo / str(metadata["candidate_test"])
    candidate.write_text(candidate.read_text() + "\n# candidate reasoning survives\n")
    candidate_test.write_text(
        candidate_test.read_text() + "\n# candidate test survives\n"
    )

    resumed, action, archived = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )

    assert action == "resumed"
    assert archived is None
    assert resumed == metadata
    assert "candidate reasoning survives" in candidate.read_text()
    assert "candidate test survives" in candidate_test.read_text()


def _fill_seed(text: str, seed: str) -> str:
    return text.replace(seed, f"{seed} candidate reasoning")


def test_next_step_reports_one_action_for_resumed_state(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])

    assert practice.next_step(practice_repo, metadata) == (
        "THINK",
        "Fill REPEAT, save, then run /continue.",
    )

    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(text)

    assert practice.next_step(practice_repo, metadata) == (
        "THINK",
        "Delete the THINKING GATE yourself, then implement below it.",
    )


def test_next_step_moves_from_build_to_verify(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"]:
        text = _fill_seed(text, str(seed))
    text = text.replace(practice.PRACTICE_LOCK + "\n", "")
    candidate.write_text(
        text.replace("raise NotImplementedError", "return sum(values)")
    )
    candidate_test = practice_repo / str(metadata["candidate_test"])
    candidate_test.write_text(
        "def test_candidate_example() -> None:\n    assert True\n"
    )

    assert practice.next_step(practice_repo, metadata) == (
        "CLOSE",
        "Run just practice-test, reconcile comments with code, then use just practice-finish.",
    )


def test_next_step_reports_candidate_test_syntax_error(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(text.replace(practice.PRACTICE_LOCK + "\n", ""))
    (practice_repo / str(metadata["candidate_test"])).write_text("def broken(:\n")

    assert practice.next_step(practice_repo, metadata) == (
        "BUILD",
        "Fix the syntax error in your test file, then run /continue.",
    )


def test_finish_pairs_rep_log_and_spaced_update_idempotently(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(practice_repo, "clarp", "arrays", "first")

    assert practice.finish_session(practice_repo, metadata, "h0 trace the edge") == 0
    assert practice.finish_session(practice_repo, metadata, "h0 trace the edge") == 0

    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    progress = (practice_repo / ".challenges/progress.md").read_text().splitlines()
    assert len(reps) == 1
    assert "clarp arrays/first h0 trace the edge" in reps[0]
    assert len(progress) == 1
    assert progress[0].startswith("- [x] arrays/first ")


def test_finish_preserves_progress_for_similar_problem_name(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(practice_repo, "clarp", "arrays", "first")
    _write(
        practice_repo / ".challenges/progress.md",
        "- [x] arrays/first_extended 2026-01-01\n",
    )

    practice.finish_session(practice_repo, metadata, "h0 trace the edge")

    progress = (practice_repo / ".challenges/progress.md").read_text()
    assert "arrays/first_extended 2026-01-01" in progress
    assert "arrays/first " in progress


def test_mode_and_problem_switch_archive_then_reset_workspace(
    practice_repo: Path,
) -> None:
    first, _, _ = practice.prepare_session(practice_repo, "reacto", "arrays", "first")
    first_candidate = practice_repo / str(first["source"])
    first_candidate.write_text(first_candidate.read_text() + "\n# reacto trail\n")

    clarp, action, reacto_archive = practice.prepare_session(
        practice_repo, "clarp", "arrays", "first"
    )

    assert action == "created"
    assert reacto_archive is not None
    assert "reacto trail" in (reacto_archive / "first.py").read_text()
    clarp_candidate = practice_repo / str(clarp["source"])
    assert "# CLARIFY:" in clarp_candidate.read_text()
    assert "# REPEAT:" not in clarp_candidate.read_text()
    assert "reacto trail" not in clarp_candidate.read_text()
    assert clarp_candidate.read_text().count(practice.PRACTICE_LOCK) == 1

    clarp_candidate.write_text(clarp_candidate.read_text() + "\n# first trail\n")
    second, action, first_archive = practice.prepare_session(
        practice_repo, "clarp", "arrays", "second"
    )

    assert action == "created"
    assert first_archive is not None
    assert "first trail" in (first_archive / "first.py").read_text()
    second_candidate = practice_repo / str(second["source"])
    assert second_candidate.name == "second.py"
    assert "first trail" not in second_candidate.read_text()
    assert not (practice_repo / ".challenges/workspace/first.py").exists()


def test_locked_session_refuses_to_run_tests(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )

    def unexpected_run(*args: object, **kwargs: object) -> None:
        raise AssertionError("pytest must not launch while the thinking gate is locked")

    monkeypatch.setattr(practice.subprocess, "run", unexpected_run)
    with pytest.raises(practice.PracticeError, match="thinking gate is still locked"):
        practice.run_tests(practice_repo, metadata)


def test_deleting_gate_before_filling_comments_still_refuses_tests(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    candidate.write_text(candidate.read_text().replace(practice.PRACTICE_LOCK, ""))

    def unexpected_run(*args: object, **kwargs: object) -> None:
        raise AssertionError("pytest must not launch before reasoning is present")

    monkeypatch.setattr(practice.subprocess, "run", unexpected_run)
    with pytest.raises(
        practice.PracticeError,
        match="gate was removed before RESTATE, EXAMPLE, INVARIANT, APPROACH",
    ):
        practice.run_tests(practice_repo, metadata)


def test_unlocked_session_tests_candidate_instead_of_reference(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError", "return sum(values)"
        )
        + "\nCANDIDATE_ONLY = True\n"
    )
    candidate_test = practice_repo / str(metadata["candidate_test"])
    candidate_test.write_text(
        "from algo.arrays.first import CANDIDATE_ONLY\n\n\n"
        "def test_candidate_module_is_installed() -> None:\n"
        "    assert CANDIDATE_ONLY is True\n"
    )

    assert practice.run_tests(practice_repo, metadata) == 0


def test_open_session_targets_reasoning_line_and_candidate_test(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "umpire", "arrays", "first"
    )
    calls: list[tuple[list[str], Path, bool]] = []

    def fake_run(args: list[str], *, cwd: Path, check: bool) -> SimpleNamespace:
        calls.append((args, cwd, check))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(practice.shutil, "which", lambda _name: "/mock/code")
    monkeypatch.setattr(practice.subprocess, "run", fake_run)

    assert practice.open_session(practice_repo, metadata)
    source = str(metadata["source"])
    source_path = practice_repo / source
    first_seed = str(metadata["seeds"][0]).split(":", 1)[0]
    line = next(
        number
        for number, text in enumerate(source_path.read_text().splitlines(), start=1)
        if first_seed in text
    )
    assert calls == [
        (
            [
                "/mock/code",
                "--reuse-window",
                str(metadata["candidate_test"]),
                "--goto",
                f"{source}:{line}",
            ],
            practice_repo,
            False,
        )
    ]


def test_watch_includes_gitignored_workspace(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    calls: list[tuple[str, list[str], dict[str, str]]] = []

    monkeypatch.setattr(practice, "_require_unlocked", lambda _root, _meta: None)
    monkeypatch.setattr(practice.shutil, "which", lambda _name: "/mock/watchexec")

    def fake_execvpe(executable: str, args: list[str], env: dict[str, str]) -> None:
        calls.append((executable, args, env))

    monkeypatch.setattr(practice.os, "execvpe", fake_execvpe)

    assert practice.run_watch(practice_repo, metadata) == 1
    assert calls[0][0] == "/mock/watchexec"
    assert "--ignore-nothing" in calls[0][1]
    assert calls[0][1][calls[0][1].index("-w") + 1] == str(
        practice_repo / ".challenges/workspace"
    )
