"""Tests for the mechanical Python target resolver."""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import cast

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import python_candidate_target as target_resolver  # type: ignore[import-not-found]


def resolve(source: str, name: str = "solve") -> ast.stmt | None:
    return cast(
        "ast.stmt | None",
        target_resolver.selected_target(ast.parse(source), name),
    )


def test_unique_top_level_definition_is_selected() -> None:
    selected = resolve("def solve() -> int:\n    return 1\n")

    assert isinstance(selected, ast.FunctionDef)


def test_duplicate_top_level_definition_fails_closed() -> None:
    source = "def solve() -> int:\n    return 1\n\ndef solve() -> int:\n    return 2\n"

    assert resolve(source) is None


def test_binding_before_definition_does_not_hide_effective_target() -> None:
    source = "solve: object\n\ndef solve() -> int:\n    return 1\n"

    assert isinstance(resolve(source), ast.FunctionDef)


@pytest.mark.parametrize(
    "rebind",
    [
        "solve = lambda: 2",
        "del solve",
        "import math as solve",
        "from math import prod as solve",
        "other = lambda value=(solve := lambda: 2): value",
        "def other(value=(solve := lambda: 2)):\n    return value",
        "try:\n    raise ValueError\nexcept ValueError as solve:\n    pass",
    ],
)
def test_later_runtime_rebinding_fails_closed(rebind: str) -> None:
    source = f"def solve() -> int:\n    return 1\n\n{rebind}\n"

    assert resolve(source) is None


@pytest.mark.parametrize(
    "rebind",
    [
        "match 2:\n    case solve:\n        pass",
        "match 2:\n    case _ as solve:\n        pass",
        "class Other:\n    global solve\n    solve = lambda: 2",
        (
            "class Outer:\n"
            "    class Inner:\n"
            "        global solve\n"
            "        solve = lambda: 2"
        ),
    ],
)
def test_control_flow_runtime_rebinding_fails_closed(rebind: str) -> None:
    source = f"def solve() -> int:\n    return 1\n\n{rebind}\n"

    assert resolve(source) is None


@pytest.mark.parametrize(
    "later_statement",
    [
        "solve: object",
        "ignored = [value for solve in [] for value in [solve]]",
        (
            "class Outer:\n"
            "    solve = 2\n"
            "    class Inner:\n"
            "        global solve\n"
            "        pass"
        ),
        "class Outer:\n    class solve:\n        pass",
        "def helper():\n    solve = 2\n    return solve",
    ],
)
def test_later_local_only_names_do_not_replace_target(later_statement: str) -> None:
    source = f"def solve() -> int:\n    return 1\n\n{later_statement}\n"

    assert isinstance(resolve(source), ast.FunctionDef)
