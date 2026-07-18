"""Prepare and drive one editor-first interview-practice workspace.

The committed algorithm implementations remain immutable reference material.
Each rep is rendered from ``HEAD`` into gitignored ``.challenges/workspace``
with a paradigm-specific comment scaffold and a candidate-owned test file.
Reference tests import the workspace implementation through a tiny pytest
plugin, so candidates can code, test, watch, and use a REPL without mutating
the packet's source tree.

Usage:
    practice_workspace.py start reacto [topic problem] [--fresh] [--no-open]
    practice_workspace.py present topic problem
    practice_workspace.py reference topic problem
    practice_workspace.py next | status | test | watch | repl | open | current
    practice_workspace.py finish "C2 L1 A2 R1 P2 h0 one fix"
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scaffold_status import section_status
from strip_solution import (
    inject_scaffold,
    module_docstring_block,
    strip_solution,
    truncate_module_docstring,
)
from study_schedule import ranked_queue

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_REL = Path(".challenges/workspace")
HISTORY_REL = Path(".challenges/history")
METADATA_NAME = "session.json"
PRACTICE_LOCK = (
    "# ==== THINKING GATE: complete the comments above, then delete this line "
    "to code ===="
)
IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")


class PracticeError(RuntimeError):
    """A user-actionable practice-workspace failure."""


@dataclass(frozen=True)
class Paradigm:
    """One reasoning vocabulary rendered into the candidate's source file."""

    title: str
    seeds: tuple[str, ...]
    lock_after: int

    @property
    def first_label(self) -> str:
        return self.seeds[0].split(":", 1)[0]

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


def _metadata_path(root: Path) -> Path:
    return _workspace(root) / METADATA_NAME


def _validate_problem(topic: str, problem: str) -> None:
    if not IDENTIFIER.fullmatch(topic) or not IDENTIFIER.fullmatch(problem):
        raise PracticeError("topic and problem must be lowercase Python identifiers")


def _draw_problem(root: Path) -> tuple[str, str]:
    queue = ranked_queue(root / ".challenges/progress.md")
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


def render_candidate(source: str, paradigm: Paradigm) -> str:
    """Return a cold stub carrying exactly one selected-paradigm scaffold."""
    cold = truncate_module_docstring(strip_solution(source))
    return inject_scaffold(
        cold,
        seeds=paradigm.seeds,
        lock_sentinel=PRACTICE_LOCK,
        lock_after=paradigm.lock_after,
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


def _candidate_test(topic: str, problem: str, candidate: str) -> str:
    module = f"algo.{topic}.{problem}"
    symbols = _public_symbols(candidate)
    import_line = (
        f"# from {module} import {', '.join(symbols)}\n"
        if symbols
        else f"# import {module}\n"
    )
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


def _pytest_plugin(module: str, candidate_name: str) -> str:
    return f'''"""Load the candidate file as {module} before pytest collection."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

MODULE = {module!r}
CANDIDATE = Path(__file__).with_name({candidate_name!r})


def pytest_configure() -> None:
    parent_name, child_name = MODULE.rsplit(".", 1)
    parent = importlib.import_module(parent_name)
    spec = importlib.util.spec_from_file_location(MODULE, CANDIDATE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {{CANDIDATE}}")
    candidate = importlib.util.module_from_spec(spec)
    sys.modules[MODULE] = candidate
    spec.loader.exec_module(candidate)
    setattr(parent, child_name, candidate)
'''


def _repl_bootstrap(module: str) -> str:
    return f'''"""Interactive bootstrap for the current practice implementation."""

from practice_plugin import pytest_configure

pytest_configure()
candidate = __import__({module!r}, fromlist=["*"])
for name in getattr(candidate, "__all__", dir(candidate)):
    if not name.startswith("_"):
        globals()[name] = getattr(candidate, name)
print("Loaded {module}; public names are available at the prompt.")
'''


def _read_metadata(root: Path) -> dict[str, Any]:
    path = _metadata_path(root)
    if not path.exists():
        raise PracticeError("no current rep; run `just practice-start <paradigm>`")
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PracticeError(f"invalid current-rep metadata: {exc}") from exc
    if not isinstance(value, dict):
        raise PracticeError("invalid current-rep metadata: expected an object")
    return value


def _archive_current(root: Path) -> Path | None:
    workspace = _workspace(root)
    if not workspace.exists():
        return None
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
    history = root / HISTORY_REL
    history.mkdir(parents=True, exist_ok=True)
    destination = history / f"{stamp}-{slug}"
    suffix = 2
    while destination.exists():
        destination = history / f"{stamp}-{slug}-{suffix}"
        suffix += 1
    shutil.move(str(workspace), destination)
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
    paradigm = PARADIGMS.get(paradigm_name)
    if paradigm is None:
        choices = ", ".join(PARADIGMS)
        raise PracticeError(f"unknown paradigm {paradigm_name!r}; choose {choices}")
    topic, problem = select_problem(root, topic, problem)

    workspace = _workspace(root)
    if workspace.exists() and not fresh:
        metadata = _read_metadata(root)
        if _same_session(metadata, paradigm_name, topic, problem):
            return metadata, "resumed", None

    source_rel = Path("src/algo") / topic / f"{problem}.py"
    reference_test_rel = Path("tests") / topic / f"test_{problem}.py"
    if not (root / reference_test_rel).is_file():
        raise PracticeError(f"missing reference tests: {reference_test_rel}")
    candidate = render_candidate(_committed_source(root, source_rel), paradigm)

    archived = _archive_current(root)
    workspace.mkdir(parents=True, exist_ok=True)
    candidate_name = f"{problem}.py"
    candidate_test_name = f"test_{problem}_candidate.py"
    candidate_path = workspace / candidate_name
    candidate_test_path = workspace / candidate_test_name
    module = f"algo.{topic}.{problem}"

    candidate_path.write_text(candidate)
    candidate_test_path.write_text(_candidate_test(topic, problem, candidate))
    (workspace / "practice_plugin.py").write_text(
        _pytest_plugin(module, candidate_name)
    )
    (workspace / "repl.py").write_text(_repl_bootstrap(module))

    metadata = {
        "schema": 1,
        "paradigm": paradigm_name,
        "paradigm_title": paradigm.title,
        "topic": topic,
        "problem": problem,
        "module": module,
        "source": candidate_path.relative_to(root).as_posix(),
        "candidate_test": candidate_test_path.relative_to(root).as_posix(),
        "reference_test": reference_test_rel.as_posix(),
        "plugin": (workspace / "practice_plugin.py").relative_to(root).as_posix(),
        "repl": (workspace / "repl.py").relative_to(root).as_posix(),
        "seeds": list(paradigm.seeds),
        "pre_code_labels": list(paradigm.pre_code_labels),
        "lock": PRACTICE_LOCK,
        "created_at": datetime.now(UTC).isoformat(),
    }
    metadata_path = _metadata_path(root)
    temporary_metadata = metadata_path.with_name(f".{metadata_path.name}.tmp")
    temporary_metadata.write_text(json.dumps(metadata, indent=2) + "\n")
    temporary_metadata.replace(metadata_path)
    return metadata, "created", archived


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
        for node in ast.walk(tree)
    )


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

    try:
        candidate_test_count = _candidate_test_count(root, metadata)
    except PracticeError:
        return "BUILD", "Fix the syntax error in your test file, then run /continue."

    if "raise NotImplementedError" in source or candidate_test_count == 0:
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
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text)
    temporary.replace(path)


