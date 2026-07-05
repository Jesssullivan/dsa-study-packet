# dsa-study-packet — agent guide

Public, company-neutral technical-interview study SSOT. Source code, tests, and
authored notes are the source of truth; the printable booklet PDF and the mkdocs
site are **generated** from them. The point of the repo is a repeatable practice
day that trains confident, non-panicked reasoning-out-loud under observation.

## Run a practice day
Use the **`practice-day`** skill (`.claude/skills/practice-day/`). It conducts the
science-grounded 4–5h block: arrival ritual → cold whiteboard CLARP reps → IDE
close+verify → targeted input → observed mock → tape review + rep log. The
human-readable rationale, hour-by-hour block, and citations live in
[`docs/guide/interview-practice-evidence.md`](docs/guide/interview-practice-evidence.md);
the method is `reference-sheets/10`; the 14-day calendar is `reference-sheets/11`.

Core recipes: `just study-spaced N` (interleaved draws) · `just interview <t> <p>`
(cold present, solution stripped) · `just study <t>` (watch tests) ·
`just rep "…"` (log a rep) · `just challenge-done <t> <p>` (spaced repetition).

## Build
`just` is the sole front door. `just packet` (booklet PDF) · `just docs` (site) ·
`just pdf-all` (reference-sheet PDFs) · `just test` / `just lint`. Cache-first Bazel
goes through `just remote-*` — never raw `bazel`. `//:booklet` is the one
composition surface that private overlays consume via `@dsa_study_packet//:booklet`.

## The public boundary (hard rule)
This repo is PUBLIC and company-neutral. Employer names, panel/interviewer notes,
req numbers, clearance facts, tailored positioning, and personal rep logs **never**
enter this tree — they live only in the private downstream overlay. `just
public-boundary` (in `just lint`, wired to CI) enforces it. If a sentence only makes
sense for one employer, it belongs downstream. Full contract:
[`docs/guide/source-of-truth.md`](docs/guide/source-of-truth.md).
