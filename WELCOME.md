# Welcome to the woodshed

When this Codespace opens you should see a **split terminal**: the left pane is
your interviewer (or guidance for getting one), the right pane is a shell with
the crib sheet. If VS Code Desktop asks **"Allow Automatic Tasks?"** — click
**Allow** (the browser client doesn't ask).

Say the line and you're practicing:

> Start my first practice rep.

No credential? Nothing is locked: Copilot Chat (sidebar → pick the
**Interviewer** agent) and the solo loop (`just interview arrays two_sum`,
method on `reference-sheets/10`) work with zero keys. `just doctor` checks the
toolchain.

## One-time setup: an interviewer that's already running when you attach

Optional, takes two minutes, and every future Codespace opens straight into a
live interviewer.

**Claude Code — pick ONE:**

- **Subscription token** (Pro/Max, no per-token billing — recommended): on any
  machine with a browser, run `claude setup-token`, copy the printed token
  immediately (it is not saved anywhere), and store it as a Codespaces secret
  named `CLAUDE_CODE_OAUTH_TOKEN` at
  [github.com/settings/codespaces](https://github.com/settings/codespaces).
  It lasts one year; rerun `claude setup-token` to renew.
- **API key** (pay-as-you-go): store a key from console.anthropic.com as the
  secret `ANTHROPIC_API_KEY`.
- Do **not** set both — the API key silently wins and bills your API account.

**Codex:** store an OpenAI key as the secret `OPENAI_API_KEY`. The container
logs the Codex TUI in for you on first build (the bare env var alone does not).
ChatGPT-plan login isn't recommended here — its auth refreshes every ~8 days
and goes stale in an ephemeral container.

**The one click people forget:** Codespaces secrets are granted per-repository.
When you create a new repo from this template, revisit
[github.com/settings/codespaces](https://github.com/settings/codespaces) and
add the new repo to your secret's access list — otherwise the key silently
isn't injected and you'll land on the no-key path.

## Choosing your interviewer's brain

Defaults are deliberately unpinned so the interviewer improves as vendors ship:

- **Claude subscribers**: your plan default is already right — Sonnet-class on
  Pro (fast, warm, cheap), Opus-class on Max (deepest judgment). API-key users:
  `claude --model sonnet` is the metered sweet spot; `--model opus` for mock
  days.
- **Codex**: rides the CLI's current default model; the repo config only sets
  medium reasoning effort so conversational turns stay snappy.
- **Copilot Free**: model is auto-selected. Copilot Pro users can pick a
  Claude Sonnet-class model in the Chat model picker — noticeably better
  interviewer tone.
