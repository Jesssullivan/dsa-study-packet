#!/usr/bin/env bash
# Devcontainer toolchain bootstrap for the practice loop.
#
# Deliberately independent of flake.nix: the Nix devshell stays the
# maintainer's local flow; containers get only the three command-line tools the
# editor practice loop needs (Python via uv, just, and watchexec). GitHub
# Copilot Chat is the native Codespaces interviewer.
#
# Modes:
#   --tools  pinned tool installs only (onCreateCommand)
#   --sync   dependency sync only (updateContentCommand)
#   --seed   seed per-user practice state (postCreateCommand)
#   (none)   run all three phases, for an explicit manual bootstrap
set -euo pipefail

UV_VERSION="0.11.27"
JUST_VERSION="1.40.0"
WATCHEXEC_VERSION="2.3.2"

BIN_DIR="$HOME/.local/bin"
export PATH="$BIN_DIR:$PATH"
# The base image ships python3.11-minimal (no `json` module); uv must never
# probe it. Always use uv-managed CPython. Mirrored in containerEnv.
export UV_PYTHON_PREFERENCE=only-managed
mkdir -p "$BIN_DIR"

log()  { echo "[setup] $*"; }
warn() { echo "[setup] WARN: $*" >&2; }

sync_deps() {
	log "syncing python deps (uv fetches CPython to satisfy requires-python)"
	uv sync --extra dev
}

seed_state() {
	# Per-user, gitignored practice state. Every Codespace user starts fresh.
	mkdir -p .challenges
	just catalog || warn "catalog preview failed (non-fatal)"
}

install_tools() {
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
		# Watch mode is optional. Never fail container creation on this helper.
		log "installing watchexec $WATCHEXEC_VERSION"
		arch="$(uname -m)"
		tarball="watchexec-$WATCHEXEC_VERSION-$arch-unknown-linux-musl"
		url="https://github.com/watchexec/watchexec/releases/download/v$WATCHEXEC_VERSION/$tarball.tar.xz"
		if curl -LsSf "$url" -o /tmp/watchexec.tar.xz \
			&& tar -xJf /tmp/watchexec.tar.xz -C /tmp \
			&& install -m 0755 "/tmp/$tarball/watchexec" "$BIN_DIR/watchexec"; then
			:
		else
			warn "watchexec install failed; watch mode unavailable; the loop still works"
		fi
		rm -rf /tmp/watchexec.tar.xz "/tmp/$tarball"
	fi
}

case "${1:-}" in
	--tools) install_tools ;;
	--sync) sync_deps ;;
	--seed) seed_state ;;
	"")
		install_tools
		sync_deps
		seed_state
		;;
	*)
		echo "usage: $0 [--tools|--sync|--seed]" >&2
		exit 2
		;;
esac

log "${1:---all} complete"
