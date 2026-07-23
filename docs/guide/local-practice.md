---
title: Local VS Code
description: Run the editor-first practice loop locally with the VS Code Dev Container or a small uv and just toolchain.
---

# Local VS Code

Run the same editor-first loop on your machine. The Dev Container matches
Codespaces; a native install needs only `uv` and `just` for the core flow.

## Set up

```bash
git clone https://github.com/Jesssullivan/dsa-study-packet.git
cd dsa-study-packet
```

Choose one lane:

=== "Dev Container"

    Open the folder in VS Code and choose **Dev Containers: Reopen in
    Container**. The container provides `uv`, `just`, and `watchexec`.

=== "Native tools"

    Install Python 3.14+, [uv](https://docs.astral.sh/uv/), and
    [just](https://just.systems/), then run:

    ```bash
    uv sync --extra dev
    just doctor
    ```

    `watchexec` is optional and only needed for `just practice-watch`. Nix
    users can run `direnv allow` for the pinned toolchain. Do not run
    `.devcontainer/setup.sh` directly on a local machine.

## Start a rep

With Copilot Chat installed and signed in, enter `/comments`. It uses ordinary
reasoning comments with no required labels or prefixes. Add a topic and problem
to choose one:

```text
/comments arrays two_sum
```

If named vocabulary helps you think, `/reacto`, `/clarp`, and `/umpire` start
the same loop with optional labels. Copilot is optional; use the conductor
directly:

```bash
just practice-start comments
just practice-start comments arrays two_sum
```

Your source and test file open under `.challenges/workspace/`. Fill the
reasoning comments, save, then delete the `THINKING GATE` yourself. Implement
the solution and add focused tests. If the tabs do not open, the command prints
their paths; `just practice-open` tries again.

## Continue and close

```bash
just practice-next       # state and one next action
just practice-test       # reference tests plus your tests
just practice-watch      # rerun on workspace changes
just practice-repl       # interactive exploration
just practice-open       # reopen both files
just practice-finish "one fix"
```

The committed solution under `src/algo/` remains unchanged, and your workspace
stays gitignored. Run `just doctor` when the toolchain looks wrong.

Candidate tests are trusted local Python, not a sandbox. The runner bounds test
time and cleans the pytest process group, but candidate tests must not launch
detached or background daemons.

Claude Code, Codex, and other external agents are optional. Install,
authenticate, and launch the one you already use; the repository does not
start one or require its credentials. A direct `just` session works without
any agent.

Ask the resident interviewer for an untimed conversational rep when you want
less editor pressure. Choose a timed board-style rep only when speaking under
a clock is the skill you mean to practice.
