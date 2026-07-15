"""Render non-destructive algorithm practice previews.

The importable helpers strip function bodies, truncate solution-bearing module
docstrings, inject a reasoning scaffold, or return the problem statement. The
CLI writes the requested preview to stdout and never modifies the input file.
Use ``just practice-start`` to create a candidate-owned workspace.

Usage:
    python scripts/strip_solution.py src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold --scaffold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --print-statement src/algo/arrays/two_sum.py

Without flags, the CLI prints a stripped preview. ``--print-statement`` prints
only the module docstring block (source lines 1 through the docstring's end).

``--cold`` removes solution-bearing docstring sections from the preview, and
``--scaffold`` adds the legacy comment scaffold. All modes are read-only.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

SCAFFOLD_SEEDS = (
    "# RESTATE: the problem in your own words: inputs, outputs, constraints",
    "# EXAMPLE: one concrete input/output pair, plus one edge case",
    "# INVARIANT: what stays true at each step (loop/recursion invariant)",
    "# APPROACH: pattern family + brute-force big-O, decided before any code",
    "# COMPLEXITY: target time / space once the approach is chosen",
)
LOCK_SENTINEL = "# ==== LOCKED: delete this line to unlock coding ===="


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


def inject_scaffold(
    source: str,
    seeds: tuple[str, ...] = SCAFFOLD_SEEDS,
    lock_sentinel: str = LOCK_SENTINEL,
    lock_after: int | None = None,
    target_name: str | None = None,
) -> str:
    """Seed the editor-practice comments above the selected stripped body.

    Targets the earliest function anywhere in the module (top-level or
    method) whose body ends in the bare ``raise`` that ``strip_solution``
    leaves behind; inserts the scaffold comments plus the LOCK sentinel at
    that statement's indentation. Idempotent: a source that already carries
    the LOCK sentinel is returned unchanged, so re-running a rep never stacks
    scaffolds. Returns the source unchanged if no stripped function exists.
    """
    if lock_sentinel in source:
        return source
    tree = ast.parse(source)
    funcs: list[ast.FunctionDef | ast.AsyncFunctionDef] = [
        n
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    if target_name is not None:
        selected = next(
            (
                node
                for node in tree.body
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                )
                and node.name == target_name
            ),
            None,
        )
        if selected is None:
            msg = f"target {target_name!r} is not a top-level function or class"
            raise ValueError(msg)
        if isinstance(selected, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs = [selected]
        else:
            class_end = selected.end_lineno or selected.lineno
            funcs = [
                node
                for node in funcs
                if selected.lineno < node.lineno
                and (node.end_lineno or node.lineno) <= class_end
            ]
    targets = sorted(
        (f for f in funcs if f.body and isinstance(f.body[-1], ast.Raise)),
        key=lambda f: f.lineno,
    )
    if not targets:
        return source
    raise_stmt = targets[0].body[-1]
    pad = " " * raise_stmt.col_offset
    lock_at = len(seeds) if lock_after is None else lock_after
    if not 0 <= lock_at <= len(seeds):
        msg = f"lock_after must be between 0 and {len(seeds)}"
        raise ValueError(msg)
    ordered = (*seeds[:lock_at], lock_sentinel, *seeds[lock_at:])
    block = [pad + line + "\n" for line in ordered]
    lines = source.splitlines(keepends=True)
    at = raise_stmt.lineno - 1
    lines[at:at] = block
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
        "--scaffold",
        action="store_true",
        help="add the legacy reasoning scaffold to the stripped preview",
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
    if args.print_statement and (args.cold or args.scaffold):
        parser.error("--print-statement cannot be combined with --cold or --scaffold")

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
            if args.scaffold:
                rendered = inject_scaffold(rendered)
    except (OSError, SyntaxError, ValueError) as exc:
        print(f"strip_solution: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
