#!/usr/bin/env bash
# Chooses and launches the resident interviewer. Runs as a VS Code task
# (runOn: folderOpen) so it owns a real interactive terminal —
# postAttachCommand is not a reliable host for an interactive REPL.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"

# .vscode/tasks.json fires this on every folderOpen — including a bare local
# clone opened without Dev Containers, where postCreateCommand never runs and
# the sentinel below is never written. Only wait for it inside a real
# container (Codespaces or local Dev Containers), where seeding is in flight.
in_container() {
	[ -f /.dockerenv ] || [ -f /run/.containerenv ] \
		|| [ -n "${CODESPACES:-}" ] || [ -n "${REMOTE_CONTAINERS:-}" ]
}

if in_container; then
	# Lifecycle ordering is not guaranteed (the folderOpen task can fire while
	# postCreate is still seeding auth) — wait for the seed sentinel, then
	# proceed regardless so a failed seed degrades to the no-key path instead
	# of hanging.
	for _ in $(seq 1 30); do
		[ -f "$HOME/.config/practice/seed-done" ] && break
		sleep 1
	done
fi

# 1) Claude Code — subscription OAuth token (no approval prompt) or API key.
#    Never set both secrets: the API key wins and bills the API account.
if command -v claude >/dev/null 2>&1 \
	&& { [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ] || [ -n "${ANTHROPIC_API_KEY:-}" ]; }; then
	echo "[interviewer] Claude Code starting. Say: Start my first practice rep."
	exec claude
fi

# 2) Codex — only when postCreate seeded auth.json (the OPENAI_API_KEY env var
#    alone does not log the TUI in; setup.sh runs the login for you).
if command -v codex >/dev/null 2>&1 && codex login status >/dev/null 2>&1; then
	echo "[interviewer] Codex starting. Say: Start my first practice rep."
	exec codex
fi

# 3) No key — Copilot Chat and the solo loop still work fully.
echo ""
echo "No interviewer credential found — that's fine:"
echo "  Copilot Chat (sidebar): pick the 'Interviewer' agent and say:"
echo "      Start my first practice rep."
echo "  Solo: just interview arrays two_sum    (method: reference-sheets/10)"
echo "  Preflight: just doctor"
echo ""
if in_container; then
	echo "Want Claude or Codex already running here next time? One-time setup"
	echo "lives in WELCOME.md (a Codespaces secret; takes two minutes)."
else
	echo "Want Claude or Codex already running here next time? Export"
	echo "CLAUDE_CODE_OAUTH_TOKEN / ANTHROPIC_API_KEY / OPENAI_API_KEY in your"
	echo "shell profile — see docs/guide/local-practice.md."
fi
echo ""
exec bash
