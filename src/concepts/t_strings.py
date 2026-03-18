"""PEP 750 Template Strings (t-strings) — Python 3.14's most impactful feature.

T-strings generalize f-strings: instead of eagerly producing a ``str``,
the ``t"..."`` prefix returns a ``Template`` object that *preserves*
both the static text fragments and the interpolated values.  This lets
library code decide **how** to combine them — enabling safe SQL, safe
HTML, structured logging, and arbitrary DSLs.

Key anatomy of a ``Template`` object
-------------------------------------
Given ``t"Hello {name}! You are {age} years old."``:

* ``template.strings``          -> ``('Hello ', '! You are ', ' years old.')``
* ``template.interpolations``   -> tuple of ``Interpolation`` objects
* ``template.values``           -> ``(name_value, age_value)``
* ``list(template)``            -> interleaved ``str`` / ``Interpolation``
                                   (empty boundary strings are *skipped*)

``Interpolation`` attributes
-----------------------------
* ``.value``       — the evaluated Python object
* ``.expression``  — the source-code text (e.g. ``'name'``)
* ``.conversion``  — ``'s'``, ``'r'``, ``'a'``, or ``None``
* ``.format_spec`` — e.g. ``'.2f'``; defaults to ``''``

References
----------
* PEP 750  — https://peps.python.org/pep-0750/
* CPython tracking issue — https://github.com/python/cpython/issues/132661
* Jim Baker's tutorial — https://github.com/davepeck/pep750-examples
"""

import html

# string.templatelib is the new stdlib module shipping with Python 3.14.
from string.templatelib import Interpolation, Template

# --------------------------------------------------------------------------- #
# Helper: apply !s / !r / !a conversion flags
# --------------------------------------------------------------------------- #


def _apply_conversion(value: object, conversion: str | None) -> object:
    """Apply the conversion flag from an ``Interpolation``.

    This mirrors what f-strings do internally:

    * ``!s`` -> ``str(value)``
    * ``!r`` -> ``repr(value)``
    * ``!a`` -> ``ascii(value)``
    * ``None`` -> leave the value as-is

    >>> _apply_conversion(42, "s")
    '42'
    >>> _apply_conversion("hello", "r")
    "'hello'"
    >>> _apply_conversion("hello", None)
    'hello'
    """
    if conversion == "s":
        return str(value)
    if conversion == "r":
        return repr(value)
    if conversion == "a":
        return ascii(value)
    return value


# --------------------------------------------------------------------------- #
# 1. sql_safe — parameterised SQL (prevents SQL injection)
# --------------------------------------------------------------------------- #


def sql_safe(template: Template) -> tuple[str, tuple[object, ...]]:
    """Convert a t-string into a parameterised SQL query.

    Every interpolation is replaced by a ``?`` placeholder, and the
    corresponding values are collected into a separate tuple.  This is
    exactly the interface that ``sqlite3.execute`` (and most DB-API 2.0
    drivers) expect.

    Why this matters: if you naively use an f-string to build SQL, a
    malicious user can supply ``'; DROP TABLE users; --`` as a value and
    your query becomes valid, destructive SQL.  With ``sql_safe``, the
    value is **never** interpolated into the query text.

    >>> user = "alice"
    >>> sql_safe(t"SELECT * FROM users WHERE name = {user}")
    ('SELECT * FROM users WHERE name = ?', ('alice',))

    >>> aid = 1
    ... val = "x"
    >>> sql_safe(t"UPDATE t SET col = {val} WHERE id = {aid}")
    ('UPDATE t SET col = ? WHERE id = ?', ('x', 1))
    """
    # We iterate over the template, which yields str fragments and
    # Interpolation objects in document order.
    query_parts: list[str] = []
    params: list[object] = []

    for item in template:
        match item:
            # Static SQL text — keep verbatim.
            case str() as fragment:
                query_parts.append(fragment)

            # Interpolated value — replace with placeholder, stash value.
            case Interpolation(value=value):
                query_parts.append("?")
                params.append(value)

    return ("".join(query_parts), tuple(params))


# --------------------------------------------------------------------------- #
# 2. html_safe — XSS-proof HTML rendering
# --------------------------------------------------------------------------- #


def html_safe(template: Template) -> str:
    """Render a t-string as HTML with all interpolations escaped.

    Static text passes through unchanged (it's trusted, author-written
    markup), but every interpolated value is run through
    ``html.escape()`` so that ``<script>`` tags, ``&``, ``"``, etc. are
    neutralised.

    >>> title = "<script>alert('xss')</script>"
    >>> html_safe(t"<h1>{title}</h1>")
    "<h1>&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;</h1>"

    >>> name = "Alice & Bob"
    >>> html_safe(t"<p>Hello, {name}!</p>")
    '<p>Hello, Alice &amp; Bob!</p>'
    """
    parts: list[str] = []

    for item in template:
        match item:
            # Trusted static HTML — keep as-is.
            case str() as fragment:
                parts.append(fragment)

            # User-supplied value — escape for HTML safety.
            case Interpolation(value=value, conversion=conversion, format_spec=spec):
                converted = _apply_conversion(value, conversion)
                formatted = format(converted, spec) if spec else str(converted)
                parts.append(html.escape(formatted))

    return "".join(parts)


# --------------------------------------------------------------------------- #
# 3. structured_log — extract names & values for JSON logging
# --------------------------------------------------------------------------- #


def structured_log(template: Template) -> dict[str, object]:
    """Extract interpolation expression names and values as a dict.

    This enables structured (JSON) logging where the log message can be
    reconstructed from the template while the individual fields are
    machine-searchable.

    The dict contains:
    * ``"_message"`` — the rendered human-readable string
    * one key per interpolation, named by its ``.expression``

    >>> user = "alice"
    ... action = "login"
    >>> result = structured_log(t"{user} performed {action}")
    >>> result["user"]
    'alice'
    >>> result["action"]
    'login'
    >>> result["_message"]
    'alice performed login'
    """
    log: dict[str, object] = {}
    message_parts: list[str] = []

    for item in template:
        match item:
            case str() as fragment:
                message_parts.append(fragment)

            case Interpolation(
                value=value, expression=expr, conversion=conv, format_spec=spec
            ):
                # Store the raw Python value under the expression name.
                log[expr] = value

                # Build the human-readable message part.
                converted = _apply_conversion(value, conv)
                formatted = format(converted, spec) if spec else str(converted)
                message_parts.append(formatted)

    log["_message"] = "".join(message_parts)
    return log


# --------------------------------------------------------------------------- #
# 4. render — general-purpose Template -> str
# --------------------------------------------------------------------------- #


def render(template: Template) -> str:
    """Render a ``Template`` to a plain string, honouring conversions and
    format specs — exactly like an f-string would.

    This is the "identity" processor: ``render(t"...")`` behaves the same
    as ``f"..."``.  It's useful as a reference implementation and as a
    building block for more complex processors.

    >>> x = 42
    >>> render(t"value = {x}")
    'value = 42'
    >>> pi = 3.14159
    >>> render(t"pi is {pi:.2f}")
    'pi is 3.14'
    >>> render(t"repr: {x!r}")
    'repr: 42'
    """
    parts: list[str] = []

    for item in template:
        match item:
            case str() as fragment:
                parts.append(fragment)

            case Interpolation(value=value, conversion=conversion, format_spec=spec):
                converted = _apply_conversion(value, conversion)
                # format() with an empty spec is equivalent to str().
                parts.append(format(converted, spec))

    return "".join(parts)
