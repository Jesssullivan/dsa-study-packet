"""Generate a challenge progress page for mkdocs.

Reads .challenges/progress.md and the full list of core-42 problems,
then renders a checklist page showing completed vs remaining problems.

Run automatically by mkdocs-gen-files during `mkdocs build`.
"""

from __future__ import annotations

import re
from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = ROOT / ".challenges" / "progress.md"

# The core 42, grouped by topic (matches challenges/index.md)
CORE_42: dict[str, list[str]] = {
    "arrays": ["two_sum", "group_anagrams", "product_except_self"],
    "two_pointers": ["three_sum", "trapping_rain_water"],
    "sliding_window": ["min_window_substring", "longest_substring_no_repeat"],
    "stacks_queues": ["valid_parentheses", "daily_temperatures"],
    "searching": ["binary_search", "search_rotated_array"],
    "linked_lists": ["reverse_linked_list", "lru_cache"],
    "trees": ["validate_bst", "level_order_traversal", "trie"],
    "graphs": [
        "number_of_islands",
        "topological_sort",
        "course_schedule",
        "dijkstra",
        "a_star_search",
        "bellman_ford",
        "minimum_spanning_tree",
    ],
    "dp": [
        "coin_change",
        "edit_distance",
        "knapsack",
        "longest_increasing_subseq",
        "longest_common_subseq",
    ],
    "heaps": ["kth_largest", "merge_k_sorted_lists"],
    "backtracking": ["subsets", "combination_sum", "n_queens"],
    "greedy": ["merge_intervals", "jump_game"],
    "strings": ["valid_palindrome", "longest_palindromic_substring"],
    "recursion": ["generate_parentheses", "flatten_nested_list"],
    "bit_manipulation": ["single_number"],
    "sorting": ["quickselect"],
}


def _parse_progress() -> dict[str, str]:
    """Parse .challenges/progress.md into {topic/problem: date} map."""
    completed: dict[str, str] = {}
    if not PROGRESS_FILE.exists():
        return completed
    for line in PROGRESS_FILE.read_text().splitlines():
        m = re.match(r"- \[x\] (\S+/\S+)\s*—?\s*(.*)", line)
        if m:
            completed[m.group(1)] = m.group(2).strip()
    return completed


def _title(name: str) -> str:
    return name.replace("_", " ").title()


def _topic_title(topic: str) -> str:
    special = {"dp": "Dynamic Programming", "stacks_queues": "Stacks & Queues"}
    return special.get(topic, _title(topic))


def main() -> None:
    completed = _parse_progress()
    total = sum(len(ps) for ps in CORE_42.values())
    done = sum(1 for t, ps in CORE_42.items() for p in ps if f"{t}/{p}" in completed)

    lines = [
        "---",
        "title: Challenge Progress",
        "---",
        "",
        "# Challenge Progress",
        "",
        f"**{done} / {total}** core problems completed.",
        "",
    ]

    if total > 0:
        pct = int(done / total * 100)
        bar_filled = pct // 5
        bar_empty = 20 - bar_filled
        lines.append(f'`{"█" * bar_filled}{"░" * bar_empty}` {pct}%')
        lines.append("")

    lines.append("---")
    lines.append("")

    for topic in CORE_42:
        problems = CORE_42[topic]
        topic_done = sum(1 for p in problems if f"{topic}/{p}" in completed)
        lines.append(f"### {_topic_title(topic)} ({topic_done}/{len(problems)})")
        lines.append("")
        for problem in problems:
            key = f"{topic}/{problem}"
            if key in completed:
                date = completed[key]
                date_str = f" — {date}" if date else ""
                lines.append(f"- [x] {_title(problem)}{date_str}")
            else:
                lines.append(f"- [ ] {_title(problem)}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("```bash")
    lines.append("just challenge-progress  # CLI view")
    lines.append("just challenge-reset     # clear all progress")
    lines.append("```")
    lines.append("")

    with mkdocs_gen_files.open("challenges/progress.md", "w") as f:
        f.write("\n".join(lines))


main()
