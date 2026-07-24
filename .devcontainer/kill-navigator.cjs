// kill-navigator.cjs
//
// WHAT: Deletes the global `navigator` binding (if present and configurable)
// before any other module in this Node process gets a chance to read it.
//
// WHY: Node 22 defines a global `navigator` (the Web-platform API surface).
// The bundled GitHub Copilot Chat extension reads `navigator` at module
// top level, and when that happens inside the REMOTE extension host
// (vscode-server, as used by GitHub Codespaces) VS Code's
// PendingMigrationError guard treats it as evidence of an inconsistent
// extension-host state and destabilizes the remote extension host,
// hanging Copilot Chat slash-commands. No upstream fix exists yet.
// See: https://github.com/microsoft/vscode/issues/312110
//
// STATUS: EXPERIMENT, not a permanent fix. This file is loaded via
// `NODE_OPTIONS=--require ...` for every Node process started inside the
// dev container (see .devcontainer/devcontainer.json), including
// vscode-server's own extension host, not just this repo's scripts.
//
// REMOVAL CONDITION: Delete this file and the matching `NODE_OPTIONS` entry
// in `.devcontainer/devcontainer.json`'s `containerEnv` once
// microsoft/vscode#312110 is confirmed fixed upstream in Codespaces (i.e.
// Copilot Chat no longer needs the global `navigator` removed to avoid
// PendingMigrationError).
//
// SAFETY: This file must never throw and must never make a Node invocation
// that loads it fail. On any unexpected condition it silently no-ops. Set
// DEBUG_KILL_NAVIGATOR=1 in the environment to get one diagnostic line on
// stderr describing what happened; it is otherwise completely silent.

'use strict';

let outcome = 'no-op: navigator absent';

try {
  const descriptor = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
  if (descriptor && descriptor.configurable) {
    delete globalThis.navigator;
    outcome = 'deleted global navigator';
  } else if (descriptor) {
    outcome = 'no-op: navigator present but not configurable';
  }
} catch (error) {
  outcome = `no-op: unexpected error (${error && error.message})`;
} finally {
  if (process.env.DEBUG_KILL_NAVIGATOR) {
    // eslint-disable-next-line no-console
    console.error(`[kill-navigator] ${outcome}`);
  }
}
