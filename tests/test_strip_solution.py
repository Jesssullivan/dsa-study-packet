"""Tests for the --print-statement docstring printer in scripts/strip_solution.py.

Guards the AST-backed statement printer that replaced the fragile awk line in
the ``interview`` recipe. The old ``awk 'c<2 {print} /\"\"\"/ {c++}'`` counted
triple-quote lines and leaked the entire solution whenever the module docstring
was a single line (both quotes on one line never reached the count of two).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
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
