"""Tests for the isolated, editor-first practice workspace."""

from __future__ import annotations

import ast
import fcntl
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from types import SimpleNamespace
from typing import Any

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import practice_workspace as practice  # type: ignore[import-not-found]  # noqa: E402
from core42 import (  # type: ignore[import-not-found]  # noqa: E402
    CORE_42,
    PRACTICE_TARGETS,
)

SOURCE = '''"""arrays / {problem}

Problem:
    Return the sum of the values.

Approach:
    This committed explanation must not reach the cold workspace.
"""

from dataclasses import dataclass


@dataclass
class Wrapper:
    value: int


def solve(values: list[int]) -> int:
    """Return the sum."""
    secret = _support(values)
    return secret


def alternate(values: list[int]) -> int:
    """Committed alternate used by the complete reference test file."""
    return _support(values)


def _support(values: list[int]) -> int:
    return sum(values)
'''


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _lock_is_available(path: Path) -> bool:
    if not path.is_file():
        return False
    with path.open("r+") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return True


def _wait_for_lock_release(path: Path, timeout: float = 3) -> bool:
    deadline = time.monotonic() + timeout
    while not _lock_is_available(path):
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.02)
    return True


def _kill_lock_holder(path: Path) -> None:
    if _lock_is_available(path):
        return
    try:
        pid = int(path.read_text().split()[0])
        os.kill(pid, signal.SIGKILL)
    except OSError, ValueError:
        pass


def _commit_fixture(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
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
            "commit",
            "-qm",
            "fixture",
        ],
        cwd=root,
        check=True,
    )


def _reference_target_only(candidate: str, committed: str, target: str) -> str:
    """Put only the committed target body into an otherwise cold candidate."""

    def selected_function(source: str) -> ast.FunctionDef | ast.AsyncFunctionDef:
        node = next(
            (
                item
                for item in ast.parse(source).body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                and item.name == target
            ),
            None,
        )
        assert node is not None
        return node

    reference_node = selected_function(committed)
    implementation = reference_node.body
    if (
        implementation
        and isinstance(implementation[0], ast.Expr)
        and isinstance(implementation[0].value, ast.Constant)
        and isinstance(implementation[0].value.value, str)
    ):
        implementation = implementation[1:]
    assert implementation

    candidate_node = selected_function(candidate)
    cold_body = candidate_node.body[-1]
    assert isinstance(cold_body, ast.Raise)
    reference_lines = committed.splitlines(keepends=True)
    candidate_lines = candidate.splitlines(keepends=True)
    start = implementation[0].lineno - 1
    end = implementation[-1].end_lineno or implementation[-1].lineno
    cold_end = cold_body.end_lineno or cold_body.lineno
    candidate_lines[cold_body.lineno - 1 : cold_end] = reference_lines[start:end]
    return "".join(candidate_lines)


def test_every_core_problem_has_a_real_practice_target() -> None:
    core = {
        (topic, problem) for topic, problems in CORE_42.items() for problem in problems
    }
    assert len(core) == 43
    assert core <= set(PRACTICE_TARGETS)


