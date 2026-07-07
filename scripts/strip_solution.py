"""Strip function bodies from an algorithm file for challenge mode.

Preserves: module docstring, imports, class definitions, function signatures,
type annotations, and function docstrings.
Replaces: function bodies with ``raise NotImplementedError``.

Usage:
    python scripts/strip_solution.py src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --print-statement src/algo/arrays/two_sum.py

``--print-statement`` writes nothing; it prints the module docstring block
(source lines 1 through the docstring's end) to stdout and leaves the file
untouched. This is the cold-interview problem statement.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def strip_solution(source: str) -> str:
    """Strip function bodies, keeping signatures and docstrings."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    # Collect ranges to replace: (start_line, end_line, indent)
    replacements: list[tuple[int, int, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
            # Has a docstring — keep it, strip the rest
            if len(body) <= 1:
                continue  # Only a docstring, nothing to strip
            body_start = body[1].lineno
        else:
            # No docstring — strip everything
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
    cuts = [i for m in ("Approach:", "When to use:", "Complexity:") if (i := doc.find(m)) != -1]
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
    the statement alone — never the solution below it.
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


def main() -> None:
    flags = {"--cold", "--print-statement"}
    args = [a for a in sys.argv[1:] if a not in flags]
    cold = "--cold" in sys.argv[1:]
    print_statement = "--print-statement" in sys.argv[1:]
    if cold and print_statement:
        print("Error: --cold and --print-statement are mutually exclusive")
        sys.exit(1)
    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} [--cold | --print-statement] <source_file>")
        sys.exit(1)

    path = Path(args[0])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    source = path.read_text()

    if print_statement:
        try:
            block = module_docstring_block(source)
        except ValueError as exc:
            print(f"Error: {exc}: {path}")
            sys.exit(1)
        sys.stdout.write(block)
        return

    stripped = strip_solution(source)
    if cold:
        stripped = truncate_module_docstring(stripped)
    path.write_text(stripped)
    print(f"Stripped{' (cold)' if cold else ''}: {path}")


if __name__ == "__main__":
    main()
