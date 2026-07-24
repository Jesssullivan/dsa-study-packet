# `.devcontainer/` notes

## EXPERIMENT: killing the global `navigator` for Copilot Chat (vscode#312110)

**Status:** experimental, container-wide workaround. Not a permanent fix.

**Problem:** Node 22 defines a global `navigator` (the Web-platform API
surface). The Copilot Chat extension bundled with VS Code / Codespaces reads
`navigator` at module top level. When that read happens inside the *remote*
extension host (`vscode-server`, which is how Codespaces runs extensions),
VS Code's `PendingMigrationError` guard treats it as evidence of an
inconsistent extension-host state and destabilizes the remote extension
host — in practice, Copilot Chat slash-commands hang. There is no upstream
fix as of this writing. Tracking issue:
<https://github.com/microsoft/vscode/issues/312110>.

**Workaround:** `.devcontainer/kill-navigator.cjs` is a tiny, defensive Node
preload that deletes `globalThis.navigator` (only if it exists and is
configurable) before any other module in the process can read it. It is
wired in via `containerEnv.NODE_OPTIONS` in `devcontainer.json`:

```json
"NODE_OPTIONS": "--require ${containerWorkspaceFolder}/.devcontainer/kill-navigator.cjs"
```

This applies to *every* Node process started in the container — including
`vscode-server`'s own extension host, not just this repo's scripts — because
`NODE_OPTIONS` is a container-wide environment variable, not something
scoped to a single invocation.

`${containerWorkspaceFolder}` is used instead of a hardcoded path so the
preload keeps resolving correctly if this repo is forked or cloned under a
different name. Per the [Dev Container spec's variable
table](https://containers.dev/implementors/json_reference/#variables-in-devcontainerjson),
`${containerWorkspaceFolder}` is documented as usable in "Any" property,
which includes `containerEnv` (this is different from `${containerEnv:VAR}`,
which the same table restricts to `remoteEnv` only, because that form needs
the container already running to introspect its environment).

### The failure mode this creates, and why it matters

`node --require <path>` exits non-zero for *every* Node invocation if
`<path>` does not resolve to a real file — and `vscode-server` itself is a
Node process. If `.devcontainer/kill-navigator.cjs` is ever moved, renamed,
or accidentally left out of a fork, or if `${containerWorkspaceFolder}`
resolves unexpectedly for some tool, the whole container's Node tooling
(including the ability to attach VS Code / Codespaces to the container at
all) can break, not just Copilot Chat.

Mitigations already in place:

- The preload script itself never throws and never breaks a Node
  invocation once it has been successfully loaded (see the file's own
  header comment for the exact contract).
- `tests/test_codespaces_config.py` pins the `NODE_OPTIONS` wiring and the
  presence/contents of the preload file, and (when `node` is available)
  actually runs the preload as a subprocess.
- `${containerWorkspaceFolder}` substitution keeps the path correct across
  forks/renames rather than hardcoding `/workspaces/dsa-study-packet`.

What is **not** mitigated: if the file is missing at container-build time
for any other reason, every Node invocation in the container will fail
until `devcontainer.json` is fixed and the container is rebuilt. Because
that includes `vscode-server`, recovery may require editing
`devcontainer.json` from outside the broken container (e.g. the GitHub web
editor, or a local clone) and then rebuilding.

### How to verify in a fresh Codespace

1. Open a fresh Codespace on this branch (or rebuild an existing one so the
   new `containerEnv` takes effect).
2. Open a terminal and run `node -e "console.log(typeof navigator)"` — it
   should print `undefined`.
3. Open Copilot Chat and run `/comments` (or any slash-command) — it should
   respond instead of hanging.

### Rollback

Delete the `NODE_OPTIONS` line from `containerEnv` in
`.devcontainer/devcontainer.json` and delete
`.devcontainer/kill-navigator.cjs`, then rebuild the container.

### Removal condition

Remove this workaround entirely once microsoft/vscode#312110 is confirmed
fixed upstream in Codespaces (Copilot Chat no longer needs the global
`navigator` removed to avoid `PendingMigrationError`).
