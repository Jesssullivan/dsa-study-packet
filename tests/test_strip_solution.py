"""Tests for the read-only transforms in scripts/strip_solution.py.

Guards the AST-backed statement printer that replaced the fragile awk line in
the ``interview`` recipe. The old ``awk 'c<2 {print} /\"\"\"/ {c++}'`` counted
triple-quote lines and leaked the entire solution whenever the module docstring
was a single line (both quotes on one line never reached the count of two).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = _SCRIPTS / "strip_solution.py"
sys.path.insert(0, str(_SCRIPTS))

import strip_solution  # type: ignore[import-not-found]  # noqa: E402

MULTI_LINE = '''"""Title line — a short summary.

Problem:
    Given an array, do the thing and return the result.
"""

from collections.abc import Sequence


def solve(nums: Sequence[int]) -> int:
    """Return the answer."""
    secret_body = 42
    return secret_body
'''

SINGLE_LINE = '''"""Statement on one line with both quotes."""

from collections.abc import Sequence


def solve(nums: Sequence[int]) -> int:
    secret_body = 42
    return secret_body
'''

NESTED_DOCSTRING = '''"""Module statement.

More statement text here.
"""


def solve(nums: list[int]) -> int:
    """Nested function docstring — a second triple-quoted string."""
    secret_body = 99
    return secret_body
'''

NO_DOCSTRING = '''from __future__ import annotations


def solve(nums: list[int]) -> int:
    return nums[0]
'''

NESTED_CLOSURE_THEN_DEF = '''"""Module doc."""


def outer(nums: list[int]) -> int:
    """Outer docstring."""
    def helper(x: int) -> int:
        y = x * 2
        z = y + 1
        return z

    return helper(nums[0])


def other(x: int) -> int:
    """Other docstring."""
    return x + 1
'''


def test_multi_line_docstring_prints_only_the_statement() -> None:
    block = strip_solution.module_docstring_block(MULTI_LINE)
    assert "Title line" in block
    assert "Problem:" in block
    assert "do the thing" in block
    # The statement ends at the closing triple quote; nothing below it leaks.
    assert block.endswith('"""\n')
    assert "def solve" not in block
    assert "secret_body" not in block


def test_single_line_docstring_does_not_leak_solution() -> None:
    # The exact case the old awk mishandled: both quotes on line 1.
    block = strip_solution.module_docstring_block(SINGLE_LINE)
    assert block == '"""Statement on one line with both quotes."""\n'
    assert "def solve" not in block
    assert "secret_body" not in block


def test_second_triple_quoted_string_never_reaches_solution_body() -> None:
    block = strip_solution.module_docstring_block(NESTED_DOCSTRING)
    assert "Module statement." in block
    assert "More statement text here." in block
    # The function docstring and body sit below the module docstring span.
    assert "Nested function docstring" not in block
    assert "def solve" not in block
    assert "secret_body" not in block


def test_missing_docstring_raises_value_error() -> None:
    with pytest.raises(ValueError):
        strip_solution.module_docstring_block(NO_DOCSTRING)


def test_nested_closure_does_not_swallow_the_following_def() -> None:
    # Regression: ast.walk() also yields the nested `helper` closure inside
    # `outer`. Treating it as its own replacement target — overlapping
    # `outer`'s own range — corrupted the line count once both replacements
    # were applied against the same mutating line list, swallowing the blank
    # separator lines (and could eat into `other` itself).
    stripped = strip_solution.strip_solution(NESTED_CLOSURE_THEN_DEF)
    assert "raise NotImplementedError" in stripped
    assert "def helper" not in stripped
    assert "secret_body" not in stripped
    assert "def other(x: int) -> int:" in stripped
    assert '"""Other docstring."""' in stripped
    # The two blank separator lines between `outer` and `other` must survive.
    assert "\n\n\ndef other(x: int) -> int:" in stripped


def test_cli_prints_stripped_preview_without_modifying_source(tmp_path: Path) -> None:
    source_file = tmp_path / "problem.py"
    source_file.write_text(MULTI_LINE)

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(source_file)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert source_file.read_text() == MULTI_LINE
    assert "raise NotImplementedError" in proc.stdout
    assert "secret_body" not in proc.stdout


def test_cli_scaffold_preview_is_also_read_only(tmp_path: Path) -> None:
    source_file = tmp_path / "problem.py"
    source_file.write_text(MULTI_LINE)

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--cold", "--scaffold", str(source_file)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert source_file.read_text() == MULTI_LINE
    assert strip_solution.LOCK_SENTINEL in proc.stdout


def test_cli_help_states_that_source_is_not_modified() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0
    assert "stdout without modifying its source" in proc.stdout
