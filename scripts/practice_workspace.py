"""Prepare and drive one editor-first interview-practice workspace.

The committed algorithm implementations remain immutable reference material.
Each rep is rendered from ``HEAD`` into gitignored ``.challenges/workspace``
with a paradigm-specific comment scaffold and a candidate-owned test file.
Reference tests import the workspace implementation through a tiny pytest
plugin, so candidates can code, test, watch, and use a REPL without mutating
the packet's source tree.

Usage:
    practice_workspace.py start reacto [topic problem] [--fresh] [--no-open]
    practice_workspace.py present [topic problem]
    practice_workspace.py reference [topic problem]
    practice_workspace.py next | status | test | watch | repl | open | current
    practice_workspace.py finish "trace before optimizing"
"""

from __future__ import annotations

import argparse
import ast
import fcntl
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core42 import PRACTICE_TARGETS
from rep_schema import RepLineError, parse_rep_line
from scaffold_status import section_status
from strip_solution import (
    inject_scaffold,
    module_docstring_block,
    strip_solution,
    truncate_module_docstring,
)
from study_schedule import ranked_queue

ROOT = Path(__file__).resolve().parents[1]
STATE_REL = Path(".challenges")
WORKSPACE_REL = Path(".challenges/workspace")
HISTORY_REL = Path(".challenges/history")
METADATA_NAME = "session.json"
METADATA_SCHEMA = 4
JOURNAL_REL = Path(".challenges/practice-closeout.json")
NON_EDITOR_RECEIPTS_REL = Path(".challenges/non-editor-receipts.json")
LOCK_REL = Path(".challenges/.practice.lock")
MAX_HISTORY_ENTRIES = 100
MAX_HISTORY_BYTES = 512 * 1024 * 1024
MAX_NON_EDITOR_RECEIPTS = 100
DEFAULT_TEST_TIMEOUT_SECONDS = 120
MAX_TEST_TIMEOUT_SECONDS = 900
TEST_PROCESS_POLL_SECONDS = 0.02
TEST_PROCESS_TERM_GRACE_SECONDS = 0.25
TEST_PROCESS_KILL_WAIT_SECONDS = 2
TEST_INPUT_KEYS = ("source", "candidate_test", "reference_test", "plugin")
PRACTICE_LOCK = (
    "# ==== THINKING GATE: complete the comments above, then delete this line "
    "to code ===="
)
IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
HEX_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_LOCAL = threading.local()


class PracticeError(RuntimeError):
    """A user-actionable practice-workspace failure."""


@dataclass(frozen=True)
class TestRun:
    """One pytest result tied to the exact files that produced it."""

    returncode: int
    before: dict[str, str]
    after: dict[str, str]
    timed_out: bool = False

    @property
    def fresh(self) -> bool:
        return self.before == self.after


@dataclass(frozen=True)
class Paradigm:
    """One reasoning vocabulary rendered into the candidate's source file."""

    title: str
    seeds: tuple[str, ...]
    lock_after: int

    @property
    def pre_code_labels(self) -> tuple[str, ...]:
        return tuple(
            seed.split(":", 1)[0].removeprefix("# ")
            for seed in self.seeds[: self.lock_after]
        )


PARADIGMS: dict[str, Paradigm] = {
    "reacto": Paradigm(
        title="REACTO",
        seeds=(
            "# REPEAT: restate inputs, outputs, constraints, and questions",
            "# EXAMPLES: one concrete case and one edge case with expected output",
            "# APPROACH: pattern, brute-force baseline, invariant, and target big-O",
            "# CODE: narrate the next implementation choice before each chunk",
            "# TEST: add cases in the candidate test tab; record a line-by-line trace",
            "# OPTIMIZE: final time/space, remaining edges, and any trade-off",
        ),
        lock_after=3,
    ),
    "clarp": Paradigm(
        title="CLARP",
        seeds=(
            "# CLARIFY: restate the contract, constraints, and open questions",
            "# LAY_OUT: example, edge case, pattern, brute-force big-O, and invariant",
            "# ATTACK: narrate the next implementation choice before each chunk",
            "# RUN: trace the stated example and record focused test cases/results",
            "# POLISH: final time/space complexity and remaining edges",
        ),
        lock_after=2,
    ),
    "umpire": Paradigm(
        title="UMPIRE",
        seeds=(
            "# UNDERSTAND: restate the contract, constraints, and questions",
            "# MATCH: connect examples and edge cases to a known pattern",
            "# PLAN: brute-force baseline, chosen invariant, steps, and target big-O",
            "# IMPLEMENT: narrate the next implementation choice before each chunk",
            "# REVIEW: trace the example and record focused test cases/results",
            "# EVALUATE: final time/space complexity, edges, and trade-offs",
        ),
        lock_after=3,
    ),
    "comments": Paradigm(
        title="comment-driven",
        seeds=(
            "# RESTATE: the problem in your own words: inputs, outputs, constraints",
            "# EXAMPLE: one concrete input/output pair, plus one edge case",
            "# INVARIANT: what stays true at each step (loop/recursion invariant)",
            "# APPROACH: pattern family + brute-force big-O, decided before any code",
            "# TESTS: cases to add in the candidate test tab and what each proves",
            "# COMPLEXITY: final time / space and remaining edges",
        ),
        lock_after=4,
    ),
}


def _workspace(root: Path) -> Path:
    return root / WORKSPACE_REL


def _confined_directory(root: Path, path: Path, label: str, *, create: bool) -> Path:
    if path.is_symlink():
        raise PracticeError(f"{label} cannot be a symlink")
    if path.exists():
        if not path.is_dir():
            raise PracticeError(f"{label} must be a directory")
    elif create:
        try:
            path.mkdir()
        except OSError as exc:
            raise PracticeError(f"cannot create {label}: {exc}") from exc
    else:
        return path
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise PracticeError(f"{label} must stay inside the repository") from exc
    return path


def _state_dir(root: Path) -> Path:
    return _confined_directory(
        root, root / STATE_REL, "private practice state", create=True
    )


def _state_file(root: Path, name: str) -> Path:
    path = _state_dir(root) / name
    if path.is_symlink():
        raise PracticeError(f"private practice file {name} cannot be a symlink")
    if path.exists() and not path.is_file():
        raise PracticeError(f"private practice file {name} must be a regular file")
    return path


def _metadata_path(root: Path) -> Path:
    return _workspace(root) / METADATA_NAME


def _validate_problem(topic: str, problem: str) -> None:
    if not IDENTIFIER.fullmatch(topic) or not IDENTIFIER.fullmatch(problem):
        raise PracticeError("topic and problem must be lowercase Python identifiers")


def _draw_problem(root: Path) -> tuple[str, str]:
    queue = ranked_queue(_state_file(root, "progress.md"))
    if not queue:
        raise PracticeError("the spaced-repetition queue is empty")
    _, topic, problem = queue[0]
    return topic, problem


def select_problem(
    root: Path, topic: str | None = None, problem: str | None = None
) -> tuple[str, str]:
    """Validate an explicit selection or draw one problem when both are absent."""
    if (topic is None) != (problem is None):
        raise PracticeError("provide both topic and problem, or omit both for a draw")
    if topic is None or problem is None:
        topic, problem = _draw_problem(root)
    _validate_problem(topic, problem)
    return topic, problem


def _committed_source(root: Path, relative: Path) -> str:
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative.as_posix()}"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or "not present in HEAD"
        raise PracticeError(f"cannot load committed {relative}: {detail}")
    return proc.stdout


def render_candidate(source: str, paradigm: Paradigm, target: str | None = None) -> str:
    """Return a cold stub carrying exactly one selected-paradigm scaffold."""
    # Redact every implementation body so alternate solutions never leak into
    # the candidate tab. The selected target alone receives the scaffold and
    # remains candidate-owned. Reference tests keep their committed non-target
    # bindings, while every helper used by the target stays a candidate-owned
    # cold stub.
    cold = truncate_module_docstring(strip_solution(source))
    return inject_scaffold(
        cold,
        seeds=paradigm.seeds,
        lock_sentinel=PRACTICE_LOCK,
        lock_after=paradigm.lock_after,
        target_name=target,
    )


