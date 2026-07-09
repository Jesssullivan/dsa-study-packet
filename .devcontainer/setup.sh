#!/usr/bin/env bash
# Devcontainer toolchain bootstrap for the practice loop.
#
# Deliberately independent of flake.nix: the Nix devshell stays the
# maintainer's local flow; containers get the four tools the practice loop
# actually needs (python via uv, just, watchexec) plus optional agent CLIs.
#
# Modes:
#   (none)   full bootstrap — pinned tool installs + dependency sync (onCreate)
#   --sync   dependency sync only (updateContentCommand)
#   --seed   seed per-user practice state (postCreateCommand)
set -euo pipefail

UV_VERSION="0.11.27"
JUST_VERSION="1.40.0"
WATCHEXEC_VERSION="2.3.2"

BIN_DIR="$HOME/.local/bin"
export PATH="$BIN_DIR:$PATH"
# The base image ships python3.11-minimal (no `json` module); uv must never
# probe it — always use uv-managed CPython. Mirrored in containerEnv.
export UV_PYTHON_PREFERENCE=only-managed
mkdir -p "$BIN_DIR"

log()  { echo "[setup] $*"; }
warn() { echo "[setup] WARN: $*" >&2; }

# --seed only runs automatically via postCreateCommand (Codespaces or local
# Dev Containers), where $HOME is the container's own throwaway home. Guard
# the global-config writes below in case someone runs this by hand on a bare
# host, where $HOME is the real machine and those writes would not be
# throwaway.
in_container() {
	[ -f /.dockerenv ] || [ -f /run/.containerenv ] \
		|| [ -n "${CODESPACES:-}" ] || [ -n "${REMOTE_CONTAINERS:-}" ]
}

sync_deps() {
	log "syncing python deps (uv fetches CPython to satisfy requires-python)"
	uv sync --extra dev
}

seed_state() {
	# Per-user, gitignored practice state — every Codespace user starts fresh.
	mkdir -p .challenges
	just catalog || warn "catalog preview failed (non-fatal)"

	if in_container; then
		# Codex TUI auth: the OPENAI_API_KEY env var alone does NOT log the TUI
		# in (it only reads ~/.codex/auth.json) — seed it here, where secrets
		# are reliably injected.
		if command -v codex >/dev/null 2>&1 && [ -n "${OPENAI_API_KEY:-}" ] \
			&& ! codex login status >/dev/null 2>&1; then
			codex login --with-api-key <<<"$OPENAI_API_KEY" \
				|| warn "codex login failed (optional — Copilot/Claude still work)"
		fi
		# Codex trust must live in the GLOBAL config — the repo-level
		# .codex/config.toml only loads after trust is granted. (auth.json
		# written above already pins API-key auth; no undocumented
		# auth-method key needed.)
		if command -v codex >/dev/null 2>&1 && [ ! -f "$HOME/.codex/config.toml" ]; then
			mkdir -p "$HOME/.codex"
			cat > "$HOME/.codex/config.toml" <<-EOF
				approval_policy = "never"
				sandbox_mode = "workspace-write"

				[projects."$PWD"]
				trust_level = "trusted"
			EOF
		fi

		# Claude Code first-run quieting: onboarding, per-project trust, and
		# (on the API-key path) the key-approval prompt — otherwise the
		# auto-launched interviewer opens on a blocking trust dialog instead
		# of a prompt. Best-effort: keys are undocumented; failure costs one
		# Enter press.
		seed_claude_json || warn "claude first-run seed failed (one extra prompt at launch)"
	else
		# Run by hand on a bare host, $HOME is the real machine, not a
		# throwaway container home — skip the global ~/.codex and
		# ~/.claude.json writes rather than silently rewrite the user's own
		# config. The bare-metal lane never needs this: just export your key
		# and run 'claude' / 'codex' yourself.
		warn "not running in a container — skipping global codex/claude config seeding"
	fi

	# Sentinel the folderOpen launcher polls — always last.
	mkdir -p "$HOME/.config/practice"
	touch "$HOME/.config/practice/seed-done"
}

seed_claude_json() {
	local py="$PWD/.venv/bin/python"
	[ -x "$py" ] || py="$(command -v python3 || true)"
	[ -n "$py" ] || return 0
	WORKSPACE="$PWD" "$py" <<-'PYEOF'
		import json, os
		path = os.path.expanduser("~/.claude.json")
		try:
		    with open(path) as f:
		        cfg = json.load(f)
		except (FileNotFoundError, ValueError):
		    cfg = {}
		cfg["hasCompletedOnboarding"] = True
		project = cfg.setdefault("projects", {}).setdefault(os.environ["WORKSPACE"], {})
		project["hasTrustDialogAccepted"] = True
		project["hasCompletedProjectOnboarding"] = True
		key = os.environ.get("ANTHROPIC_API_KEY", "")
		if key:
		    approved = cfg.setdefault("customApiKeyResponses", {}).setdefault("approved", [])
		    if key[-20:] not in approved:
		        approved.append(key[-20:])
		with open(path, "w") as f:
		    json.dump(cfg, f, indent=2)
		    f.write("\n")
	PYEOF
}

case "${1:-}" in
	--sync) sync_deps; exit 0 ;;
	--seed) seed_state; exit 0 ;;
esac

if ! command -v uv >/dev/null 2>&1; then
	log "installing uv $UV_VERSION"
	curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | sh
fi

if ! command -v just >/dev/null 2>&1; then
	log "installing just $JUST_VERSION"
	curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh \
		| bash -s -- --tag "$JUST_VERSION" --to "$BIN_DIR"
fi

if ! command -v watchexec >/dev/null 2>&1; then
	# Only `just study` (watch mode) needs watchexec — never fail the boot on it.
	log "installing watchexec $WATCHEXEC_VERSION"
	arch="$(uname -m)"
	tarball="watchexec-$WATCHEXEC_VERSION-$arch-unknown-linux-musl"
	url="https://github.com/watchexec/watchexec/releases/download/v$WATCHEXEC_VERSION/$tarball.tar.xz"
	if curl -LsSf "$url" -o /tmp/watchexec.tar.xz \
		&& tar -xJf /tmp/watchexec.tar.xz -C /tmp \
		&& install -m 0755 "/tmp/$tarball/watchexec" "$BIN_DIR/watchexec"; then
		:
	else
		warn "watchexec install failed — 'just study' watch mode unavailable; loop still works"
	fi
	rm -rf /tmp/watchexec.tar.xz "/tmp/$tarball"
fi

# Optional interviewer CLIs. Claude Code arrives via its devcontainer feature;
# Codex is npm-only (no official feature yet). Neither is load-bearing.
if command -v npm >/dev/null 2>&1 && ! command -v codex >/dev/null 2>&1; then
	log "installing OpenAI Codex CLI (optional)"
	npm install -g @openai/codex || warn "codex install failed (optional — Copilot/Claude still work)"
fi

sync_deps
log "bootstrap complete"
