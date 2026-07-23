"""Tests for the AGENTS.md persona fan-out generator and its drift guard."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from gen_agent_instructions import (  # type: ignore[import-not-found]
    AGENT_TOOLS,
    AGENTS,
    BEGIN_MARKER,
    END_MARKER,
    PROMPT_SPECS,
    PersonaMarkerError,
    extract_persona,
    generated_files,
    render_continue_prompt,
    render_copilot_instructions,
    render_interviewer_agent,
    render_start_prompt,
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
        rendered = render_copilot_instructions(persona)
        assert persona in rendered
        assert rendered.endswith("\n")

    def test_repo_wide_persona_is_scoped_to_practice(self) -> None:
        rendered = render_copilot_instructions(extract_persona(AGENTS.read_text()))
        assert "For repository maintenance" in " ".join(rendered.split())

    def test_agent_file_is_thin_adapter_without_direct_edit_tools(self) -> None:
        rendered = render_interviewer_agent()
        assert rendered.startswith("---\nname: Interviewer\n")
        assert "target: vscode\n" in rendered
        assert "`AGENTS.md`" in rendered
        assert "practice-start" in rendered
        assert "practice-finish" in rendered
        assert "just catalog" in rendered
        assert "START" in rendered
        assert "QUEUE" in rendered
        assert "MATCH" in rendered
        assert "CHOOSE" in rendered
        assert "NOT_FOUND" in rendered
        assert "SUGGEST" in rendered
        assert "edit/editFiles" not in rendered
        assert "not a security boundary" in rendered
        assert rendered.endswith("\n")
        for tool in AGENT_TOOLS:
            assert f"  - {tool}\n" in rendered

    def test_start_prompt_is_one_command_and_candidate_preserving(self) -> None:
        rendered = render_start_prompt("reacto", "Start a REACTO editor rep")
        assert "just practice-start reacto" in rendered
        assert "just catalog" in rendered
        assert "`READY`" in rendered
        assert "`START: topic/problem`" in rendered
        assert "just practice-start reacto topic problem" in rendered
        assert "`QUEUE`" in rendered
        assert "`CHOOSE`" in rendered
        assert "`NOT_FOUND`" in rendered
        assert "`SUGGEST`" in rendered
        assert "practice-finish" in rendered
        assert "tree-search" in rendered
        assert "editor-open" in rendered
        assert "`SOURCE:`" in rendered
        assert "`TEST:`" in rendered
        assert "Never edit candidate files" in rendered

    def test_continue_prompt_delegates_state_to_one_command(self) -> None:
        rendered = render_continue_prompt()
        assert "just practice-next" in rendered
        assert "practice-status" not in rendered
        assert "practice-current" not in rendered

    def test_start_prompts_fit_the_low_power_budget(self) -> None:
        for name, description in PROMPT_SPECS.items():
            rendered = render_start_prompt(name, description)
            assert len(rendered.split()) <= 90


class TestGeneratedFiles:
    def test_deterministic_and_targets_expected_paths(self) -> None:
        first, second = generated_files(), generated_files()
        assert first == second
        assert {path.name for path in first} == {
            "clarp.prompt.md",
            "comments.prompt.md",
            "continue.prompt.md",
            "copilot-instructions.md",
            "interviewer.agent.md",
            "reacto.prompt.md",
            "umpire.prompt.md",
        }

    def test_committed_files_match_ssot(self) -> None:
        # The same invariant the CI drift guard enforces: a failure here means
        # AGENTS.md changed without `just gen-agents` being re-run.
        for path, expected in generated_files().items():
            assert path.read_text() == expected, f"{path.name}: run just gen-agents"
