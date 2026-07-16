"""Report reasoning-comment presence for an editor-practice scaffold.

``section_status`` preserves the labeled scaffold contract for older sessions.
``candidate_comment_evidence`` also recognizes ordinary Python comments before
and after coding begins. Neither function judges whether the reasoning is
correct.

Usage:
    python scripts/scaffold_status.py src/algo/arrays/two_sum.py
"""

from __future__ import annotations

import ast
import io
import re
import sys
import tokenize
import unicodedata
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_solution import LOCK_SENTINEL, SCAFFOLD_SEEDS

PLACEHOLDERS = frozenset({"answer", "fill here", "placeholder", "tbd", "todo"})
PLACEHOLDER_ONLY = re.compile(
    r"^(?:answer(?:\s+here)?|fill(?:\s+(?:here|later|in|this\s+in))?|"
    r"(?:(?:write|insert)\s+)?(?:your\s+)?(?:answer|code|implementation)"
    r"(?:\s+goes)?\s+here|"
    r"not\s+implemented(?:\s+yet)?|"
    r"placeholder|tbd)(?:[.!?:]*)$",
    re.IGNORECASE,
)
TASK_MARKER_PREFIX = re.compile(
    r"^(?:todo|fixme|xxx|hack)\b",
    re.IGNORECASE,
)
DIRECTIVE_PREFIX = re.compile(
    r"^(?:!|noqa\b|type:|pyright:|mypy:|pylint:|ruff:|"
    r"fmt:|isort:|pragma:|nosec\b|coverage:|coding[:=]|(?:end)?region\b)",
    re.IGNORECASE,
)
RELATION_OPERATORS = ("->", "=>", "==", "!=", "<=", ">=")
COMPLEXITY_EVIDENCE = re.compile(r"\bO\(([^)]+)\)", re.IGNORECASE)


@dataclass(frozen=True)
class CommentEvidence:
    """Candidate-authored comment counts before and after coding starts."""

    pre_code: int
    post_code: int


@dataclass(frozen=True)
class CommentSnapshot:
    """Distinct meaningful comment keys and their current static placement."""

    pre_keys: frozenset[str]
    post_keys: frozenset[str]
    anchored_post_keys: frozenset[str]
    legacy_post_keys: frozenset[str]
    all_keys: frozenset[str]

    @property
    def evidence(self) -> CommentEvidence:
        return CommentEvidence(len(self.pre_keys), len(self.post_keys))


@dataclass(frozen=True)
class _Comment:
    row: int
    column: int
    text: str


@dataclass(frozen=True)
class _Scope:
    start: int
    end: int
    column: int
    body_column: int
    first_code: int
    forced_post_rows: frozenset[int]


def _meaningful_comment(text: str) -> bool:
    """Keep the original labeled-scaffold presence semantics."""
    normalized = text.removeprefix("#").strip().lower()
    return (
        any(character.isalnum() for character in normalized)
        and normalized not in PLACEHOLDERS
    )


def section_status(
    text: str,
    seeds: tuple[str, ...] = SCAFFOLD_SEEDS,
    lock_sentinel: str = LOCK_SENTINEL,
) -> dict[str, str]:
    """Return the legacy labeled-scaffold status, byte-for-byte in behavior."""
    labels = tuple(seed.split(":", 1)[0].removeprefix("# ") for seed in seeds)
    lines = [line.strip() for line in text.splitlines()]
    markers = tuple(f"# {label}:" for label in labels)
    status: dict[str, str] = {}
    for label, seed, marker in zip(labels, seeds, markers, strict=True):
        starts = [i for i, line in enumerate(lines) if line.startswith(marker)]
        if not starts:
            status[label] = "missing"
            continue
        start = starts[0]
        block = [lines[start]]
        for line in lines[start + 1 :]:
            if line.startswith(markers) or line == lock_sentinel:
                break
            # Once the candidate unlocks, executable code follows the final
            # marker. It is not evidence that the final reasoning comment was
            # filled in.
            if line and not line.startswith("#"):
                break
            if line:
                block.append(line)
        seed_text = seed.removeprefix(marker).strip()
        prompt_text = block[0].removeprefix(marker).strip()
        inline_answer = prompt_text != seed_text and _meaningful_comment(prompt_text)
        continuation_answer = any(_meaningful_comment(line) for line in block[1:])
        filled = inline_answer or continuation_answer
        status[label] = "filled" if filled else "empty"
    return status


