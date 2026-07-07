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

sync_deps() {
	log "syncing python deps (uv fetches CPython to satisfy requires-python)"
	uv sync --extra dev
}

seed_state() {
	# Per-user, gitignored practice state — every Codespace user starts fresh.
	mkdir -p .challenges
	just catalog || warn "catalog preview failed (non-fatal)"
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
