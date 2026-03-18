---
title: Concept Modules
---

# Concept Modules

Six production-level Python modules covering topics that surface in practical problem solving, system design, and code review rounds. Each module is heavily commented for self-study.

```bash
just test-concepts    # run concept module tests (installs numpy/scipy/flask/pydantic)
just study-concept    # watch mode
```

---

<div class="grid cards" markdown>

-   :material-code-string:{ .lg .middle } **T-Strings (PEP 750)**

    ---

    Lazy interpolation, safe SQL/HTML templating, structured logging with Python 3.14 template strings.

    [:octicons-arrow-right-24: t-strings](t-strings.md)

-   :material-language-python:{ .lg .middle } **Advanced Typing**

    ---

    Protocol, TypeVar, ParamSpec, TypeGuard, `@overload`, and the new PEP 695 `type` syntax.

    [:octicons-arrow-right-24: advanced-typing](advanced-typing.md)

-   :material-test-tube:{ .lg .middle } **Hypothesis Patterns**

    ---

    Property-based testing with `@given`, `@composite` strategies, stateful testing, and `SortedList`.

    [:octicons-arrow-right-24: hypothesis-patterns](hypothesis-patterns.md)

-   :material-sine-wave:{ .lg .middle } **FFT / DCT**

    ---

    Signal processing fundamentals: FFT, inverse FFT, DCT, frequency analysis. Relevant to ADS-B and weather radar.

    [:octicons-arrow-right-24: fft-dct](fft-dct.md)

-   :material-flask:{ .lg .middle } **Modern Flask**

    ---

    Flask 3.x patterns: async views, class-based views, nested blueprints, app factory, testing.

    [:octicons-arrow-right-24: modern-flask](modern-flask.md)

-   :material-shield-check:{ .lg .middle } **Validation (Pydantic v2)**

    ---

    Model validators, discriminated unions, serialization, and comparison with TypeScript's Zod.

    [:octicons-arrow-right-24: validation](validation.md)

</div>

---

## Concept-to-Algorithm Connections

| Module | Connects To | Why |
|--------|-------------|-----|
| t_strings | Template pattern | Parameterized queries in `sql_safe()`, analogous to DP building solutions from templates |
| advanced_typing | `Stack[T]` | Same LIFO structure used in `valid_parentheses.py` and `daily_temperatures.py` |
| hypothesis_patterns | `bisect` | Same binary search strategy as `longest_increasing_subseq.py` |
| fft_dct | Sensor data pipelines | Relevant when target employer asks about ADS-B signal processing or weather radar |
| modern_flask | API layer | Pairs with `validation.py` for full request lifecycle |
| validation | Runtime types | Runtime counterpart to `advanced_typing`'s static type system |