def _marker(seed: str) -> str | None:
    body = _comment_body(seed)
    label, separator, _prompt = body.partition(":")
    if not separator:
        return None
    return label + ":"


def _comment_body(comment: str) -> str:
    return comment.removeprefix("#").strip()


def _canonical(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text)
    folded = unicodedata.normalize("NFKC", folded.casefold())
    normalized = " ".join(
        folded.split()
    )
    end = len(normalized)
    while end and unicodedata.category(normalized[end - 1]) == "Po":
        end -= 1
    return normalized[:end].rstrip()


def _placeholder_form(text: str) -> str:
    value = text.strip()
    pairs = {"[": "]", "(": ")", "{": "}", "<": ">"}
    while len(value) >= 2 and pairs.get(value[0]) == value[-1]:
        value = value[1:-1].strip()
    value = re.sub(r"[-_]+", " ", value)
    return " ".join(value.split())


def _has_symbol_evidence(text: str) -> bool:
    if any(
        any(character.isalnum() for character in match.group(1))
        for match in COMPLEXITY_EVIDENCE.finditer(text)
    ):
        return True

    def operand(value: str) -> bool:
        stripped = value.strip()
        return any(character.isalnum() for character in stripped) or stripped in {
            "[]",
            "{}",
            "()",
        }

    return any(
        separator and operand(left) and operand(right)
        for operator in RELATION_OPERATORS
        for left, separator, right in [text.partition(operator)]
    )


def _evidence_key(text: str) -> str | None:
    """Normalize one candidate comment and reject non-reasoning scaffolding."""
    body = _comment_body(text)
    canonical = _canonical(body)
    placeholder_form = _placeholder_form(canonical)
    if (
        not canonical
        or canonical == "..."
        or PLACEHOLDER_ONLY.fullmatch(placeholder_form)
        or TASK_MARKER_PREFIX.match(placeholder_form)
        or DIRECTIVE_PREFIX.match(placeholder_form)
    ):
        return None

    words = re.findall(r"[^\W_]+", canonical)
    alphanumeric = [character for character in canonical if character.isalnum()]
    non_latin_phrase = len(alphanumeric) >= 2 and any(
        not character.isascii() for character in alphanumeric
    )
    if len(words) < 2 and not non_latin_phrase and not _has_symbol_evidence(canonical):
        return None
    return canonical


def _token_comments(text: str) -> list[_Comment]:
    comments: list[_Comment] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comments.append(
                    _Comment(token.start[0], token.start[1], token.string.strip())
                )
    except IndentationError, tokenize.TokenError:
        return []
    return comments


def _node_start(node: ast.stmt) -> int:
    decorators = getattr(node, "decorator_list", ())
    return min([node.lineno, *(decorator.lineno for decorator in decorators)])


class _GlobalVisitor(ast.NodeVisitor):
    def __init__(self, name: str) -> None:
        self.name = name
        self.found = False

    def visit_Global(self, node: ast.Global) -> None:
        self.found |= self.name in node.names

    def visit_FunctionDef(self, _node: ast.FunctionDef) -> None:
        return

    def visit_AsyncFunctionDef(self, _node: ast.AsyncFunctionDef) -> None:
        return

    def visit_ClassDef(self, _node: ast.ClassDef) -> None:
        return

    def visit_Lambda(self, _node: ast.Lambda) -> None:
        return


