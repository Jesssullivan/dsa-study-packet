# AGENTS.md — AI Agent Workflows for This Repo

This documents how AI agents (Claude Code, etc.) can assist with interview prep
before and after (never during) the actual interview.

## Available MCP Servers

These are configured in `~/.claude/settings.json` and available to Claude Code agents:

| MCP Server | Purpose | Useful For |
|-----------|---------|------------|
| **Mermaid Chart** | Diagram generation and validation | System design diagrams, algorithm flow visualization |
| **WebFetch** | Fetch web pages | Pulling latest docs, checking API references |
| **WebSearch** | Search the web | Finding new problems, researching target employer updates |

### Potentially Useful MCPs to Add

These MCPs would enhance agent capabilities for this repo. Configure in
`~/.claude/settings.json` under `mcpServers`:

```jsonc
{
  "mcpServers": {
    // Persistent knowledge graph — track study progress, weak areas, insights
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-memory"]
    },
    // Sequential thinking — useful for complex algorithm analysis
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    },
    // Research — look up algorithm papers, proofs, mathematical foundations
    "arxiv": {
      "command": "npx",
      "args": ["-y", "arxiv-mcp-server"]
    }
  }
}
```

## Pre-Interview Agent Workflows

### 1. Generate Practice Problems

```
Prompt: "Generate a new medium-difficulty graph problem relevant to target employer's
aviation domain. Create the problem file and tests using `just new graphs
<name>`, then implement a solution."
```

The agent will:
- Scaffold with `just new`
- Write problem description in the docstring
- Implement the solution with proper typing
- Write 4-6 test cases + hypothesis property tests
- Run `just lint` to verify

### 2. Review & Improve Existing Solutions

```
Prompt: "Review my implementation of src/algo/graphs/dijkstra.py. Check for:
correctness, edge cases, complexity analysis accuracy, cleaner Python idioms.
Suggest improvements but don't over-engineer."
```

### 3. Mock Interview Simulation

```
Prompt: "Give me a timed algorithm problem. I'll solve it in src/algo/ and
you evaluate my solution as an interviewer would — time complexity, space
complexity, code quality, edge cases I missed."
```

### 4. Explain an Algorithm

```
Prompt: "Explain the A* algorithm from src/algo/graphs/a_star_search.py.
Walk through the code step by step, trace it with a small example grid,
and explain when A* is better than Dijkstra."
```

### 5. Weak Area Drilling

```
Prompt: "I struggle with dynamic programming. Go through all DP problems in
src/algo/dp/ and explain the recurrence relation for each. Then quiz me on
identifying the sub-problem structure for new problems."
```

### 6. System Design Practice

```
Prompt: "Walk me through designing a real-time flight route optimization
system. Reference reference-sheets/06-system-design.md and RESEARCH.md for
employer-specific context. Ask me clarifying questions like an interviewer would."
```

### 7. Code Reading Practice

```
Prompt: "Present me with src/practice/code_reading/ex01_caching_service.py.
Don't tell me the issues — let me identify them, then grade my analysis
against the answer key at the bottom."
```

## Post-Interview Agent Workflows

### 8. Debrief & Gap Analysis

```
Prompt: "I just finished my target employer interview. Here's what I was asked: [describe].
Identify which topics in this repo cover those areas and which gaps I should
fill for future interviews."
```

### 9. Add Missing Topics

```
Prompt: "Add a new concept module for [topic]. Follow the style in
src/concepts/ — heavy comments, web references, paired tests. Add it to
README.md."
```

### 10. Generate Reference Material

```
Prompt: "Create a new reference sheet reference-sheets/08-[topic].md covering
[topic]. Follow the format of existing sheets — concise, printable, with
code examples and complexity notes."
```

## Agent Best Practices

1. **Always run `just lint`** after making changes — mypy strict catches real bugs
2. **Follow existing style** — read CLAUDE.md and an existing file before creating new ones
3. **Don't over-engineer** — this is a study repo, not production code
4. **Add "When to use"** guidance to new implementations
5. **Keep reference sheets concise** — they need to be printable
6. **Use `just new` for scaffolding** — maintains consistent structure
7. **Run `just test` before finishing** — 529+ tests should stay green

## Cross-Reference: Problem → Real-World Application

See `reference-sheets/08-cross-reference-guide.md` for a complete mapping of
which algorithms and patterns to use for different problem types, with pointers
to the specific implementations in this repo.

## Sharing This Repo

This repo is designed to be shareable. Others can:
1. `git clone` + `direnv allow` → full dev environment via nix
2. `just test` → verify everything works
3. Use `reference-sheets/07-interview-day-guide.md` on test day
5. Use the agent workflows above for AI-assisted study
