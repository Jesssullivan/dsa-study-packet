#!/usr/bin/env bash
# Optional terminal banner used by the container smoke check and explicit
# invocations. It is fast, offline, and has no side effects.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"

have() { command -v "$1" >/dev/null 2>&1 && echo "ok" || echo "--"; }

echo ""
echo "The DSA Woodshed: practice technical interviews like an instrument"
echo "======================================================="
echo ""
echo "  toolchain   uv [$(have uv)]  just [$(have just)]  watchexec [$(have watchexec)]"
echo "  interviewer Copilot Chat [confirm sign-in and access in VS Code]"
echo ""
echo "  If Copilot Chat is available, select the Interviewer agent and choose a mode:"
echo ""
echo "      /reacto [topic problem]    comments -> code -> tests -> optimize"
echo "      /clarp  [topic problem]    clarify -> plan -> run -> polish"
echo "      /umpire [topic problem]    understand -> plan -> implement -> review"
echo "      /comments [topic problem]  plain thinking comments in the editor"
echo ""
echo "  The problem source and candidate-test file open together. Write ordinary"
echo "  source comments or docstrings in your own words, before and alongside code."
echo "  Write them in the file, not Chat. Save, then use /continue for one current"
echo "  state and next action. No prefixes, comment counts, or gate deletion."
echo ""
echo "  Drive the same loop without Chat:"
echo "      just practice-start reacto arrays two_sum"
echo "      just practice-next        # one current state and next action"
echo "      just practice-test        # exact problem + candidate tests"
echo "      just practice-watch       # rerun those tests on save"
echo "      just practice-repl        # load the candidate module interactively"
echo "      just practice-finish \"one fix\"  # log and schedule the next review"
echo ""
echo "  Method: reference-sheets/10 · Ramp: reference-sheets/11"
echo "  Preflight: just doctor · All commands: just --list"
echo ""
