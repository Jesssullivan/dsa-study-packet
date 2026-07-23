"""Unit tests for the Copilot preToolUse guard (scripts/hooks/guard_pretooluse.py).

Exercises the persona invariant directly: the agent never edits
candidate-owned files under .challenges/, and never runs an unbounded rm -rf
or a forced git push. Maintenance edits to src/ and tests/ must stay allowed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_HOOKS_SCRIPTS = ROOT / "scripts" / "hooks"
sys.path.insert(0, str(_HOOKS_SCRIPTS))

from guard_pretooluse import decide  # type: ignore[import-not-found]  # noqa: E402

GUARD_SCRIPT = _HOOKS_SCRIPTS / "guard_pretooluse.py"


def test_denies_edit_targeting_candidate_workspace() -> None:
    decision = decide(
        {
            "toolName": "Edit",
            "toolArgs": {"file_path": ".challenges/workspace/two_sum.py"},
        }
    )
    assert decision["permissionDecision"] == "deny"
    assert "candidate" in decision["permissionDecisionReason"]
    assert "themselves" in decision["permissionDecisionReason"]


def test_denies_write_targeting_candidate_workspace_via_nested_args() -> None:
    decision = decide(
        {
            "toolName": "create_file",
            "toolArgs": {"params": {"path": "./.challenges/workspace/notes.md"}},
        }
    )
    assert decision["permissionDecision"] == "deny"


def test_allows_edit_targeting_maintained_source() -> None:
    decision = decide(
        {
            "toolName": "Edit",
            "toolArgs": {"file_path": "src/algo/arrays/two_sum.py"},
        }
    )
    assert decision["permissionDecision"] == "allow"


def test_allows_edit_targeting_tests_tree() -> None:
    decision = decide(
        {
            "toolName": "str_replace_editor",
            "toolArgs": {"path": "tests/test_hooks_guard.py"},
        }
    )
    assert decision["permissionDecision"] == "allow"


def test_allows_maintenance_edit_whose_content_mentions_workspace() -> None:
    decision = decide(
        {
            "toolName": "Edit",
            "toolArgs": {
                "file_path": "docs/guide/local-practice.md",
                "new_string": "Personal state belongs under .challenges/ only.",
            },
        }
    )
    assert decision["permissionDecision"] == "allow"


def test_read_only_tool_never_denies_even_over_candidate_path() -> None:
    decision = decide(
        {
            "toolName": "readFile",
            "toolArgs": {"file_path": ".challenges/workspace/two_sum.py"},
        }
    )
    assert decision["permissionDecision"] == "allow"


def test_toolargs_as_json_encoded_string_is_parsed() -> None:
    decision = decide(
        {
            "toolName": "Write",
            "toolArgs": json.dumps({"file_path": ".challenges/workspace/x.py"}),
        }
    )
    assert decision["permissionDecision"] == "deny"


def test_denies_rm_rf_outside_workspace_absolute_path() -> None:
    decision = decide(
        {
            "toolName": "runInTerminal",
            "toolArgs": {"command": "rm -rf /var/tmp/scratch"},
        }
    )
    assert decision["permissionDecision"] == "deny"
    assert "rm -rf" in decision["permissionDecisionReason"]


def test_denies_rm_fr_short_flags_targeting_home() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "rm -fr ~/Downloads"}}
    )
    assert decision["permissionDecision"] == "deny"


def test_denies_rm_rf_targeting_braced_home_variable() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "rm -rf ${HOME}/scratch"}}
    )
    assert decision["permissionDecision"] == "deny"


def test_denies_rm_long_flags_targeting_parent_traversal() -> None:
    decision = decide(
        {
            "toolName": "shell",
            "toolArgs": {"command": "rm --recursive --force ../sibling-repo"},
        }
    )
    assert decision["permissionDecision"] == "deny"


def test_allows_rm_rf_inside_workspace() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "rm -rf .challenges/tmp"}}
    )
    assert decision["permissionDecision"] == "allow"


def test_allows_plain_rm_without_force_recursive_flags() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "rm /var/tmp/one-file.txt"}}
    )
    assert decision["permissionDecision"] == "allow"


def test_denies_git_push_force_long_flag() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "git push --force origin main"}}
    )
    assert decision["permissionDecision"] == "deny"
    assert "force" in decision["permissionDecisionReason"]


def test_denies_git_push_force_short_flag() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "git push -f origin main"}}
    )
    assert decision["permissionDecision"] == "deny"


def test_denies_git_push_force_with_lease() -> None:
    decision = decide(
        {
            "toolName": "terminal",
            "toolArgs": {"command": "git push --force-with-lease"},
        }
    )
    assert decision["permissionDecision"] == "deny"


def test_allows_plain_git_push() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "git push origin main"}}
    )
    assert decision["permissionDecision"] == "allow"


def test_allows_unrelated_shell_command() -> None:
    decision = decide(
        {"toolName": "bash", "toolArgs": {"command": "uv run pytest -q"}}
    )
    assert decision["permissionDecision"] == "allow"


def test_missing_tool_name_and_args_default_to_allow() -> None:
    assert decide({})["permissionDecision"] == "allow"


def test_main_reads_stdin_and_prints_a_decision() -> None:
    payload = json.dumps(
        {"toolName": "Edit", "toolArgs": {"file_path": ".challenges/x.py"}}
    )
    proc = subprocess.run(
        [sys.executable, str(GUARD_SCRIPT)],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0
    decision = json.loads(proc.stdout)
    assert decision["permissionDecision"] == "deny"


def test_main_denies_via_nonzero_exit_on_unparseable_payload() -> None:
    proc = subprocess.run(
        [sys.executable, str(GUARD_SCRIPT)],
        input="not json",
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 2
