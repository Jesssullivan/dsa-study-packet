---
name: practice-day
description: Conduct Jess's daily 4–5h whiteboard + IDE interview-practice block. Use when she says "run my practice day", "let's practice", "start today's block", or at the start of a study session. Picks interleaved cold drills, gates timed sub-blocks (arrival ritual → cold whiteboard CLARP reps → IDE close+verify → targeted input → observed mock → tape review), logs reps. Trains confident, non-panicked reasoning-out-loud under observation for senior/DoD-level technical interviews — not LeetCode volume. Grounded in the science in docs/guide/interview-practice-evidence.md.
---

# Practice Day Conductor

Run ONE focused deliberate-practice day (~4–5h ceiling) from `~/git/dsa-study-packet`.
The target is: *make my reasoning inspectable while the problem moves, without panicking.*
Structure the day as 3–4 effortful sub-blocks with real breaks — effortful practice
degrades past ~90 min without recovery (Ericsson 1993). 4–5h is a **ceiling**, not a
quota to pad with passive video.

## Before you start
- Confirm the whiteboard, a phone/camera to record, and the printed desk stack
  (sheets 01/03/05/10/11 + booklet) are ready.
- Ask the mode: **full day** (~4–5h, all blocks) or **short** (~90 min = ritual + Block 1 + close).
- Draw today's problems **interleaved**: `just study-spaced 3`. Interleave topics;
  never block one topic for the whole day (Rohrer & Taylor 2007) unless the interview
  is explicitly single-topic.

## The blocks — announce each, time it, don't overrun

### 0 · Arrival ritual (10 min) — anxiety inoculation
Have Jess do, in order: **(a)** ~3 min slow diaphragmatic breathing, ~4–6 breaths/min
(Ma 2017); **(b)** ~5 min **expressive writing** — free-write the worries about the
interview, then set it aside (Ramirez & Beilock 2011); **(c)** one **reappraisal**
line out loud: *"my heart rate is my body getting me ready — I'm up for this"*
(Jamieson 2010; Brooks 2014, "I'm excited" beats "calm down"). Never say "just relax."

### 1 · Cold whiteboard reps (75–90 min) — retrieval + think-aloud, observed
Per drawn problem: `just interview <topic> <problem>` — **cold**: statement only,
solution stripped (retrieval practice beats rereading — Roediger & Karpicke 2006).
**Recording ON** (rehearse the exact social-evaluative condition — choking is worst
on under-practiced, working-memory-heavy problems, Beilock 2001/2004). Jess **stands**
and runs **CLARP out loud** (sheet 10 §2): Clarify → Lay out → Attack → Run → Polish.
YOUR job: watch, and every ~2 min interrupt — *"why did you do that?"* or add a
constraint. Concurrent narration does not impair solving (Ericsson & Simon 1980);
silence is lost signal. 2–4 problems.

### 2 · IDE close + verify (60–75 min) — make it actually run
Implement each board solution in the stripped file; `just study <topic>` until tests
pass. Jess narrates aloud where the typed version diverged from the board version and
why (shipping more working code that runs clean correlates with advancing —
interviewing.io). Then `just challenge-done <topic> <problem>` (feeds spaced
repetition — Cepeda 2006).

**— BREAK 15 min (a real break) —**

### 3 · Targeted input (30–45 min) — only what a rep exposed
Read today's rubric scores + logged misses. Pick exactly ONE: a single
mock-interview video matched to the weakness (Video Shelf in
`docs/guide/interview-practice-evidence.md`), OR 2–3 worked examples of the pattern
that cost the most (worked examples help for genuinely new patterns — Sweller 1988).
No passive playlist grinding.

### 4 · Observed mock (30–45 min; ~3×/week) — the real stressor
A full mock with a person — Ann early (she just watches and asks "why?"; hand her the
sheet 10 §5 rubric), a technical peer or an LLM interviewer later (Daryanto 2025).
Offer hints: **taking a hint is a positive signal, not a failure** (interviewing.io).

## Close every block
- **2 min** tape review, no more. Score the sheet 10 §5 rubric.
- `just rep "<topic>/<problem> C_ L_ A_ R_ P_ <one fix for tomorrow>"`.
- Name ONE thing to fix next rep. **Stop clean** — never grind past a bad rep.
  Panic training works by repeated recoveries, not by punishing the nervous system.

## Standing rules
- Interleave, not block. Cold-first, always. Out-loud, always. Record, always.
- One anti-panic reframe to repeat: a single nervous round is statistically normal
  even for strong candidates (interviewing.io) — it is a collaboration, not a verdict.
- **Public boundary:** never put employer/panel specifics, req numbers, or personal
  rep logs into this repo. This skill trains the general skill only; tailored prep
  lives in the private overlay.
