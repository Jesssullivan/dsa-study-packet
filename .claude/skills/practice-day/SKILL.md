---
name: practice-day
description: Conduct an explicitly requested full 4 to 5 hour interview-practice day, multi-block practice session, or short 90-minute block. Default to editor-first coding reps with real tests, breaks, targeted review, and an optional board or observed mock. Do not trigger on a generic request to practice one problem.
---

# Practice day conductor

Read the persona block in repo-root `AGENTS.md`; it is authoritative. Use this
skill only when the candidate explicitly requests a full practice day,
multi-block session, or 90-minute block. Route a generic single-rep request to
the `interviewer` skill.

Ask whether they want the full 4 to 5 hour ceiling or the short 90-minute
block. Offer the arrival reset once. Never treat regulation as a gate or score.

## Short block

1. Draw three interleaved options with `just study-spaced 3`.
2. Let the candidate choose one printed editor command, or use the first.
3. Run that exact `just practice-start` command. Default to its CLARP editor
   mode unless the candidate requests REACTO, UMPIRE, or plain comments.
4. Follow the `AGENTS.md` editor state loop: `just practice-next`, then `just
   practice-test`, `just practice-watch`, or `just practice-repl` when allowed.
5. Close with one win, one fix, and `just practice-finish` using a concrete
   note. Stop at 90 minutes even if work remains.

## Full day

Use three effortful blocks with real 15-minute breaks. Four to five hours is a
ceiling, not a quota.

### Block 1: editor-first retrieval, 75 to 90 minutes

Run one or two cold editor reps from `just study-spaced 3`. For each rep, use
the state loop and finish command above. The candidate owns all source, tests,
and gate edits.

### Block 2: focused transfer, 60 to 75 minutes

Choose one new draw or revisit the single weakness exposed in Block 1. Require
a focused test, a line-by-line trace, and reconciliation between the saved
comments and code. Do not add unrelated reading.

### Block 3: observed pressure, 30 to 45 minutes

Offer either a timed board rep or an observed mock. This block is optional,
especially for a first-time or anxious candidate. If chosen, follow the
interviewer cadence, silence rules, and hint ladder in `AGENTS.md`. A human
observer may score with reference sheet 10 while the agent stays silent.

Finish with a two-minute review: one success, one gap, one next action. Use
`just study-spaced 1` only to show tomorrow's next draw; do not start it.

## Standing rules

- Editor-first is the default. Whiteboard is an optional requested variant.
- Interleave topics. Prefer retrieval and coding over passive review.
- Never exceed 90 minutes without a real break.
- Never edit candidate-owned files or solve the problem.
- Keep employer details and personal logs outside tracked public files.
