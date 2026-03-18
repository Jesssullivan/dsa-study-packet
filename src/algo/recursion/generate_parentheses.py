"""Generate Parentheses — all valid combinations of n pairs.

Problem:
    Given n pairs of parentheses, generate all combinations of
    well-formed (balanced) parentheses.

Approach:
    Backtracking: maintain counts of open and close parens placed so far.
    Add '(' if open < n. Add ')' if close < open. Base case: length == 2*n.

When to use:
    Generating all valid structures (expressions, trees, paths). Classic
    backtracking with pruning. Output count follows Catalan numbers.

Complexity:
    Time:  O(4^n / sqrt(n)) — nth Catalan number
    Space: O(n) — recursion depth (excluding output)
"""


def generate_parentheses(n: int) -> list[str]:
    """Return all valid combinations of *n* pairs of parentheses.

    >>> generate_parentheses(1)
    ['()']
    >>> sorted(generate_parentheses(2))
    ['(())', '()()']
    """
    result: list[str] = []

    def backtrack(current: list[str], open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append("".join(current))
            return
        if open_count < n:
            current.append("(")
            backtrack(current, open_count + 1, close_count)
            current.pop()
        if close_count < open_count:
            current.append(")")
            backtrack(current, open_count, close_count + 1)
            current.pop()

    if n > 0:
        backtrack([], 0, 0)
    return result
