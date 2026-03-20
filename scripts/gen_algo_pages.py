"""Auto-generate algorithm documentation pages for mkdocs.

Reads all algorithm source files under src/algo/{topic}/{problem}.py,
parses their module docstrings, and generates:

- docs/algorithms/{topic}/{problem}.md  — per-problem pages
- docs/algorithms/{topic}/index.md      — per-topic index tables
- docs/algorithms/index.md              — top-level grid of all topics
- docs/SUMMARY.md                       — literate-nav sidebar

Run automatically by mkdocs-gen-files during `mkdocs build`.
"""

from __future__ import annotations

import re
from pathlib import Path

import mkdocs_gen_files

# ── Paths ────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
ALGO_SRC = ROOT / "src" / "algo"
CONCEPTS_SRC = ROOT / "src" / "concepts"
PRACTICE_SRC = ROOT / "src" / "practice"
REFERENCE_DIR = ROOT / "reference-sheets"
TESTS_DIR = ROOT / "tests"

# ── Mermaid diagrams for key algorithms ──────────────────────────────

MERMAID_DIAGRAMS: dict[str, str] = {
    "binary_search": """\
```mermaid
flowchart TD
    A["lo = 0, hi = n - 1"] --> B{"lo <= hi?"}
    B -- No --> C["return -1<br/>(not found)"]
    B -- Yes --> D["mid = lo + (hi - lo) // 2"]
    D --> E{"nums[mid] == target?"}
    E -- Yes --> F["return mid"]
    E -- No --> G{"nums[mid] < target?"}
    G -- Yes --> H["lo = mid + 1<br/>(search right half)"]
    G -- No --> I["hi = mid - 1<br/>(search left half)"]
    H --> B
    I --> B

    style A fill:#7c3aed,color:#fff
    style F fill:#059669,color:#fff
    style C fill:#dc2626,color:#fff
```""",
    "dijkstra": """\
```mermaid
flowchart TD
    A["Initialize dist[source] = 0<br/>dist[all others] = inf"] --> B["Push (0, source)<br/>to min-heap"]
    B --> C{"Heap empty?"}
    C -- Yes --> D["Return dist array"]
    C -- No --> E["Pop (d, u) with<br/>smallest distance"]
    E --> F{"d > dist[u]?<br/>(stale entry)"}
    F -- Yes --> C
    F -- No --> G["For each neighbor v<br/>of u with weight w"]
    G --> H{"d + w < dist[v]?"}
    H -- Yes --> I["dist[v] = d + w<br/>Push (d+w, v) to heap"]
    H -- No --> J["Skip — no improvement"]
    I --> G
    J --> G
    G -- "All neighbors<br/>processed" --> C

    style A fill:#7c3aed,color:#fff
    style D fill:#059669,color:#fff
    style F fill:#f59e0b,color:#000
```""",
    "topological_sort": """\
```mermaid
flowchart TD
    A["Build adjacency list<br/>Compute in-degree for each node"] --> B["Enqueue all nodes<br/>with in-degree 0"]
    B --> C{"Queue empty?"}
    C -- Yes --> D{"len(order) == V?"}
    D -- Yes --> E["Return order<br/>(valid topological sort)"]
    D -- No --> F["Return [] — cycle detected"]
    C -- No --> G["Dequeue node u<br/>Append u to order"]
    G --> H["For each neighbor v of u:<br/>in-degree[v] -= 1"]
    H --> I{"in-degree[v] == 0?"}
    I -- Yes --> J["Enqueue v"]
    I -- No --> K["Continue"]
    J --> C
    K --> C

    style A fill:#7c3aed,color:#fff
    style E fill:#059669,color:#fff
    style F fill:#dc2626,color:#fff
```""",
}

# ── Docstring parser ─────────────────────────────────────────────────

_SECTION_RE = re.compile(
    r"^(Problem|Approach|When to use|Complexity):\s*$",
    re.MULTILINE,
)


