# Welcome to the woodshed

Start in the editor. Open Copilot Chat and choose one comment format:

```text
/reacto
/clarp
/umpire
/comments
```

The command draws the next due problem. Add a topic and problem when you want
one directly, such as `/reacto arrays two_sum`.

Two gitignored files open under `.challenges/workspace/`: your source and your
test file. Fill the reasoning comments, save, and delete the `THINKING GATE`
yourself. Then implement and add examples or edge cases. The interviewer does
not write your code, tests, or gate.

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

Copilot is optional. `just practice-start reacto` begins the same rep from a
terminal. Codespaces needs no repository API key and starts no external agent.
Claude Code, Codex, and other CLIs are optional tools you launch and
authenticate yourself.

For a slower surface, ask for an untimed conversational rep. Use timed
board-style practice only when narration under a clock is today's target.