def present_problem(root: Path, topic: str, problem: str) -> str:
    """Return a cold statement from committed source without creating a rep."""
    _validate_problem(topic, problem)
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    source = truncate_module_docstring(_committed_source(root, source_rel))
    try:
        return module_docstring_block(source)
    except ValueError as exc:
        raise PracticeError(f"cannot present {topic}/{problem}: {exc}") from exc


def reference_solution(root: Path, topic: str, problem: str) -> str:
    """Return the committed implementation without touching working files."""
    _validate_problem(topic, problem)
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    return _committed_source(root, source_rel)


def _public_symbols(source: str) -> list[str]:
    tree = ast.parse(source)
    return [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    ]


def _practice_target(topic: str, problem: str, source: str) -> str:
    """Return the explicit Core target, with a narrow fixture fallback."""
    configured = PRACTICE_TARGETS.get((topic, problem))
    symbols = _public_symbols(source)
    if configured is not None:
        if configured not in symbols:
            raise PracticeError(
                f"configured target {configured!r} is absent from {topic}/{problem}"
            )
        return configured
    if len(symbols) == 1:
        return symbols[0]
    raise PracticeError(f"no unambiguous practice target for {topic}/{problem}")


def _candidate_test(topic: str, problem: str, target: str) -> str:
    module = f"algo.{topic}.{problem}"
    import_line = f"# from {module} import {target}\n"
    return (
        f'"""Candidate-owned tests for {topic}/{problem}.\n\n'
        "Add focused examples before and while you implement. These run beside\n"
        "the packet's reference tests with `just practice-test`.\n"
        '"""\n\n'
        "# Import the public names shown below, then replace the placeholders.\n"
        f"{import_line}"
        "#\n"
        "# def test_concrete_example() -> None:\n"
        "#     assert ...\n"
        "#\n"
        "# def test_edge_case() -> None:\n"
        "#     assert ...\n"
    )


def _pytest_plugin(
    module: str,
    candidate_name: str,
    source_rel: Path,
    target: str,
) -> str:
    return f'''"""Load the cold candidate target for the packet's locked tests."""

from __future__ import annotations

import importlib
import importlib.util
import subprocess
import sys
import types
from pathlib import Path

MODULE = {module!r}
CANDIDATE = Path(__file__).with_name({candidate_name!r})
ROOT = Path(__file__).resolve().parents[2]
SOURCE_REL = {source_rel.as_posix()!r}
TARGET = {target!r}
SUPPORT: tuple[str, ...] = ()
_REFERENCE: types.ModuleType | None = None
_CANDIDATE_MODULE: types.ModuleType | None = None


def _committed_reference() -> types.ModuleType:
    proc = subprocess.run(
        ["git", "show", f"HEAD:{{SOURCE_REL}}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or "not present in HEAD"
        raise RuntimeError(f"cannot load committed {{SOURCE_REL}}: {{detail}}")
    reference_name = f"_practice_reference_{{MODULE}}"
    reference = types.ModuleType(reference_name)
    reference.__file__ = str(ROOT / SOURCE_REL)
    reference.__package__ = MODULE.rpartition(".")[0]
    sys.modules[reference_name] = reference
    exec(compile(proc.stdout, reference.__file__, "exec"), reference.__dict__)
    return reference


def _load_candidate() -> tuple[types.ModuleType, types.ModuleType, str]:
    parent_name, child_name = MODULE.rsplit(".", 1)
    parent = importlib.import_module(parent_name)
    spec = importlib.util.spec_from_file_location(MODULE, CANDIDATE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {{CANDIDATE}}")
    candidate = importlib.util.module_from_spec(spec)
    sys.modules[MODULE] = candidate
    spec.loader.exec_module(candidate)
    return candidate, parent, child_name


def load_candidate() -> types.ModuleType:
    """Install the cold candidate module for an interactive REPL."""
    candidate, parent, child_name = _load_candidate()
    sys.modules[MODULE] = candidate
    setattr(parent, child_name, candidate)
    return candidate


def pytest_configure() -> None:
    global _CANDIDATE_MODULE, _REFERENCE
    reference = _committed_reference()
    candidate, parent, child_name = _load_candidate()
    for name, value in vars(candidate).items():
        if name not in vars(reference) and not name.startswith("__"):
            setattr(reference, name, value)
    _REFERENCE = reference
    _CANDIDATE_MODULE = candidate
    sys.modules[MODULE] = reference
    setattr(parent, child_name, reference)


def pytest_collection_modifyitems(items: list[object]) -> None:
    """Swap only the selected implementation after test modules import."""
    if _REFERENCE is None or _CANDIDATE_MODULE is None:
        raise RuntimeError("practice plugin was not configured")
    reference_target = getattr(_REFERENCE, TARGET)
    candidate_target = getattr(_CANDIDATE_MODULE, TARGET)
    for item in items:
        test_module = getattr(item, "module", None)
        if test_module is None:
            continue
        for name, value in tuple(vars(test_module).items()):
            if value is reference_target:
                setattr(test_module, name, candidate_target)
    setattr(_REFERENCE, TARGET, candidate_target)
    parent_name, child_name = MODULE.rsplit(".", 1)
    parent = importlib.import_module(parent_name)
    sys.modules[MODULE] = _CANDIDATE_MODULE
    setattr(parent, child_name, _CANDIDATE_MODULE)
'''


def _repl_bootstrap(module: str, target: str) -> str:
    return f'''"""Interactive bootstrap for the current practice implementation."""

from practice_plugin import TARGET, load_candidate

candidate = load_candidate()
globals()[TARGET] = getattr(candidate, TARGET)
print("Loaded {module}.{target}; helpers remain cold in the candidate module.")
'''


def _parse_timestamp(value: object, field: str) -> str:
    if type(value) is not str:
        raise PracticeError(f"invalid current-rep metadata: {field} must be text")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise PracticeError(
            f"invalid current-rep metadata: {field} is not ISO-8601"
        ) from exc
    if parsed.tzinfo is None:
        raise PracticeError(
            f"invalid current-rep metadata: {field} must include a timezone"
        )
    return value


def _validate_digest_map(value: object, field: str) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != set(TEST_INPUT_KEYS):
        raise PracticeError(
            f"invalid current-rep metadata: {field} must cover all test inputs"
        )
    result: dict[str, str] = {}
    for key in TEST_INPUT_KEYS:
        digest = value.get(key)
        if type(digest) is not str or HEX_DIGEST.fullmatch(digest) is None:
            raise PracticeError(
                f"invalid current-rep metadata: {field}.{key} is not a digest"
            )
        result[key] = digest
    return result


def _required_file(root: Path, relative: str, *, workspace: bool) -> Path:
    if workspace:
        _state_dir(root)
    path = root / relative
    boundary = _workspace(root) if workspace else root
    if workspace and boundary.is_symlink():
        raise PracticeError(
            "invalid current-rep metadata: workspace cannot be a symlink"
        )
    try:
        root_resolved = root.resolve(strict=True)
        boundary_resolved = boundary.resolve(strict=True)
        boundary_resolved.relative_to(root_resolved)
        path.resolve(strict=True).relative_to(boundary_resolved)
    except (FileNotFoundError, ValueError) as exc:
        raise PracticeError(
            f"invalid current-rep metadata: required file is missing or unconfined: {relative}"
        ) from exc
    if path.is_symlink() or not path.is_file():
        raise PracticeError(
            f"invalid current-rep metadata: required regular file is missing: {relative}"
        )
    return path


