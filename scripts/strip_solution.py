"""Render non-destructive algorithm practice previews.

The importable helpers strip function bodies, truncate solution-bearing module
docstrings, or return the problem statement. The CLI writes the requested
preview to stdout and never modifies the input file. Use ``just
practice-start`` to create a candidate-owned workspace.

Usage:
    python scripts/strip_solution.py src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --print-statement src/algo/arrays/two_sum.py

Without flags, the CLI prints a stripped preview. ``--print-statement`` prints
only the module docstring block (source lines 1 through the docstring's end).

``--cold`` removes solution-bearing docstring sections from the preview. All
modes are read-only.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


def strip_solution(source: str) -> str:
    """Strip every implementation, keeping signatures and docstrings."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    all_funcs: list[ast.FunctionDef | ast.AsyncFunctionDef] = [
        n
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    # Collect ranges to replace: (start_line, end_line, indent)
    replacements: list[tuple[int, int, int]] = []

    for node in all_funcs:
        # Nested functions (closures, helpers defined inside another function)
        # are already stripped by their enclosing function's replacement; an
        # independent entry for them would overlap that outer range and, once
        # both are applied against the same mutating `lines` list, corrupt
        # whatever follows (e.g. swallow the blank lines before the next
        # top-level def). Only outermost functions get their own replacement.
        if any(
            other is not node
            and other.lineno <= node.lineno
            and (node.end_lineno or node.lineno) <= (other.end_lineno or other.lineno)
            for other in all_funcs
        ):
            continue

        # Skip nested functions (helpers inside classes are fine)
        body = node.body
        if not body:
            continue

        # Find where the docstring ends (or body starts if no docstring)
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            # Has a docstring. Keep it and strip the rest.
            if len(body) <= 1:
                continue  # Only a docstring, nothing to strip
            body_start = body[1].lineno
        else:
            # No docstring. Strip everything.
            body_start = first.lineno

        body_end = body[-1].end_lineno or body[-1].lineno

        # Detect indentation from the def line
        def_line = lines[node.lineno - 1]
        indent = len(def_line) - len(def_line.lstrip())
        body_indent = indent + 4

        replacements.append((body_start, body_end, body_indent))

    if not replacements:
        return source

    # Apply replacements in reverse order to preserve line numbers
    replacements.sort(reverse=True)
    for start, end, indent in replacements:
        stub = " " * indent + "raise NotImplementedError\n"
        lines[start - 1 : end] = [stub]

    return "".join(lines)


def truncate_module_docstring(source: str) -> str:
    """Cold mode: cut Approach/When to use/Complexity from the module docstring."""
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return source
    doc = first.value.value
    cuts = [
        i
        for m in ("Approach:", "When to use:", "Complexity:")
        if (i := doc.find(m)) != -1
    ]
    if not cuts:
        return source
    lines = source.splitlines(keepends=True)
    end = first.end_lineno or first.lineno
    lines[first.lineno - 1 : end] = [f'"""{doc[: min(cuts)].rstrip()}\n"""\n']
    return "".join(lines)


def module_docstring_block(source: str) -> str:
    """Return the module docstring block verbatim (source lines 1..docstring end).

    Preserves original formatting exactly. Raises ``ValueError`` if the module
    has no docstring. Unlike a triple-quote line count, this uses the AST node
    span, so a single-line ``\"\"\"Statement.\"\"\"`` and a module whose body
    contains later triple-quoted strings (e.g. function docstrings) both yield
    the statement alone, never the solution below it.
    """
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        msg = "module has no docstring"
        raise ValueError(msg)
    lines = source.splitlines(keepends=True)
    end = first.end_lineno or first.lineno
    return "".join(lines[:end])


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview a stripped algorithm on stdout without modifying its source."
    )
    parser.add_argument(
        "--cold",
        action="store_true",
        help="remove solution-bearing module-docstring sections from the preview",
    )
    parser.add_argument(
        "--print-statement",
        action="store_true",
        help="print only the module problem statement",
    )
    parser.add_argument("source_file", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.print_statement and args.cold:
        parser.error("--print-statement cannot be combined with --cold")

    path: Path = args.source_file
    if not path.is_file():
        parser.error(f"source file not found: {path}")

    try:
        source = path.read_text()
        if args.print_statement:
            rendered = module_docstring_block(source)
        else:
            rendered = strip_solution(source)
            if args.cold:
                rendered = truncate_module_docstring(rendered)
    except (OSError, SyntaxError, ValueError) as exc:
        print(f"strip_solution: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
