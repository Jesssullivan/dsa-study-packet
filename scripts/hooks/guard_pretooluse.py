"""Copilot ``preToolUse`` hook: enforce "the agent never edits candidate-owned
files" (see AGENTS.md).

Denies file-edit/write tool calls that target ``.challenges/**`` (the
candidate's own workspace) and clearly destructive shell patterns (``rm -rf``
outside this workspace, ``git push --force``). Every deny carries a reason
telling the calling agent what to do instead. Only path-shaped argument
fields are inspected for the ``.challenges/`` marker, so maintenance edits
that merely mention the workspace in file content stay allowed. Schema and
doc source: .github/hooks/README.md.

Run as a hook (stdin -> stdout, exit 0 unless the payload itself is
unreadable, in which case exit 2 so the caller's own fail-closed default
applies):

    python3 scripts/hooks/guard_pretooluse.py
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterator
from typing import Any

CANDIDATE_WORKSPACE_MARKER = ".challenges/"

# Tool-name substrings (case-insensitive) that mark a file-mutating tool
# across the runtimes that read this hook: Copilot CLI/cloud agent, and
# Claude Code's compatible "PreToolUse" plugin format.
EDIT_TOOL_NAME_HINTS = (
    "edit",
    "write",
    "create_file",
    "createfile",
    "applypatch",
    "apply_patch",
    "str_replace",
    "replace_string",
)

# Argument-key substrings (case-insensitive) that mark a path-shaped value.
# Content fields like new_string/old_string/content must not trip the
# workspace marker, or edits to docs that mention .challenges/ get denied.
PATH_KEY_HINTS = (
    "path",
    "file",
    "filename",
    "target",
    "uri",
    "notebook",
)

# Tool-name substrings that mark a shell/terminal execution tool.
SHELL_TOOL_NAME_HINTS = (
    "bash",
    "shell",
    "terminal",
    "exec",
    "runcommand",
    "run_command",
)

_RM_WORD = re.compile(r"\brm\b")
_RM_COMBINED_FLAGS = re.compile(
    r"(?<![\w-])-[A-Za-z]*[rR][A-Za-z]*[fF][A-Za-z]*(?![\w-])"
    r"|(?<![\w-])-[A-Za-z]*[fF][A-Za-z]*[rR][A-Za-z]*(?![\w-])"
)
_RM_LONG_RECURSIVE = re.compile(r"--recursive\b")
_RM_LONG_FORCE = re.compile(r"--force\b")
# A target is "outside the workspace" when it is absolute, home-relative, or
# escapes via a parent-directory traversal; a bare relative path stays inside.
_UNSAFE_RM_TARGET = re.compile(r"(?:^|\s)(?:/|~|\$\{?HOME\}?|\.\.(?:/|\\|$))")
_GIT_PUSH = re.compile(r"\bgit\s+push\b")
_FORCE_FLAG = re.compile(r"--force(?:-with-lease)?\b|(?<![\w-])-f\b")


def _iter_strings(value: Any) -> Iterator[str]:
    """Yield every string leaf inside a JSON-shaped value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_strings(item)


def _parse_tool_args(tool_args: Any) -> Any:
    """``toolArgs`` is documented as an object in one place and a JSON-encoded
    string in another; accept either shape."""
    if isinstance(tool_args, str):
        try:
            return json.loads(tool_args)
        except json.JSONDecodeError:
            return tool_args
    return tool_args


def _matches_any_hint(name: str, hints: tuple[str, ...]) -> bool:
    lowered = name.lower()
    return any(hint in lowered for hint in hints)


def _iter_path_strings(value: Any, key_hinted: bool = False) -> Iterator[str]:
    """Yield string leaves reachable only through path-shaped keys."""
    if isinstance(value, str):
        if key_hinted:
            yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            hinted = key_hinted or _matches_any_hint(str(key), PATH_KEY_HINTS)
            yield from _iter_path_strings(item, hinted)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_path_strings(item, key_hinted)


def _targets_candidate_workspace(tool_args: Any) -> bool:
    # A bare-string argument to an edit tool is itself path-shaped.
    if isinstance(tool_args, str):
        return CANDIDATE_WORKSPACE_MARKER in tool_args
    return any(
        CANDIDATE_WORKSPACE_MARKER in text
        for text in _iter_path_strings(tool_args)
    )


def _has_recursive_force_flags(command_text: str) -> bool:
    if _RM_COMBINED_FLAGS.search(command_text):
        return True
    return bool(
        _RM_LONG_RECURSIVE.search(command_text) and _RM_LONG_FORCE.search(command_text)
    )


def _is_destructive_rm(command_text: str) -> bool:
    if not _RM_WORD.search(command_text):
        return False
    if not _has_recursive_force_flags(command_text):
        return False
    return bool(_UNSAFE_RM_TARGET.search(command_text))


def _is_force_push(command_text: str) -> bool:
    for statement in re.split(r"&&|\|\||;|\n", command_text):
        if _GIT_PUSH.search(statement) and _FORCE_FLAG.search(statement):
            return True
    return False


def decide(payload: dict[str, Any]) -> dict[str, Any]:
    """Return one preToolUse decision for a single hook invocation payload."""
    tool_name = str(payload.get("toolName", ""))
    tool_args = _parse_tool_args(payload.get("toolArgs"))

    if _matches_any_hint(
        tool_name, EDIT_TOOL_NAME_HINTS
    ) and _targets_candidate_workspace(tool_args):
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "candidate-owned file under .challenges/; relay the exact "
                "error and ask the candidate to make this edit themselves"
            ),
        }

    if _matches_any_hint(tool_name, SHELL_TOOL_NAME_HINTS):
        command_text = "\n".join(_iter_strings(tool_args))
        if _is_destructive_rm(command_text):
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "rm -rf targets a path outside this workspace; relay the "
                    "exact command and ask the candidate to run it themselves "
                    "if they intend it"
                ),
            }
        if _is_force_push(command_text):
            return {
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "git push --force rewrites shared history; relay the "
                    "exact command and ask the candidate to run it themselves "
                    "if they intend it"
                ),
            }

    return {"permissionDecision": "allow"}


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        print(f"guard_pretooluse: invalid JSON payload: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(decide(payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
