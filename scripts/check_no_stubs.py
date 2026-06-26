"""CI guard: no unfinished stubs in the study material.

Statically scans every src/algo and src/concepts module (AST, no import side
effects) and fails if any raises NotImplementedError or fails to parse. Catches
an abandoned challenge edit before it ships (the kind of breakage that once
slipped in as a half-finished top_k_frequent.py).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PACKAGES = ("algo", "concepts")


def _raises_not_implemented(node: ast.Raise) -> bool:
    exc = node.exc
    if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
        return exc.func.id == "NotImplementedError"
    if isinstance(exc, ast.Name):
        return exc.id == "NotImplementedError"
    return False


def main() -> int:
    failures: list[str] = []
    for pkg in PACKAGES:
        pkg_dir = SRC / pkg
        if not pkg_dir.is_dir():
            continue
        for py in sorted(pkg_dir.rglob("*.py")):
            if py.name == "__init__.py":
                continue
            rel = py.relative_to(ROOT)
            try:
                tree = ast.parse(py.read_text())
            except SyntaxError as exc:
                failures.append(f"{rel}: syntax error: {exc}")
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Raise) and _raises_not_implemented(node):
                    failures.append(f"{rel}:{node.lineno}: raises NotImplementedError (unfinished stub)")

    if failures:
        print("Stub check FAILED:", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("No-stub check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