def _validate_metadata(root: Path, value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PracticeError("invalid current-rep metadata: expected an object")
    required = {
        "schema",
        "session_id",
        "paradigm",
        "paradigm_title",
        "topic",
        "problem",
        "target",
        "module",
        "source",
        "candidate_test",
        "reference_test",
        "plugin",
        "repl",
        "seeds",
        "pre_code_labels",
        "lock",
        "created_at",
    }
    finished_fields = {
        "finished_at",
        "finish_note",
        "finish_state",
        "test_outcome",
        "test_inputs_before",
        "test_inputs_after",
    }
    keys = set(value)
    if not required <= keys or keys - required - finished_fields:
        missing = sorted(required - keys)
        extra = sorted(keys - required - finished_fields)
        raise PracticeError(
            f"invalid current-rep metadata fields (missing={missing}, extra={extra})"
        )
    has_finished = bool(keys & finished_fields)
    if has_finished and not finished_fields <= keys:
        missing = sorted(finished_fields - keys)
        raise PracticeError(
            f"invalid current-rep metadata: partial closeout fields {missing}"
        )
    if type(value["schema"]) is not int or value["schema"] != METADATA_SCHEMA:
        raise PracticeError(
            f"invalid current-rep metadata: schema must be {METADATA_SCHEMA}"
        )
    session_id = value["session_id"]
    if type(session_id) is not str:
        raise PracticeError("invalid current-rep metadata: session_id must be text")
    try:
        parsed_id = uuid.UUID(session_id)
    except (ValueError, AttributeError) as exc:
        raise PracticeError(
            "invalid current-rep metadata: malformed session_id"
        ) from exc
    if parsed_id.version != 4 or str(parsed_id) != session_id:
        raise PracticeError("invalid current-rep metadata: session_id must be UUID4")

    for field in ("paradigm", "topic", "problem", "target"):
        if type(value[field]) is not str:
            raise PracticeError(f"invalid current-rep metadata: {field} must be text")
    paradigm_name = value["paradigm"]
    paradigm = PARADIGMS.get(paradigm_name)
    if paradigm is None:
        raise PracticeError("invalid current-rep metadata: unknown paradigm")
    topic = value["topic"]
    problem = value["problem"]
    _validate_problem(topic, problem)
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    committed = _committed_source(root, source_rel)
    target = PRACTICE_TARGETS.get((topic, problem))
    if target is None:
        target = _practice_target(topic, problem, committed)
    module = f"algo.{topic}.{problem}"
    candidate_name = f"{problem}.py"
    expected = {
        "paradigm_title": paradigm.title,
        "target": target,
        "module": module,
        "source": (WORKSPACE_REL / candidate_name).as_posix(),
        "candidate_test": (WORKSPACE_REL / f"test_{problem}_candidate.py").as_posix(),
        "reference_test": (Path("tests") / topic / f"test_{problem}.py").as_posix(),
        "plugin": (WORKSPACE_REL / "practice_plugin.py").as_posix(),
        "repl": (WORKSPACE_REL / "repl.py").as_posix(),
        "lock": PRACTICE_LOCK,
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise PracticeError(
                f"invalid current-rep metadata: {field} is not canonical"
            )
    if value.get("seeds") != list(paradigm.seeds):
        raise PracticeError("invalid current-rep metadata: seeds do not match paradigm")
    if value.get("pre_code_labels") != list(paradigm.pre_code_labels):
        raise PracticeError(
            "invalid current-rep metadata: pre-code labels do not match paradigm"
        )
    _parse_timestamp(value["created_at"], "created_at")

    for field in ("source", "candidate_test", "plugin", "repl"):
        _required_file(root, str(value[field]), workspace=True)
    _required_file(root, str(value["reference_test"]), workspace=False)
    plugin = root / str(value["plugin"])
    expected_plugin = _pytest_plugin(module, candidate_name, source_rel, target)
    if not has_finished and plugin.read_text() != expected_plugin:
        raise PracticeError("invalid current-rep metadata: practice plugin drifted")
    repl = root / str(value["repl"])
    if repl.read_text() != _repl_bootstrap(module, target):
        raise PracticeError("invalid current-rep metadata: REPL bootstrap drifted")

    if has_finished:
        _parse_timestamp(value["finished_at"], "finished_at")
        note = value["finish_note"]
        if type(note) is not str or not note or note != " ".join(note.split()):
            raise PracticeError("invalid current-rep metadata: malformed finish_note")
        if type(value["finish_state"]) is not str or value["finish_state"] not in {
            "THINK",
            "BUILD",
            "REFLECT",
            "CLOSE",
        }:
            raise PracticeError("invalid current-rep metadata: bad finish_state")
        if type(value["test_outcome"]) is not str or value["test_outcome"] not in {
            "not_run",
            "passed",
            "failed",
        }:
            raise PracticeError("invalid current-rep metadata: bad test_outcome")
        _validate_digest_map(value["test_inputs_before"], "test_inputs_before")
        _validate_digest_map(value["test_inputs_after"], "test_inputs_after")
    return dict(value)


def _journal_path(root: Path) -> Path:
    return _state_file(root, JOURNAL_REL.name)


def _non_editor_receipts_path(root: Path) -> Path:
    return _state_file(root, NON_EDITOR_RECEIPTS_REL.name)


def _parse_receipt_date(value: object) -> str:
    if type(value) is not str:
        raise PracticeError("invalid non-editor closeout receipt date")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise PracticeError("invalid non-editor closeout receipt date") from exc
    if parsed.isoformat() != value:
        raise PracticeError("invalid non-editor closeout receipt date")
    return value


def _parse_non_editor_receipts(text: str) -> list[dict[str, str]]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PracticeError(f"invalid non-editor closeout receipts: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "receipts"}:
        raise PracticeError("invalid non-editor closeout receipt fields")
    receipts = value["receipts"]
    if type(value["schema"]) is not int or value["schema"] != 1:
        raise PracticeError("invalid non-editor closeout receipt schema")
    if not isinstance(receipts, list) or len(receipts) > MAX_NON_EDITOR_RECEIPTS:
        raise PracticeError("invalid non-editor closeout receipt list")
    result: list[dict[str, str]] = []
    for receipt in receipts:
        if not isinstance(receipt, dict) or set(receipt) != {
            "fingerprint",
            "recovered_on",
        }:
            raise PracticeError("invalid non-editor closeout receipt entry")
        fingerprint = receipt["fingerprint"]
        if type(fingerprint) is not str or HEX_DIGEST.fullmatch(fingerprint) is None:
            raise PracticeError("invalid non-editor closeout receipt fingerprint")
        result.append(
            {
                "fingerprint": fingerprint,
                "recovered_on": _parse_receipt_date(receipt["recovered_on"]),
            }
        )
    fingerprints = [receipt["fingerprint"] for receipt in result]
    if len(set(fingerprints)) != len(fingerprints):
        raise PracticeError("duplicate non-editor closeout receipt fingerprint")
    return result


def _non_editor_receipts(root: Path) -> list[dict[str, str]]:
    path = _non_editor_receipts_path(root)
    if not path.exists():
        return []
    try:
        return _parse_non_editor_receipts(path.read_text())
    except OSError as exc:
        raise PracticeError(f"cannot read non-editor closeout receipts: {exc}") from exc


def _receipt_is_active(recovered_on: str, today: str) -> bool:
    recovered = datetime.strptime(_parse_receipt_date(recovered_on), "%Y-%m-%d").date()
    current = datetime.strptime(_parse_receipt_date(today), "%Y-%m-%d").date()
    return recovered <= current <= recovered + timedelta(days=1)


def _has_active_non_editor_receipt(root: Path, fingerprint: str, today: str) -> bool:
    return any(
        receipt["fingerprint"] == fingerprint
        and _receipt_is_active(receipt["recovered_on"], today)
        for receipt in _non_editor_receipts(root)
    )


def _non_editor_receipt_text(root: Path, fingerprint: str, recovered_on: str) -> str:
    if HEX_DIGEST.fullmatch(fingerprint) is None:
        raise PracticeError("invalid non-editor closeout fingerprint")
    recovered_on = _parse_receipt_date(recovered_on)
    receipts = _non_editor_receipts(root)
    previous = next(
        (receipt for receipt in receipts if receipt["fingerprint"] == fingerprint),
        None,
    )
    if previous is not None and _receipt_is_active(
        previous["recovered_on"], recovered_on
    ):
        current = previous
    else:
        current = {"fingerprint": fingerprint, "recovered_on": recovered_on}
    receipts = [
        receipt for receipt in receipts if receipt["fingerprint"] != fingerprint
    ]
    receipts.append(current)
    return (
        json.dumps(
            {
                "schema": 1,
                "receipts": receipts[-MAX_NON_EDITOR_RECEIPTS:],
            },
            indent=2,
        )
        + "\n"
    )


def _closeout_destinations(root: Path, files: dict[str, str]) -> dict[str, Path]:
    """Confine every journal destination before replay writes any file."""
    destinations: dict[str, Path] = {}
    state_files = {
        Path(".challenges/reps.md").as_posix(): "reps.md",
        Path(".challenges/progress.md").as_posix(): "progress.md",
        NON_EDITOR_RECEIPTS_REL.as_posix(): NON_EDITOR_RECEIPTS_REL.name,
    }
    session_rel = (WORKSPACE_REL / METADATA_NAME).as_posix()
    for relative in files:
        state_name = state_files.get(relative)
        if state_name is not None:
            destinations[relative] = _state_file(root, state_name)
        elif relative == session_rel:
            destinations[relative] = _required_file(root, relative, workspace=True)
        else:  # The file-set validation should make this unreachable.
            raise PracticeError(f"invalid closeout journal destination: {relative}")
    return destinations


def _recover_closeout(
    root: Path, *, record_non_editor_receipt: bool = True
) -> dict[str, Any] | None:
    path = _journal_path(root)
    if path.is_symlink():
        raise PracticeError("closeout journal cannot be a symlink")
    if not path.exists():
        return None
    try:
        journal = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PracticeError(f"invalid closeout journal: {exc}") from exc
    if not isinstance(journal, dict) or set(journal) != {
        "schema",
        "kind",
        "fingerprint",
        "files",
    }:
        raise PracticeError("invalid closeout journal fields")
    if (
        type(journal["schema"]) is not int
        or journal["schema"] != 1
        or type(journal["kind"]) is not str
        or journal["kind"] not in {"editor", "non_editor"}
    ):
        raise PracticeError("invalid closeout journal header")
    if type(journal["fingerprint"]) is not str or not journal["fingerprint"]:
        raise PracticeError("invalid closeout journal fingerprint")
    files = journal["files"]
    if not isinstance(files, dict):
        raise PracticeError("invalid closeout journal payload")
    allowed = {
        Path(".challenges/reps.md").as_posix(),
        Path(".challenges/progress.md").as_posix(),
        NON_EDITOR_RECEIPTS_REL.as_posix(),
        (WORKSPACE_REL / METADATA_NAME).as_posix(),
    }
    paired = {
        Path(".challenges/reps.md").as_posix(),
        Path(".challenges/progress.md").as_posix(),
    }
    if journal["kind"] == "editor":
        required = paired | {(WORKSPACE_REL / METADATA_NAME).as_posix()}
    else:
        required = paired
    if set(files) != required or set(files) - allowed:
        raise PracticeError("invalid closeout journal file set")
    replay_files = dict(files)
    if journal["kind"] == "non_editor" and (
        type(journal["fingerprint"]) is not str
        or HEX_DIGEST.fullmatch(journal["fingerprint"]) is None
    ):
        raise PracticeError("invalid non-editor closeout fingerprint")
    receipt = NON_EDITOR_RECEIPTS_REL.as_posix()
    if journal["kind"] == "non_editor" and record_non_editor_receipt:
        replay_files[receipt] = _non_editor_receipt_text(
            root,
            str(journal["fingerprint"]),
            date.today().isoformat(),
        )
    for relative, text in replay_files.items():
        if type(text) is not str:
            raise PracticeError("invalid closeout journal file contents")
        if relative == receipt:
            receipts = _parse_non_editor_receipts(text)
            if journal["fingerprint"] not in {
                current["fingerprint"] for current in receipts
            }:
                raise PracticeError(
                    "non-editor closeout receipt does not match journal"
                )
    destinations = _closeout_destinations(root, replay_files)
    for relative in (
        Path(".challenges/reps.md").as_posix(),
        Path(".challenges/progress.md").as_posix(),
        receipt,
        (WORKSPACE_REL / METADATA_NAME).as_posix(),
    ):
        if relative not in replay_files:
            continue
        _replace_file(destinations[relative], replay_files[relative])
    path.unlink()
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return journal


@contextmanager
def _practice_lock(
    root: Path, *, shared: bool = False
) -> Iterator[dict[str, Any] | None]:
    """Lock private state, recovering a pending closeout before use."""
    try:
        key = str(root.resolve(strict=True))
    except FileNotFoundError as exc:
        raise PracticeError("repository root does not exist") from exc
    held: dict[str, dict[str, Any]] = getattr(_LOCAL, "practice_locks", {})
    if key in held:
        record = held[key]
        if record["shared"] and not shared:
            raise PracticeError("cannot upgrade a shared practice lock")
        record["depth"] += 1
        try:
            yield record["recovery"]
        finally:
            record["depth"] -= 1
        return

    state = _state_dir(root)
    lock_path = state / LOCK_REL.name
    if lock_path.is_symlink():
        raise PracticeError("practice lock cannot be a symlink")
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_flags |= getattr(os, "O_NOFOLLOW", 0)
    file_flags = os.O_RDWR | os.O_CREAT | os.O_APPEND
    file_flags |= getattr(os, "O_NOFOLLOW", 0)
    directory = os.open(state, directory_flags)
    try:
        descriptor = os.open(lock_path.name, file_flags, 0o600, dir_fd=directory)
    except OSError as exc:
        raise PracticeError(f"cannot open practice lock safely: {exc}") from exc
    finally:
        os.close(directory)
    handle = os.fdopen(descriptor, "a+")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH if shared else fcntl.LOCK_EX)
        recovery = None
        if shared and _journal_path(root).exists():
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            recovery = _recover_closeout(root)
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
        elif not shared:
            recovery = _recover_closeout(root)
    except BaseException:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()
        raise
    record = {
        "depth": 1,
        "handle": handle,
        "recovery": recovery,
        "shared": shared,
    }
    held[key] = record
    _LOCAL.practice_locks = held
    try:
        yield recovery
    finally:
        del held[key]
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def _read_metadata(root: Path) -> dict[str, Any]:
    _state_dir(root)
    workspace = _workspace(root)
    if workspace.is_symlink():
        raise PracticeError(
            "invalid current-rep metadata: workspace cannot be a symlink"
        )
    if workspace.exists():
        _confined_directory(root, workspace, "practice workspace", create=False)
    path = _metadata_path(root)
    if path.is_symlink():
        raise PracticeError("invalid current-rep metadata: session file is a symlink")
    if not path.exists():
        raise PracticeError("no current rep; run `just practice-start <paradigm>`")
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PracticeError(f"invalid current-rep metadata: {exc}") from exc
    return _validate_metadata(root, value)


def current_metadata(root: Path) -> dict[str, Any]:
    """Recover private state, then return the validated current session."""
    with _practice_lock(root, shared=True):
        return _read_metadata(root)


def _archive_current(root: Path) -> Path | None:
    workspace = _workspace(root)
    if workspace.is_symlink():
        raise PracticeError("practice workspace cannot be a symlink")
    if not workspace.exists():
        return None
    _confined_directory(root, workspace, "practice workspace", create=False)
    try:
        current = _read_metadata(root)
    except PracticeError:
        current = {}
    parts = [
        str(current.get("paradigm", "unknown")),
        str(current.get("topic", "unknown")),
        str(current.get("problem", "unknown")),
    ]
    slug = "-".join(re.sub(r"[^a-zA-Z0-9_-]+", "-", part) for part in parts)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    history = _confined_directory(
        root, root / HISTORY_REL, "practice history", create=True
    )
    entries = sum(1 for item in history.iterdir() if item.is_dir())
    if entries >= MAX_HISTORY_ENTRIES:
        raise PracticeError(
            f"practice history has reached {MAX_HISTORY_ENTRIES} entries; "
            "move old archives elsewhere before starting a new rep"
        )
    archived_bytes = sum(
        item.stat().st_size
        for item in history.rglob("*")
        if item.is_file() and not item.is_symlink()
    )
    workspace_bytes = sum(
        item.stat().st_size
        for item in workspace.rglob("*")
        if item.is_file() and not item.is_symlink()
    )
    if archived_bytes + workspace_bytes > MAX_HISTORY_BYTES:
        raise PracticeError(
            "practice history would exceed 512 MiB; move old archives elsewhere "
            "before starting a new rep"
        )
    session_suffix = str(current.get("session_id", uuid.uuid4()))[:8]
    destination = history / f"{stamp}-{slug[:80]}-{session_suffix}"
    if destination.exists():
        destination = history / f"{stamp}-{slug[:70]}-{uuid.uuid4().hex[:12]}"
    workspace.replace(destination)
    return destination


def _same_session(
    metadata: dict[str, Any], paradigm: str, topic: str, problem: str
) -> bool:
    return all(
        metadata.get(key) == value
        for key, value in (
            ("paradigm", paradigm),
            ("topic", topic),
            ("problem", problem),
        )
    )


def prepare_session(
    root: Path,
    paradigm_name: str,
    topic: str | None = None,
    problem: str | None = None,
    *,
    fresh: bool = False,
) -> tuple[dict[str, Any], str, Path | None]:
    """Create or resume one current workspace.

    Returns ``(metadata, action, archived_path)`` where action is ``created``
    or ``resumed``. A different/fresh session archives the previous workspace.
    """
    with _practice_lock(root):
        paradigm = PARADIGMS.get(paradigm_name)
        if paradigm is None:
            choices = ", ".join(PARADIGMS)
            raise PracticeError(f"unknown paradigm {paradigm_name!r}; choose {choices}")
        topic, problem = select_problem(root, topic, problem)

        workspace = _workspace(root)
        if workspace.is_symlink():
            raise PracticeError("practice workspace cannot be a symlink")
        if workspace.exists() and not fresh:
            try:
                metadata = _read_metadata(root)
            except PracticeError:
                metadata = None
            if (
                metadata is not None
                and "finished_at" not in metadata
                and _same_session(metadata, paradigm_name, topic, problem)
            ):
                return metadata, "resumed", None

        source_rel = Path("src/algo") / topic / f"{problem}.py"
        reference_test_rel = Path("tests") / topic / f"test_{problem}.py"
        if not (root / reference_test_rel).is_file():
            raise PracticeError(f"missing reference tests: {reference_test_rel}")
        committed = _committed_source(root, source_rel)
        target = _practice_target(topic, problem, committed)
        candidate = render_candidate(committed, paradigm, target)

        challenges = _state_dir(root)
        temporary = Path(
            tempfile.mkdtemp(prefix=".workspace-", suffix=".tmp", dir=challenges)
        )
        candidate_name = f"{problem}.py"
        candidate_test_name = f"test_{problem}_candidate.py"
        module = f"algo.{topic}.{problem}"
        metadata = {
            "schema": METADATA_SCHEMA,
            "session_id": str(uuid.uuid4()),
            "paradigm": paradigm_name,
            "paradigm_title": paradigm.title,
            "topic": topic,
            "problem": problem,
            "target": target,
            "module": module,
            "source": (WORKSPACE_REL / candidate_name).as_posix(),
            "candidate_test": (WORKSPACE_REL / candidate_test_name).as_posix(),
            "reference_test": reference_test_rel.as_posix(),
            "plugin": (WORKSPACE_REL / "practice_plugin.py").as_posix(),
            "repl": (WORKSPACE_REL / "repl.py").as_posix(),
            "seeds": list(paradigm.seeds),
            "pre_code_labels": list(paradigm.pre_code_labels),
            "lock": PRACTICE_LOCK,
            "created_at": datetime.now(UTC).isoformat(),
        }
        archived: Path | None = None
        try:
            (temporary / candidate_name).write_text(candidate)
            (temporary / candidate_test_name).write_text(
                _candidate_test(topic, problem, target)
            )
            (temporary / "practice_plugin.py").write_text(
                _pytest_plugin(module, candidate_name, source_rel, target)
            )
            (temporary / "repl.py").write_text(_repl_bootstrap(module, target))
            (temporary / METADATA_NAME).write_text(
                json.dumps(metadata, indent=2) + "\n"
            )
            archived = _archive_current(root)
            temporary.replace(workspace)
        except BaseException:
            if temporary.exists():
                shutil.rmtree(temporary)
            if archived is not None and not workspace.exists() and archived.exists():
                archived.replace(workspace)
            raise
        return _read_metadata(root), "created", archived


def _cursor_line(root: Path, metadata: dict[str, Any]) -> int:
    path = root / str(metadata["source"])
    first = str(metadata["seeds"][0]).split(":", 1)[0]
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if first in line:
            return number
    return 1


def open_session(root: Path, metadata: dict[str, Any]) -> bool:
    """Open candidate source at its first comment and the candidate test tab."""
    code = shutil.which("code")
    source = str(metadata["source"])
    candidate_test = str(metadata["candidate_test"])
    line = _cursor_line(root, metadata)
    if code is None:
        print(f"Open {source}:{line} and {candidate_test}")
        return False
    proc = subprocess.run(
        [code, "--reuse-window", candidate_test, "--goto", f"{source}:{line}"],
        cwd=root,
        check=False,
    )
    if proc.returncode != 0:
        print(f"Open {source}:{line} and {candidate_test}")
        return False
    print(f"Opened {source}:{line} and {candidate_test}")
    return True


def _print_start(
    root: Path,
    metadata: dict[str, Any],
    action: str,
    archived: Path | None,
) -> None:
    print(module_docstring_block((root / str(metadata["source"])).read_text()).rstrip())
    print()
    print(
        f"{metadata['paradigm_title']} rep {action}: "
        f"{metadata['topic']}/{metadata['problem']}"
    )
    if archived is not None:
        print(f"Previous workspace archived: {archived.relative_to(root)}")
    show_next(root, metadata)


def _statuses(root: Path, metadata: dict[str, Any]) -> dict[str, str]:
    source = (root / str(metadata["source"])).read_text()
    seeds = tuple(str(seed) for seed in metadata["seeds"])
    lock = str(metadata["lock"])
    return section_status(source, seeds=seeds, lock_sentinel=lock)


def _candidate_test_count(root: Path, metadata: dict[str, Any]) -> int:
    try:
        tree = ast.parse((root / str(metadata["candidate_test"])).read_text())
    except SyntaxError as exc:
        raise PracticeError(f"candidate tests have a syntax error: {exc}") from exc
    return sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        for node in tree.body
    )


def _candidate_source_syntax(root: Path, metadata: dict[str, Any]) -> str | None:
    try:
        ast.parse((root / str(metadata["source"])).read_text())
    except SyntaxError as exc:
        return str(exc)
    return None


def _target_is_implemented(source: str, target: str) -> bool:
    tree = ast.parse(source)
    selected = next(
        (
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.name == target
        ),
        None,
    )
    if selected is None:
        return False

    def is_not_implemented(node: ast.AST) -> bool:
        if not isinstance(node, ast.Raise) or node.exc is None:
            return False
        exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
        return isinstance(exc, ast.Name) and exc.id == "NotImplementedError"

    return not any(is_not_implemented(node) for node in ast.walk(selected))


def show_status(root: Path, metadata: dict[str, Any]) -> int:
    for label, state in _statuses(root, metadata).items():
        print(f"{label}: {state}")
    source = (root / str(metadata["source"])).read_text()
    print(f"lock: {'locked' if str(metadata['lock']) in source else 'unlocked'}")
    try:
        count = _candidate_test_count(root, metadata)
    except PracticeError:
        print("candidate tests: syntax error")
        return 1
    print(f"candidate tests: {count}")
    return 0


def next_step(root: Path, metadata: dict[str, Any]) -> tuple[str, str]:
    """Return the current state and one deterministic candidate action."""
    statuses = _statuses(root, metadata)
    source = (root / str(metadata["source"])).read_text()
    pre_code = [str(label) for label in metadata["pre_code_labels"]]

    for label in pre_code:
        if statuses.get(label) != "filled":
            return "THINK", f"Fill {label}, save, then run /continue."
    if str(metadata["lock"]) in source:
        return (
            "THINK",
            "Delete the THINKING GATE yourself, then implement below it.",
        )

    if _candidate_source_syntax(root, metadata) is not None:
        return "BUILD", "Fix the syntax error in your source file, then run /continue."

    try:
        candidate_test_count = _candidate_test_count(root, metadata)
    except PracticeError:
        return "BUILD", "Fix the syntax error in your test file, then run /continue."

    if (
        not _target_is_implemented(source, str(metadata["target"]))
        or candidate_test_count == 0
    ):
        return (
            "BUILD",
            "Implement the solution and add at least one focused test in your test file.",
        )

    labels = [seed.split(":", 1)[0].removeprefix("# ") for seed in metadata["seeds"]]
    post_code = labels[len(pre_code) :]
    for index, label in enumerate(post_code):
        if statuses.get(label) != "filled":
            state = "BUILD" if index == 0 else "REFLECT"
            return state, f"Fill {label} from your code and trace, then run /continue."

    return (
        "CLOSE",
        "Run just practice-test, reconcile comments with code, then use just practice-finish.",
    )


def show_next(root: Path, metadata: dict[str, Any]) -> int:
    state, next_action = next_step(root, metadata)
    print(f"STATE: {state}")
    print(f"SOURCE: {metadata['source']}")
    print(f"TEST: {metadata['candidate_test']}")
    print(f"NEXT: {next_action}")
    return 0


def _replace_file(path: Path, text: str) -> None:
    if path.is_symlink():
        raise PracticeError(f"refusing to replace symlinked file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def _normalized_note(note: str) -> str:
    normalized = " ".join(note.split())
    if not normalized:
        raise PracticeError("finish note is empty; name one specific fix")
    if len(normalized) > 500:
        raise PracticeError("finish note is too long; keep it under 500 characters")
    return normalized


def _append_rep_text(path: Path, rep_line: str) -> str:
    if path.is_symlink():
        raise PracticeError("private rep log cannot be a symlink")
    lines = path.read_text().splitlines() if path.exists() else []
    return "\n".join([*lines, rep_line]) + "\n"


def _progress_text(path: Path, topic: str, problem: str, today: str) -> str:
    if path.is_symlink():
        raise PracticeError("private progress file cannot be a symlink")
    key = f"{topic}/{problem}"
    line = f"- [x] {key} {today}"
    existing = path.read_text().splitlines() if path.exists() else []
    key_line = re.compile(rf"^- \[x\] {re.escape(key)}(?:\s|$)")
    kept = [current for current in existing if key_line.match(current) is None]
    return "\n".join([*kept, line]) + "\n"


def _commit_closeout(
    root: Path,
    *,
    kind: str,
    fingerprint: str,
    files: dict[str, str],
) -> None:
    """Write full desired state first, then replay it idempotently."""
    journal = {
        "schema": 1,
        "kind": kind,
        "fingerprint": fingerprint,
        "files": files,
    }
    _replace_file(_journal_path(root), json.dumps(journal, indent=2) + "\n")
    _recover_closeout(root, record_non_editor_receipt=False)


def _print_closed(paradigm: str, key: str, test_outcome: str | None = None) -> None:
    print(f"CLOSED: {paradigm} {key}")
    print("LOGGED: .challenges/reps.md")
    print("SPACED: .challenges/progress.md")
    if test_outcome is not None:
        print(f"TESTS: {test_outcome}")
    print("NEXT: Run just study-spaced 1 when you want another rep.")


def finish_session(root: Path, metadata: dict[str, Any], note: str) -> int:
    """Log one rep and schedule its next review through one idempotent command."""
    supplied_id = metadata.get("session_id") if isinstance(metadata, dict) else None
    normalized_note = _normalized_note(note)
    test_run: TestRun | None = None
    with _practice_lock(root, shared=True):
        current = _read_metadata(root)
        if supplied_id != current["session_id"]:
            raise PracticeError(
                "stale rep session; reload `just practice-current` before closing"
            )
        topic = str(current["topic"])
        problem = str(current["problem"])
        paradigm = str(current["paradigm"])
        key = f"{topic}/{problem}"
        if "finished_at" in current:
            _print_closed(paradigm, key, str(current["test_outcome"]))
            return 0

        rep = f"{paradigm} {key} fix: {normalized_note}"
        try:
            parse_rep_line(rep)
        except RepLineError as exc:
            raise PracticeError(
                f"finish note does not form a valid rep log: {exc}"
            ) from exc

        state, _ = next_step(root, current)
        if state == "CLOSE":
            before = _prepare_test_run(root, current, require_unlocked=True)
        else:
            before = _test_input_digests(root, current)
    if state == "CLOSE":
        test_run = _execute_test_run(root, current, before)
        after = test_run.after
        test_outcome = "passed" if test_run.returncode == 0 else "failed"
    else:
        after = dict(before)
        test_outcome = "not_run"

    with _practice_lock(root):
        if test_run is not None:
            _restore_plugin_for_same_session(root, current)
        current = _read_metadata(root)
        if supplied_id != current["session_id"]:
            raise PracticeError(
                "stale rep session; reload `just practice-current` before closing"
            )
        topic = str(current["topic"])
        problem = str(current["problem"])
        paradigm = str(current["paradigm"])
        key = f"{topic}/{problem}"
        if "finished_at" in current:
            _print_closed(paradigm, key, str(current["test_outcome"]))
            return 0
        if test_run is not None and test_run.timed_out:
            raise PracticeError(
                f"focused tests exceeded {_test_timeout_seconds()} seconds; "
                "the rep remains open"
            )
        if before != after:
            raise PracticeError(
                "test inputs changed while pytest was running; retry before closing"
            )
        if _test_input_digests(root, current) != after:
            raise PracticeError("practice files changed while closing; retry")
        final_state, _ = next_step(root, current)
        if final_state != state:
            raise PracticeError("practice state changed while closing; retry")

        today = date.today().isoformat()
        reps = _state_file(root, "reps.md")
        progress = _state_file(root, "progress.md")
        finished = dict(current)
        finished.update(
            {
                "finished_at": datetime.now(UTC).isoformat(),
                "finish_note": normalized_note,
                "finish_state": state,
                "test_outcome": test_outcome,
                "test_inputs_before": before,
                "test_inputs_after": after,
            }
        )
        files = {
            reps.relative_to(root).as_posix(): _append_rep_text(
                reps, f"- {today} {rep}"
            ),
            progress.relative_to(root).as_posix(): _progress_text(
                progress, topic, problem, today
            ),
            _metadata_path(root).relative_to(root).as_posix(): (
                json.dumps(finished, indent=2) + "\n"
            ),
        }
        _commit_closeout(
            root,
            kind="editor",
            fingerprint=str(current["session_id"]),
            files=files,
        )
        _read_metadata(root)
        _print_closed(paradigm, key, test_outcome)
        return 0


def log_rep(root: Path, line: str) -> int:
    """Append one validated non-editor rep line without shell interpolation."""
    normalized = " ".join(line.split())
    try:
        parse_rep_line(normalized)
    except RepLineError as exc:
        raise PracticeError(f"invalid rep line: {exc}") from exc
    with _practice_lock(root):
        reps = _state_file(root, "reps.md")
        dated = f"- {date.today().isoformat()} {normalized}"
        _replace_file(reps, _append_rep_text(reps, dated))
    print(dated)
    return 0


def complete_problem(root: Path, topic: str, problem: str) -> int:
    """Update one exact problem key in the private spaced-review file."""
    _validate_problem(topic, problem)
    with _practice_lock(root):
        progress = _state_file(root, "progress.md")
        _replace_file(
            progress,
            _progress_text(progress, topic, problem, date.today().isoformat()),
        )
    print(f"Marked complete: {topic}/{problem}")
    return 0


def finish_non_editor(root: Path, topic: str, problem: str, line: str) -> int:
    """Atomically pair a validated rep with the exact supplied draw.

    Identical same-day content is treated as a retry because this legacy command
    has no caller-provided idempotency key. Crash-recovery receipts extend that
    retry window through the calendar day after recovery, then expire so the
    same practice content can be logged again.
    """
    _validate_problem(topic, problem)
    normalized = " ".join(line.split())
    try:
        parsed = parse_rep_line(normalized)
    except RepLineError as exc:
        raise PracticeError(f"invalid rep line: {exc}") from exc
    if (parsed.topic, parsed.problem) != (topic, problem):
        raise PracticeError(
            "rep slug does not match the exact topic/problem being completed"
        )
    today = date.today().isoformat()
    fingerprint = hashlib.sha256(
        f"{topic}\0{problem}\0{normalized}".encode()
    ).hexdigest()
    with _practice_lock(root):
        if _has_active_non_editor_receipt(root, fingerprint, today):
            _print_closed(parsed.mode or "legacy", f"{topic}/{problem}")
            return 0
        reps = _state_file(root, "reps.md")
        progress = _state_file(root, "progress.md")
        dated = f"- {today} {normalized}"
        expected_progress = f"- [x] {topic}/{problem} {today}"
        if (
            reps.exists()
            and dated in reps.read_text().splitlines()
            and progress.exists()
            and expected_progress in progress.read_text().splitlines()
        ):
            # With no caller-provided idempotency key, an identical same-day
            # close is indistinguishable from a retry. A new day permits a new
            # rep unless a recent crash-recovery receipt says otherwise.
            _print_closed(parsed.mode or "legacy", f"{topic}/{problem}")
            return 0
        files = {
            reps.relative_to(root).as_posix(): _append_rep_text(reps, dated),
            progress.relative_to(root).as_posix(): _progress_text(
                progress, topic, problem, today
            ),
        }
        _commit_closeout(
            root,
            kind="non_editor",
            fingerprint=fingerprint,
            files=files,
        )
    _print_closed(parsed.mode or "legacy", f"{topic}/{problem}")
    return 0


def _require_unlocked(root: Path, metadata: dict[str, Any]) -> None:
    source = (root / str(metadata["source"])).read_text()
    if str(metadata["lock"]) in source:
        labels = ", ".join(str(label) for label in metadata["pre_code_labels"])
        raise PracticeError(
            f"thinking gate is still locked; fill {labels}, save, then delete it yourself"
        )
    statuses = _statuses(root, metadata)
    incomplete = [
        str(label)
        for label in metadata["pre_code_labels"]
        if statuses.get(str(label)) != "filled"
    ]
    if incomplete:
        labels = ", ".join(incomplete)
        raise PracticeError(
            f"thinking gate was removed before {labels} were filled; "
            "complete those comments and save"
        )


def _practice_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    paths = [str(_workspace(root)), str(root / "src")]
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def _pytest_args(metadata: dict[str, Any]) -> list[str]:
    return [
        "-m",
        "pytest",
        "-p",
        "practice_plugin",
        str(metadata["reference_test"]),
        str(metadata["candidate_test"]),
        "-v",
    ]


def _test_input_digests(root: Path, metadata: dict[str, Any]) -> dict[str, str]:
    digests: dict[str, str] = {}
    for key in TEST_INPUT_KEYS:
        path = root / str(metadata[key])
        try:
            contents = path.read_bytes()
        except OSError as exc:
            raise PracticeError(f"cannot digest test input {path}: {exc}") from exc
        digests[key] = hashlib.sha256(contents).hexdigest()
    return digests


def _require_committed_reference_test(root: Path, metadata: dict[str, Any]) -> None:
    relative = Path(str(metadata["reference_test"]))
    path = root / relative
    try:
        working = path.read_text()
    except OSError as exc:
        raise PracticeError(f"cannot read reference tests {relative}: {exc}") from exc
    committed = _committed_source(root, relative)
    if working != committed:
        raise PracticeError(
            "reference tests differ from committed HEAD; restore them before practice"
        )


def _test_timeout_seconds() -> int:
    raw = os.environ.get(
        "PRACTICE_TEST_TIMEOUT_SECONDS", str(DEFAULT_TEST_TIMEOUT_SECONDS)
    )
    try:
        value = int(raw)
    except ValueError as exc:
        raise PracticeError(
            "PRACTICE_TEST_TIMEOUT_SECONDS must be a whole number"
        ) from exc
    if not 1 <= value <= MAX_TEST_TIMEOUT_SECONDS:
        raise PracticeError(
            f"PRACTICE_TEST_TIMEOUT_SECONDS must be between 1 and "
            f"{MAX_TEST_TIMEOUT_SECONDS}"
        )
    return value


def _test_process_exited_unreaped(proc: subprocess.Popen[bytes]) -> bool:
    """Observe one child exit without freeing its PID/process-group identity."""
    try:
        result = os.waitid(
            os.P_PID,
            proc.pid,
            os.WEXITED | os.WNOHANG | os.WNOWAIT,
        )
    except ChildProcessError as exc:
        raise PracticeError("focused test process was reaped unexpectedly") from exc
    return result is not None


def _wait_for_test_process(proc: subprocess.Popen[bytes], timeout: int) -> bool:
    """Return whether pytest exited before ``timeout``, without reaping it."""
    deadline = time.monotonic() + timeout
    while not _test_process_exited_unreaped(proc):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(TEST_PROCESS_POLL_SECONDS, remaining))
    return True


def _signal_test_process_group(
    proc: subprocess.Popen[bytes], signal_number: int
) -> bool:
    """Signal pytest's still-reserved process group, if it has live members."""
    if proc.returncode is not None:
        # Popen has already reaped the leader, so its numeric PID/PGID may have
        # been reused. Never signal a group once that identity is unreserved.
        return False
    try:
        os.killpg(proc.pid, signal_number)
    except (PermissionError, ProcessLookupError):
        # macOS reports EPERM for a group containing only an unreaped zombie;
        # Linux generally reports ESRCH. Either means there is nothing this
        # process can signal.
        return False
    return True


def _sweep_test_process_group(proc: subprocess.Popen[bytes]) -> int:
    """Stop every pytest descendant, then reap the still-reserved leader."""
    if proc.returncode is not None:
        return proc.returncode

    if _signal_test_process_group(proc, signal.SIGTERM):
        deadline = time.monotonic() + TEST_PROCESS_TERM_GRACE_SECONDS
        while _signal_test_process_group(proc, 0):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(TEST_PROCESS_POLL_SECONDS, remaining))
        _signal_test_process_group(proc, signal.SIGKILL)

    # This is deliberately the first wait()/poll() call. WNOWAIT kept the
    # leader as a zombie until every group signal completed, so proc.pid could
    # not be recycled into an unrelated process group between observation and
    # cleanup.
    try:
        return proc.wait(timeout=TEST_PROCESS_KILL_WAIT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        raise PracticeError("focused test process resisted SIGKILL") from exc


def _prepare_test_run(
    root: Path, metadata: dict[str, Any], *, require_unlocked: bool
) -> dict[str, str]:
    if require_unlocked:
        _require_unlocked(root, metadata)
    _require_committed_reference_test(root, metadata)
    return _test_input_digests(root, metadata)


def _execute_test_run(
    root: Path, metadata: dict[str, Any], before: dict[str, str]
) -> TestRun:
    timeout = _test_timeout_seconds()
    try:
        proc = subprocess.Popen(
            [sys.executable, *_pytest_args(metadata)],
            cwd=root,
            env=_practice_env(root),
            start_new_session=True,
        )
    except OSError as exc:
        raise PracticeError(f"cannot launch focused tests: {exc}") from exc
    try:
        exited = _wait_for_test_process(proc, timeout)
    except BaseException:
        with suppress(Exception):
            _sweep_test_process_group(proc)
        raise
    returncode = _sweep_test_process_group(proc)
    timed_out = not exited
    if timed_out:
        returncode = 124
    after = _test_input_digests(root, metadata)
    return TestRun(
        returncode=returncode,
        before=before,
        after=after,
        timed_out=timed_out,
    )


def _raw_session_id(root: Path) -> str | None:
    workspace = _workspace(root)
    if workspace.is_symlink() or not workspace.is_dir():
        return None
    try:
        _confined_directory(root, workspace, "practice workspace", create=False)
    except PracticeError:
        return None
    path = _metadata_path(root)
    if path.is_symlink() or not path.is_file():
        return None
    try:
        value = json.loads(path.read_text())
    except OSError, json.JSONDecodeError:
        return None
    session_id = value.get("session_id") if isinstance(value, dict) else None
    return session_id if isinstance(session_id, str) else None


def _restore_plugin_for_same_session(root: Path, metadata: dict[str, Any]) -> None:
    if _raw_session_id(root) != metadata.get("session_id"):
        return
    plugin = root / str(metadata["plugin"])
    if plugin.is_symlink():
        raise PracticeError("practice plugin became a symlink while tests ran")
    source_rel = Path("src/algo") / str(metadata["topic"]) / f"{metadata['problem']}.py"
    expected_plugin = _pytest_plugin(
        str(metadata["module"]),
        Path(str(metadata["source"])).name,
        source_rel,
        str(metadata["target"]),
    )
    if not plugin.exists() or plugin.read_text() != expected_plugin:
        _replace_file(plugin, expected_plugin)


def run_tests(root: Path, metadata: dict[str, Any]) -> int:
    with _practice_lock(root, shared=True):
        current = _read_metadata(root)
        if metadata.get("session_id") != current["session_id"]:
            raise PracticeError("stale rep session; reload `just practice-current`")
        before = _prepare_test_run(root, current, require_unlocked=True)
    result = _execute_test_run(root, current, before)
    with _practice_lock(root):
        _restore_plugin_for_same_session(root, current)
        latest = _read_metadata(root)
        if current["session_id"] != latest["session_id"]:
            raise PracticeError("stale rep session; reload `just practice-current`")
        latest_digests = _test_input_digests(root, latest)
    if result.timed_out:
        print(
            f"practice: focused tests exceeded {_test_timeout_seconds()} seconds; "
            "the rep remains open",
            file=sys.stderr,
        )
        return 124
    if not result.fresh or latest_digests != result.after:
        print(
            "practice: test inputs changed while pytest was running; "
            "rerun for a fresh result",
            file=sys.stderr,
        )
        return 3
    return result.returncode


def run_watch(root: Path, metadata: dict[str, Any]) -> int:
    _require_unlocked(root, metadata)
    _require_committed_reference_test(root, metadata)
    watchexec = shutil.which("watchexec")
    if watchexec is None:
        raise PracticeError("watchexec is missing; use `just practice-test`")
    reference_test = root / str(metadata["reference_test"])
    args = [
        watchexec,
        "--ignore-nothing",
        "-e",
        "py",
        "-w",
        str(_workspace(root)),
        "-w",
        str(reference_test),
        "--",
        "just",
        "practice-test",
    ]
    os.execvpe(watchexec, args, os.environ.copy())
    return 1  # pragma: no cover - exec replaces the process


def run_repl(root: Path, metadata: dict[str, Any]) -> int:
    _require_unlocked(root, metadata)
    repl = root / str(metadata["repl"])
    os.execvpe(
        sys.executable,
        [sys.executable, "-i", str(repl)],
        _practice_env(root),
    )
    return 1  # pragma: no cover - exec replaces the process


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start", help="create or resume an editor rep")
    start.add_argument("paradigm", choices=tuple(PARADIGMS))
    start.add_argument("topic", nargs="?")
    start.add_argument("problem", nargs="?")
    start.add_argument("--fresh", action="store_true")
    start.add_argument("--no-open", action="store_true")
    present = commands.add_parser(
        "present", help="print one committed cold statement without opening the editor"
    )
    present.add_argument("topic", nargs="?")
    present.add_argument("problem", nargs="?")
    reference = commands.add_parser(
        "reference", help="print one committed implementation without restoring files"
    )
    reference.add_argument("topic", nargs="?")
    reference.add_argument("problem", nargs="?")
    for name in ("next", "status", "test", "watch", "repl", "open", "current"):
        commands.add_parser(name)
    finish = commands.add_parser(
        "finish", help="log the current rep and schedule its next review"
    )
    finish.add_argument("note")
    log = commands.add_parser("log", help="append one validated private rep")
    log.add_argument("line")
    complete = commands.add_parser("complete", help="schedule one exact review")
    complete.add_argument("topic")
    complete.add_argument("problem")
    finish_non_editor_parser = commands.add_parser(
        "finish-non-editor", help="atomically log and schedule a non-editor rep"
    )
    finish_non_editor_parser.add_argument("topic")
    finish_non_editor_parser.add_argument("problem")
    finish_non_editor_parser.add_argument("line")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "present":
            topic, problem = select_problem(ROOT, args.topic, args.problem)
            print(present_problem(ROOT, topic, problem).rstrip())
            print()
            print(f"PRACTICE: {topic}/{problem}")
            print("NEXT: Ask the candidate to restate the problem and clarify it.")
            return 0
        if args.command == "reference":
            if args.topic is None and args.problem is None:
                current = current_metadata(ROOT)
                topic = str(current["topic"])
                problem = str(current["problem"])
            else:
                topic, problem = select_problem(ROOT, args.topic, args.problem)
            print(reference_solution(ROOT, topic, problem).rstrip())
            return 0
        if args.command == "start":
            metadata, action, archived = prepare_session(
                ROOT,
                args.paradigm,
                args.topic,
                args.problem,
                fresh=args.fresh,
            )
            if not args.no_open and not os.environ.get("PRACTICE_NO_OPEN"):
                open_session(ROOT, metadata)
            _print_start(ROOT, metadata, action, archived)
            return 0
        if args.command == "log":
            return log_rep(ROOT, args.line)
        if args.command == "complete":
            return complete_problem(ROOT, args.topic, args.problem)
        if args.command == "finish-non-editor":
            return finish_non_editor(ROOT, args.topic, args.problem, args.line)

        metadata = current_metadata(ROOT)
        if args.command == "next":
            return show_next(ROOT, metadata)
        if args.command == "status":
            return show_status(ROOT, metadata)
        if args.command == "test":
            return run_tests(ROOT, metadata)
        if args.command == "watch":
            return run_watch(ROOT, metadata)
        if args.command == "repl":
            return run_repl(ROOT, metadata)
        if args.command == "open":
            return 0 if open_session(ROOT, metadata) else 1
        if args.command == "current":
            print(json.dumps(metadata, indent=2))
            return 0
        if args.command == "finish":
            return finish_session(ROOT, metadata, args.note)
    except PracticeError as exc:
        print(f"practice: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
