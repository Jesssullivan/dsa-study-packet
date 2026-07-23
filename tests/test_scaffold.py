"""Tests for editor-practice scaffold injection and presence gates."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scaffold_status import (  # type: ignore[import-not-found]
    CommentEvidence,
    candidate_comment_evidence,
    section_status,
)
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

    @pytest.mark.parametrize("answer", ["", "...", "TODO", "placeholder"])
    def test_label_or_placeholder_alone_does_not_count(self, answer: str) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        seed = SCAFFOLD_SEEDS[0]
        marker = seed.split(":", 1)[0] + ":"
        text = text.replace(seed, f"{marker} {answer}".rstrip())

        assert section_status(text)["RESTATE"] == "empty"

    def test_deleted_label_is_missing(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(f"    {SCAFFOLD_SEEDS[2]}\n", "")
        assert section_status(text)["INVARIANT"] == "missing"

    def test_executable_line_after_unlock_does_not_fill_final_section(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(f"    {LOCK_SENTINEL}\n", "")

        assert section_status(text)["COMPLEXITY"] == "empty"

    def test_blank_and_wrapped_continuations_keep_legacy_behavior(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            f"    {SCAFFOLD_SEEDS[0]}\n",
            f"    {SCAFFOLD_SEEDS[0]}\n\n"
            "    # Return the sum of the values.\n"
            "    # Empty input returns zero.\n",
        )

        assert section_status(text)["RESTATE"] == "filled"


class TestCandidateCommentEvidence:
    def evidence(self, text: str) -> CommentEvidence:
        return candidate_comment_evidence(
            text,
            pre_code_count=4,
            natural_pre_code_count=3,
            target="solve",
        )

    def test_ordinary_comments_count_without_framework_labels(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        replacements = (
            "# Return the sum of all input values.",
            "# [1, 2] returns 3; an empty list returns 0.",
            "# The running total equals the sum of values already visited.",
        )
        for seed, replacement in zip(SCAFFOLD_SEEDS[:3], replacements, strict=True):
            text = text.replace(seed, replacement)
        for seed in SCAFFOLD_SEEDS[3:]:
            text = text.replace(f"    {seed}\n", "")

        assert self.evidence(text).pre_code == 3
        assert self.evidence(text).post_code == 0

        text = text.replace(f"    {LOCK_SENTINEL}\n", "").replace(
            "    raise NotImplementedError",
            "    total = sum(nums)\n"
            "    # The loop-free implementation is O(n) in the input length.\n"
            "    return total",
        )

        assert self.evidence(text).pre_code == 3
        assert self.evidence(text).post_code == 1

    def test_comments_after_executable_code_do_not_count_as_planning(self) -> None:
        text = (
            "def solve() -> int:\n"
            "    value = 1\n"
            "    # Return the value after checking the simple case.\n"
            "    # An input-free call returns one.\n"
            "    # A constant result needs no additional storage.\n"
            f"    {LOCK_SENTINEL}\n"
            "    return value\n"
        )

        assert self.evidence(text).pre_code == 0

    def test_noise_and_duplicates_do_not_inflate_count(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        replacements = [
            "# TODO later",
            "# noqa: E501",
            "# x",
            "# 1",
            "# Use a running total.",
            "# Use a running total.",
        ]
        text = text.replace(
            f"    {SCAFFOLD_SEEDS[0]}\n",
            "\n".join(f"    {comment}" for comment in replacements) + "\n",
        )
        for seed in SCAFFOLD_SEEDS[1:]:
            text = text.replace(f"    {seed}\n", "")

        assert self.evidence(text).pre_code == 1

    def test_natural_filter_allows_substantive_answer_language(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            SCAFFOLD_SEEDS[0],
            "# Answer with two indices once a complement appears.",
        )

        assert self.evidence(text).pre_code == 1

    @pytest.mark.parametrize(
        "placeholder",
        [
            "answer",
            "answer here",
            "answer here。",
            "fill here",
            "fill here\uff01",
            "[fill here]",
            "fill-in",
            "fill later",
            "fill later\uff1f",
            "fill this in",
            "(answer here)",
            "YOUR CODE HERE",
            "write your answer here",
            "write answer here",
            "write code here",
            "write implementation here",
            "your implementation here",
            "code goes here",
            "answer goes here",
            "your answer goes here",
            "not implemented yet",
            "implementation goes here",
            "insert code here",
            "[TODO: fill later]",
            "placeholder",
            "tbd",
        ],
    )
    def test_unlabeled_placeholders_are_not_evidence(self, placeholder: str) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], f"# {placeholder}")

        assert self.evidence(text).pre_code == 0

    def test_non_latin_reasoning_comments_count(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # 入力値の合計を返します。\n"
            "    # 空ならゼロを返します。\n"
            "    # 各要素を一度確認します。\n"
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_concise_cjk_reasoning_comments_count(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # 返回和\n"
            "    # 空为零\n"
            "    # 单遍历\n"
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_region_directives_do_not_count(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# region solution code")
        text = text.replace(SCAFFOLD_SEEDS[1], "# endregion")
        text = text.replace(SCAFFOLD_SEEDS[2], "# type: list[int]")

        assert self.evidence(text).pre_code == 0

    def test_fullwidth_task_markers_and_directives_do_not_count(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# \uff34\uff2f\uff24\uff2f later")
        text = text.replace(SCAFFOLD_SEEDS[1], "# \uff26\uff29\uff38\uff2d\uff25 later")
        text = text.replace(SCAFFOLD_SEEDS[2], "# \uff4e\uff4f\uff51\uff41\uff1a E501")

        assert self.evidence(text).pre_code == 0

    def test_fullwidth_ascii_noise_does_not_gain_non_latin_status(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# \uff58\uff58")
        text = text.replace(SCAFFOLD_SEEDS[1], "# \uff59\uff59")
        text = text.replace(SCAFFOLD_SEEDS[2], "# \uff5a\uff5a")

        assert self.evidence(text).pre_code == 0

    def test_terminal_punctuation_does_not_defeat_deduplication(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# Use a map")
        text = text.replace(SCAFFOLD_SEEDS[1], "# Use a map.")
        text = text.replace(SCAFFOLD_SEEDS[2], "# Use a map!")

        assert self.evidence(text).pre_code == 1

    def test_compatibility_styled_letters_do_not_defeat_deduplication(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        styled = (
            "\U0001d414\U0001d42c\U0001d41e "
            "\U0001d41a "
            "\U0001d426\U0001d41a\U0001d429"
        )
        styled_caps = (
            "\U0001d414\U0001d412\U0001d404 "
            "\U0001d400 "
            "\U0001d40c\U0001d400\U0001d40f"
        )
        text = text.replace(SCAFFOLD_SEEDS[0], "# Use a map")
        text = text.replace(SCAFFOLD_SEEDS[1], f"# {styled}")
        text = text.replace(SCAFFOLD_SEEDS[2], f"# {styled_caps}")

        assert self.evidence(text).pre_code == 1

    def test_unicode_terminal_punctuation_does_not_defeat_deduplication(
        self,
    ) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# 入力値の合計を返します")
        text = text.replace(SCAFFOLD_SEEDS[1], "# 入力値の合計を返します。")
        text = text.replace(SCAFFOLD_SEEDS[2], "# 入力値の合計を返します\uff01")

        assert self.evidence(text).pre_code == 1

    def test_concise_symbolic_examples_are_real_comments(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(SCAFFOLD_SEEDS[0], "# [] -> []")
        text = text.replace(SCAFFOLD_SEEDS[1], "# O(n) time")

        assert self.evidence(text).pre_code == 2

    def test_fullwidth_symbolic_example_is_a_real_comment(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            SCAFFOLD_SEEDS[0],
            "# \uff3b\uff3d \uff1d\uff1e \uff3b\uff3d",
        )

        assert self.evidence(text).pre_code == 1

    def test_bare_symbols_and_unmatched_brackets_are_not_reasoning(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        replacements = ("# ->", "# ==", "# []", "# " + "[" * 100_000)
        for seed, replacement in zip(SCAFFOLD_SEEDS[:4], replacements, strict=True):
            text = text.replace(seed, replacement)

        assert self.evidence(text).pre_code == 0

    def test_placeholder_shaped_symbolic_comments_are_not_reasoning(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        replacements = ("# ? -> ?", "# ? == ?", "# O(?)")
        for seed, replacement in zip(SCAFFOLD_SEEDS[:3], replacements, strict=True):
            text = text.replace(seed, replacement)

        assert self.evidence(text).pre_code == 0

    def test_legacy_labeled_answers_remain_compatible(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        answers = (
            "Return the sum of every value.",
            "An empty list returns zero.",
            "The running total covers every visited value.",
            "Use one pass through the input.",
            "Trace the saved three-value example.",
        )
        for seed, answer in zip(SCAFFOLD_SEEDS, answers, strict=True):
            marker = seed.split(":", 1)[0]
            text = text.replace(seed, f"{marker}: {answer}")

        evidence = self.evidence(text)
        assert evidence.pre_code == 4
        assert evidence.post_code == 1

    def test_legacy_labels_use_natural_filters_and_deduplicate(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        answers = (
            "TODO later",
            "noqa: E501",
            "x",
            "Use a map.",
            "Use a map!",
        )
        for seed, answer in zip(SCAFFOLD_SEEDS, answers, strict=True):
            marker = seed.split(":", 1)[0]
            text = text.replace(seed, f"{marker}: {answer}")

        assert self.evidence(text) == CommentEvidence(pre_code=1, post_code=0)

    def test_lowercase_legacy_labels_count(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            SCAFFOLD_SEEDS[0],
            "# restate: Return the sum of every value.",
        )

        assert self.evidence(text).pre_code == 1

    def test_optional_labels_work_on_inline_code_comments(self) -> None:
        text = (
            "def solve(nums: list[int]) -> list[int]:\n"
            "    # Return the matching pair of indices.\n"
            "    # [2, 7] with target 9 returns [0, 1].\n"
            "    # Use a map from each prior value to its index.\n"
            "    seen = {}  # approach: store each prior value\n"
            "    pass  # example: trace the saved pair through the map\n"
            "    return []  # complexity: O(n) time and O(n) space\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=3)

    def test_wrapped_legacy_answer_counts_once(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            f"    {SCAFFOLD_SEEDS[0]}\n",
            f"    {SCAFFOLD_SEEDS[0]}\n"
            "    # Return the sum of every value.\n",
        )

        assert self.evidence(text).pre_code == 1

    def test_multiline_wrapped_legacy_answer_counts_once(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            f"    {SCAFFOLD_SEEDS[0]}\n",
            f"    {SCAFFOLD_SEEDS[0]}\n"
            "    # Return the sum of\n"
            "    # all values in\n"
            "    # the input list.\n",
        )

        assert self.evidence(text).pre_code == 1

    def test_filled_legacy_label_does_not_swallow_next_natural_comment(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            SCAFFOLD_SEEDS[0],
            "# RESTATE: Return the sum of every value.\n"
            "    # An empty list returns zero.",
        )

        assert self.evidence(text).pre_code == 2

    def test_wrapped_legacy_answer_stops_before_a_new_comment_block(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            f"    {SCAFFOLD_SEEDS[0]}\n",
            f"    {SCAFFOLD_SEEDS[0]}\n"
            "    # Return the sum of every value.\n"
            "\n"
            "    # An empty list returns zero.\n",
        )
        text = text.replace(
            SCAFFOLD_SEEDS[3],
            "# APPROACH: Visit every value once.",
        )

        assert self.evidence(text).pre_code == 3

    def test_pre_code_labels_below_implementation_do_not_unlock(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    total = sum(nums)\n"
            "    # RESTATE: Return the sum of every value.\n"
            "    # EXAMPLE: An empty list returns zero.\n"
            "    # INVARIANT: The total covers every input value.\n"
            "    # APPROACH: Visit each value exactly once.\n"
            "    return total\n"
        )

        assert self.evidence(text).pre_code == 0

    def test_strings_and_exact_scaffold_text_are_not_evidence(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            "    raise NotImplementedError",
            '    note = "# ordinary looking comment"\n'
            '    prompt = "# Return the sum of every value"\n'
            "    raise NotImplementedError",
        )

        assert self.evidence(text) == CommentEvidence(0, 0)

    def test_marker_shaped_lines_inside_a_string_are_not_legacy_evidence(
        self,
    ) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text = text.replace(
            "    raise NotImplementedError",
            "    note = '''\n"
            "# RESTATE: candidate-looking text\n"
            "# EXAMPLE: [1, 2] returns 3\n"
            "# INVARIANT: the total covers prior values\n"
            "'''\n"
            "    raise NotImplementedError",
        )

        assert self.evidence(text) == CommentEvidence(0, 0)

    def test_comments_outside_the_target_do_not_count(self) -> None:
        text = inject_scaffold(strip_solution(MODULE))
        text += "\n# This distant module comment is not candidate reasoning.\n"

        evidence = self.evidence(text)
        assert evidence.pre_code == 0
        assert evidence.post_code == 0

    def test_comments_with_shallower_indentation_do_not_count(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            " # Return the sum of every value.\n"
            " # An empty list returns zero.\n"
            " # Visit each value once.\n"
            "    return sum(nums)\n"
            " # Trace the example through the return.\n"
            " # The implementation takes O(n) time.\n"
            " # Negative values still contribute to the sum.\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    def test_comment_on_following_helper_decorator_is_outside_target(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit each value exactly once.\n"
            "    return sum(nums)\n"
            "\n"
            "@cache  # Cache helper states between calls.\n"
            "def helper() -> int:\n"
            "    return 1\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_duplicate_target_definitions_fail_closed(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
            "\n"
            "def solve(nums: list[int]) -> int:\n"
            "    return -1\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    def test_later_target_assignment_fails_closed(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
            "\n"
            "solve = lambda nums: -1\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    def test_assignment_before_target_definition_does_not_hide_target(self) -> None:
        text = (
            "solve: object\n"
            "\n"
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    @pytest.mark.parametrize(
        "rebind",
        [
            "del solve",
            "other = lambda value=(solve := lambda nums: -1): value",
            "def other(value=(solve := lambda nums: -1)):\n    return value",
        ],
    )
    def test_later_runtime_rebinding_fails_closed(self, rebind: str) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
            "\n"
            f"{rebind}\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    @pytest.mark.parametrize(
        "rebind",
        [
            "match 2:\n    case solve:\n        pass",
            "match 2:\n    case _ as solve:\n        pass",
            (
                "class Other:\n"
                "    global solve\n"
                "    solve = lambda nums: -1"
            ),
            (
                "class Outer:\n"
                "    class Inner:\n"
                "        global solve\n"
                "        solve = lambda nums: -1"
            ),
        ],
    )
    def test_control_flow_runtime_rebinding_fails_closed(self, rebind: str) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
            "\n"
            f"{rebind}\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    @pytest.mark.parametrize(
        "later_statement",
        [
            "solve: object",
            "ignored = [value for solve in [] for value in [solve]]",
            (
                "class Outer:\n"
                "    solve = 2\n"
                "    class Inner:\n"
                "        global solve\n"
                "        pass"
            ),
            "class Outer:\n    class solve:\n        pass",
        ],
    )
    def test_non_rebinding_later_statements_keep_target_visible(
        self, later_statement: str
    ) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    return sum(nums)\n"
            "\n"
            f"{later_statement}\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_selected_target_decorator_comment_counts_as_implementation(self) -> None:
        text = (
            "@cache  # Memoize each state after it is solved.\n"
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Visit every value once.\n"
            "    total = sum(nums)\n"
            "    # Trace the saved example through the sum.\n"
            "    return total  # The implementation takes O(n) time.\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=3)

    def test_syntax_error_fails_closed(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Restate the input and output.\n"
            "    # [] -> 0.\n"
            "    # Use a running total.\n"
            "    value = (\n"
        )

        assert self.evidence(text) == CommentEvidence(0, 0)

    def test_class_target_spans_its_methods(self) -> None:
        text = (
            "# Outside the target.\n"
            "class Solver:\n"
            "    def solve(self, nums: list[int]) -> int:\n"
            "        # Return the sum of all values.\n"
            "        # [] returns 0.\n"
            "        total = sum(nums)\n"
            "        # The implementation takes O(n) time.\n"
            "        return total\n"
            "\n"
            "    def helper(self) -> None:\n"
            "        # This public method is still part of the class target.\n"
            "        return None\n"
        )

        evidence = candidate_comment_evidence(
            text,
            pre_code_count=4,
            target="Solver",
        )

        assert evidence == CommentEvidence(pre_code=2, post_code=2)

    def test_class_level_reasoning_comments_count_for_a_class_target(self) -> None:
        text = (
            "class Solver:\n"
            "    # Store the values supplied by the caller.\n"
            "    # Empty input leaves an empty stored list.\n"
            "    # Keep construction linear in the number of values.\n"
            "    def __init__(self, nums: list[int]) -> None:\n"
            "        self.nums = nums\n"
        )

        evidence = candidate_comment_evidence(
            text,
            pre_code_count=4,
            natural_pre_code_count=3,
            target="Solver",
        )

        assert evidence == CommentEvidence(pre_code=3, post_code=0)

    def test_comments_after_class_body_code_are_post_code(self) -> None:
        text = (
            "class Solver:\n"
            "    cache: dict[int, int] = {}\n"
            "    # Store each input value for later queries.\n"
            "    # Empty input leaves the instance empty.\n"
            "    # Construction visits each input once.\n"
            "    def __init__(self, nums: list[int]) -> None:\n"
            "        self.nums = nums\n"
        )

        evidence = candidate_comment_evidence(
            text,
            pre_code_count=4,
            natural_pre_code_count=3,
            target="Solver",
        )

        assert evidence == CommentEvidence(pre_code=0, post_code=3)

    def test_three_post_code_moments_are_exposed(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # [] returns 0.\n"
            "    # Use a running total.\n"
            "    total = 0\n"
            "    # Add the current value to the total.\n"
            "    for value in nums:\n"
            "        total += value  # The total covers the visited prefix.\n"
            "    # The single pass takes O(n) time.\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=3)

    def test_comment_immediately_above_first_statement_is_post_code(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    # Initialize the accumulator before scanning.\n"
            "    total = 0\n"
            "    for value in nums:\n"
            "        total += value\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=1)

    def test_extra_planning_comments_cannot_complete_post_code_gates(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    # Ask whether the input can contain negatives.\n"
            "    # Keep the implementation to one pass.\n"
            "    # Initialize the accumulator before scanning.\n"
            "    total = 0\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=1)

    def test_skipped_planning_comment_can_count_when_repeated_beside_code(
        self,
    ) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    # The implementation takes O(n) time.\n"
            "    # Initialize the accumulator before scanning.\n"
            "    total = 0\n"
            "    return total  # The implementation takes O(n) time.\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=2)

    def test_prose_starting_with_post_label_word_is_not_a_phase_marker(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Complexity should stay linear for large inputs.\n"
            "    # Initialize the accumulator before scanning.\n"
            "    total = 0\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=1)


class TestDocstringCommentEvidence:
    def evidence(self, text: str) -> CommentEvidence:
        return candidate_comment_evidence(
            text,
            pre_code_count=4,
            natural_pre_code_count=3,
            target="solve",
        )

    def test_def_docstring_lines_count_as_pre_code_evidence(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            '    """Return the sum of all input values.\n'
            "\n"
            "    An empty list returns zero.\n"
            "    Visit each value once.\n"
            '    """\n'
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_module_docstring_never_counts_with_named_target(self) -> None:
        text = (
            '"""Module problem statement.\n'
            "\n"
            "This restates the problem, gives an example, and names a pattern.\n"
            '"""\n'
            "\n"
            "\n"
            "def solve(nums: list[int]) -> int:\n"
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    def test_module_docstring_never_counts_with_no_target(self) -> None:
        text = (
            '"""Module problem statement.\n'
            "\n"
            "This restates the problem, gives an example, and names a pattern.\n"
            '"""\n'
            "\n"
            "\n"
            "def solve(nums: list[int]) -> int:\n"
            "    raise NotImplementedError\n"
        )

        evidence = candidate_comment_evidence(
            text, pre_code_count=4, natural_pre_code_count=3, target=None
        )

        assert evidence == CommentEvidence(pre_code=0, post_code=0)

    def test_docstring_abutting_first_code_does_not_get_adjacency_promotion(
        self,
    ) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            '    """Initialize the accumulator before scanning."""\n'
            "    total = 0\n"
            "    for value in nums:\n"
            "        total += value\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_ordinary_comment_at_same_row_still_gets_adjacency_promotion(
        self,
    ) -> None:
        """Confirms the contrast case: real comments keep the promotion."""
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    # Initialize the accumulator before scanning.\n"
            "    total = 0\n"
            "    for value in nums:\n"
            "        total += value\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=1)

    def test_nested_helper_docstring_after_first_code_counts_as_post(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    total = 0\n"
            "    def helper(value: int) -> int:\n"
            '        """Add one value to the running total safely."""\n'
            "        return value\n"
            "    for value in nums:\n"
            "        total += helper(value)\n"
            "    return total\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=1)

    @pytest.mark.parametrize(
        "docstring_body",
        ["TODO", "fill here", "x", "placeholder"],
    )
    def test_placeholder_docstring_lines_are_rejected(
        self, docstring_body: str
    ) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            f'    """{docstring_body}"""\n'
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=0, post_code=0)

    def test_identical_comment_and_docstring_text_counts_once(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            '    """Return the sum of every value."""\n'
            "    # Return the sum of every value.\n"
            "    # An empty list returns zero.\n"
            "    # Use a running total.\n"
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)

    def test_docstring_lines_before_the_thinking_gate_count_pre(self) -> None:
        text = (
            "def solve(nums: list[int]) -> int:\n"
            '    """Return the sum of every value.\n'
            "\n"
            "    An empty list returns zero.\n"
            "    Use a running total.\n"
            '    """\n'
            f"    {LOCK_SENTINEL}\n"
            "    raise NotImplementedError\n"
        )

        assert self.evidence(text) == CommentEvidence(pre_code=3, post_code=0)
