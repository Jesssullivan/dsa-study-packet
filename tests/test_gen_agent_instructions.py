"""Tests for the AGENTS.md persona fan-out generator and its drift guard."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from gen_agent_instructions import (  # type: ignore[import-not-found]
    BEGIN_MARKER,
    END_MARKER,
    PersonaMarkerError,
    extract_persona,
    generated_files,
    render_copilot_instructions,
    render_interviewer_agent,
)


def wrap(body: str) -> str:
    return f"preamble\n{BEGIN_MARKER}\n{body}\n{END_MARKER}\npostamble\n"


class TestExtractPersona:
    def test_happy_path_trims_surrounding_blanks_only(self) -> None:
        assert extract_persona(wrap("\n\nline one\n\n  line two\n\n")) == (
            "line one\n\n  line two"
        )

    def test_missing_markers(self) -> None:
        with pytest.raises(PersonaMarkerError):
            extract_persona("no markers here\n")

    def test_duplicated_begin_marker(self) -> None:
        with pytest.raises(PersonaMarkerError):
            extract_persona(wrap(f"body\n{BEGIN_MARKER}"))

    def test_reversed_markers(self) -> None:
        with pytest.raises(PersonaMarkerError):
            extract_persona(f"{END_MARKER}\nbody\n{BEGIN_MARKER}\n")

    def test_empty_region(self) -> None:
        with pytest.raises(PersonaMarkerError):
            extract_persona(wrap("\n \n"))


class TestRendering:
    def test_outputs_inline_persona_and_end_with_newline(self) -> None:
        persona = "persona body"
        for rendered in (
            render_copilot_instructions(persona),
            render_interviewer_agent(persona),
        ):
            assert persona in rendered
            assert rendered.endswith("\n")

    def test_agent_file_has_frontmatter(self) -> None:
        rendered = render_interviewer_agent("persona body")
        assert rendered.startswith("---\nname: Interviewer\n")


class TestGeneratedFiles:
    def test_deterministic_and_targets_expected_paths(self) -> None:
        first, second = generated_files(), generated_files()
        assert first == second
        rels = sorted(p.name for p in first)
        assert rels == ["copilot-instructions.md", "interviewer.agent.md"]

    def test_committed_files_match_ssot(self) -> None:
        # The same invariant the CI drift guard enforces: a failure here means
        # AGENTS.md changed without `just gen-agents` being re-run.
        for path, expected in generated_files().items():
            assert path.read_text() == expected, f"{path.name}: run just gen-agents"
