"""Valid parentheses.

Problem:
    Given a string containing just the characters '(', ')', '{', '}',
    '[' and ']', determine if the input string is valid. A string is
    valid if every open bracket is closed by the same type of bracket
    in the correct order.

Approach:
    Use a stack. Push opening brackets; on a closing bracket, check
    that the stack top matches. The string is valid iff the stack is
    empty at the end.

When to use:
    Matching/nesting validation — balanced brackets, HTML tags, expression
    parsing. Any problem where openers must be closed in LIFO order.
    Keywords: "valid", "balanced", "nested", "well-formed".

Complexity:
    Time:  O(n) -- single pass
    Space: O(n) -- stack in worst case (all openers)
"""


def is_valid(s: str) -> bool:
    """Return True if *s* contains valid matched brackets.

    >>> is_valid("()[]{}")
    True
    >>> is_valid("(]")
    False
    >>> is_valid("([)]")
    False
    """
    stack: list[str] = []
    match = {")": "(", "]": "[", "}": "{"}

    for ch in s:
        if ch in match:
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)

    return not stack
