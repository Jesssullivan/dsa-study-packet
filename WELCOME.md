# Welcome to the woodshed

Start in the editor. Open Copilot Chat and choose one practice mode:

```text
/reacto
/clarp
/umpire
/comments
```

The command draws the next due problem. Add a topic and problem when you want
one directly, such as `/reacto arrays two_sum`.

Two gitignored files open under `.challenges/workspace/`: your source and your
test file. Write ordinary source comments or docstrings in your own words,
before and alongside the code. The comments belong in the file, not the Chat
composer, and need no prefixes or minimum count. Save, then enter `/continue`
so the interviewer can read the saved files and return one current state and
next action. There is no gate to delete. The interviewer does not write your
code or tests.

Enter `/continue` after a save, or use the terminal controls:

```bash
just practice-next
just practice-test
just practice-watch
just practice-repl
just practice-open
```

Finish with one useful correction:

```bash
just practice-finish "state the one fix"
```

Copilot is optional. When using it, confirm Chat is signed in and available in
the VS Code UI. `just practice-start reacto` begins the same rep from a
terminal. Codespaces needs no repository API key and starts no external agent.
Claude Code, Codex, and other CLIs are optional tools you launch and
authenticate yourself.

On the first terminal action, choose **Enable Auto Approve** from the Allow
menu and accept once. Keep **Default approvals**; this repository adds rules
only for its listed Woodshed commands. Your VS Code defaults and user settings
remain separate. Terminal sandboxing is off because VS Code's preview
Bubblewrap sandbox cannot nest here. The Codespace boundary, command allowlist,
and pre-tool guard still apply.

For a slower surface, ask for an untimed conversational rep. Use timed
board-style practice only when narration under a clock is today's target.
