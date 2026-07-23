# Repo hooks

`candidate-workspace-guard.json` runs `scripts/hooks/guard_pretooluse.py` on
every `preToolUse` event and enforces the resident-interviewer invariant in
AGENTS.md: the agent never edits candidate-owned files.

The guard denies:

- any file-edit/write tool call whose path-shaped arguments reference
  `.challenges/**` (the candidate's own workspace), with a reason telling the
  agent to relay the error and ask the candidate to make the edit themselves
- `rm -rf` (or `-fr`, `--recursive --force`) targeting a path outside this
  workspace (absolute, `~`, `$HOME`, `${HOME}`, or a `..` traversal)
- `git push --force`, `--force-with-lease`, or `-f`

It never blocks maintenance edits under `src/`, `tests/`, or docs — only a
`.challenges/` marker in a path-shaped argument field trips the file-edit
rule, never file content that merely mentions the workspace.

## Contract

JSON hook files carry no comments, so the schema and behavior live here
instead. `version` and `hooks.<eventName>` mirror the documented repo-hooks
format; each `preToolUse` entry is a `command` hook that pipes the event
payload (`toolName`, `toolArgs`, ...) to the script over stdin and reads back
`{"permissionDecision": "allow" | "deny", "permissionDecisionReason": "..."}`
on stdout with exit 0. A non-zero exit denies regardless of stdout.

Doc source: `docs.github.com/en/copilot/reference/hooks-reference` and
`docs.github.com/en/copilot/concepts/agents/hooks` (fetched 2026-07-15).
Only the Copilot cloud agent and Copilot CLI are documented as reading
`.github/hooks/*.json`; no IDE/VS Code chat surface is documented as honoring
it. The `bash` field is used (not `powershell`) because this repo's
Codespaces surface is Linux-only.
