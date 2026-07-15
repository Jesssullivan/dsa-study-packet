"""The Core 42 problem set, grouped by topic.

Single source of truth shared by the progress-page generator and the
spaced-repetition scheduler (keeps the two from drifting).
"""

from __future__ import annotations

CORE_42: dict[str, list[str]] = {
    "arrays": ["two_sum", "group_anagrams", "product_except_self", "top_k_frequent"],
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
    "math": ["sieve_of_eratosthenes"],
}

# One implementation target per catalog algorithm. Several modules intentionally
# contain alternate solutions, helper data structures, or conversion helpers.
# An editor rep redacts every implementation body. This target alone receives
# the reasoning scaffold and drives completion. Reference tests keep committed
# non-target bindings; helpers used by the target remain candidate-owned stubs.
PRACTICE_TARGETS: dict[tuple[str, str], str] = {
    ("arrays", "two_sum"): "two_sum",
    ("arrays", "group_anagrams"): "group_anagrams",
    ("arrays", "product_except_self"): "product_except_self",
    ("arrays", "top_k_frequent"): "top_k_frequent",
    ("two_pointers", "container_with_most_water"): "max_area",
    ("two_pointers", "three_sum"): "three_sum",
    ("two_pointers", "trapping_rain_water"): "trap",
    ("sliding_window", "min_window_substring"): "min_window",
    ("sliding_window", "longest_substring_no_repeat"): ("length_of_longest_substring"),
    ("stacks_queues", "min_stack"): "MinStack",
    ("stacks_queues", "valid_parentheses"): "is_valid",
    ("stacks_queues", "daily_temperatures"): "daily_temperatures",
    ("searching", "binary_search"): "binary_search",
    ("searching", "find_minimum_rotated"): "find_min",
    ("searching", "search_rotated_array"): "search_rotated",
    ("linked_lists", "merge_two_sorted"): "merge_two_sorted",
    ("linked_lists", "reverse_linked_list"): "reverse_iterative",
    ("linked_lists", "lru_cache"): "LRUCache",
    ("trees", "invert_tree"): "invert_tree",
    ("trees", "validate_bst"): "is_valid_bst",
    ("trees", "level_order_traversal"): "level_order",
    ("trees", "max_depth"): "max_depth",
    ("trees", "trie"): "Trie",
    ("graphs", "clone_graph"): "clone_graph",
    ("graphs", "number_of_islands"): "num_islands",
    ("graphs", "topological_sort"): "topological_sort_kahn",
    ("graphs", "course_schedule"): "can_finish",
    ("graphs", "dijkstra"): "dijkstra",
    ("graphs", "a_star_search"): "a_star",
    ("graphs", "bellman_ford"): "bellman_ford",
    ("graphs", "geohash_grid"): "encode",
    ("graphs", "kd_tree"): "KDTree",
    ("graphs", "minimum_spanning_tree"): "kruskal",
    ("graphs", "network_delay_time"): "network_delay_time",
    ("graphs", "network_flow"): "edmonds_karp",
    ("graphs", "word_ladder"): "ladder_length",
    ("dp", "climbing_stairs"): "climb_stairs",
    ("dp", "coin_change"): "coin_change",
    ("dp", "constraint_satisfaction"): "CSP",
    ("dp", "edit_distance"): "edit_distance",
    ("dp", "knapsack"): "knapsack",
    ("dp", "longest_increasing_subseq"): "length_of_lis",
    ("dp", "longest_common_subseq"): "longest_common_subsequence",
    ("dp", "traveling_salesman_dp"): "tsp",
    ("heaps", "kth_largest"): "find_kth_largest",
    ("heaps", "merge_k_sorted_lists"): "merge_k_sorted",
    ("heaps", "task_scheduler"): "least_interval",
    ("backtracking", "subsets"): "subsets",
    ("backtracking", "combination_sum"): "combination_sum",
    ("backtracking", "n_queens"): "solve_n_queens",
    ("backtracking", "permutations"): "permutations",
    ("greedy", "interval_scheduling"): "max_non_overlapping",
    ("greedy", "merge_intervals"): "merge_intervals",
    ("greedy", "jump_game"): "can_jump",
    ("strings", "longest_common_prefix"): "longest_common_prefix",
    ("strings", "valid_palindrome"): "is_palindrome",
    ("strings", "longest_palindromic_substring"): ("longest_palindromic_substring"),
    ("strings", "string_to_integer_atoi"): "my_atoi",
    ("strings", "valid_anagram"): "is_anagram",
    ("recursion", "generate_parentheses"): "generate_parentheses",
    ("recursion", "flatten_nested_list"): "flatten_recursive",
    ("recursion", "letter_combinations_phone"): "letter_combinations",
    ("recursion", "pow_x_n"): "my_pow",
    ("recursion", "tower_of_hanoi"): "tower_of_hanoi",
    ("bit_manipulation", "counting_bits"): "counting_bits",
    ("bit_manipulation", "reverse_bits"): "reverse_bits",
    ("bit_manipulation", "single_number"): "single_number",
    ("sorting", "merge_sort_inversions"): "count_inversions",
    ("sorting", "quickselect"): "quickselect",
    ("math", "sieve_of_eratosthenes"): "sieve_of_eratosthenes",
    ("patterns", "sliding_window"): "max_sum_subarray",
}


def _validate_practice_targets() -> None:
    expected = {
        (topic, problem) for topic, problems in CORE_42.items() for problem in problems
    }
    if not expected <= set(PRACTICE_TARGETS):
        missing = sorted(expected - set(PRACTICE_TARGETS))
        msg = f"PRACTICE_TARGETS lost Core entries (missing={missing})"
        raise RuntimeError(msg)


_validate_practice_targets()
