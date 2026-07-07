# Whiteboard Performance & Panic Protocol

The other reference sheets train *what you know*. This one trains *what you do
while someone is watching you think* — the part that decides whiteboard,
live-coding, and "talk me through it" rounds. It is written for people who
know more than they can show under observation, and who panic.

Core premise: **these rounds do not score a correct answer. They score
observable signals of how you work.** Panic makes you go silent and chase the
answer; the fix is to run a loud, visible *process* you can execute even while
scared. The process is a checklist. You can run a checklist with shaking hands.

This sheet is the **method**. The day-by-day calendar and daily loop live in
[sheet 11](11-14-day-whiteboard-ramp.md).

---

## 1. What is actually being scored

An interviewer leaves the room grading five signals, roughly in this order:

1. **Problem intake** — did you clarify before coding? (constraints, examples, edge cases)
2. **Communication** — could they follow your thinking out loud? Silence = lost signal.
3. **Collaboration** — did you take hints, ask, and adjust *with* them (a coworker), or perform *at* them?
4. **Correctness under your own test** — did you trace your code on an example and find your own bugs?
5. **Complexity awareness** — do you know what your solution costs and what's better?

Note what is **not** on the list: solving it fast, solving it alone, solving it
without hints, an optimal answer on the first try. A candidate who narrates a
brute force, states its cost, and improves it *with* the interviewer outscores a
silent candidate who types the optimal answer. **Your job is to make your
thinking visible, not to be a genius in silence.**

> Reframe to carry in: *"I am not being tested. I am pair-programming with a
> colleague on a problem neither of us has open-sourced yet."* That is literally
> the thing they are hiring for.

---

## 2. The loop: CLARP (say each header out loud)

A five-phase spine. Announce the phase you're in ("Okay — clarifying first").
Announcing the phase *is* the communication signal, and it buys you thinking time.

| Phase | Out loud | On the board |
|-------|----------|--------------|
| **C — Clarify** | "Let me make sure I have the problem. Input is…, output is…, and can I assume…?" | Write the signature + 1 example I/O + constraints |
| **L — Lay out** | "Brute force first so we have something correct: … That's O(n²). I think we can do better with …" | Write the approach in 3–4 plain-English bullets before any code |
| **A — Attack** | "I'll implement the hash-map version. Let me talk as I go." | Code the bullets, top to bottom |
| **R — Run** | "Let me trace this on `[2,7,11]`, target 9." | Walk the example line by line, updating variable values on the board |
| **P — Polish** | "Time is O(n), space O(n). Edge cases: empty input, no solution, duplicates." | Note complexity + the edge cases you handled |

The order is load-bearing. **Never skip C and L to start coding** — jumping to
code is the single most common panic tell and it forfeits signals 1 and 2. Two
minutes of clarifying out loud is never wasted.

---

## 3. Panic first-aid (when your mind goes blank)

Grounded in evidence-based performance-anxiety techniques (diaphragmatic
breathing; "expressive writing" to clear the blank; narrative over abstraction):

1. **Board-dump on arrival (expressive writing).** Before the problem, in the
   first 30 seconds, write your templates in a corner of the board: the CLARP
   headers, and 2–3 pattern skeletons you rehearse (binary-search bounds; BFS
   queue; hash-map counting). This externalizes memory so panic can't erase it —
   the formulas are already on the wall.
2. **One physiological breath.** A slow exhale-longer-than-inhale breath (in 4,
   out 6) once, deliberately. It is the fastest way to drop the adrenaline spike
   enough to speak. Practice it so it's automatic, not a thing you forget.
3. **Narrate the stuck, don't hide it.** Say the true sentence: *"I'm blanking
   for a second — let me re-read the problem and think out loud."* This reads as
   composure, not failure, and it re-opens collaboration (often the interviewer
   nudges).
4. **Shrink the problem.** Solve `n = 1`, then `n = 2`, by hand on the board.
   Almost every algorithm is visible in the tiny case. This is the "narrative"
   move — a concrete story instead of abstract numbers.
5. **Fall back to correct-and-slow.** A working brute force you can state the
   cost of beats an optimal solution you can't finish. Ship it, then optimize.

Rule: **a stuck moment narrated is a passing moment; a stuck moment gone silent
is a failing one.** The panic is not the problem — going quiet is.

---

## 4. Asking questions & working synchronously (the collaboration signal)

These are the exact scripts. Use them verbatim until they're yours.

**Clarifying (before coding — always ask ≥2):**
- "Can I assume the input fits in memory / is already sorted / has no duplicates?"
- "What should I return on an empty input or when there's no valid answer?"
- "Are we optimizing for time, or is space tight here too?"

**Taking a hint (this is a *positive* signal — accept, don't defend):**
- "That's a good nudge — let me follow it. So if I use a heap instead of sorting…"
- Never argue with a hint. The interviewer is telling you the answer they want to see you reach *with* them.

**Thinking out loud without rambling (narrate decisions, not keystrokes):**
- Good: "I'm choosing a hash map here so lookups are O(1) instead of scanning."
- Skip: reading each character you type.

**When you disagree or see a tradeoff (shows seniority):**
- "We could sort for simplicity, O(n log n), or use a heap for O(n log k) if k is small — which matters more here?"

**Checking in (makes it synchronous):**
- "Does this approach match what you had in mind before I code it?"
- "Want me to handle the duplicate case now or note it and move on?"

---

## 5. Self-review rubric (grade each rep 0–2)

The daily loop and calendar live in sheet 11. After each rep, watch **two
minutes** of the tape — no more — and score yourself. The camera is the
training stressor: it manufactures the "someone is watching" pressure you are
desensitizing to.

| Signal | 0 | 1 | 2 |
|--------|---|---|---|
| Talked continuously | long silences | some gaps | narrated throughout |
| Clarified before coding | jumped to code | one question | ≥2, wrote example first |
| Traced own code | didn't | partially | full trace, found issues |
| Stated complexity | forgot | time only | time + space + edge cases |
| Composure | visible spiral | recovered slowly | named it, breathed, continued |

Target: not a perfect 10, just **+1 on your weakest row each day.** Two weeks of
+1 is a transformed interview. Log one line per rep (`just rep "…"`) and note
ONE thing to fix next rep.

---

## 6. Get a human in the loop

The camera desensitizes you to being observed; a person desensitizes you to
being *interrupted and judged*. Both are the real stressor, split in two.

- **A friendly practice partner** (e.g. a family member willing to Zoom) is
  perfect early on: they don't need to know the CS. Their job is to *watch you
  present and interrupt with "why did you do that?"* — that alone trains
  composure and narration. Hand them the §5 rubric to grade you.
- **A technical mock** (peer, or an AI interviewer) once the reflex exists:
  someone who can throw a real hint or a follow-up constraint mid-problem.
- Rotate stressors so no single format stays scary.

---

## 7. Interview-morning version (the one-page panic card)

1. Board-dump templates + CLARP headers in the corner first thing.
2. One slow breath (in 4, out 6) before you touch the marker.
3. Clarify out loud — ask two questions before any code.
4. Brute force first, state its cost, *then* optimize.
5. Narrate decisions, not keystrokes. Silence = lost points.
6. Trace your code on a tiny example. Find your own bug.
7. Blanking? Say so, breathe, shrink to n=1. Stuck-and-talking passes.
8. It's a colleague and a problem, not a test and a judge.

## 8. Research backing

The web guide carries the evidence and video shelf:
`docs/guide/interview-practice-evidence.md`.
