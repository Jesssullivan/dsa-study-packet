"""Resolve the effective Python definition for a candidate-owned target.

The practice loop needs one mechanical answer: does the module still expose
the single top-level function or class selected for the rep?  A later
module-scope binding can replace that definition at runtime, so a name lookup
alone is not sufficient.

This module deliberately knows nothing about comments, reasoning, or practice
states.
"""

from __future__ import annotations

import ast

CandidateTarget = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


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

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
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


def selected_target(tree: ast.Module, target: str) -> CandidateTarget | None:
    """Return one definition only when no later runtime binding replaces it."""
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
