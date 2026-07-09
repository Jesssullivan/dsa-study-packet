---
title: Local VS Code Quickstart
---

# Local VS Code Quickstart

!!! abstract "What this page is"
    A tight quickstart for practicing from **your own machine** in local VS
    Code instead of GitHub Codespaces. Two lanes: **Dev Containers** (same
    container Codespaces uses) or **bare metal** (just `uv` + `just`, no
    Docker at all). Same rungs, same commands, same interviewer — only where
    the toolchain comes from differs.

## 1. Clone it

```bash
git clone https://github.com/Jesssullivan/dsa-study-packet.git
cd dsa-study-packet
```

## 2. Pick a lane

=== "Dev Containers (recommended if you have Docker)"

    Open the folder in VS Code, then **Reopen in Container** (Command
    Palette → "Dev Containers: Reopen in Container"). This runs the exact
    same `.devcontainer/` bootstrap Codespaces uses — `uv`, `just`,
    `watchexec`, and (if you have Docker/Podman running) the container builds
    the toolchain for you. If VS Code asks **"Allow Automatic Tasks?"**,
    click **Allow** — that is the practice-loop launcher below.

    The container's `$HOME` is its own throwaway filesystem, not your real
    machine, so this lane behaves identically to Codespaces: same seeding,
    same first-run trust dialogs handled for you.

=== "Bare metal (no container)"

    Open the folder directly in VS Code — no Dev Containers extension
    required. Nothing in `.devcontainer/` runs automatically here (its
    lifecycle hooks only fire inside a container), so install the four tools
    the practice loop needs yourself:

    ```bash
    # uv (Python + dependency manager)
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # just (recipe runner)
    curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
    # watchexec (optional — only 'just study' watch mode needs it)
    # macOS: brew install watchexec   ·   or your package manager of choice
    ```

    Then sync dependencies and check the toolchain:

    ```bash
    uv sync --extra dev
    just doctor
    ```

    `just doctor` exits non-zero only if a **core** tool (`uv`, `just`) is
    missing — `watchexec`, `git`, and every interviewer CLI are informational,
    since the loop still works without them. Nix users: `direnv allow` (or
    `nix develop --impure`) pins all four tools plus `tectonic`/`pandoc` for
    PDF generation in one step — see the [Getting Started](getting-started.md)
    Nix tab.

    Never run `.devcontainer/setup.sh` by hand on bare metal — it is written
    for the container lifecycle. Its `--seed` mode would otherwise seed your
    **real** global `~/.claude.json` / `~/.codex` config instead of a
    throwaway container home; it detects that it is not in a container and
    skips those writes with a warning, but you should not need it at all here.

## 3. Give your interviewer a credential (optional)

Nothing is locked without one — Copilot Chat and the solo loop
(`just interview arrays two_sum`) work with zero keys. To have Claude Code or
Codex attach automatically, export **one** of these in your shell profile
(`~/.zshrc`, `~/.bashrc`, …) before opening the integrated terminal, so it
inherits the value:

| Variable | Interviewer | Notes |
|----------|-------------|-------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code (subscription) | From `claude setup-token`; no per-token billing |
| `ANTHROPIC_API_KEY` | Claude Code (API) | Pay-as-you-go; wins over the token above if both are set |
| `OPENAI_API_KEY` | Codex | Run `codex login --device-auth` instead if you would rather not export a key |

This is the local equivalent of the Codespaces secret described in the
repo's `WELCOME.md` — same variable names everywhere, just set as a normal
shell export instead of a GitHub secret.

## 4. The zero-click launcher fires here too

`.vscode/tasks.json` runs a `folderOpen` task the moment you open this repo
in **any** VS Code window — container or bare metal. It launches
`.devcontainer/launch-agent.sh`, which:

1. Picks Claude Code if `claude` is on `PATH` and one of the env vars above is
   set, else Codex if it is already logged in, else drops you into a plain
   shell with the same "say the line" instructions as Codespaces.
2. On bare metal it skips the container-only "wait for seeding" pause (there
   is nothing to wait for outside a container) and starts immediately.

If you would rather not have a terminal auto-launch every time you open the
folder, remove or rename the `"practice: start"` task in `.vscode/tasks.json`
locally — it is a convenience, not a requirement.

## 5. `code --goto` (rung 2's file-jump)

`just interview-comment <topic> <problem>` opens the stub at its `RESTATE:`
line using the `code` CLI, then falls back to printing the path if `code`
is not on `PATH`. Local VS Code only installs this shell command on request:
Command Palette → **"Shell Command: Install 'code' command in PATH"**. Once
installed, the same command works whether you are in a Dev Container or bare
metal — it always targets the local VS Code window.

## 6. Same rungs, same commands

Nothing about the practice ladder changes locally — it is the same
resident-interviewer persona (`AGENTS.md`) and the same recipes as
Codespaces:

```bash
just doctor                          # preflight
just study-spaced 1                  # today's spaced-repetition draw
just interview arrays two_sum        # cold problem, solution stripped
just interview-comment arrays two_sum   # rung 2: comment scaffold, save-gated
just study arrays                    # watch mode: tests re-run on save
just rep "arrays/two_sum C2 L1 A2 R1 P2 h0 <one fix>"
just challenge-done arrays two_sum
```

Tell your agent **"Start my first practice rep."** and go — the same one
placement question, the same ladder, the same closeout.