def test_every_catalog_algorithm_can_start_with_one_explicit_target(
    tmp_path: Path,
) -> None:
    catalog = {
        (path.parent.name, path.stem)
        for path in (REPO_ROOT / "src/algo").glob("*/*.py")
        if path.name != "__init__.py"
    }
    assert len(catalog) == 71
    assert set(PRACTICE_TARGETS) == catalog

    for topic, problem in sorted(catalog):
        source = (REPO_ROOT / f"src/algo/{topic}/{problem}.py").read_text()
        target = PRACTICE_TARGETS[(topic, problem)]
        assert (REPO_ROOT / f"tests/{topic}/test_{problem}.py").is_file()
        assert target in practice._public_symbols(source)
        assert practice._practice_target(topic, problem, source) == target
        candidate = practice.render_candidate(
            source, practice.PARADIGMS["comments"], target
        )
        candidate_tree = ast.parse(candidate)
        visible_definitions = [
            node
            for node in candidate_tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
        assert visible_definitions[-1].name == target
        assert {node.name for node in visible_definitions[:-1]} <= {
            "GraphNode",
            "ListNode",
            "TreeNode",
        }
        loaded_names = {
            node.id
            for node in ast.walk(candidate_tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }
        for node in candidate_tree.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            for alias in node.names:
                assert (alias.asname or alias.name.split(".", 1)[0]) in loaded_names
        assert all(
            ast.get_docstring(node, clean=False) is None
            for definition in visible_definitions
            for node in ast.walk(definition)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        )
        if isinstance(visible_definitions[-1], ast.ClassDef):
            assert all(
                not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                or node.name == "__init__"
                or not node.name.startswith("_")
                for node in visible_definitions[-1].body
            )
        namespace: dict[str, object] = {}
        exec(compile(candidate, f"{topic}/{problem}.py", "exec"), namespace)
        assert target in namespace
        assert candidate.count(practice.PRACTICE_LOCK) == 1
        output = tmp_path / topic / f"{problem}.py"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(candidate)

    lint = subprocess.run(
        ["ruff", "check", "--isolated", "--select", "F821", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert lint.returncode == 0, lint.stdout + lint.stderr


def test_candidate_renderer_hides_named_alternates_and_strategy_imports() -> None:
    kth = practice.render_candidate(
        (REPO_ROOT / "src/algo/heaps/kth_largest.py").read_text(),
        practice.PARADIGMS["comments"],
        "find_kth_largest",
    )
    topo = practice.render_candidate(
        (REPO_ROOT / "src/algo/graphs/topological_sort.py").read_text(),
        practice.PARADIGMS["comments"],
        "topological_sort_kahn",
    )
    csp = practice.render_candidate(
        (REPO_ROOT / "src/algo/dp/constraint_satisfaction.py").read_text(),
        practice.PARADIGMS["comments"],
        "CSP",
    )

    assert "heapq" not in kth
    assert "nlargest" not in kth
    assert "dfs" not in topo.lower()
    assert "from collections.abc import Callable, Mapping, Sequence" in csp


@pytest.fixture
def practice_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setitem(practice.PRACTICE_TARGETS, ("arrays", "first"), "solve")
    monkeypatch.setitem(practice.PRACTICE_TARGETS, ("arrays", "second"), "solve")
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
                f"from algo.arrays.{problem} import alternate, solve\n\n\n"
                f"def test_{problem}() -> None:\n"
                "    assert solve([1, 2, 3]) == 6\n\n\n"
                "def test_committed_alternate() -> None:\n"
                "    assert alternate([1, 2, 3]) == 6\n"
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
    assert "return _support(values)" not in candidate.read_text()
    assert "def alternate" not in candidate.read_text()
    assert "from dataclasses import dataclass" not in candidate.read_text()
    assert metadata["schema"] == 4
    assert uuid.UUID(metadata["session_id"]).version == 4
    assert metadata["target"] == "solve"
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


def test_problem_selection_draws_first_due_and_rejects_empty_queue(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        practice, "ranked_queue", lambda _path: [(10, "arrays", "first")]
    )
    assert practice.select_problem(practice_repo) == ("arrays", "first")

    monkeypatch.setattr(practice, "ranked_queue", lambda _path: [])
    with pytest.raises(practice.PracticeError, match="queue is empty"):
        practice.select_problem(practice_repo)


def test_reference_reads_committed_solution_without_restoring_tracked_file(
    practice_repo: Path,
) -> None:
    tracked = practice_repo / "src/algo/arrays/first.py"
    tracked.write_text('"""Candidate work in progress."""\n')

    reference = practice.reference_solution(practice_repo, "arrays", "first")

    assert "secret = _support(values)" in reference
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


def _complete_session(root: Path, metadata: dict[str, Any]) -> None:
    candidate = root / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError", "return sum(values)"
        )
    )
    (root / str(metadata["candidate_test"])).write_text(
        "def test_candidate_example() -> None:\n    assert True\n"
    )


def test_next_step_reports_one_action_for_resumed_state(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])

    assert practice.next_step(practice_repo, metadata) == (
        "THINK",
        "Write your reasoning in the REPEAT source comment, save, then run /continue.",
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
    _complete_session(practice_repo, metadata)

    assert practice.finish_session(practice_repo, metadata, "h0 trace the edge") == 0
    assert practice.finish_session(practice_repo, metadata, "h0 trace the edge") == 0

    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    progress = (practice_repo / ".challenges/progress.md").read_text().splitlines()
    assert len(reps) == 1
    assert "clarp arrays/first fix: h0 trace the edge" in reps[0]
    assert len(progress) == 1
    assert progress[0].startswith("- [x] arrays/first ")


def test_status_remains_available_while_finish_runs_candidate_tests(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)
    started = Event()
    release = Event()

    def slow_pytest(
        root: Path, current: dict[str, Any], before: dict[str, str]
    ) -> practice.TestRun:
        started.set()
        assert release.wait(timeout=5)
        return practice.TestRun(
            returncode=0,
            before=before,
            after=practice._test_input_digests(root, current),
        )

    monkeypatch.setattr(practice, "_execute_test_run", slow_pytest)
    with ThreadPoolExecutor(max_workers=2) as pool:
        closing = pool.submit(
            practice.finish_session, practice_repo, metadata, "trace the edge"
        )
        assert started.wait(timeout=2)
        reading = pool.submit(practice.current_metadata, practice_repo)
        try:
            assert reading.result(timeout=1)["session_id"] == metadata["session_id"]
        finally:
            release.set()
        assert closing.result(timeout=5) == 0


def test_finish_preserves_progress_for_similar_problem_name(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(practice_repo, "clarp", "arrays", "first")
    _complete_session(practice_repo, metadata)
    _write(
        practice_repo / ".challenges/progress.md",
        "- [x] arrays/first_extended 2026-01-01\n",
    )

    practice.finish_session(practice_repo, metadata, "h0 trace the edge")

    progress = (practice_repo / ".challenges/progress.md").read_text()
    assert "arrays/first_extended 2026-01-01" in progress
    assert "arrays/first " in progress


def test_locked_session_can_close_without_claiming_tests_ran(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )

    assert (
        practice.finish_session(
            practice_repo, metadata, "C1 starts this free-text note"
        )
        == 0
    )

    finished = practice.current_metadata(practice_repo)
    assert finished["finish_state"] == "THINK"
    assert finished["test_outcome"] == "not_run"
    assert finished["finish_note"] == "C1 starts this free-text note"
    assert (practice_repo / ".challenges/reps.md").is_file()
    assert (practice_repo / ".challenges/progress.md").is_file()


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

    monkeypatch.setattr(practice, "_execute_test_run", unexpected_run)
    with pytest.raises(
        practice.PracticeError,
        match="write your reasoning in the RESTATE, EXAMPLE, INVARIANT, APPROACH source comments",
    ):
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

    monkeypatch.setattr(practice, "_execute_test_run", unexpected_run)
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


def test_candidate_is_active_during_test_module_import(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError",
            "if values:\n        return sum(values)\n    return -1",
        )
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "from algo.arrays.first import solve\n\n"
        "EMPTY_RESULT = solve([])\n\n\n"
        "def test_empty_input() -> None:\n"
        "    assert EMPTY_RESULT == 0\n"
    )

    assert practice.run_tests(practice_repo, metadata) == 1


def test_ambient_pytest_options_cannot_turn_failures_into_collection_only(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
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
            "raise NotImplementedError", "return 0"
        )
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "def test_candidate_smoke() -> None:\n    assert True\n"
    )
    monkeypatch.setenv("PYTEST_ADDOPTS", "--collect-only")
    monkeypatch.setenv("PYTEST_PLUGINS", "untrusted_plugin")

    env = practice._practice_env(practice_repo)
    assert "PYTEST_ADDOPTS" not in env
    assert "PYTEST_PLUGINS" not in env
    assert env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"
    assert practice.run_tests(practice_repo, metadata) == 1


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


def test_watch_runs_guarded_recipe_for_workspace_and_reference_test(
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
    args = calls[0][1]
    assert "--ignore-nothing" in args
    watch_paths = [args[index + 1] for index, arg in enumerate(args) if arg == "-w"]
    assert watch_paths == [
        str(practice_repo / ".challenges/workspace"),
        str(practice_repo / str(metadata["reference_test"])),
    ]
    assert args[args.index("--") + 1 :] == ["just", "practice-test"]


def test_watch_missing_optional_helper_is_actionable(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    monkeypatch.setattr(practice, "_require_unlocked", lambda _root, _meta: None)
    monkeypatch.setattr(practice.shutil, "which", lambda _name: None)

    with pytest.raises(practice.PracticeError, match="use `just practice-test`"):
        practice.run_watch(practice_repo, metadata)


def test_candidate_source_syntax_error_stays_in_build(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(text.replace(practice.PRACTICE_LOCK + "\n", "") + "\nif (\n")

    assert practice.next_step(practice_repo, metadata) == (
        "BUILD",
        "Fix the syntax error in your source file, then run /continue.",
    )


def test_nested_test_function_does_not_count_as_candidate_test(
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
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "def helper() -> None:\n"
        "    def test_nested_does_not_collect() -> None:\n"
        "        assert True\n"
    )

    assert practice.next_step(practice_repo, metadata)[0] == "BUILD"


def test_pytest_class_method_counts_as_candidate_test(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError", "return sum(values)"
        )
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "class TestCandidate:\n"
        "    def test_example(self) -> None:\n"
        "        assert True\n"
    )

    assert practice.next_step(practice_repo, metadata)[0] == "CLOSE"


@pytest.mark.parametrize(
    "candidate_tests",
    [
        "__test__ = False\n\n\ndef test_hidden() -> None:\n    assert True\n",
        (
            "class TestHidden:\n"
            "    __test__ = False\n\n"
            "    def test_hidden(self) -> None:\n"
            "        assert True\n"
        ),
    ],
)
def test_uncollected_tests_do_not_advance_state(
    practice_repo: Path, candidate_tests: str
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError", "return sum(values)"
        )
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(candidate_tests)

    assert practice.next_step(practice_repo, metadata)[0] == "BUILD"


def test_candidate_helper_stub_does_not_hide_implemented_target(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(
        text.replace(practice.PRACTICE_LOCK + "\n", "").replace(
            "raise NotImplementedError", "return sum(values)", 1
        )
        + "\n\ndef optional_backend() -> None:\n    raise NotImplementedError\n"
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "def test_candidate_example() -> None:\n    assert True\n"
    )

    assert practice.next_step(practice_repo, metadata)[0] == "CLOSE"


def test_committed_private_support_is_not_injected_into_candidate_tests(
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
            "raise NotImplementedError", "return _support(values)", 1
        )
    )
    (practice_repo / str(metadata["candidate_test"])).write_text(
        "def test_candidate_smoke() -> None:\n    assert True\n"
    )

    plugin = (practice_repo / str(metadata["plugin"])).read_text()
    assert "SUPPORT: tuple[str, ...] = ()" in plugin
    assert "getattr(reference, name)" not in plugin
    assert practice.run_tests(practice_repo, metadata) == 1


@pytest.mark.parametrize(
    ("topic", "problem", "target", "omitted_helper"),
    [
        ("recursion", "flatten_nested_list", "flatten_recursive", "_flatten_helper"),
        ("graphs", "number_of_islands", "num_islands", "_bfs"),
        ("graphs", "minimum_spanning_tree", "kruskal", "UnionFind"),
    ],
)
def test_real_helper_dependent_target_cannot_use_committed_implementation(
    tmp_path: Path,
    topic: str,
    problem: str,
    target: str,
    omitted_helper: str,
) -> None:
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    test_rel = Path("tests") / topic / f"test_{problem}.py"
    committed = (REPO_ROOT / source_rel).read_text()
    _write(tmp_path / ".gitignore", ".challenges/\n")
    _write(tmp_path / "src/algo/__init__.py", "")
    _write(tmp_path / f"src/algo/{topic}/__init__.py", "")
    _write(tmp_path / source_rel, committed)
    _write(tmp_path / test_rel, (REPO_ROOT / test_rel).read_text())
    _commit_fixture(tmp_path)

    metadata, _, _ = practice.prepare_session(tmp_path, "comments", topic, problem)
    candidate_path = tmp_path / str(metadata["source"])
    candidate = _reference_target_only(candidate_path.read_text(), committed, target)
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        candidate = _fill_seed(candidate, str(seed))
    candidate = candidate.replace(practice.PRACTICE_LOCK + "\n", "")
    candidate_path.write_text(candidate)

    assert all(
        not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        or node.name != omitted_helper
        for node in ast.parse(candidate).body
    )
    assert practice.run_tests(tmp_path, metadata) == 1


def test_repl_exposes_only_target_and_omits_committed_helpers(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [
            str(practice_repo / practice.WORKSPACE_REL),
            str(practice_repo / "src"),
        ]
    )
    code = (
        "import runpy\n"
        f"ns = runpy.run_path({str(practice_repo / str(metadata['repl']))!r})\n"
        "assert 'solve' in ns\n"
        "assert '_support' not in ns\n"
        "assert 'alternate' not in ns\n"
        "assert not hasattr(ns['candidate'], '_support')\n"
        "assert not hasattr(ns['candidate'], 'alternate')\n"
    )

    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=practice_repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr


def test_pytest_args_use_the_complete_reference_module(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )

    args = practice._pytest_args(metadata)
    assert args[args.index("-p") + 1] == "practice_plugin"
    assert str(metadata["reference_test"]) in args
    assert all("::" not in arg for arg in args)


def test_modified_reference_tests_are_refused_before_pytest(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)
    reference = practice_repo / str(metadata["reference_test"])
    reference.write_text("def test_false_pass() -> None:\n    assert True\n")

    def unexpected_run(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("pytest must not run with edited reference tests")

    monkeypatch.setattr(practice, "_execute_test_run", unexpected_run)
    with pytest.raises(practice.PracticeError, match="differ from committed HEAD"):
        practice.run_tests(practice_repo, metadata)


def test_metadata_rejects_noncanonical_paths(practice_repo: Path) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    metadata["source"] = "src/algo/arrays/first.py"
    (practice_repo / ".challenges/workspace/session.json").write_text(
        json.dumps(metadata) + "\n"
    )

    with pytest.raises(practice.PracticeError, match="source is not canonical"):
        practice.current_metadata(practice_repo)


def test_metadata_rejects_symlinked_workspace(practice_repo: Path) -> None:
    practice.prepare_session(practice_repo, "reacto", "arrays", "first")
    workspace = practice_repo / practice.WORKSPACE_REL
    real = workspace.with_name("workspace-real")
    workspace.rename(real)
    workspace.symlink_to(real, target_is_directory=True)

    with pytest.raises(practice.PracticeError, match="workspace cannot be a symlink"):
        practice.current_metadata(practice_repo)


@pytest.mark.parametrize("operation", ["start", "log", "complete", "finish_non_editor"])
def test_symlinked_private_state_never_writes_outside_repository(
    practice_repo: Path, operation: str
) -> None:
    outside = practice_repo.with_name(f"{practice_repo.name}-{operation}-outside")
    outside.mkdir()
    (practice_repo / practice.STATE_REL).symlink_to(outside, target_is_directory=True)

    def action() -> object:
        if operation == "start":
            return practice.prepare_session(
                practice_repo, "comments", "arrays", "first"
            )
        if operation == "log":
            return practice.log_rep(
                practice_repo,
                "talk arrays/first C1 L1 A1 R1 P1 h0 trace the edge",
            )
        if operation == "complete":
            return practice.complete_problem(practice_repo, "arrays", "first")
        return practice.finish_non_editor(
            practice_repo,
            "arrays",
            "first",
            "talk arrays/first C1 L1 A1 R1 P1 h0 trace the edge",
        )

    with pytest.raises(practice.PracticeError, match="cannot be a symlink"):
        action()

    assert list(outside.iterdir()) == []


def test_symlinked_private_log_and_lock_are_refused(practice_repo: Path) -> None:
    state = practice_repo / practice.STATE_REL
    state.mkdir()
    outside = practice_repo.with_name(f"{practice_repo.name}-state-files-outside")
    outside.mkdir()
    (state / "reps.md").symlink_to(outside / "reps.md")

    with pytest.raises(practice.PracticeError, match=r"reps\.md cannot be a symlink"):
        practice.log_rep(
            practice_repo,
            "talk arrays/first C1 L1 A1 R1 P1 h0 trace the edge",
        )
    assert not (outside / "reps.md").exists()

    (state / "reps.md").unlink()
    (state / ".practice.lock").unlink()
    (state / ".practice.lock").symlink_to(outside / "lock")
    with pytest.raises(practice.PracticeError, match="lock cannot be a symlink"):
        practice.complete_problem(practice_repo, "arrays", "first")
    assert not (outside / "lock").exists()


def test_closeout_recovery_confines_every_destination_before_replay(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    original_replace = practice._replace_file

    class InjectedCrash(BaseException):
        pass

    def crash_after_journal(path: Path, text: str) -> None:
        original_replace(path, text)
        if path == practice_repo / practice.JOURNAL_REL:
            raise InjectedCrash

    monkeypatch.setattr(practice, "_replace_file", crash_after_journal)
    with pytest.raises(InjectedCrash):
        practice.finish_session(practice_repo, metadata, "trace the edge")
    assert (practice_repo / practice.JOURNAL_REL).is_file()
    assert not (practice_repo / ".challenges/reps.md").exists()
    assert not (practice_repo / ".challenges/progress.md").exists()

    monkeypatch.setattr(practice, "_replace_file", original_replace)
    workspace = practice_repo / practice.WORKSPACE_REL
    workspace.rename(workspace.with_name("workspace-preserved"))
    outside = practice_repo.with_name(f"{practice_repo.name}-recovery-outside")
    outside.mkdir()
    workspace.symlink_to(outside, target_is_directory=True)

    with pytest.raises(practice.PracticeError, match="workspace cannot be a symlink"):
        practice.current_metadata(practice_repo)

    assert list(outside.iterdir()) == []
    assert not (practice_repo / ".challenges/reps.md").exists()
    assert not (practice_repo / ".challenges/progress.md").exists()
    assert (practice_repo / practice.JOURNAL_REL).is_file()


@pytest.mark.parametrize("field", ["source", "plugin"])
def test_metadata_rejects_symlinked_required_file(
    practice_repo: Path, field: str
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    path = practice_repo / str(metadata[field])
    path.unlink()
    path.symlink_to(practice_repo / "src/algo/arrays/first.py")

    with pytest.raises(
        practice.PracticeError, match="required file is missing or unconfined"
    ):
        practice.current_metadata(practice_repo)


def test_invalid_partial_workspace_is_archived_and_rebuilt(
    practice_repo: Path,
) -> None:
    workspace = practice_repo / ".challenges/workspace"
    _write(workspace / "partial.txt", "candidate work\n")

    metadata, action, archived = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )

    assert action == "created"
    assert archived is not None
    assert (archived / "partial.txt").read_text() == "candidate work\n"
    assert metadata["schema"] == 4


def test_failed_build_never_replaces_the_visible_workspace(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    candidate.write_text(candidate.read_text() + "\n# preserve me\n")

    def fail_candidate_test(*_args: object, **_kwargs: object) -> str:
        raise OSError("injected render failure")

    monkeypatch.setattr(practice, "_candidate_test", fail_candidate_test)
    with pytest.raises(OSError, match="injected render failure"):
        practice.prepare_session(practice_repo, "clarp", "arrays", "second", fresh=True)

    assert "preserve me" in candidate.read_text()
    assert not list((practice_repo / ".challenges").glob(".workspace-*.tmp"))


def test_finished_session_starts_a_distinct_new_rep(practice_repo: Path) -> None:
    first, _, _ = practice.prepare_session(practice_repo, "reacto", "arrays", "first")
    practice.finish_session(practice_repo, first, "trace before optimizing")

    second, action, archived = practice.prepare_session(
        practice_repo, "reacto", "arrays", "first"
    )

    assert action == "created"
    assert archived is not None
    assert second["session_id"] != first["session_id"]


def test_stale_session_cannot_close_a_new_workspace(practice_repo: Path) -> None:
    first, _, _ = practice.prepare_session(practice_repo, "reacto", "arrays", "first")
    practice.prepare_session(practice_repo, "reacto", "arrays", "second", fresh=True)

    with pytest.raises(practice.PracticeError, match="stale rep session"):
        practice.finish_session(practice_repo, first, "trace before optimizing")


def test_failing_close_state_is_logged_with_failed_outcome(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(practice_repo, "clarp", "arrays", "first")
    _complete_session(practice_repo, metadata)
    candidate = practice_repo / str(metadata["source"])
    candidate.write_text(
        candidate.read_text().replace("return sum(values)", "return 0")
    )

    assert practice.finish_session(practice_repo, metadata, "trace the failure") == 0

    finished = practice.current_metadata(practice_repo)
    assert finished["finish_state"] == "CLOSE"
    assert finished["test_outcome"] == "failed"
    assert set(finished["test_inputs_before"]) == set(practice.TEST_INPUT_KEYS)
    assert set(finished["test_inputs_after"]) == set(practice.TEST_INPUT_KEYS)


def test_distinct_sessions_keep_duplicate_human_readable_reps(
    practice_repo: Path,
) -> None:
    first, _, _ = practice.prepare_session(practice_repo, "comments", "arrays", "first")
    practice.finish_session(practice_repo, first, "trace the edge")
    second, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    practice.finish_session(practice_repo, second, "trace the edge")

    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    assert len(reps) == 2
    assert reps[0] == reps[1]


@pytest.mark.parametrize("crash_name", ["reps.md", "progress.md", "session.json"])
def test_closeout_journal_recovers_each_sequential_replace_exactly_once(
    practice_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    crash_name: str,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    original_replace = practice._replace_file

    class InjectedCrash(BaseException):
        pass

    crashed = False

    def crash_after_replace(path: Path, text: str) -> None:
        nonlocal crashed
        original_replace(path, text)
        if path.name == crash_name and not crashed:
            crashed = True
            raise InjectedCrash

    monkeypatch.setattr(practice, "_replace_file", crash_after_replace)
    with pytest.raises(InjectedCrash):
        practice.finish_session(practice_repo, metadata, "trace the edge")
    assert (practice_repo / practice.JOURNAL_REL).is_file()

    monkeypatch.setattr(practice, "_replace_file", original_replace)
    finished = practice.current_metadata(practice_repo)
    assert finished["finished_at"]
    assert not (practice_repo / practice.JOURNAL_REL).exists()
    assert practice.finish_session(practice_repo, metadata, "trace the edge") == 0
    assert len((practice_repo / ".challenges/reps.md").read_text().splitlines()) == 1
    assert (
        len((practice_repo / ".challenges/progress.md").read_text().splitlines()) == 1
    )


@pytest.mark.parametrize("changed_key", ["reference_test", "plugin"])
def test_test_result_is_stale_when_any_non_candidate_input_changes(
    practice_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    changed_key: str,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    text = candidate.read_text()
    for seed in metadata["seeds"][: len(metadata["pre_code_labels"])]:
        text = _fill_seed(text, str(seed))
    candidate.write_text(text.replace(practice.PRACTICE_LOCK + "\n", ""))

    def mutating_run(
        root: Path, current: dict[str, Any], before: dict[str, str]
    ) -> practice.TestRun:
        path = practice_repo / str(metadata[changed_key])
        path.write_text(path.read_text() + "\n# changed during test\n")
        return practice.TestRun(
            returncode=0,
            before=before,
            after=practice._test_input_digests(root, current),
        )

    monkeypatch.setattr(practice, "_execute_test_run", mutating_run)

    assert practice.run_tests(practice_repo, metadata) == 3
    if changed_key == "plugin":
        assert (
            practice.current_metadata(practice_repo)["session_id"]
            == metadata["session_id"]
        )


def test_candidate_tests_run_without_holding_the_state_lock(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)

    def nested_state_write(
        root: Path, current: dict[str, Any], before: dict[str, str]
    ) -> practice.TestRun:
        assert practice.complete_problem(root, "arrays", "second") == 0
        return practice.TestRun(
            returncode=0,
            before=before,
            after=practice._test_input_digests(root, current),
        )

    monkeypatch.setattr(practice, "_execute_test_run", nested_state_write)

    assert practice.run_tests(practice_repo, metadata) == 0


def _spawn_test_process_tree(
    child_lock: Path, *, parent_returncode: int | None, child_ignores_term: bool
) -> subprocess.Popen[bytes]:
    signal_setup = (
        "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n" if child_ignores_term else ""
    )
    child_source = (
        "import fcntl\n"
        "import os\n"
        "import signal\n"
        "import time\n"
        "from pathlib import Path\n"
        f"{signal_setup}"
        'path = Path(os.environ["PRACTICE_CHILD_LOCK"])\n'
        'with path.open("w") as handle:\n'
        "    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)\n"
        '    handle.write(f"{os.getpid()} {os.getpgrp()}")\n'
        "    handle.flush()\n"
        "    time.sleep(30)\n"
    )
    parent_end = (
        f"raise SystemExit({parent_returncode})"
        if parent_returncode is not None
        else "time.sleep(30)"
    )
    parent_source = (
        "import os\n"
        "import subprocess\n"
        "import sys\n"
        "import time\n"
        "from pathlib import Path\n"
        f"child_source = {child_source!r}\n"
        'subprocess.Popen([sys.executable, "-c", child_source])\n'
        'path = Path(os.environ["PRACTICE_CHILD_LOCK"])\n'
        "deadline = time.monotonic() + 2\n"
        "while (not path.is_file() or not path.read_text()) "
        "and time.monotonic() < deadline:\n"
        "    time.sleep(0.01)\n"
        f"{parent_end}\n"
    )
    proc = subprocess.Popen(
        [sys.executable, "-c", parent_source],
        env=os.environ | {"PRACTICE_CHILD_LOCK": str(child_lock)},
        start_new_session=True,
    )
    deadline = time.monotonic() + 2
    while (not child_lock.is_file() or not child_lock.read_text()) and (
        time.monotonic() < deadline
    ):
        time.sleep(0.01)
    if not child_lock.is_file() or not child_lock.read_text():
        practice._sweep_test_process_group(proc)
        raise AssertionError("background child did not acquire its lock")
    return proc


@pytest.mark.parametrize("parent_returncode", [0, 7])
def test_completed_parent_sweeps_background_child(
    tmp_path: Path, parent_returncode: int
) -> None:
    child_lock = tmp_path / f"completed-{parent_returncode}-child.lock"
    proc = _spawn_test_process_tree(
        child_lock,
        parent_returncode=parent_returncode,
        child_ignores_term=False,
    )
    try:
        assert practice._wait_for_test_process(proc, 2)
        assert practice._sweep_test_process_group(proc) == parent_returncode
        assert _wait_for_lock_release(child_lock)
    finally:
        if proc.returncode is None:
            practice._sweep_test_process_group(proc)
        _kill_lock_holder(child_lock)


def test_timeout_sweeps_term_ignoring_background_child(tmp_path: Path) -> None:
    child_lock = tmp_path / "timeout-child.lock"
    proc = _spawn_test_process_tree(
        child_lock, parent_returncode=None, child_ignores_term=True
    )
    started = time.monotonic()
    try:
        assert not practice._wait_for_test_process(proc, 1)
        assert practice._sweep_test_process_group(proc) != 0
        assert time.monotonic() - started < 4
        assert _wait_for_lock_release(child_lock)
    finally:
        if proc.returncode is None:
            practice._sweep_test_process_group(proc)
        _kill_lock_holder(child_lock)


def test_group_sweep_never_signals_after_leader_was_reaped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proc = subprocess.Popen(
        [sys.executable, "-c", "pass"],
        start_new_session=True,
    )
    assert proc.wait(timeout=2) == 0

    def unexpected_signal(_group: int, _signal: int) -> None:
        pytest.fail("reaped process group must never be signaled")

    monkeypatch.setattr(os, "killpg", unexpected_signal)
    assert practice._sweep_test_process_group(proc) == 0


def test_hanging_candidate_test_is_killed_at_the_bounded_deadline(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)
    candidate = practice_repo / str(metadata["source"])
    candidate.write_text(
        candidate.read_text().replace("return sum(values)", "while True:\n        pass")
    )
    monkeypatch.setenv("PRACTICE_TEST_TIMEOUT_SECONDS", "1")

    started = time.monotonic()
    assert practice.run_tests(practice_repo, metadata) == 124
    assert time.monotonic() - started < 5
    assert "finished_at" not in practice.current_metadata(practice_repo)


def test_finish_timeout_leaves_rep_open_without_logs(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)

    def timed_out(
        _root: Path, _current: dict[str, Any], before: dict[str, str]
    ) -> practice.TestRun:
        return practice.TestRun(
            returncode=124,
            before=before,
            after=dict(before),
            timed_out=True,
        )

    monkeypatch.setattr(practice, "_execute_test_run", timed_out)
    with pytest.raises(practice.PracticeError, match="rep remains open"):
        practice.finish_session(practice_repo, metadata, "trace the edge")

    assert "finished_at" not in practice.current_metadata(practice_repo)
    assert not (practice_repo / ".challenges/reps.md").exists()
    assert not (practice_repo / ".challenges/progress.md").exists()


def test_stale_test_inputs_abort_before_closeout_journal(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    _complete_session(practice_repo, metadata)

    def mutating_pytest(
        root: Path, current: dict[str, Any], before: dict[str, str]
    ) -> practice.TestRun:
        reference = practice_repo / str(metadata["reference_test"])
        reference.write_text(reference.read_text() + "\n# changed during test\n")
        return practice.TestRun(
            returncode=0,
            before=before,
            after=practice._test_input_digests(root, current),
        )

    monkeypatch.setattr(practice, "_execute_test_run", mutating_pytest)
    with pytest.raises(practice.PracticeError, match="inputs changed"):
        practice.finish_session(practice_repo, metadata, "trace the edge")

    assert not (practice_repo / practice.JOURNAL_REL).exists()
    assert not (practice_repo / ".challenges/reps.md").exists()
    assert not (practice_repo / ".challenges/progress.md").exists()
    assert "finished_at" not in practice.current_metadata(practice_repo)


def test_finish_non_editor_requires_exact_parsed_draw(practice_repo: Path) -> None:
    line = "talk arrays/second C1 L1 A1 R1 P1 h0 trace the edge"

    with pytest.raises(practice.PracticeError, match="slug does not match"):
        practice.finish_non_editor(practice_repo, "arrays", "first", line)
    assert not (practice_repo / ".challenges/reps.md").exists()

    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0
    assert "arrays/second" in (practice_repo / ".challenges/reps.md").read_text()


def test_successful_non_editor_closeout_is_retry_idempotent(
    practice_repo: Path,
) -> None:
    line = "talk arrays/second C1 L1 A1 R1 P1 h0 trace the edge"

    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0
    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0

    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    progress = (practice_repo / ".challenges/progress.md").read_text().splitlines()
    assert len(reps) == 1
    assert len(progress) == 1
    assert not (practice_repo / practice.NON_EDITOR_RECEIPTS_REL).exists()


def test_non_editor_recovery_is_idempotent_across_date_rollover(
    practice_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    line = "talk arrays/second C1 L1 A1 R1 P1 h0 trace the edge"
    real_date = practice.date

    class FrozenDate:
        current = real_date(2026, 7, 15)

        @classmethod
        def today(cls) -> object:
            return cls.current

    monkeypatch.setattr(practice, "date", FrozenDate)
    original_replace = practice._replace_file

    class InjectedCrash(BaseException):
        pass

    crashed = False

    def crash_after_rep(path: Path, text: str) -> None:
        nonlocal crashed
        original_replace(path, text)
        if path.name == "reps.md" and not crashed:
            crashed = True
            raise InjectedCrash

    monkeypatch.setattr(practice, "_replace_file", crash_after_rep)
    with pytest.raises(InjectedCrash):
        practice.finish_non_editor(practice_repo, "arrays", "second", line)

    FrozenDate.current = real_date(2026, 7, 16)
    monkeypatch.setattr(practice, "_replace_file", original_replace)
    # An unrelated command may be the first process to recover the journal.
    assert practice.complete_problem(practice_repo, "arrays", "first") == 0
    assert not (practice_repo / practice.JOURNAL_REL).exists()
    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0
    FrozenDate.current = real_date(2026, 7, 17)
    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0

    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    progress = (practice_repo / ".challenges/progress.md").read_text().splitlines()
    assert len(reps) == 1
    assert reps[0].startswith("- 2026-07-15 ")
    assert progress == [
        "- [x] arrays/second 2026-07-15",
        "- [x] arrays/first 2026-07-16",
    ]
    receipt = practice._non_editor_receipts(practice_repo)
    assert receipt == [
        {
            "fingerprint": hashlib.sha256(
                f"arrays\0second\0{line}".encode()
            ).hexdigest(),
            "recovered_on": "2026-07-16",
        }
    ]

    # Once the short recovery window expires, identical practice is a new rep.
    FrozenDate.current = real_date(2026, 7, 18)
    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0
    assert practice.finish_non_editor(practice_repo, "arrays", "second", line) == 0
    reps = (practice_repo / ".challenges/reps.md").read_text().splitlines()
    progress = (practice_repo / ".challenges/progress.md").read_text().splitlines()
    assert len(reps) == 2
    assert reps[1].startswith("- 2026-07-18 ")
    assert progress == [
        "- [x] arrays/first 2026-07-16",
        "- [x] arrays/second 2026-07-18",
    ]
    assert not (practice_repo / practice.JOURNAL_REL).exists()


def test_non_editor_receipts_are_bounded(practice_repo: Path) -> None:
    receipts = practice._non_editor_receipts_path(practice_repo)
    fingerprints = [
        f"{index:064x}" for index in range(practice.MAX_NON_EDITOR_RECEIPTS + 3)
    ]
    for fingerprint in fingerprints:
        practice._replace_file(
            receipts,
            practice._non_editor_receipt_text(practice_repo, fingerprint, "2026-07-15"),
        )

    assert [
        receipt["fingerprint"]
        for receipt in practice._non_editor_receipts(practice_repo)
    ] == fingerprints[-practice.MAX_NON_EDITOR_RECEIPTS :]


def test_reference_cli_without_args_uses_current_session(
    practice_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    practice.prepare_session(practice_repo, "comments", "arrays", "first")
    monkeypatch.setattr(practice, "ROOT", practice_repo)
    monkeypatch.setattr(sys, "argv", ["practice_workspace.py", "reference"])

    assert practice.main() == 0
    assert "secret = _support(values)" in capsys.readouterr().out


def test_history_limits_refuse_without_destroying_current_workspace(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    candidate = practice_repo / str(metadata["source"])
    candidate.write_text(candidate.read_text() + "\n# preserve me\n")
    history = practice_repo / practice.HISTORY_REL
    for index in range(practice.MAX_HISTORY_ENTRIES):
        (history / f"old-{index}").mkdir(parents=True)

    with pytest.raises(practice.PracticeError, match="history has reached"):
        practice.prepare_session(
            practice_repo, "comments", "arrays", "second", fresh=True
        )
    assert "preserve me" in candidate.read_text()


def test_history_byte_limit_refuses_without_moving_current_workspace(
    practice_repo: Path,
) -> None:
    metadata, _, _ = practice.prepare_session(
        practice_repo, "comments", "arrays", "first"
    )
    history_file = practice_repo / practice.HISTORY_REL / "old" / "large.bin"
    history_file.parent.mkdir(parents=True)
    with history_file.open("wb") as handle:
        handle.truncate(practice.MAX_HISTORY_BYTES + 1)

    with pytest.raises(practice.PracticeError, match="exceed 512 MiB"):
        practice.prepare_session(
            practice_repo, "comments", "arrays", "second", fresh=True
        )
    assert (practice_repo / str(metadata["source"])).is_file()
