---
title: Local VS Code
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

With Copilot Chat installed and signed in, enter `/reacto`, `/clarp`,
`/umpire`, or `/comments`. Add a topic and problem to choose one:

```text
/reacto arrays two_sum
```

Copilot is optional. Use the same conductor directly:

```bash
just practice-start reacto
just practice-start clarp arrays two_sum
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

Claude Code, Codex, and other external agents are optional. Install,
authenticate, and launch the one you already use; the repository does not
start one or require its credentials. A direct `just` session works without
any agent.

Ask the resident interviewer for an untimed conversational rep when you want
less editor pressure. Choose a timed board-style rep only when speaking under
a clock is the skill you mean to practice.
