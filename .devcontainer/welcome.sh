#!/usr/bin/env bash
# postAttach banner — runs on every attach: fast, offline, no side effects.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"

have() { command -v "$1" >/dev/null 2>&1 && echo "ok" || echo "--"; }

echo ""
echo "The DSA Woodshed — practice technical interviews like an instrument"
echo "======================================================="
echo ""
echo "  toolchain   uv [$(have uv)]  just [$(have just)]  watchexec [$(have watchexec)]"
echo "  agents      copilot [built into Codespaces]  claude [$(have claude)]  codex [$(have codex)]"
echo ""
echo "  Start in one line — tell your agent (Copilot Chat sidebar, or"
echo "  'claude' / 'codex' in this terminal):"
echo ""
echo "      Start my first practice rep."
echo ""
echo "  Or drive it yourself:"
echo "      just interview arrays two_sum    # cold problem, solution stripped"
echo "      just interview-comment arrays two_sum   # think in comments, save-gated"
echo "      just study arrays                # tests in watch mode"
echo "      just solution arrays two_sum     # restore when done"
echo ""
echo "  Method: reference-sheets/10 · Ramp: reference-sheets/11"
echo "  Preflight: just doctor · Fresh slate: just challenge-reset · All: just --list"
if ! command -v claude >/dev/null 2>&1 || ! command -v codex >/dev/null 2>&1; then
	echo ""
	echo "  Optional richer interviewers:"
	command -v claude >/dev/null 2>&1 || echo "    claude:  set CLAUDE_CODE_OAUTH_TOKEN (Pro/Max, from 'claude setup-token') or ANTHROPIC_API_KEY secret, or run 'claude' (paste-code login)"
	command -v codex  >/dev/null 2>&1 || echo "    codex:   run 'codex login --device-auth' or set OPENAI_API_KEY secret"
fi
echo ""