def finish_session(root: Path, metadata: dict[str, Any], note: str) -> int:
    """Log one rep and schedule its next review through one idempotent command."""
    note = " ".join(note.split())
    if not note:
        raise PracticeError("finish note is empty; name one specific fix")

    topic = str(metadata["topic"])
    problem = str(metadata["problem"])
    paradigm = str(metadata["paradigm"])
    today = date.today().isoformat()
    rep = f"{paradigm} {topic}/{problem} {note}"
    rep_line = f"- {today} {rep}"

    reps = root / ".challenges/reps.md"
    existing_reps = reps.read_text().splitlines() if reps.exists() else []
    if rep_line not in existing_reps:
        _replace_file(reps, "\n".join([*existing_reps, rep_line]) + "\n")

    progress = root / ".challenges/progress.md"
    key = f"{topic}/{problem}"
    progress_line = f"- [x] {key} {today}"
    existing_progress = progress.read_text().splitlines() if progress.exists() else []
    key_line = re.compile(rf"^- \[x\] {re.escape(key)}(?:\s|$)")
    updated = [line for line in existing_progress if key_line.match(line) is None]
    _replace_file(progress, "\n".join([*updated, progress_line]) + "\n")

    finished = dict(metadata)
    finished["finished_at"] = datetime.now(UTC).isoformat()
    finished["finish_note"] = note
    _replace_file(_metadata_path(root), json.dumps(finished, indent=2) + "\n")

    print(f"CLOSED: {paradigm} {key}")
    print("LOGGED: .challenges/reps.md")
    print("SPACED: .challenges/progress.md")
    print("NEXT: Run just study-spaced 1 when you want another rep.")
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


def run_tests(root: Path, metadata: dict[str, Any]) -> int:
    _require_unlocked(root, metadata)
    proc = subprocess.run(
        [sys.executable, *_pytest_args(metadata)],
        cwd=root,
        env=_practice_env(root),
        check=False,
    )
    return proc.returncode


def run_watch(root: Path, metadata: dict[str, Any]) -> int:
    _require_unlocked(root, metadata)
    watchexec = shutil.which("watchexec")
    if watchexec is None:
        raise PracticeError("watchexec is missing; use `just practice-test`")
    args = [
        watchexec,
        "--ignore-nothing",
        "-e",
        "py",
        "-w",
        str(_workspace(root)),
        "--",
        sys.executable,
        *_pytest_args(metadata),
    ]
    os.execvpe(watchexec, args, _practice_env(root))
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
    reference.add_argument("topic")
    reference.add_argument("problem")
    for name in ("next", "status", "test", "watch", "repl", "open", "current"):
        commands.add_parser(name)
    finish = commands.add_parser(
        "finish", help="log the current rep and schedule its next review"
    )
    finish.add_argument("note")
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
            print(reference_solution(ROOT, args.topic, args.problem).rstrip())
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

        metadata = _read_metadata(ROOT)
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
