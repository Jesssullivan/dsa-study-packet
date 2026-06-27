"""The Core 42 problem set, grouped by topic.

Single source of truth shared by the progress-page generator and the
spaced-repetition scheduler (keeps the two from drifting).
"""

from __future__ import annotations

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
