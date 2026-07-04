# dsa-study-packet — algorithm practice
set dotenv-load := false

default:
    @just --list

# ──────────────────────────────────────────────
# Testing
# ──────────────────────────────────────────────

# Run all tests
test *args:
    uv run pytest {{ args }}

# Run tests for a specific topic
practice topic:
    uv run pytest tests/{{ topic }}/ -v

# Run tests in watch mode (re-runs on file change)
test-watch *args:
    watchexec -e py -- uv run pytest {{ args }}

# Study a topic: run tests in watch mode for a specific topic
study topic:
    watchexec -e py -w src/algo/{{ topic }} -w tests/{{ topic }} -- uv run pytest tests/{{ topic }}/ -v

# Run concept module tests (installs optional deps)
test-concepts *args:
    uv run --extra concepts pytest tests/concepts/ -v {{ args }}

# Study a concept: run concept tests in watch mode
study-concept:
    watchexec -e py -w src/concepts -w tests/concepts -- uv run --extra concepts pytest tests/concepts/ -v

# Run benchmark suite
bench *args:
    uv run pytest -m bench --benchmark-enable --benchmark-sort=fullname {{ args }}

# Run tests with coverage (statement + branch) over the algo + concept sources
cov *args:
    uv run pytest --cov=src/algo --cov=src/concepts --cov-branch --cov-report=term-missing {{ args }}

# ──────────────────────────────────────────────
# Code quality
# ──────────────────────────────────────────────

# Run ruff linter + mypy type checker + repo guards
lint:
    uv run ruff check src/ tests/ scripts/
    uv run mypy
    uv run python scripts/check_public_boundary.py
    uv run python scripts/check_no_stubs.py
    uv run python scripts/validate_appendix_schema.py

# Check that private prep material has not entered the public packet tree
public-boundary:
    uv run python scripts/check_public_boundary.py

# Format code with ruff
fmt:
    uv run ruff format src/ tests/
    uv run ruff check --fix src/ tests/

# Check formatting without modifying files
fmt-check:
    uv run ruff format --check src/ tests/

# ──────────────────────────────────────────────
# Scaffolding
# ──────────────────────────────────────────────

# Scaffold a new problem: just new <topic> <problem_name>
new topic problem:
    #!/usr/bin/env bash
    set -euo pipefail

    src_dir="src/algo/{{ topic }}"
    test_dir="tests/{{ topic }}"
    src_file="${src_dir}/{{ problem }}.py"
    test_file="${test_dir}/test_{{ problem }}.py"

    mkdir -p "$src_dir" "$test_dir"

    # Ensure __init__.py files exist
    touch "src/algo/__init__.py"
    [ -f "${src_dir}/__init__.py" ] || touch "${src_dir}/__init__.py"
    [ -f "tests/__init__.py" ] || touch "tests/__init__.py"
    [ -f "${test_dir}/__init__.py" ] || touch "${test_dir}/__init__.py"

    if [ -f "$src_file" ]; then
        echo "Already exists: $src_file"
        exit 1
    fi

    # Source file
    cat > "$src_file" << 'PYEOF'
    """{{ topic }} / {{ problem }}

    Problem:
        TODO: describe the problem

    Approach:
        TODO: describe your approach

    Complexity:
        Time:  O(?)
        Space: O(?)
    """


    def solve() -> None:
        raise NotImplementedError
    PYEOF
    # Remove leading whitespace from heredoc
    sed -i '' 's/^    //' "$src_file" 2>/dev/null || sed -i 's/^    //' "$src_file"

    # Test file
    cat > "$test_file" << 'PYEOF'
    """Tests for {{ topic }} / {{ problem }}."""

    from algo.{{ topic }}.{{ problem }} import solve


    class TestSolve:
        def test_placeholder(self) -> None:
            """TODO: replace with real tests."""
            assert True
    PYEOF
    sed -i '' 's/^    //' "$test_file" 2>/dev/null || sed -i 's/^    //' "$test_file"

    echo "Created:"
    echo "  $src_file"
    echo "  $test_file"

# ──────────────────────────────────────────────
# PDF generation
# ──────────────────────────────────────────────

