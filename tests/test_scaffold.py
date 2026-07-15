"""Tests for editor-practice scaffold injection and presence gates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scaffold_status import section_status  # type: ignore[import-not-found]
from strip_solution import (  # type: ignore[import-not-found]
    LOCK_SENTINEL,
    SCAFFOLD_SEEDS,
    inject_scaffold,
    strip_solution,
)

MODULE = '''"""topic / problem

Problem:
    Do the thing.
"""


def solve(nums: list[int]) -> int:
    """Return the answer."""
    total = 0
    for n in nums:
        total += n
    return total
'''


class TestInjectScaffold:
    def test_scaffold_lands_above_raise_at_body_indent(self) -> None:
        result = inject_scaffold(strip_solution(MODULE))
        lines = result.splitlines()
        raise_at = lines.index("    raise NotImplementedError")
        assert lines[raise_at - 1] == f"    {LOCK_SENTINEL}"
        for offset, seed in enumerate(reversed(SCAFFOLD_SEEDS), start=2):
            assert lines[raise_at - offset] == f"    {seed}"

    def test_class_method_target(self) -> None:
        source = "class Solver:\n    def solve(self) -> None:\n        return None\n"
        result = inject_scaffold(strip_solution(source), target_name="Solver")
        assert f"        {LOCK_SENTINEL}" in result.splitlines()

    def test_selected_function_wins_over_earlier_legitimate_raise(self) -> None:
        source = (
            "def optional_backend() -> None:\n"
            "    raise RuntimeError('not installed')\n"
            "\n\n"
            "def solve() -> int:\n"
            "    return 42\n"
        )
        stripped = strip_solution(source)
        result = inject_scaffold(stripped, target_name="solve")
        lines = result.splitlines()
        lock_at = lines.index(f"    {LOCK_SENTINEL}")
        assert lock_at > lines.index("def solve() -> int:")

    def test_selected_class_wins_over_earlier_function_stub(self) -> None:
        source = (
            "def alternate() -> int:\n"
            "    return 1\n"
            "\n\n"
            "class Solver:\n"
            "    def solve(self) -> int:\n"
            "        return 42\n"
        )
        result = inject_scaffold(strip_solution(source), target_name="Solver")
        lines = result.splitlines()
        lock_at = lines.index(f"        {LOCK_SENTINEL}")
        assert lock_at > lines.index("class Solver:")

    def test_no_function_is_a_noop(self) -> None:
        source = '"""Doc only."""\n\nANSWER = 42\n'
        assert inject_scaffold(source) == source

    def test_idempotent_on_rerun(self) -> None:
        once = inject_scaffold(strip_solution(MODULE))
        assert inject_scaffold(once) == once
        assert once.count(LOCK_SENTINEL) == 1

    def test_earliest_method_wins_over_later_helper(self) -> None:
        # Class-based problems with a trailing top-level helper (kd_tree shape):
        # the scaffold must gate the first real method, not the helper.
        source = (
            "class Tree:\n"
            "    def build(self) -> None:\n"
            "        return None\n"
            "\n"
            "    def query(self) -> None:\n"
            "        return None\n"
            "\n"
            "\n"
            "def _helper() -> int:\n"
            "    return 1\n"
        )
        lines = inject_scaffold(strip_solution(source)).splitlines()
        lock_at = lines.index(f"        {LOCK_SENTINEL}")
        assert lock_at < lines.index("class Tree:") + 10
        assert lines.index("def _helper() -> int:") > lock_at

    def test_without_scaffold_flag_output_unchanged(self) -> None:
        # Legacy strip stays byte-identical; scaffolding is opt-in.
        assert LOCK_SENTINEL not in strip_solution(MODULE)


class TestScaffoldStatus:
    def test_fresh_scaffold_is_empty_and_locked(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        status = section_status(text)
        assert set(status.values()) == {"empty"}
        assert LOCK_SENTINEL in text

    def test_edited_seed_line_counts_as_filled(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            "# RESTATE: the problem in your own words: inputs, outputs, constraints",
            "# RESTATE: sum the list; ints in, one int out; empty list allowed",
        )
        assert section_status(text)["RESTATE"] == "filled"
        assert section_status(text)["EXAMPLE"] == "empty"

    def test_content_below_seed_counts_as_filled(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        seed = SCAFFOLD_SEEDS[1]
        text = text.replace(f"    {seed}", f"    {seed}\n    # [1, 2, 3] -> 6; [] -> 0")
        assert section_status(text)["EXAMPLE"] == "filled"

    def test_deleted_label_is_missing(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(f"    {SCAFFOLD_SEEDS[2]}\n", "")
        assert section_status(text)["INVARIANT"] == "missing"

    def test_executable_line_after_unlock_does_not_fill_final_section(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(f"    {LOCK_SENTINEL}\n", "")

        assert section_status(text)["COMPLEXITY"] == "empty"
