# `.devcontainer/` notes

## Known upstream Codespaces blocker: `PendingMigrationError`

**Status:** unresolved upstream; there is no known working repository
workaround.

A fresh Codespace at exact packet SHA
`534fca42b4df9acc028bae6257f80763d4678e51` disproved the former
container-wide `NODE_OPTIONS` preload:

- the VS Code server process inherited `NODE_OPTIONS`;
- the remote extension-host process had `NODE_OPTIONS` unset because VS
  Code's `extensionHostProcess.js` removes it before extension startup; and
- `remoteexthost.log` still recorded repeated `PendingMigrationError` stacks
  rooted in the built-in `GitHub.codespaces` 1.18.15 extension.

The preload therefore never reached the process where the observed failure
occurred. It also changed every ordinary Node process in the container, and
a missing preload file could make those processes fail before VS Code
attached. The file and wiring were removed under
[packet issue #105](https://github.com/Jesssullivan/dsa-study-packet/issues/105).

Removal does **not** mean the upstream problem is fixed. Track
[microsoft/vscode#312110](https://github.com/microsoft/vscode/issues/312110)
as a related upstream `PendingMigrationError` report, not proof of an
identical root cause. Its published stack is rooted in bundled Copilot; this
exact-head Codespace's observed stack was rooted in built-in
`GitHub.codespaces` 1.18.15. Require a new exact-head Codespace acceptance
run before changing status. Copilot extension selection is a separate
experiment tracked by
[packet issue #94](https://github.com/Jesssullivan/dsa-study-packet/issues/94).

### Operator-safe evidence

For a new reproduction:

1. Create a new branch-specific Codespace and record its checkout SHA, VS
   Code version, and extension versions.
2. Verify Copilot sign-in and entitlement in the editor UI. Do not use
   repository `gh` authentication as a proxy.
3. Compare only the presence or absence of `NODE_OPTIONS` in the VS Code
   server and remote extension-host processes. Do not publish full process
   environments, settings sync data, or complete logs.
4. Extract only the relevant `PendingMigrationError` stack and extension
   identifier from `remoteexthost.log`. Redact tokens, user paths, and
   unrelated extension data.
5. Run the source-native practice acceptance separately, then stop or delete
   the disposable Codespace.

The practice acceptance remains the product signal. Process and log evidence
only establishes where the upstream editor failure occurs; it must not be
used to infer that the learner workflow passed.