def _parse_docstring(source: str) -> dict[str, str]:
    """Extract structured sections from a module docstring.

    Returns a dict with keys: title, problem, approach, when_to_use,
    time, space.  Missing sections get empty-string values.
    """
    result: dict[str, str] = {
        "title": "",
        "problem": "",
        "approach": "",
        "when_to_use": "",
        "time": "",
        "space": "",
    }

    # Extract the module docstring (triple-quoted block at the top)
    m = re.match(r'^"""(.*?)"""', source, re.DOTALL)
    if not m:
        m = re.match(r"^'''(.*?)'''", source, re.DOTALL)
    if not m:
        return result

    docstring = m.group(1)

    # Title is the first line
    lines = docstring.strip().splitlines()
    if lines:
        result["title"] = lines[0].rstrip(".")

    # Split into sections using the header pattern
    section_headers = list(_SECTION_RE.finditer(docstring))
    sections: dict[str, str] = {}
    for i, match in enumerate(section_headers):
        name = match.group(1)
        start = match.end()
        end = section_headers[i + 1].start() if i + 1 < len(section_headers) else len(docstring)
        body = docstring[start:end].strip()
        # Dedent: remove leading 4-space indent from continuation lines
        dedented = "\n".join(
            line[4:] if line.startswith("    ") else line
            for line in body.splitlines()
        )
        sections[name] = dedented.strip()

    result["problem"] = sections.get("Problem", "")
    result["approach"] = sections.get("Approach", "")
    result["when_to_use"] = sections.get("When to use", "")

    # Parse complexity into time/space
    complexity = sections.get("Complexity", "")
    for line in complexity.splitlines():
        line = line.strip()
        if line.lower().startswith("time:"):
            result["time"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("space:"):
            result["space"] = line.split(":", 1)[1].strip()

    return result


def _title_from_filename(filename: str) -> str:
    """Convert a snake_case filename to Title Case.

    >>> _title_from_filename("two_sum")
    'Two Sum'
    >>> _title_from_filename("lru_cache")
    'Lru Cache'
    """
    return filename.replace("_", " ").title()


def _topic_title(topic: str) -> str:
    """Convert topic dir name to display title.

    >>> _topic_title("stacks_queues")
    'Stacks & Queues'
    >>> _topic_title("dp")
    'Dynamic Programming'
    """
    special = {
        "dp": "Dynamic Programming",
        "stacks_queues": "Stacks & Queues",
        "linked_lists": "Linked Lists",
        "bit_manipulation": "Bit Manipulation",
        "sliding_window": "Sliding Window",
        "two_pointers": "Two Pointers",
    }
    if topic in special:
        return special[topic]
    return topic.replace("_", " ").title()


# ── Page generators ──────────────────────────────────────────────────


def _gen_problem_page(
    topic: str,
    problem: str,
    source: str,
) -> str:
    """Generate the markdown content for a single problem page."""
    info = _parse_docstring(source)
    name = _title_from_filename(problem)

    lines: list[str] = [
        "---",
        f"title: {name}",
        "---",
        "",
        f"# {name}",
        "",
    ]

    if info["problem"]:
        lines += ["## Problem", "", info["problem"], ""]

    if info["approach"]:
        lines += ["## Approach", "", info["approach"], ""]

    # Insert mermaid diagram if one exists for this algorithm
    if problem in MERMAID_DIAGRAMS:
        lines += ["### Algorithm Flow", "", MERMAID_DIAGRAMS[problem], ""]

    if info["when_to_use"]:
        lines += ["## When to Use", "", info["when_to_use"], ""]

    if info["time"] or info["space"]:
        lines += [
            "## Complexity",
            "",
            "| | |",
            "|---|---|",
            f'| **Time** | `{info["time"]}` |',
            f'| **Space** | `{info["space"]}` |',
            "",
        ]

    # Implementation tabs
    test_path = f"tests/{topic}/test_{problem}.py"
    test_file = TESTS_DIR / topic / f"test_{problem}.py"
    has_tests = test_file.exists()

    lines += [
        "## Implementation",
        "",
        '=== "Solution"',
        "",
        f"    ::: algo.{topic}.{problem}",
        "        options:",
        "          show_source: true",
        "",
    ]

    if has_tests:
        lines += [
            '=== "Tests"',
            "",
            f'    ```python title="{test_path}"',
            f'    --8<-- "{test_path}"',
            "    ```",
            "",
        ]

    lines += [
        '=== "Challenge"',
        "",
        '    !!! question "Implement it yourself"',
        "",
        f"        **Run:** `just challenge {topic} {problem}`",
        "",
        f"        Then implement the functions to make all tests pass.",
        f"        Use `just study {topic}` for watch mode.",
        "",
        '    ??? success "Reveal Solution"',
        "",
        f"        ::: algo.{topic}.{problem}",
        "            options:",
        "              show_source: true",
        "",
    ]

    return "\n".join(lines)


def _gen_topic_index(
    topic: str,
    problems: list[tuple[str, dict[str, str]]],
) -> str:
    """Generate the index page for a topic."""
    title = _topic_title(topic)
    lines = [
        "---",
        f"title: {title}",
        "---",
        "",
        f"# {title}",
        "",
        "| Problem | Complexity | Key Pattern |",
        "|---------|-----------|-------------|",
    ]

    for problem, info in sorted(problems, key=lambda x: x[0]):
        name = _title_from_filename(problem)
        time = info["time"] if info["time"] else "---"
        # First line of "when to use" as key pattern
        when = info["when_to_use"].splitlines()[0] if info["when_to_use"] else "---"
        # Truncate long patterns
        if len(when) > 80:
            when = when[:77] + "..."
        lines.append(f"| [{name}]({problem}.md) | `{time}` | {when} |")

    lines.append("")
    return "\n".join(lines)


def _gen_algorithms_index(
    topics: dict[str, list[tuple[str, dict[str, str]]]],
) -> str:
    """Generate the top-level algorithms overview page."""
    total_problems = sum(len(probs) for probs in topics.values())
    lines = [
        "---",
        "title: Algorithms",
        "---",
        "",
        "# Algorithms",
        "",
        f"> **{total_problems} implementations** across **{len(topics)} topics**",
        "",
        "| Topic | Problems | Key Algorithms |",
        "|-------|----------|---------------|",
    ]

    for topic in sorted(topics):
        title = _topic_title(topic)
        probs = topics[topic]
        count = len(probs)
        # Show up to 3 problem names as highlights
        highlights = ", ".join(
            _title_from_filename(p) for p, _ in sorted(probs)[:3]
        )
        if count > 3:
            highlights += ", ..."
        lines.append(
            f"| [{title}]({topic}/index.md) | {count} | {highlights} |"
        )

    lines.append("")
    return "\n".join(lines)


def _gen_summary(
    topics: dict[str, list[tuple[str, dict[str, str]]]],
) -> str:
    """Generate the SUMMARY.md for literate-nav."""
    lines = [
        "* [Home](index.md)",
        "* Algorithms",
        "    * [Overview](algorithms/index.md)",
    ]

    for topic in sorted(topics):
        title = _topic_title(topic)
        lines.append(f"    * {title}")
        lines.append(f"        * [Overview](algorithms/{topic}/index.md)")
        for problem, _ in sorted(topics[topic], key=lambda x: x[0]):
            name = _title_from_filename(problem)
            lines.append(f"        * [{name}](algorithms/{topic}/{problem}.md)")

    # Concepts section
    lines.append("* Concepts")
    lines.append("    * [Overview](concepts/index.md)")
    concept_files = sorted(CONCEPTS_SRC.glob("*.py"))
    for f in concept_files:
        if f.name == "__init__.py":
            continue
        name = _title_from_filename(f.stem)
        slug = f.stem.replace("_", "-")
        lines.append(f"    * [{name}](concepts/{slug}.md)")

    # Reference section — link to docs/reference/ wrapper pages (not source sheets)
    lines.append("* Reference")
    lines.append("    * [Overview](reference/index.md)")
    ref_docs = sorted(Path("docs/reference").glob("*.md"))
    for f in ref_docs:
        if f.name == "index.md":
            continue
        name = f.stem.split("-", 1)[-1].replace("-", " ").title() if "-" in f.stem else f.stem
        lines.append(f"    * [{name}](reference/{f.name})")

    # Practice and Challenges
    lines.append("* [Practice](practice/index.md)")
    lines.append("* Challenges")
    lines.append("    * [Daily Drill](challenges/index.md)")
    lines.append("    * [Progress](challenges/progress.md)")

    # Guide
    lines.append("* Guide")
    lines.append("    * [When to Use What](guide/when-to-use-what.md)")

    lines.append("")
    return "\n".join(lines)


# ── Main entry point ─────────────────────────────────────────────────


def main() -> None:
    """Scan algo source tree and write generated pages."""
    # Collect all topics and their problems
    topics: dict[str, list[tuple[str, dict[str, str]]]] = {}

    topic_dirs = sorted(
        d for d in ALGO_SRC.iterdir()
        if d.is_dir() and d.name != "__pycache__"
    )

    for topic_dir in topic_dirs:
        topic = topic_dir.name
        problems: list[tuple[str, dict[str, str]]] = []

        source_files = sorted(topic_dir.glob("*.py"))
        for src_file in source_files:
            if src_file.name == "__init__.py":
                continue

            problem = src_file.stem
            source = src_file.read_text()
            info = _parse_docstring(source)

            # Generate per-problem page
            page_content = _gen_problem_page(topic, problem, source)
            page_path = f"algorithms/{topic}/{problem}.md"
            with mkdocs_gen_files.open(page_path, "w") as f:
                f.write(page_content)

            problems.append((problem, info))

        if problems:
            topics[topic] = problems

            # Generate topic index
            topic_index = _gen_topic_index(topic, problems)
            with mkdocs_gen_files.open(f"algorithms/{topic}/index.md", "w") as f:
                f.write(topic_index)

    # Generate top-level algorithms index
    algo_index = _gen_algorithms_index(topics)
    with mkdocs_gen_files.open("algorithms/index.md", "w") as f:
        f.write(algo_index)

    # Generate SUMMARY.md for literate-nav
    summary = _gen_summary(topics)
    with mkdocs_gen_files.open("SUMMARY.md", "w") as f:
        f.write(summary)


main()
