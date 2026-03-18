"""Tests for PEP 750 template-string processors.

Each test class targets one processor from ``concepts.t_strings`` and
demonstrates the safety/correctness guarantees that t-strings provide
over plain f-strings.
"""

from hypothesis import given
from hypothesis import strategies as st

from concepts.t_strings import html_safe, render, sql_safe, structured_log

# --------------------------------------------------------------------------- #
# sql_safe
# --------------------------------------------------------------------------- #


class TestSqlSafe:
    """Parameterised-SQL generation from t-strings."""

    def test_basic_select(self) -> None:
        name = "alice"
        query, params = sql_safe(t"SELECT * FROM users WHERE name = {name}")
        assert query == "SELECT * FROM users WHERE name = ?"
        assert params == ("alice",)

    def test_injection_attempt_produces_placeholder(self) -> None:
        """The classic SQL-injection payload must NOT appear in the query."""
        evil = "'; DROP TABLE users; --"
        query, params = sql_safe(t"SELECT * FROM users WHERE name = {evil}")

        # The query text must contain a placeholder, NOT the payload.
        assert "DROP" not in query
        assert query == "SELECT * FROM users WHERE name = ?"
        # The dangerous string is safely in the params tuple.
        assert params == ("'; DROP TABLE users; --",)

    def test_multiple_params(self) -> None:
        uid = 7
        role = "admin"
        query, params = sql_safe(t"UPDATE users SET role = {role} WHERE id = {uid}")
        assert query == "UPDATE users SET role = ? WHERE id = ?"
        assert params == ("admin", 7)

    def test_no_interpolations(self) -> None:
        query, params = sql_safe(t"SELECT 1")
        assert query == "SELECT 1"
        assert params == ()


# --------------------------------------------------------------------------- #
# html_safe
# --------------------------------------------------------------------------- #


class TestHtmlSafe:
    """XSS-proof HTML rendering from t-strings."""

    def test_xss_script_tag_escaped(self) -> None:
        evil = "<script>alert('xss')</script>"
        result = html_safe(t"<div>{evil}</div>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_normal_text_passes_through(self) -> None:
        name = "Alice"
        result = html_safe(t"<p>Hello, {name}!</p>")
        assert result == "<p>Hello, Alice!</p>"

    def test_ampersand_escaped(self) -> None:
        text = "Tom & Jerry"
        result = html_safe(t"<span>{text}</span>")
        assert "&amp;" in result

    def test_static_html_not_escaped(self) -> None:
        """Static markup written by the developer is trusted."""
        val = "ok"
        result = html_safe(t"<b>{val}</b>")
        assert result.startswith("<b>")
        assert result.endswith("</b>")


# --------------------------------------------------------------------------- #
# structured_log
# --------------------------------------------------------------------------- #


class TestStructuredLog:
    """JSON-structured logging from t-strings."""

    def test_extracts_correct_keys_and_values(self) -> None:
        user = "alice"
        action = "login"
        result = structured_log(t"{user} performed {action}")
        assert result["user"] == "alice"
        assert result["action"] == "login"

    def test_message_key_is_rendered(self) -> None:
        user = "bob"
        code = 200
        result = structured_log(t"{user} got status {code}")
        assert result["_message"] == "bob got status 200"

    def test_numeric_values_preserved(self) -> None:
        latency_ms = 42.7
        result = structured_log(t"request took {latency_ms}ms")
        # The raw numeric value is stored, not a string.
        assert result["latency_ms"] == 42.7
        assert isinstance(result["latency_ms"], float)


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #


class TestRender:
    """General-purpose Template -> str rendering."""

    def test_basic_render(self) -> None:
        x = 42
        assert render(t"value = {x}") == "value = 42"

    def test_format_spec_applied(self) -> None:
        pi = 3.14159
        assert render(t"pi is {pi:.2f}") == "pi is 3.14"

    def test_conversion_s(self) -> None:
        x = 42
        assert render(t"{x!s}") == "42"

    def test_conversion_r(self) -> None:
        s = "hi"
        assert render(t"{s!r}") == "'hi'"

    def test_conversion_a(self) -> None:
        s = "\u00e9"  # e-with-acute
        result = render(t"{s!a}")
        assert result == r"'\xe9'"

    @given(text=st.text(min_size=0, max_size=100))
    def test_roundtrip_with_hypothesis(self, text: str) -> None:
        """render(t"...{x}...") should match f"...{x}..." for any string."""
        rendered = render(t"prefix-{text}-suffix")
        expected = f"prefix-{text}-suffix"
        assert rendered == expected