class _RebindingVisitor(ast.NodeVisitor):
    """Find module-scope bindings without descending into nested scopes."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.found = False

    def visit_Name(self, node: ast.Name) -> None:
        if node.id == self.name and isinstance(node.ctx, (ast.Store, ast.Del)):
            self.found = True

    def _visit_function_header(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        self.found |= node.name == self.name
        for expression in [
            *node.decorator_list,
            *node.args.defaults,
            *(value for value in node.args.kw_defaults if value is not None),
            *(
                argument.annotation
                for argument in [
                    *node.args.posonlyargs,
                    *node.args.args,
                    *node.args.kwonlyargs,
                ]
                if argument.annotation is not None
            ),
            *(
                argument.annotation
                for argument in [node.args.vararg, node.args.kwarg]
                if argument is not None and argument.annotation is not None
            ),
            *([node.returns] if node.returns is not None else []),
        ]:
            self.visit(expression)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function_header(node)

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> None:
        self._visit_function_header(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_class(node, header_binds_module=True)

    def _visit_class(
        self,
        node: ast.ClassDef,
        *,
        header_binds_module: bool,
    ) -> None:
        if header_binds_module:
            self.found |= node.name == self.name
            for expression in [
                *node.decorator_list,
                *node.bases,
                *(keyword.value for keyword in node.keywords),
            ]:
                self.visit(expression)
        global_visitor = _GlobalVisitor(self.name)
        for statement in node.body:
            global_visitor.visit(statement)
        if global_visitor.found:
            for statement in node.body:
                self.visit(statement)
        else:
            for statement in node.body:
                self._visit_executed_nested_classes(statement)

    def _visit_executed_nested_classes(self, node: ast.AST) -> None:
        if isinstance(node, ast.ClassDef):
            self._visit_class(node, header_binds_module=False)
            return
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda),
        ):
            return
        for child in ast.iter_child_nodes(node):
            self._visit_executed_nested_classes(child)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for expression in [
            *node.args.defaults,
            *(value for value in node.args.kw_defaults if value is not None),
        ]:
            self.visit(expression)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.visit(node.annotation)
        if node.value is not None:
            self.visit(node.target)
            self.visit(node.value)

    def _visit_comprehension(
        self,
        element: ast.expr,
        generators: list[ast.comprehension],
    ) -> None:
        for generator in generators:
            self.visit(generator.iter)
            for condition in generator.ifs:
                self.visit(condition)
        self.visit(element)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node.elt, node.generators)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._visit_comprehension(node.elt, node.generators)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node.elt, node.generators)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._visit_comprehension(node.key, node.generators)
        self.visit(node.value)

    def visit_MatchAs(self, node: ast.MatchAs) -> None:
        self.found |= node.name == self.name
        if node.pattern is not None:
            self.visit(node.pattern)

    def visit_MatchStar(self, node: ast.MatchStar) -> None:
        self.found |= node.name == self.name

    def visit_MatchMapping(self, node: ast.MatchMapping) -> None:
        self.found |= node.rest == self.name
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            bound = alias.asname or alias.name.split(".", 1)[0]
            self.found |= bound == self.name

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.found |= alias.name == "*" or (alias.asname or alias.name) == self.name

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.found |= node.name == self.name
        for statement in node.body:
            self.visit(statement)


def _selected_target(tree: ast.Module, target: str) -> ast.stmt | None:
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name == target
    ]
    if len(matches) != 1:
        return None
    selected = matches[0]
    selected_index = tree.body.index(selected)
    for statement in tree.body[selected_index + 1 :]:
        visitor = _RebindingVisitor(target)
        visitor.visit(statement)
        if visitor.found:
            return None
    return selected


def _target_scope(text: str, target: str | None) -> _Scope | None:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None

    if target is None:
        lines = text.splitlines()
        return _Scope(1, len(lines), -1, 0, len(lines) + 1, frozenset())

    selected = _selected_target(tree, target)
    if selected is None:
        return None

    lines = text.splitlines()
    host: ast.FunctionDef | ast.AsyncFunctionDef
    if isinstance(selected, (ast.FunctionDef, ast.AsyncFunctionDef)):
        host = selected
        start = _node_start(selected)
        column = selected.col_offset
        following = [
            _node_start(node) for node in tree.body if node.lineno > selected.lineno
        ]
        end = min(following) - 1 if following else len(lines)
    else:
        methods = [
            node
            for node in selected.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        if not methods:
            return None
        host = min(methods, key=lambda node: node.lineno)
        start = _node_start(selected)
        column = selected.col_offset
        later_top_level = [
            _node_start(node) for node in tree.body if node.lineno > selected.lineno
        ]
        end = min(later_top_level) - 1 if later_top_level else len(lines)

    body = list(host.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    first_code = body[0].lineno if body else end + 1
    if isinstance(selected, ast.ClassDef):
        class_body = list(selected.body)
        if (
            class_body
            and isinstance(class_body[0], ast.Expr)
            and isinstance(class_body[0].value, ast.Constant)
            and isinstance(class_body[0].value.value, str)
        ):
            class_body = class_body[1:]
        class_code = [
            statement
            for statement in class_body
            if not isinstance(
                statement,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            )
        ]
        if class_code:
            first_code = min(first_code, class_code[0].lineno)
    indentation_body = selected.body if isinstance(selected, ast.ClassDef) else host.body
    body_column = min(
        (statement.col_offset for statement in indentation_body),
        default=column + 4,
    )
    forced_post_rows = {
        decorator.lineno for decorator in getattr(selected, "decorator_list", ())
    }
    if isinstance(selected, ast.ClassDef):
        forced_post_rows.update(
            decorator.lineno for decorator in getattr(host, "decorator_list", ())
        )
    return _Scope(
        start,
        end,
        column,
        body_column,
        first_code,
        frozenset(forced_post_rows),
    )


def _legacy_evidence(
    text: str,
    comments: list[_Comment],
    seeds: tuple[str, ...],
    lock_sentinel: str,
    *,
    pre_code_count: int,
    scope: _Scope,
) -> tuple[set[str], set[str], set[int]]:
    """Count real labeled comments and claim their wrapped answer rows."""
    lines = text.splitlines()
    by_row = {comment.row: comment for comment in comments}
    markers = tuple(_marker(seed) for seed in seeds)
    labeled_markers = tuple(marker for marker in markers if marker is not None)
    pre: set[str] = set()
    post: set[str] = set()
    seen: set[str] = set()
    claimed: set[int] = set()
    lock_rows = [
        comment.row
        for comment in comments
        if _canonical(_comment_body(comment.text))
        == _canonical(_comment_body(lock_sentinel))
    ]
    pre_boundary = min([scope.first_code, *lock_rows])
    for index, (seed, marker) in enumerate(zip(seeds, markers, strict=True)):
        prompt_body = _comment_body(seed)
        occurrence = next(
            (
                comment
                for comment in comments
                if lines[comment.row - 1].strip().startswith("#")
                and _comment_body(comment.text).casefold().startswith(
                    (marker or prompt_body).casefold()
                )
            ),
            None,
        )
        if occurrence is None:
            continue
        claimed.add(occurrence.row)
        body = _comment_body(occurrence.text)
        if marker is None:
            key = (
                None
                if _canonical(body) == _canonical(prompt_body)
                else _evidence_key(body)
            )
        else:
            prompt = seed.split(":", 1)[1].strip()
            answer = body[len(marker) :].strip()
            key = (
                None
                if _canonical(answer) == _canonical(prompt)
                else _evidence_key(answer)
            )

        if marker is not None and key is None:
            for row in range(occurrence.row + 1, scope.end + 1):
                line = lines[row - 1].strip()
                if not line:
                    break
                continuation = by_row.get(row)
                if continuation is None or not line.startswith("#"):
                    break
                continuation_body = _comment_body(continuation.text)
                if any(
                    continuation_body.casefold().startswith(candidate.casefold())
                    for candidate in labeled_markers
                ) or _canonical(line) == _canonical(lock_sentinel):
                    break
                claimed.add(row)
                if key is None:
                    key = _evidence_key(continuation.text)

        if (
            key is None
            or key in seen
            or (index < pre_code_count and occurrence.row >= pre_boundary)
        ):
            continue
        seen.add(key)
        destination = pre if index < pre_code_count else post
        destination.add(key)

    return pre, post, claimed


def _natural_comment(
    comment: str,
    seeds: tuple[str, ...],
    lock_sentinel: str,
) -> str | None:
    body = _comment_body(comment)
    canonical = _canonical(body)
    generated = {_canonical(_comment_body(seed)) for seed in seeds}
    generated.update(
        _canonical(seed.split(":", 1)[1]) for seed in seeds if ":" in seed
    )
    if canonical in generated or canonical == _canonical(_comment_body(lock_sentinel)):
        return None
    for seed in seeds:
        marker = _marker(seed)
        if marker is None:
            continue
        if body.casefold().startswith(marker.casefold()):
            answer = body[len(marker) :].strip()
            prompt = seed.split(":", 1)[1].strip()
            if _canonical(answer) == _canonical(prompt):
                return None
            return _evidence_key(answer)
    return _evidence_key(body)


def candidate_comment_snapshot(
    text: str,
    *,
    seeds: tuple[str, ...] = SCAFFOLD_SEEDS,
    lock_sentinel: str = LOCK_SENTINEL,
    pre_code_count: int,
    natural_pre_code_count: int | None = None,
    target: str | None = None,
) -> CommentSnapshot:
    """Return distinct candidate comments and their current static placement."""
    scope = _target_scope(text, target)
    if scope is None:
        return CommentSnapshot(
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
            frozenset(),
        )

    comments = [
        comment
        for comment in _token_comments(text)
        if scope.start <= comment.row <= scope.end
        and comment.column >= scope.body_column
    ]
    legacy_pre, legacy_post, claimed_rows = _legacy_evidence(
        text,
        comments,
        seeds,
        lock_sentinel,
        pre_code_count=pre_code_count,
        scope=scope,
    )
    lock_rows = [
        comment.row
        for comment in comments
        if _canonical(_comment_body(comment.text))
        == _canonical(_comment_body(lock_sentinel))
    ]
    cutoff = min([scope.first_code, *lock_rows])

    natural_pre: set[str] = set()
    natural_post: set[str] = set()
    anchored_natural_post: set[str] = set()
    seen = legacy_pre | legacy_post
    all_keys = set(seen)
    natural_pre_limit = (
        pre_code_count if natural_pre_code_count is None else natural_pre_code_count
    )
    adjacent_post_used = False
    for comment in comments:
        if comment.row in claimed_rows:
            continue
        candidate = _natural_comment(comment.text, seeds, lock_sentinel)
        if candidate is None:
            continue
        all_keys.add(candidate)
        if candidate in seen:
            continue
        if not lock_rows and comment.row in scope.forced_post_rows:
            before_code = False
        elif lock_rows:
            before_code = comment.row < cutoff
        elif comment.row >= scope.first_code:
            before_code = False
        elif len(legacy_pre) + len(natural_pre) < natural_pre_limit:
            before_code = True
        elif comment.row == scope.first_code - 1 and not adjacent_post_used:
            before_code = False
            adjacent_post_used = True
        else:
            # Extra planning comments cannot satisfy trace or complexity gates.
            continue
        seen.add(candidate)
        destination = natural_pre if before_code else natural_post
        destination.add(candidate)
        if not before_code and (
            comment.row >= scope.first_code
            or comment.row in scope.forced_post_rows
        ):
            anchored_natural_post.add(candidate)

    return CommentSnapshot(
        pre_keys=frozenset(legacy_pre | natural_pre),
        post_keys=frozenset(legacy_post | natural_post),
        anchored_post_keys=frozenset(anchored_natural_post),
        legacy_post_keys=frozenset(legacy_post),
        all_keys=frozenset(all_keys),
    )


def candidate_comment_evidence(
    text: str,
    *,
    seeds: tuple[str, ...] = SCAFFOLD_SEEDS,
    lock_sentinel: str = LOCK_SENTINEL,
    pre_code_count: int,
    natural_pre_code_count: int | None = None,
    target: str | None = None,
) -> CommentEvidence:
    """Count candidate comments in the selected target without judging content."""
    return candidate_comment_snapshot(
        text,
        seeds=seeds,
        lock_sentinel=lock_sentinel,
        pre_code_count=pre_code_count,
        natural_pre_code_count=natural_pre_code_count,
        target=target,
    ).evidence


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <source_file>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        return 1
    text = path.read_text()
    for label, state in section_status(text).items():
        print(f"{label}: {state}")
    print(f"lock: {'locked' if LOCK_SENTINEL in text else 'unlocked'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
