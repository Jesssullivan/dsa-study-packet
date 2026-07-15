"""Strip function bodies from an algorithm file for challenge mode.

Preserves: module docstring, imports, class definitions, function signatures,
type annotations, and function docstrings.
Replaces: function bodies with ``raise NotImplementedError``.

Usage:
    python scripts/strip_solution.py src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --cold --scaffold src/algo/arrays/two_sum.py
    python scripts/strip_solution.py --print-statement src/algo/arrays/two_sum.py

``--print-statement`` writes nothing; it prints the module docstring block
(source lines 1 through the docstring's end) to stdout and leaves the file
untouched. This is the cold-interview problem statement.

``--scaffold`` (rung-2 comment-driven mode) additionally seeds the think-aloud
comment scaffold above the first stripped function's ``raise``, ending with a
LOCK line the candidate deletes themselves to unlock coding.
"""

from __future__ import annotations

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
    """Strip function bodies, keeping signatures and docstrings."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)

    all_funcs = [
        n
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    def _span(n: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[int, int]:
        return n.lineno, (n.end_lineno or n.lineno)

    def _contained_in_another(n: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        n_start, n_end = _span(n)
        for other in all_funcs:
            if other is n:
                continue
            o_start, o_end = _span(other)
            if (
                o_start <= n_start
                and n_end <= o_end
                and (o_start, o_end) != (n_start, n_end)
            ):
                return True
        return False

    # Collect ranges to replace: (start_line, end_line, indent)
    replacements: list[tuple[int, int, int]] = []

    for node in all_funcs:
        # Nested functions (closures, helpers defined inside another function)
        # are already stripped by their enclosing function's replacement — an
        # independent entry for them would overlap that outer range and, once
        # both are applied against the same mutating `lines` list, corrupt
        # whatever follows (e.g. swallow the blank lines before the next
        # top-level def). Only outermost functions get their own replacement.
        if _contained_in_another(node):
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
) -> str:
    """Seed the rung-2 comment scaffold above the first stripped function body.

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
    funcs = [
        n
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
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


def main() -> None:
    flags = {"--cold", "--print-statement", "--scaffold"}
    args = [a for a in sys.argv[1:] if a not in flags]
    cold = "--cold" in sys.argv[1:]
    print_statement = "--print-statement" in sys.argv[1:]
    scaffold = "--scaffold" in sys.argv[1:]
    if print_statement and (cold or scaffold):
        print("Error: --print-statement excludes --cold/--scaffold")
        sys.exit(1)
    if len(args) != 1:
        print(
            f"Usage: {sys.argv[0]} [--cold] [--scaffold] [--print-statement] <source_file>"
        )
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
    if scaffold:
        stripped = inject_scaffold(stripped)
    path.write_text(stripped)
    print(
        f"Stripped{' (cold)' if cold else ''}{' +scaffold' if scaffold else ''}: {path}"
    )


if __name__ == "__main__":
    main()