# Convert a single reference sheet to PDF
pdf file:
    pandoc "{{ file }}" -o "{{ without_extension(file) }}.pdf" \
        --pdf-engine=tectonic \
        -V geometry:margin=0.75in \
        -V fontsize=10pt \
        -V colorlinks=true

# Convert all reference sheets to PDF
pdf-all:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p reference-sheets/pdf
    for f in reference-sheets/*.md; do
        name="$(basename "${f%.md}")"
        echo "Converting $f → reference-sheets/pdf/${name}.pdf"
        pandoc "$f" -o "reference-sheets/pdf/${name}.pdf" \
            --pdf-engine=tectonic \
            -V geometry:margin=0.75in \
            -V fontsize=10pt \
            -V colorlinks=true
    done
    echo "Done. PDFs in reference-sheets/pdf/"

# Generate printable PDF booklet (decision trees + 1 algo per page)
pdf-booklet:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Generating booklet.tex..."
    uv run python scripts/gen_booklet.py
    echo "Compiling booklet.pdf with tectonic..."
    tectonic booklet.tex
    mkdir -p docs/assets
    cp booklet.pdf docs/assets/booklet.pdf
    echo "Done -> booklet.pdf and docs/assets/booklet.pdf"

# Build the latest printable study packet from source code and notes
packet: pdf-booklet

# --------------------------------------------------
# GloriousFlywheel cache-first Bazel (sole entrypoint)
# --------------------------------------------------
# `import? "justfile.flywheel"` (added by `flywheel-frontdoor-kit --patch-justfile`)
# provides flywheel-doctor/verify/enroll/consumer-env + the gloriousflywheel-bazel
# wrapper recipes. The recipes below are the repo-local cache-first front door:
# they delegate to the wrapper when BAZEL_REMOTE_CACHE is attached and degrade to
# a local disk_cache build otherwise. Never call raw bazel -- always `just remote-*`.

# Cache-first compile of a target set (default //:booklet, the neutral packet).
remote-compile *targets:
    #!/usr/bin/env bash
    set -euo pipefail
    set -a; [ -f .env.flywheel.local ] && . ./.env.flywheel.local; set +a
    targets="{{ targets }}"; [ -n "$targets" ] || targets="//:booklet"
    if [ -n "${BAZEL_REMOTE_CACHE:-}" ]; then
        exec just flywheel-build $targets
    fi
    echo "compatibility-local-only (BAZEL_REMOTE_CACHE unset) -> local disk_cache build: $targets"
    exec "${BAZEL_BIN:-bazelisk}" build $targets

# Cache-first build (default //:booklet); thin alias over remote-compile.
remote-build *targets:
    @just remote-compile {{ targets }}

# Cache-first bazel test (default //...). `just test` runs the real uv/pytest suite.
remote-test *targets:
    #!/usr/bin/env bash
    set -euo pipefail
    set -a; [ -f .env.flywheel.local ] && . ./.env.flywheel.local; set +a
    targets="{{ targets }}"; [ -n "$targets" ] || targets="//..."
    if [ -n "${BAZEL_REMOTE_CACHE:-}" ]; then
        exec just flywheel-test $targets
    fi
    echo "compatibility-local-only (BAZEL_REMOTE_CACHE unset) -> local bazel test: $targets"
    exec "${BAZEL_BIN:-bazelisk}" test $targets

# GloriousFlywheel attachment/contract gate (no build). Exits 0 when unattached.
remote-check:
    #!/usr/bin/env bash
    set -euo pipefail
    set -a; [ -f .env.flywheel.local ] && . ./.env.flywheel.local; set +a
    if [ -z "${BAZEL_REMOTE_CACHE:-}" ]; then
        echo "compatibility-local-only: BAZEL_REMOTE_CACHE unset; nothing to verify (ok)."
        exit 0
    fi
    just flywheel-doctor
    just flywheel-verify

# Build the overlay-pattern demo (examples/overlay-demo) -> wrapped PDF
# Cache-first via remote-build (no raw bazel); booklet.tex is regenerated first.
overlay-demo:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Generating booklet.tex..."
    uv run python scripts/gen_booklet.py
    echo "Composing overlay demo via the cache-first front door..."
    just remote-build //examples/overlay-demo:study_packet_example
    echo "-> bazel-bin/examples/overlay-demo/study_packet_example.pdf"

# ──────────────────────────────────────────────
# Documentation (MkDocs)
# ──────────────────────────────────────────────

# Generate algorithm-visualizer traces (SSOT frame data)
traces:
    uv run python scripts/gen_traces.py

# Serve docs locally with live reload
docs: traces
    uv run --extra docs mkdocs serve

# Build docs site
docs-build: traces
    uv run --extra docs mkdocs build

# ──────────────────────────────────────────────
# Challenge mode
# ──────────────────────────────────────────────

# Start a challenge: strips solution, shows failing tests
challenge topic problem:
    #!/usr/bin/env bash
    set -euo pipefail
    src="src/algo/{{ topic }}/{{ problem }}.py"
    backup=".challenges/{{ topic }}/{{ problem }}.py.solution"
    if [ ! -f "$src" ]; then echo "Error: $src not found"; exit 1; fi
    mkdir -p ".challenges/{{ topic }}"
    if [ ! -f "$backup" ]; then cp "$src" "$backup"; fi
    uv run python scripts/strip_solution.py "$src"
    echo "Challenge: $src — implement the functions to make tests pass"
    echo "  Run:  just study {{ topic }}"
    echo "  Peek: just solution {{ topic }} {{ problem }}"
    uv run pytest "tests/{{ topic }}/test_{{ problem }}.py" -v 2>&1 | tail -20 || true

# Restore the full solution
solution topic problem:
    #!/usr/bin/env bash
    set -euo pipefail
    backup=".challenges/{{ topic }}/{{ problem }}.py.solution"
    if [ ! -f "$backup" ]; then echo "No backup for {{ topic }}/{{ problem }}"; exit 1; fi
    cp "$backup" "src/algo/{{ topic }}/{{ problem }}.py"
    echo "Solution restored: src/algo/{{ topic }}/{{ problem }}.py"

# Mark a challenge as completed
challenge-done topic problem:
    #!/usr/bin/env bash
    set -euo pipefail
    progress=".challenges/progress.md"
    touch "$progress"
    entry="- [x] {{ topic }}/{{ problem }} — $(date +%Y-%m-%d)"
    if ! grep -q "{{ topic }}/{{ problem }}" "$progress" 2>/dev/null; then
        echo "$entry" >> "$progress"
    else
        sed -i '' "s|.*{{ topic }}/{{ problem }}.*|$entry|" "$progress"
    fi
    echo "Marked complete: {{ topic }}/{{ problem }}"

# Show challenge progress
challenge-progress:
    @cat .challenges/progress.md 2>/dev/null || echo "No challenges completed yet."

# Spaced-repetition: show the next problems due for drilling (default 5)
study-spaced n="5":
    @uv run python scripts/study_schedule.py {{ n }}

# Reset challenge progress (clear all completions)
challenge-reset:
    rm -f .challenges/progress.md
    @echo "Progress cleared."

# Interview mode: cold problem — statement only (no Approach/Complexity), no auto-tests
interview topic problem:
    #!/usr/bin/env bash
    set -euo pipefail
    src="src/algo/{{ topic }}/{{ problem }}.py"
    backup=".challenges/{{ topic }}/{{ problem }}.py.solution"
    if [ ! -f "$src" ]; then echo "Error: $src not found"; exit 1; fi
    mkdir -p ".challenges/{{ topic }}"
    if [ ! -f "$backup" ]; then cp "$src" "$backup"; fi
    uv run python scripts/strip_solution.py --cold "$src" >/dev/null
    awk 'c<2 {print} /"""/ {c++}' "$src"
    echo "Interview (cold): CLARP at the board first, then implement in $src"
    echo "  Verify: just study {{ topic }}   Restore: just solution {{ topic }} {{ problem }}"
    echo "  Log:    just rep \"{{ topic }}/{{ problem }} C_ L_ A_ R_ P_ <one fix>\""

# Log one practice rep (appends to gitignored .challenges/reps.md)
rep line:
    @mkdir -p .challenges && echo "- $(date +%Y-%m-%d) {{ line }}" >> .challenges/reps.md && tail -1 .challenges/reps.md

import? "justfile.flywheel"
