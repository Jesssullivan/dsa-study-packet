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
    practice_workspace.py open [topic problem]
    practice_workspace.py next | status | test | watch | repl | current
    practice_workspace.py finish "trace before optimizing"
"""

from __future__ import annotations

import argparse
import ast
import builtins
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
from catalog import selection_error
from core42 import PRACTICE_TARGETS
from rep_schema import RepLineError, parse_rep_line
from scaffold_status import (
    CommentEvidence,
    CommentSnapshot,
    _selected_target,
    candidate_comment_snapshot,
)
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
COMMENT_RECEIPT_NAME = "comment-receipt.json"
METADATA_SCHEMA = 4
COMMENT_RECEIPT_SCHEMA = 1
JOURNAL_REL = Path(".challenges/practice-closeout.json")
NON_EDITOR_RECEIPTS_REL = Path(".challenges/non-editor-receipts.json")
LOCK_REL = Path(".challenges/.practice.lock")
MAX_HISTORY_ENTRIES = 100
MAX_HISTORY_BYTES = 512 * 1024 * 1024
MAX_NON_EDITOR_RECEIPTS = 100
MAX_REQUIRED_PRE_CODE_COMMENTS = 3
REQUIRED_POST_CODE_COMMENTS = 3
MAX_COMMENT_RECEIPT_KEYS = 256
DEFAULT_TEST_TIMEOUT_SECONDS = 120
MAX_TEST_TIMEOUT_SECONDS = 900
EDITOR_OPEN_TIMEOUT_SECONDS = 10
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
class CommentReceipt:
    """Private temporal evidence for comments added after the thinking phase."""

    armed: bool
    observed: frozenset[str]
    accepted: frozenset[str]


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
            "# Write what this function should return and any assumptions in your own words.",
            "# Work one ordinary example and one edge case by hand.",
            "# Note the simplest correct plan and what must stay true while it runs.",
            "# Narrate the next code choice before implementing it.",
            "# Trace one example and note which tests prove the important edges.",
            "# Record the final time and space costs plus anything still uncertain.",
        ),
        lock_after=3,
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


def _validate_practice_selection(root: Path, topic: str, problem: str) -> None:
    """Reject non-canonical pairs before any source or test path is read."""
    _validate_problem(topic, problem)
    if (topic, problem) not in PRACTICE_TARGETS:
        raise PracticeError(selection_error(topic, problem, root))


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
    has_topic = topic not in (None, "")
    has_problem = problem not in (None, "")
    if has_topic != has_problem:
        supplied = topic if has_topic else problem
        raise PracticeError(
            "provide both topic and problem, or omit both for a draw\n"
            f"MATCH: one natural name, {supplied!r}, is not an exact pair\n"
            f'NEXT: run `just catalog "{supplied}"` for exact topic/problem pairs.'
        )
    if not has_topic and not has_problem:
        topic, problem = _draw_problem(root)
    assert topic is not None
    assert problem is not None
    _validate_practice_selection(root, topic, problem)
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


_BUILTIN_NAMES = frozenset(dir(builtins))
_DEFINITION = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


def _has_cold_stub(node: ast.AST) -> bool:
    return any(
        isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
        and member.body
        and isinstance(member.body[-1], ast.Raise)
        for member in ast.walk(node)
    )


def _select_candidate_definition(tree: ast.Module, target: str | None) -> _DEFINITION:
    definitions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    if target is not None:
        selected = next((node for node in definitions if node.name == target), None)
    else:
        # The target-less API is retained for preview tests. Prefer a top-level
        # function so an earlier input model such as ListNode is not mistaken
        # for the exercise target.
        selected = next(
            (
                node
                for node in definitions
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and _has_cold_stub(node)
            ),
            None,
        )
        if selected is None:
            selected = next(
                (node for node in definitions if _has_cold_stub(node)), None
            )
    if selected is None:
        label = target or "a public definition"
        raise ValueError(f"candidate target {label!r} is absent")
    return selected


def _drop_definition_docstrings(node: ast.AST) -> None:
    for definition in ast.walk(node):
        if not isinstance(
            definition, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            continue
        if (
            definition.body
            and isinstance(definition.body[0], ast.Expr)
            and isinstance(definition.body[0].value, ast.Constant)
            and isinstance(definition.body[0].value.value, str)
        ):
            definition.body.pop(0)


def _prune_candidate_interface(selected: _DEFINITION) -> _DEFINITION:
    if isinstance(selected, ast.ClassDef):
        selected.body = [
            member
            for member in selected.body
            if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
            and (member.name == "__init__" or not member.name.startswith("_"))
        ]
        if not selected.body:
            selected.body = [ast.Pass()]
    _drop_definition_docstrings(selected)
    return selected


def _type_parameter_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for member in ast.walk(node):
        for parameter in getattr(member, "type_params", ()):
            name = getattr(parameter, "name", None)
            if isinstance(name, str):
                names.add(name)
    return names


def _external_names(node: ast.AST, *, own_names: set[str] | None = None) -> set[str]:
    loaded = {
        member.id
        for member in ast.walk(node)
        if isinstance(member, ast.Name) and isinstance(member.ctx, ast.Load)
    }
    bound = {member.arg for member in ast.walk(node) if isinstance(member, ast.arg)}
    bound.update(
        member.id
        for member in ast.walk(node)
        if isinstance(member, ast.Name) and isinstance(member.ctx, ast.Store)
    )
    bound.update(_type_parameter_names(node))
    bound.update(own_names or ())
    return loaded - bound - _BUILTIN_NAMES


def _candidate_support_class(node: ast.ClassDef) -> ast.ClassDef:
    """Keep a constructible input model without exposing algorithm helpers."""
    kept: list[ast.stmt] = []
    for member in node.body:
        if (
            isinstance(member, ast.Expr)
            and isinstance(member.value, ast.Constant)
            and isinstance(member.value.value, str)
        ):
            continue
        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if member.name == "__repr__":
                continue
            if member.name != "__init__":
                raise ValueError(
                    f"candidate support class {node.name!r} is not data-only"
                )
            kept.append(member)
            continue
        if isinstance(member, ast.Assign):
            names = {
                target.id for target in member.targets if isinstance(target, ast.Name)
            }
            if names != {"__slots__"}:
                raise ValueError(
                    f"candidate support class {node.name!r} is not data-only"
                )
            kept.append(member)
            continue
        if isinstance(member, (ast.AnnAssign, ast.Pass)):
            kept.append(member)
            continue
        raise ValueError(f"candidate support class {node.name!r} is not data-only")
    node.body = kept or [ast.Pass()]
    _drop_definition_docstrings(node)
    return node


def _register_imports(
    bindings: dict[str, tuple[str, int, ast.AST, ast.alias]],
    node: ast.Import | ast.ImportFrom,
    order: int,
) -> None:
    for alias in node.names:
        if alias.name == "*":
            continue
        if isinstance(node, ast.Import):
            name = alias.asname or alias.name.split(".", 1)[0]
        else:
            name = alias.asname or alias.name
        bindings[name] = ("import", order, node, alias)


def _dependency_bindings(
    original: ast.Module,
) -> dict[str, tuple[str, int, ast.AST, ast.alias | None]]:
    bindings: dict[str, tuple[str, int, ast.AST, ast.alias | None]] = {}
    for index, node in enumerate(original.body):
        order = index * 1000
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            _register_imports(bindings, node, order)
            continue
        if (
            isinstance(node, ast.If)
            and isinstance(node.test, ast.Name)
            and node.test.id == "TYPE_CHECKING"
        ):
            for nested_index, nested in enumerate(node.body, start=1):
                if isinstance(nested, (ast.Import, ast.ImportFrom)):
                    _register_imports(bindings, nested, order + nested_index)
            continue
        if isinstance(node, ast.TypeAlias) and isinstance(node.name, ast.Name):
            bindings[node.name.id] = ("alias", order, node, None)
            continue
        if isinstance(node, ast.ClassDef):
            bindings[node.name] = ("class", order, node, None)
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target_node in targets:
                if isinstance(target_node, ast.Name):
                    bindings[target_node.id] = ("assignment", order, node, None)
    return bindings


def _candidate_dependencies(
    original: ast.Module, selected: _DEFINITION
) -> list[ast.stmt]:
    bindings = _dependency_bindings(original)
    pending = sorted(_external_names(selected, own_names={selected.name}), reverse=True)
    visited: set[str] = set()
    imports: dict[int, tuple[ast.Import | ast.ImportFrom, list[ast.alias]]] = {}
    nodes: dict[int, ast.stmt] = {}

    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        dependency = bindings.get(name)
        if dependency is None:
            raise ValueError(f"candidate interface name {name!r} is unresolved")
        kind, order, node, alias = dependency
        if kind == "import":
            assert isinstance(node, (ast.Import, ast.ImportFrom))
            assert alias is not None
            template, aliases = imports.setdefault(order, (node, []))
            if all(
                (item.name, item.asname) != (alias.name, alias.asname)
                for item in aliases
            ):
                aliases.append(alias)
            continue
        if kind == "alias":
            assert isinstance(node, ast.TypeAlias)
            nodes[order] = node
            pending.extend(
                sorted(_external_names(node, own_names={name}), reverse=True)
            )
            continue
        if kind == "class":
            assert isinstance(node, ast.ClassDef)
            support = _candidate_support_class(node)
            nodes[order] = support
            pending.extend(
                sorted(_external_names(support, own_names={name}), reverse=True)
            )
            continue
        assert kind == "assignment"
        assert isinstance(node, (ast.Assign, ast.AnnAssign))
        value = node.value
        if value is None:
            raise ValueError(f"candidate interface value {name!r} has no default")
        try:
            ast.literal_eval(value)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"candidate interface value {name!r} is not a literal"
            ) from exc
        nodes[order] = node
        pending.extend(sorted(_external_names(node, own_names={name}), reverse=True))

    rendered: dict[int, ast.stmt] = dict(nodes)
    for order, (template, aliases) in imports.items():
        wanted = {(alias.name, alias.asname) for alias in aliases}
        aliases = [
            alias for alias in template.names if (alias.name, alias.asname) in wanted
        ]
        if isinstance(template, ast.Import):
            rendered[order] = ast.Import(names=aliases)
        else:
            rendered[order] = ast.ImportFrom(
                module=template.module,
                names=aliases,
                level=template.level,
            )
    return [rendered[order] for order in sorted(rendered)]


def render_candidate(source: str, paradigm: Paradigm, target: str | None = None) -> str:
    """Return one cold public interface with its minimum input-model surface."""
    # Stripping every body is insufficient: alternate names, imports, comments,
    # and definition docstrings can still disclose the intended approach.
    original = ast.parse(source)
    cold_tree = ast.parse(truncate_module_docstring(strip_solution(source)))
    selected = _prune_candidate_interface(
        _select_candidate_definition(cold_tree, target)
    )
    dependencies = _candidate_dependencies(original, selected)

    statement = ast.get_docstring(cold_tree, clean=False)
    body: list[ast.stmt] = []
    if statement is not None:
        body.append(ast.Expr(value=ast.Constant(value=statement)))
    body.append(
        ast.ImportFrom(
            module="__future__",
            names=[ast.alias(name="annotations")],
            level=0,
        )
    )
    body.extend([*dependencies, selected])
    cold = ast.unparse(
        ast.fix_missing_locations(ast.Module(body=body, type_ignores=[]))
    )
    cold += "\n"
    return inject_scaffold(
        cold,
        seeds=paradigm.seeds,
        lock_sentinel=PRACTICE_LOCK,
        lock_after=paradigm.lock_after,
        target_name=selected.name,
    )


def present_problem(root: Path, topic: str, problem: str) -> str:
    """Return a cold statement from committed source without creating a rep."""
    _validate_practice_selection(root, topic, problem)
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    source = truncate_module_docstring(_committed_source(root, source_rel))
    try:
        return module_docstring_block(source)
    except ValueError as exc:
        raise PracticeError(f"cannot present {topic}/{problem}: {exc}") from exc


def reference_solution(root: Path, topic: str, problem: str) -> str:
    """Return the committed implementation without touching working files."""
    _validate_practice_selection(root, topic, problem)
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

import pytest

MODULE = {module!r}
CANDIDATE = Path(__file__).with_name({candidate_name!r})
CANDIDATE_TEST = Path(__file__).with_name(
    f"test_{{CANDIDATE.stem}}_candidate.py"
)
ROOT = Path(__file__).resolve().parents[2]
SOURCE_REL = {source_rel.as_posix()!r}
TARGET = {target!r}
SUPPORT: tuple[str, ...] = ()
_REFERENCE: types.ModuleType | None = None
_CANDIDATE_MODULE: types.ModuleType | None = None
_REFERENCE_TARGET: object | None = None


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
    global _CANDIDATE_MODULE, _REFERENCE, _REFERENCE_TARGET
    reference = _committed_reference()
    candidate, parent, child_name = _load_candidate()
    for name, value in vars(candidate).items():
        if name not in vars(reference) and not name.startswith("__"):
            setattr(reference, name, value)
    _REFERENCE = reference
    _CANDIDATE_MODULE = candidate
    _REFERENCE_TARGET = getattr(reference, TARGET)
    setattr(reference, TARGET, getattr(candidate, TARGET))
    sys.modules[MODULE] = reference
    setattr(parent, child_name, reference)


def pytest_collection_modifyitems(items: list[object]) -> None:
    """Repair direct aliases captured before the candidate facade was installed."""
    if _REFERENCE is None or _CANDIDATE_MODULE is None or _REFERENCE_TARGET is None:
        raise RuntimeError("practice plugin was not configured")
    candidate_target = getattr(_CANDIDATE_MODULE, TARGET)
    for item in items:
        test_module = getattr(item, "module", None)
        if test_module is None:
            continue
        for name, value in tuple(vars(test_module).items()):
            if value is _REFERENCE_TARGET:
                setattr(test_module, name, candidate_target)
    setattr(_REFERENCE, TARGET, candidate_target)
    parent_name, child_name = MODULE.rsplit(".", 1)
    parent = importlib.import_module(parent_name)
    sys.modules[MODULE] = _CANDIDATE_MODULE
    setattr(parent, child_name, _CANDIDATE_MODULE)
    candidate_path = CANDIDATE_TEST.resolve()
    if not any(
        Path(str(getattr(item, "path", ""))).resolve() == candidate_path
        for item in items
    ):
        raise pytest.UsageError(
            "candidate test file collected no tests; add a top-level test_ function"
        )
'''


def _repl_bootstrap(module: str, target: str) -> str:
    return f'''"""Interactive bootstrap for the current practice implementation."""

from practice_plugin import TARGET, load_candidate

candidate = load_candidate()
globals()[TARGET] = getattr(candidate, TARGET)
print("Loaded {module}.{target}; signature input types are available on candidate.")
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
    prepared_fields = {"prepared_only", "presented_at"}
    keys = set(value)
    if not required <= keys or keys - required - finished_fields - prepared_fields:
        missing = sorted(required - keys)
        extra = sorted(keys - required - finished_fields - prepared_fields)
        raise PracticeError(
            f"invalid current-rep metadata fields (missing={missing}, extra={extra})"
        )
    has_finished = bool(keys & finished_fields)
    is_prepared = value.get("prepared_only") is True
    if "prepared_only" in value and not is_prepared:
        raise PracticeError(
            "invalid current-rep metadata: prepared_only must be true when present"
        )
    if is_prepared and has_finished:
        raise PracticeError(
            "invalid current-rep metadata: prepared tabs cannot be finished"
        )
    if "presented_at" in value:
        if not is_prepared:
            raise PracticeError(
                "invalid current-rep metadata: only prepared tabs can be presented"
            )
        _parse_timestamp(value["presented_at"], "presented_at")
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
    session_rel = (WORKSPACE_REL / METADATA_NAME).as_posix()
    if journal["kind"] == "editor":
        valid_file_sets = {frozenset(paired | {session_rel})}
    else:
        valid_file_sets = {
            frozenset(paired),
            frozenset(paired | {session_rel}),
        }
    if frozenset(files) not in valid_file_sets or set(files) - allowed:
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


def _unfinished_session_error(
    metadata: dict[str, Any], paradigm: str, topic: str, problem: str
) -> PracticeError:
    current = f"{metadata['paradigm']} {metadata['topic']}/{metadata['problem']}"
    return PracticeError(
        f"unfinished editor rep: {current}\n"
        'NEXT: run `just practice-finish "<one concrete fix>"`, '
        "then retry; or explicitly archive it with "
        f"`just practice-new {paradigm} {topic} {problem}`."
    )


def _is_prepared(metadata: dict[str, Any]) -> bool:
    return metadata.get("prepared_only") is True


def _is_presented(metadata: dict[str, Any]) -> bool:
    return _is_prepared(metadata) and "presented_at" in metadata


def _prepared_workspace_is_pristine(root: Path, metadata: dict[str, Any]) -> bool:
    """Return whether prepared candidate-owned files still match their seed."""
    if not _is_prepared(metadata):
        return False
    topic = str(metadata["topic"])
    problem = str(metadata["problem"])
    target = str(metadata["target"])
    source_rel = Path("src/algo") / topic / f"{problem}.py"
    committed = _committed_source(root, source_rel)
    expected = {
        str(metadata["source"]): render_candidate(
            committed, PARADIGMS[str(metadata["paradigm"])], target
        ),
        str(metadata["candidate_test"]): _candidate_test(topic, problem, target),
        str(metadata["plugin"]): _pytest_plugin(
            str(metadata["module"]), f"{problem}.py", source_rel, target
        ),
        str(metadata["repl"]): _repl_bootstrap(str(metadata["module"]), target),
    }
    workspace = _workspace(root)
    expected_entries = {
        (root / relative).relative_to(workspace) for relative in expected
    } | {Path(METADATA_NAME)}
    entries = list(workspace.iterdir())
    if any(path.is_symlink() or not path.is_file() for path in entries):
        return False
    if {path.relative_to(workspace) for path in entries} != expected_entries:
        return False
    return all(
        (root / relative).read_text() == text for relative, text in expected.items()
    )


def _prepared_session_error(
    metadata: dict[str, Any], paradigm: str, topic: str, problem: str
) -> PracticeError:
    current = f"{metadata['topic']}/{metadata['problem']}"
    return PracticeError(
        f"prepared candidate tabs contain unclosed work for {current}\n"
        f"NEXT: keep it with `just practice-start comments {current.replace('/', ' ')}`; "
        "close the matching talk or board rep; or explicitly archive it with "
        f"`just practice-new {paradigm} {topic} {problem}`."
    )


def prepare_session(
    root: Path,
    paradigm_name: str,
    topic: str | None = None,
    problem: str | None = None,
    *,
    fresh: bool = False,
    match_any_paradigm: bool = False,
    prepared_only: bool = False,
) -> tuple[dict[str, Any], str, Path | None]:
    """Create or resume one current workspace.

    Returns ``(metadata, action, archived_path)`` where action is ``created``
    or ``resumed``. A different/fresh session archives the previous workspace.
    """
    paradigm = PARADIGMS.get(paradigm_name)
    if paradigm is None:
        choices = ", ".join(PARADIGMS)
        raise PracticeError(f"unknown paradigm {paradigm_name!r}; choose {choices}")

    explicit = topic not in (None, "") or problem not in (None, "")
    selected = select_problem(root, topic, problem) if explicit else None
    with _practice_lock(root):
        if selected is None:
            topic, problem = select_problem(root)
        else:
            topic, problem = selected

        workspace = _workspace(root)
        if workspace.is_symlink():
            raise PracticeError("practice workspace cannot be a symlink")
        if workspace.exists() and not fresh:
            try:
                metadata = _read_metadata(root)
            except PracticeError:
                metadata = None
            if metadata is not None and "finished_at" not in metadata:
                same_target = (metadata["topic"], metadata["problem"]) == (
                    topic,
                    problem,
                )
                if _is_prepared(metadata):
                    if prepared_only and same_target:
                        return metadata, "resumed", None
                    if (
                        not prepared_only
                        and same_target
                        and metadata["paradigm"] == paradigm_name
                    ):
                        activated = dict(metadata)
                        activated.pop("prepared_only")
                        activated.pop("presented_at", None)
                        _replace_file(
                            _metadata_path(root), json.dumps(activated, indent=2) + "\n"
                        )
                        return _read_metadata(root), "resumed", None
                    prepared_is_pristine = _prepared_workspace_is_pristine(
                        root, metadata
                    )
                    if not prepared_is_pristine and not _is_presented(metadata):
                        raise _prepared_session_error(
                            metadata, paradigm_name, topic, problem
                        )
                elif _same_session(metadata, paradigm_name, topic, problem) or (
                    match_any_paradigm and same_target
                ):
                    return metadata, "resumed", None
                else:
                    raise _unfinished_session_error(
                        metadata, paradigm_name, topic, problem
                    )

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
        if prepared_only:
            metadata["prepared_only"] = True
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


def prepare_open_target(
    root: Path, topic: str | None, problem: str | None
) -> dict[str, Any]:
    """Return safe candidate tabs for one exact selection.

    A matching unfinished workspace is reopened without changing its paradigm
    or contents. With no current workspace, the ordinary-comments renderer
    creates the same stripped candidate surface used by an editor rep. A
    different unfinished workspace keeps the normal switch boundary.
    """
    metadata, _, archived = prepare_session(
        root,
        "comments",
        topic,
        problem,
        match_any_paradigm=True,
        prepared_only=True,
    )
    if archived is not None:
        print(f"Previous workspace archived: {archived.relative_to(root)}")
    return metadata


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
    try:
        proc = subprocess.run(
            [code, "--reuse-window", candidate_test, "--goto", f"{source}:{line}"],
            cwd=root,
            check=False,
            timeout=EDITOR_OPEN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"Open {source}:{line} and {candidate_test}")
        return False
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


def _comment_evidence(source: str, metadata: dict[str, Any]) -> CommentEvidence:
    return _comment_snapshot(source, metadata).evidence


def _comment_snapshot(source: str, metadata: dict[str, Any]) -> CommentSnapshot:
    seeds = tuple(str(seed) for seed in metadata["seeds"])
    lock = str(metadata["lock"])
    pre_required, _ = _comment_requirements(metadata)
    return candidate_comment_snapshot(
        source,
        seeds=seeds,
        lock_sentinel=lock,
        pre_code_count=len(metadata["pre_code_labels"]),
        natural_pre_code_count=pre_required,
        target=str(metadata["target"]),
    )


def _comment_receipt_path(root: Path) -> Path:
    return _workspace(root) / COMMENT_RECEIPT_NAME


def _comment_key_digest(session_id: str, key: str) -> str:
    return hashlib.sha256(f"{session_id}\0{key}".encode()).hexdigest()


def _comment_key_digests(
    snapshot: CommentSnapshot, session_id: str
) -> tuple[set[str], set[str], set[str], set[str]]:
    all_keys = {
        _comment_key_digest(session_id, key) for key in snapshot.all_keys
    }
    pre_keys = {
        _comment_key_digest(session_id, key) for key in snapshot.pre_keys
    }
    anchored_post_keys = {
        _comment_key_digest(session_id, key)
        for key in snapshot.anchored_post_keys
    }
    legacy_post_keys = {
        _comment_key_digest(session_id, key)
        for key in snapshot.legacy_post_keys
    }
    return all_keys, pre_keys, anchored_post_keys, legacy_post_keys


def _read_comment_receipt(
    root: Path, metadata: dict[str, Any]
) -> CommentReceipt | None:
    path = _comment_receipt_path(root)
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise PracticeError("comment receipt must be a regular file")
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PracticeError(f"invalid comment receipt: {exc}") from exc
    expected_fields = {"schema", "session_id", "armed", "observed", "accepted"}
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise PracticeError("invalid comment receipt fields")
    if value["schema"] != COMMENT_RECEIPT_SCHEMA:
        raise PracticeError("invalid comment receipt schema")
    if value["session_id"] != metadata["session_id"]:
        raise PracticeError("comment receipt belongs to a different practice session")
    if type(value["armed"]) is not bool:
        raise PracticeError("invalid comment receipt armed state")

    def digest_set(field: str) -> frozenset[str]:
        items = value[field]
        if not isinstance(items, list) or len(items) > MAX_COMMENT_RECEIPT_KEYS:
            raise PracticeError(f"invalid comment receipt {field} list")
        if any(type(item) is not str or HEX_DIGEST.fullmatch(item) is None for item in items):
            raise PracticeError(f"invalid comment receipt {field} digest")
        if len(set(items)) != len(items):
            raise PracticeError(f"duplicate comment receipt {field} digest")
        return frozenset(items)

    observed = digest_set("observed")
    accepted = digest_set("accepted")
    if not accepted <= observed:
        raise PracticeError("comment receipt accepted keys were not observed")
    return CommentReceipt(bool(value["armed"]), observed, accepted)


def _comment_receipt_text(
    metadata: dict[str, Any], receipt: CommentReceipt
) -> str:
    value = {
        "schema": COMMENT_RECEIPT_SCHEMA,
        "session_id": metadata["session_id"],
        "armed": receipt.armed,
        "observed": sorted(receipt.observed),
        "accepted": sorted(receipt.accepted),
    }
    return json.dumps(value, indent=2) + "\n"


def _effective_comment_evidence(
    root: Path,
    metadata: dict[str, Any],
    source: str,
    snapshot: CommentSnapshot,
) -> CommentEvidence:
    receipt = _read_comment_receipt(root, metadata)
    if receipt is None:
        pre_required, _ = _comment_requirements(metadata)
        post_count = (
            len(snapshot.anchored_post_keys | snapshot.legacy_post_keys)
            if str(metadata["lock"]) not in source
            and len(snapshot.pre_keys) >= pre_required
            else 0
        )
        return CommentEvidence(
            len(snapshot.pre_keys), post_count
        )
    current, pre_keys, anchored_post, _legacy_post = _comment_key_digests(
        snapshot, str(metadata["session_id"])
    )
    active_post = (set(receipt.accepted) & current) - pre_keys
    if str(metadata["lock"]) not in source:
        eligible = current if receipt.armed else anchored_post
        active_post.update((current - set(receipt.observed)) & eligible)
        active_post.difference_update(pre_keys)
    return CommentEvidence(len(snapshot.pre_keys), len(active_post))


def _advance_comment_receipt(
    root: Path,
    metadata: dict[str, Any],
    source: str,
    snapshot: CommentSnapshot,
) -> CommentEvidence:
    previous_receipt = _read_comment_receipt(root, metadata)
    receipt = previous_receipt
    if receipt is None:
        receipt = CommentReceipt(False, frozenset(), frozenset())
    current, pre_keys, anchored_post, legacy_post = _comment_key_digests(
        snapshot, str(metadata["session_id"])
    )
    observed = set(receipt.observed)
    accepted = set(receipt.accepted)
    pre_required, _ = _comment_requirements(metadata)
    locked = str(metadata["lock"]) in source
    armed = receipt.armed
    pre_complete = len(snapshot.pre_keys) >= pre_required
    if locked or not pre_complete:
        if locked and pre_complete:
            armed = True
    else:
        if armed:
            accepted.update(current - observed)
        else:
            initial_anchors = anchored_post
            if previous_receipt is None:
                initial_anchors |= legacy_post
            accepted.update((current - observed) & initial_anchors)
        armed = True
    observed.update(current)
    if len(observed) > MAX_COMMENT_RECEIPT_KEYS:
        raise PracticeError(
            "comment receipt is full; start a fresh rep before adding more comments"
        )
    accepted.intersection_update(observed)
    updated = CommentReceipt(armed, frozenset(observed), frozenset(accepted))
    source_path = root / str(metadata["source"])
    if source_path.read_text() != source:
        raise PracticeError("source changed while reading comments; run /continue again")
    receipt_path = _comment_receipt_path(root)
    _replace_file(receipt_path, _comment_receipt_text(metadata, updated))
    if source_path.read_text() != source:
        if previous_receipt is None:
            if receipt_path.is_symlink():
                raise PracticeError(
                    "comment receipt became a symlink while reading comments"
                )
            receipt_path.unlink(missing_ok=True)
        else:
            _replace_file(
                receipt_path,
                _comment_receipt_text(metadata, previous_receipt),
            )
        raise PracticeError("source changed while reading comments; run /continue again")
    active_post = (accepted & current) - pre_keys
    return CommentEvidence(len(snapshot.pre_keys), len(active_post))


def _comment_requirements(metadata: dict[str, Any]) -> tuple[int, int]:
    pre_code = min(MAX_REQUIRED_PRE_CODE_COMMENTS, len(metadata["pre_code_labels"]))
    return pre_code, REQUIRED_POST_CODE_COMMENTS


def _candidate_test_count(root: Path, metadata: dict[str, Any]) -> int:
    try:
        tree = ast.parse((root / str(metadata["candidate_test"])).read_text())
    except SyntaxError as exc:
        raise PracticeError(f"candidate tests have a syntax error: {exc}") from exc

    missing = object()
    unknown = object()
    binding_type = tuple[str, ast.AST | None]
    other_binding: binding_type = ("other", None)
    object_flags: dict[int, object] = {}
    abstract_functions: set[int] = set()
    identity_decorators: set[int] = set()
    class_bases: dict[int, tuple[binding_type, ...]] = {}
    class_members: dict[int, dict[str, binding_type]] = {}
    class_flags: dict[int, object] = {}

    def literal(value: ast.expr) -> object:
        try:
            return ast.literal_eval(value)
        except (ValueError, TypeError, RecursionError):
            return unknown

    def resolved_literal(value: ast.expr, env: dict[str, binding_type]) -> object:
        result = literal(value)
        if result is not unknown or not isinstance(value, ast.Name):
            return result
        kind, constant = env.get(value.id, other_binding)
        if kind == "constant" and isinstance(constant, ast.expr):
            return literal(constant)
        return unknown

    def attribute_path(value: ast.expr) -> tuple[str, ...] | None:
        path: list[str] = []
        current = value
        while isinstance(current, ast.Attribute):
            path.append(current.attr)
            current = current.value
        if not isinstance(current, ast.Name):
            return None
        path.append(current.id)
        return tuple(reversed(path))

    def resolve_binding(
        value: ast.expr, env: dict[str, binding_type]
    ) -> binding_type:
        if isinstance(value, ast.Name):
            return env.get(value.id, other_binding)
        path = attribute_path(value)
        if path is not None and len(path) >= 2:
            owner, owner_node = env.get(path[0], other_binding)
            if (
                owner in {"class", "instance"}
                and isinstance(owner_node, ast.ClassDef)
                and len(path) == 2
            ):
                member_kind, member = class_members.get(id(owner_node), {}).get(
                    path[1], other_binding
                )
                if (
                    member_kind == "function"
                    and member is not None
                    and id(member) in identity_decorators
                ):
                    return ("safe_decorator", member)
            if owner == "pytest_module" and path[1] == "fixture":
                return ("fixture_decorator", value)
            if owner == "pytest_module" and path[1] == "mark":
                return ("safe_decorator", value)
            if owner == "pytest_mark":
                return ("safe_decorator", value)
            if owner == "hypothesis_module" and path[1] in {
                "example",
                "given",
                "reproduce_failure",
                "seed",
                "settings",
            }:
                return ("safe_decorator", value)
            if owner == "unittest_module" and path[1] == "TestCase":
                return ("unittest_base", value)
            if (
                owner == "unittest_module"
                and len(path) >= 3
                and path[1:3] == ("mock", "patch")
            ):
                return ("safe_decorator", value)
            if owner == "unittest_mock_module" and path[1] == "patch":
                return ("safe_decorator", value)
            if owner == "safe_decorator":
                return ("safe_decorator", value)
            if owner == "abc_module" and path[1] == "ABC":
                return ("abc_base", value)
            if owner == "abc_module" and path[1] == "abstractmethod":
                return ("abstract_decorator", value)
        if isinstance(value, ast.Call):
            resolved = resolve_binding(value.func, env)
            if resolved[0] in {"fixture_decorator", "safe_decorator"}:
                return resolved
            if resolved[0] == "class":
                return ("instance", resolved[1])
        constant = literal(value)
        if constant is not unknown:
            return ("constant", value)
        return other_binding

    def is_identity_decorator(
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> bool:
        if not isinstance(node, ast.FunctionDef):
            return False
        positional = [*node.args.posonlyargs, *node.args.args]
        return (
            len(positional) == 1
            and node.args.vararg is None
            and not node.args.kwonlyargs
            and node.args.kwarg is None
            and len(node.body) == 1
            and isinstance(node.body[0], ast.Return)
            and isinstance(node.body[0].value, ast.Name)
            and node.body[0].value.id == positional[0].arg
        )

    def decorator_kinds(
        decorators: list[ast.expr],
        env: dict[str, binding_type],
        *,
        in_class: bool,
    ) -> set[str]:
        kinds: set[str] = set()
        for decorator in decorators:
            resolved, resolved_node = resolve_binding(decorator, env)
            base = decorator.func if isinstance(decorator, ast.Call) else decorator
            if resolved in {
                "fixture_decorator",
                "safe_decorator",
                "abstract_decorator",
            }:
                kinds.add(resolved)
            elif (
                (
                    resolved == "function"
                    and resolved_node is not None
                    and id(resolved_node) in identity_decorators
                )
                or (
                    isinstance(base, ast.Name)
                    and (
                        base.id == "staticmethod"
                        or (in_class and base.id == "classmethod")
                    )
                    and base.id not in env
                )
            ):
                kinds.add("safe_decorator")
            else:
                kinds.add("unknown")
        return kinds

    def bind_target(
        target: ast.expr,
        binding: binding_type,
        env: dict[str, binding_type],
        local_names: set[str],
    ) -> None:
        if isinstance(target, ast.Name):
            env[target.id] = binding
            local_names.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                bind_target(element, other_binding, env, local_names)
        elif isinstance(target, ast.Starred):
            bind_target(target.value, other_binding, env, local_names)

    def delete_target(
        target: ast.expr,
        env: dict[str, binding_type],
        local_names: set[str],
    ) -> None:
        if isinstance(target, ast.Name):
            env.pop(target.id, None)
            local_names.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                delete_target(element, env, local_names)

    def set_object_flag(
        target: ast.expr, value: object, env: dict[str, binding_type]
    ) -> bool:
        if not (
            isinstance(target, ast.Attribute)
            and target.attr == "__test__"
            and isinstance(target.value, ast.Name)
        ):
            return False
        subject = env.get(target.value.id, other_binding)[1]
        if subject is not None:
            object_flags[id(subject)] = value
        return True

    def delete_object_flag(
        target: ast.expr, env: dict[str, binding_type]
    ) -> bool:
        if not (
            isinstance(target, ast.Attribute)
            and target.attr == "__test__"
            and isinstance(target.value, ast.Name)
        ):
            return False
        subject = env.get(target.value.id, other_binding)[1]
        if subject is not None:
            object_flags.pop(id(subject), None)
        return True

    class _ConditionalBindingVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.names: set[str] = set()

        def visit_Name(self, node: ast.Name) -> None:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                self.names.add(node.id)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.names.add(node.name)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.names.add(node.name)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.names.add(node.name)

        def visit_Lambda(self, _node: ast.Lambda) -> None:
            return

        def visit_Import(self, node: ast.Import) -> None:
            self.names.update(
                alias.asname or alias.name.split(".", 1)[0] for alias in node.names
            )

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            self.names.update(alias.asname or alias.name for alias in node.names)

        def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
            if node.name is not None:
                self.names.add(node.name)
            for statement in node.body:
                self.visit(statement)

    def analyze_namespace(
        body: list[ast.stmt],
        outer_env: dict[str, binding_type],
        *,
        in_class: bool,
    ) -> tuple[dict[str, binding_type], object]:
        env = dict(outer_env)
        local_names: set[str] = set()
        namespace_flag: object = missing
        simple_statements = (
            ast.Import,
            ast.ImportFrom,
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
            ast.Assign,
            ast.AnnAssign,
            ast.Delete,
        )
        for statement in body:
            if isinstance(statement, ast.Import):
                for alias in statement.names:
                    name = alias.asname or alias.name.split(".", 1)[0]
                    kind = {
                        "pytest": "pytest_module",
                        "unittest": "unittest_module",
                        "abc": "abc_module",
                        "hypothesis": "hypothesis_module",
                        "unittest.mock": (
                            "unittest_mock_module"
                            if alias.asname is not None
                            else "unittest_module"
                        ),
                    }.get(alias.name, "other")
                    env[name] = (kind, statement)
                    local_names.add(name)
            elif isinstance(statement, ast.ImportFrom):
                for alias in statement.names:
                    name = alias.asname or alias.name
                    kind = {
                        ("pytest", "fixture"): "fixture_decorator",
                        ("pytest", "mark"): "pytest_mark",
                        ("hypothesis", "example"): "safe_decorator",
                        ("hypothesis", "given"): "safe_decorator",
                        ("hypothesis", "reproduce_failure"): "safe_decorator",
                        ("hypothesis", "seed"): "safe_decorator",
                        ("hypothesis", "settings"): "safe_decorator",
                        ("unittest", "TestCase"): "unittest_base",
                        ("unittest", "mock"): "unittest_mock_module",
                        ("unittest.mock", "patch"): "safe_decorator",
                        ("abc", "ABC"): "abc_base",
                        ("abc", "abstractmethod"): "abstract_decorator",
                    }.get((statement.module, alias.name), "other")
                    env[name] = (kind, statement)
                    local_names.add(name)
            elif isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kinds = decorator_kinds(
                    statement.decorator_list, env, in_class=in_class
                )
                if "abstract_decorator" in kinds:
                    abstract_functions.add(id(statement))
                if is_identity_decorator(statement):
                    identity_decorators.add(id(statement))
                kind = (
                    "fixture_value"
                    if "fixture_decorator" in kinds
                    else "other"
                    if "unknown" in kinds
                    else "function"
                )
                env[statement.name] = (kind, statement)
                local_names.add(statement.name)
            elif isinstance(statement, ast.ClassDef):
                bases: list[binding_type] = []
                for base in statement.bases:
                    if isinstance(base, ast.Name) and base.id == "object" and base.id not in env:
                        bases.append(("object_base", base))
                    else:
                        bases.append(resolve_binding(base, env))
                class_bases[id(statement)] = tuple(bases)
                members, own_flag = analyze_namespace(
                    statement.body, env, in_class=True
                )
                class_members[id(statement)] = members
                class_flags[id(statement)] = own_flag
                kinds = decorator_kinds(
                    statement.decorator_list, env, in_class=in_class
                )
                kind = "other" if "unknown" in kinds else "class"
                env[statement.name] = (kind, statement)
                local_names.add(statement.name)
            elif isinstance(statement, ast.Assign):
                value = resolved_literal(statement.value, env)
                binding = resolve_binding(statement.value, env)
                for target in statement.targets:
                    if set_object_flag(target, value, env):
                        continue
                    if isinstance(target, ast.Name) and target.id == "__test__":
                        namespace_flag = value
                    bind_target(target, binding, env, local_names)
            elif isinstance(statement, ast.AnnAssign):
                if statement.value is None:
                    continue
                value = resolved_literal(statement.value, env)
                if not set_object_flag(statement.target, value, env):
                    if (
                        isinstance(statement.target, ast.Name)
                        and statement.target.id == "__test__"
                    ):
                        namespace_flag = value
                    bind_target(
                        statement.target,
                        resolve_binding(statement.value, env),
                        env,
                        local_names,
                    )
            elif isinstance(statement, ast.Delete):
                for target in statement.targets:
                    if delete_object_flag(target, env):
                        continue
                    if isinstance(target, ast.Name) and target.id == "__test__":
                        namespace_flag = missing
                    delete_target(target, env, local_names)
            elif not isinstance(statement, simple_statements):
                visitor = _ConditionalBindingVisitor()
                visitor.visit(statement)
                for name in visitor.names:
                    env[name] = other_binding
                    local_names.add(name)
                    if name == "__test__":
                        namespace_flag = missing
        return (
            {name: env[name] for name in local_names if name in env},
            namespace_flag,
        )

    module_bindings, module_flag = analyze_namespace(tree.body, {}, in_class=False)
    if module_flag is unknown or (
        module_flag is not missing and not bool(module_flag)
    ):
        return 0

    def node_flag(node: ast.AST) -> object:
        return object_flags.get(id(node), missing)

    def flag_blocks(value: object) -> bool:
        return value is unknown or (value is not missing and not bool(value))

    def effective_class_flag(
        node: ast.ClassDef, seen: frozenset[int] = frozenset()
    ) -> object:
        if id(node) in seen:
            return unknown
        external = node_flag(node)
        if external is not missing:
            return external
        own = class_flags.get(id(node), missing)
        if own is not missing:
            return own
        next_seen = seen | {id(node)}
        for base in inherited_nodes(node):
            inherited = effective_class_flag(base, next_seen)
            if inherited is not missing:
                return inherited
        return missing

    def unittest_case(node: ast.ClassDef, seen: frozenset[int] = frozenset()) -> bool:
        if id(node) in seen:
            return False
        next_seen = seen | {id(node)}
        for kind, base_node in class_bases.get(id(node), ()):
            if kind == "unittest_base":
                return True
            if (
                kind == "class"
                and isinstance(base_node, ast.ClassDef)
                and unittest_case(base_node, next_seen)
            ):
                return True
        return False

    def inherited_nodes(node: ast.ClassDef) -> tuple[ast.ClassDef, ...]:
        return tuple(
            base_node
            for kind, base_node in class_bases.get(id(node), ())
            if kind == "class" and isinstance(base_node, ast.ClassDef)
        )

    def unknown_pytest_base(node: ast.ClassDef) -> bool:
        return any(
            kind not in {"class", "object_base", "abc_base"}
            for kind, _base in class_bases.get(id(node), ())
        )

    def constructor_blocked(
        node: ast.ClassDef, seen: frozenset[int] = frozenset()
    ) -> bool:
        if id(node) in seen:
            return True
        members = class_members.get(id(node), {})
        if "__init__" in members or "__new__" in members:
            return True
        next_seen = seen | {id(node)}
        return any(constructor_blocked(base, next_seen) for base in inherited_nodes(node))

    def abstract_names(
        node: ast.ClassDef, seen: frozenset[int] = frozenset()
    ) -> set[str]:
        if id(node) in seen:
            return {"<inheritance-cycle>"}
        next_seen = seen | {id(node)}
        names: set[str] = set()
        for base in inherited_nodes(node):
            names.update(abstract_names(base, next_seen))
        for name, (_kind, member) in class_members.get(id(node), {}).items():
            names.discard(name)
            if member is not None and id(member) in abstract_functions:
                names.add(name)
        return names

    def visible_members(
        node: ast.ClassDef, seen: frozenset[int] = frozenset()
    ) -> dict[str, binding_type]:
        if id(node) in seen:
            return {}
        next_seen = seen | {id(node)}
        members: dict[str, binding_type] = {}
        # Python's leftmost base wins. Updating right to left preserves that
        # precedence for the simple local hierarchies this static hint accepts.
        for base in reversed(inherited_nodes(node)):
            members.update(visible_members(base, next_seen))
        members.update(class_members.get(id(node), {}))
        return members

    def method_names(node: ast.ClassDef, *, is_unittest: bool) -> set[str]:
        names: set[str] = set()
        for name, (kind, member) in visible_members(node).items():
            if kind != "function" or member is None:
                continue
            flag = node_flag(member)
            if flag_blocks(flag):
                continue
            if name.startswith("test") or (not is_unittest and flag is True):
                names.add(name)
        return names

    def class_test_count(
        node: ast.ClassDef,
        collection_name: str,
        seen: frozenset[int] = frozenset(),
    ) -> int:
        if id(node) in seen:
            return 0
        effective_flag = effective_class_flag(node)
        if flag_blocks(effective_flag):
            return 0
        is_unittest = unittest_case(node)
        forced = effective_flag is True
        if not is_unittest and (
            not (collection_name.startswith("Test") or forced)
            or unknown_pytest_base(node)
            or constructor_blocked(node)
            or bool(abstract_names(node))
        ):
            return 0
        methods = len(method_names(node, is_unittest=is_unittest))
        if is_unittest:
            return methods
        next_seen = seen | {id(node)}
        nested = sum(
            class_test_count(member, name, next_seen)
            for name, (kind, member) in class_members.get(id(node), {}).items()
            if kind == "class" and isinstance(member, ast.ClassDef)
        )
        return methods + nested

    count = 0
    for name, (kind, node) in module_bindings.items():
        if kind == "function" and node is not None:
            flag = node_flag(node)
            if (name.startswith("test") or flag is True) and not flag_blocks(flag):
                count += 1
        elif kind == "class" and isinstance(node, ast.ClassDef):
            count += class_test_count(node, name)
    return count


def _candidate_source_syntax(source: str) -> str | None:
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return str(exc)
    return None


def _target_definition(source: str, target: str) -> ast.AST | None:
    tree = ast.parse(source)
    selected = _selected_target(tree, target)
    if selected is None or (
        isinstance(selected, ast.ClassDef)
        and not any(
            isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
            for member in selected.body
        )
    ):
        return None
    return selected


def _target_is_implemented(source: str, target: str) -> bool:
    selected = _target_definition(source, target)
    if selected is None:
        return False

    def is_not_implemented(node: ast.AST) -> bool:
        if not isinstance(node, ast.Raise) or node.exc is None:
            return False
        exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
        return isinstance(exc, ast.Name) and exc.id == "NotImplementedError"

    return not any(is_not_implemented(node) for node in ast.walk(selected))


def show_status(root: Path, metadata: dict[str, Any]) -> int:
    source = (root / str(metadata["source"])).read_text()
    snapshot = _comment_snapshot(source, metadata)
    evidence = _effective_comment_evidence(root, metadata, source, snapshot)
    pre_required, post_required = _comment_requirements(metadata)
    print(f"pre-code comments: {min(evidence.pre_code, pre_required)}/{pre_required}")
    print(
        f"post-code comments: {min(evidence.post_code, post_required)}/{post_required}"
    )
    print(f"lock: {'locked' if str(metadata['lock']) in source else 'unlocked'}")
    try:
        count = _candidate_test_count(root, metadata)
    except PracticeError:
        print("candidate tests: syntax error")
        return 1
    print(f"candidate tests: {count}")
    return 0


def _next_step_from_source(
    root: Path,
    metadata: dict[str, Any],
    source: str,
    evidence: CommentEvidence,
) -> tuple[str, str]:
    if _candidate_source_syntax(source) is not None:
        return "BUILD", "Fix the syntax error in your source file, then run /continue."
    target = str(metadata["target"])
    if _target_definition(source, target) is None:
        return (
            "BUILD",
            f"Restore the required `{target}` definition, then run /continue.",
        )

    pre_required, post_required = _comment_requirements(metadata)
    if evidence.pre_code < pre_required:
        remaining = pre_required - evidence.pre_code
        noun = "comment" if remaining == 1 else "comments"
        location = (
            "above the gate"
            if str(metadata["lock"]) in source
            else "before the implementation"
        )
        return (
            "THINK",
            f"Add {remaining} more ordinary reasoning {noun} {location}, "
            "save, then run /continue.",
        )
    if str(metadata["lock"]) in source:
        return (
            "THINK",
            "Delete the THINKING GATE yourself, then implement below it.",
        )

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

    post_actions = (
        (
            "BUILD",
            "Write a new ordinary implementation comment beside the code it explains, "
            "save, then run /continue.",
        ),
        (
            "REFLECT",
            "Write a new ordinary comment tracing the saved example through the code, "
            "save, then run /continue.",
        ),
        (
            "REFLECT",
            "Write a new ordinary comment with final complexity or a remaining edge, "
            "save, then run /continue.",
        ),
    )
    if evidence.post_code < post_required:
        return post_actions[min(evidence.post_code, len(post_actions) - 1)]

    return (
        "CLOSE",
        "Run just practice-test, reconcile comments with code, then use just practice-finish.",
    )


def next_step(root: Path, metadata: dict[str, Any]) -> tuple[str, str]:
    """Return the current state without advancing temporal comment evidence."""
    source = (root / str(metadata["source"])).read_text()
    snapshot = _comment_snapshot(source, metadata)
    evidence = _effective_comment_evidence(root, metadata, source, snapshot)
    return _next_step_from_source(root, metadata, source, evidence)


def show_next(root: Path, metadata: dict[str, Any]) -> int:
    with _practice_lock(root):
        current = _read_metadata(root)
        if metadata.get("session_id") != current["session_id"]:
            raise PracticeError("stale rep session; reload `just practice-current`")
        source = (root / str(current["source"])).read_text()
        snapshot = _comment_snapshot(source, current)
        evidence = _advance_comment_receipt(root, current, source, snapshot)
        state, next_action = _next_step_from_source(
            root, current, source, evidence
        )
    print(f"STATE: {state}")
    print(f"SOURCE: {current['source']}")
    print(f"TEST: {current['candidate_test']}")
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
    with _practice_lock(root):
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

        source = (root / str(current["source"])).read_text()
        snapshot = _comment_snapshot(source, current)
        evidence = _advance_comment_receipt(root, current, source, snapshot)
        state, _ = _next_step_from_source(root, current, source, evidence)
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
        current: dict[str, Any] | None = None
        metadata_path = _metadata_path(root)
        if metadata_path.exists() or metadata_path.is_symlink():
            candidate = _read_metadata(root)
            if _is_prepared(candidate) and (
                candidate["topic"],
                candidate["problem"],
            ) == (topic, problem):
                current = candidate
        presented_text: str | None = None
        if current is not None and not _is_presented(current):
            presented = dict(current)
            presented["presented_at"] = datetime.now(UTC).isoformat()
            presented_text = json.dumps(presented, indent=2) + "\n"
        if _has_active_non_editor_receipt(root, fingerprint, today):
            if presented_text is not None:
                reps = _state_file(root, "reps.md")
                progress = _state_file(root, "progress.md")
                _commit_closeout(
                    root,
                    kind="non_editor",
                    fingerprint=fingerprint,
                    files={
                        reps.relative_to(root).as_posix(): reps.read_text(),
                        progress.relative_to(root).as_posix(): progress.read_text(),
                        metadata_path.relative_to(root).as_posix(): presented_text,
                    },
                )
            _print_closed(parsed.mode or "legacy", f"{topic}/{problem}")
            return 0
        reps = _state_file(root, "reps.md")
        progress = _state_file(root, "progress.md")
        dated = f"- {today} {normalized}"
        expected_progress = f"- [x] {topic}/{problem} {today}"
        reps_text = reps.read_text() if reps.exists() else ""
        progress_text = progress.read_text() if progress.exists() else ""
        already_logged = (
            dated in reps_text.splitlines()
            and expected_progress in progress_text.splitlines()
        )
        if already_logged and presented_text is None:
            # With no caller-provided idempotency key, an identical same-day
            # close is indistinguishable from a retry. A new day permits a new
            # rep unless a recent crash-recovery receipt says otherwise.
            _print_closed(parsed.mode or "legacy", f"{topic}/{problem}")
            return 0
        files = {
            reps.relative_to(root).as_posix(): (
                reps_text if already_logged else _append_rep_text(reps, dated)
            ),
            progress.relative_to(root).as_posix(): _progress_text(
                progress, topic, problem, today
            ),
        }
        if presented_text is not None:
            files[metadata_path.relative_to(root).as_posix()] = presented_text
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
    syntax_error = _candidate_source_syntax(source)
    if syntax_error is not None:
        raise PracticeError(f"source has a syntax error: {syntax_error}")
    target = str(metadata["target"])
    if _target_definition(source, target) is None:
        raise PracticeError(f"source no longer defines required target {target!r}")
    evidence = _comment_evidence(source, metadata)
    pre_required, _ = _comment_requirements(metadata)
    remaining = max(0, pre_required - evidence.pre_code)
    if str(metadata["lock"]) in source:
        if remaining:
            noun = "comment" if remaining == 1 else "comments"
            raise PracticeError(
                "thinking gate is still locked; add "
                f"{remaining} ordinary reasoning {noun} above it, save, then "
                "delete the gate yourself"
            )
        raise PracticeError(
            "thinking gate is still locked; delete the gate yourself before "
            "running code"
        )
    if remaining:
        noun = "comment" if remaining == 1 else "comments"
        raise PracticeError(
            "thinking gate was removed before enough pre-code reasoning was "
            f"present; add {remaining} ordinary {noun} before the implementation "
            "and save"
        )


def _practice_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTEST_ADDOPTS", None)
    env.pop("PYTEST_PLUGINS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
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
    except PermissionError, ProcessLookupError:
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
    _require_committed_reference_test(root, metadata)
    before = _test_input_digests(root, metadata)
    if require_unlocked:
        _require_unlocked(root, metadata)
    after = _test_input_digests(root, metadata)
    if before != after:
        raise PracticeError("practice files changed during test preflight; retry")
    return after


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
    for name in ("next", "status", "test", "watch", "repl", "current"):
        commands.add_parser(name)
    open_parser = commands.add_parser(
        "open", help="open current or exact safe candidate tabs"
    )
    open_parser.add_argument("topic", nargs="?")
    open_parser.add_argument("problem", nargs="?")
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
        if args.command == "open":
            with _practice_lock(ROOT):
                if args.topic is not None or args.problem is not None:
                    metadata = prepare_open_target(ROOT, args.topic, args.problem)
                else:
                    metadata = _read_metadata(ROOT)
                return 0 if open_session(ROOT, metadata) else 1

        metadata = current_metadata(ROOT)
        if _is_prepared(metadata) and args.command not in {"open", "current"}:
            raise PracticeError(
                "candidate tabs are prepared, but no editor rep is active\n"
                "NEXT: run `just practice-start <paradigm> "
                f"{metadata['topic']} {metadata['problem']}` or keep talking."
            )
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
