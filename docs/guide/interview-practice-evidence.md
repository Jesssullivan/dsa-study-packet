---
title: Interview Practice Evidence
---

# Interview Practice Evidence

Use this page to decide what to do with a four-hour study block. The short
answer: do cold editor reps with comments, code, tests, and a trace; review a
little tape; then watch or read exactly what the rep exposed. Board work and
observed mocks are optional pressure variants. Do not turn video into a second
passive curriculum.

For senior technical interviews, bias every rep toward explicit assumptions,
constraints, traceability, verification, failure modes, and calm collaboration
under interruption. The target is not "I know LeetCode." The target is "I can
make my reasoning inspectable while the problem moves."

## How To Use This Page

The actual daily loop and calendar live in
[sheet 11](../reference/11-14-day-whiteboard-ramp.md). This page explains why
that loop is built from cold retrieval, think-aloud practice, observation
stress, tape review, interleaving, and short targeted refreshers.

If the day goes badly, do not extend the block. Stop with a clean next rep. Panic
training works by repeated recoveries, not by grinding until the nervous system
learns that the board is punishment.

## Why The Loop Works

Four to five hours is a **ceiling** of effortful deliberate practice, not a
quota to pad with passive video (Ericsson 1993). Sheet 11 turns that ceiling
into the actual daily schedule; `just practice-day <day>` renders it without a
second copy here.

The schedule interleaves retrieval instead of blocking one topic (Rohrer &
Taylor 2007), makes reasoning observable through comments and narration
(Ericsson & Simon 1980), verifies it with code and tests, and uses real breaks
to protect effort quality (Ericsson 1993). Targeted input comes only after a rep
exposes a specific miss (Sweller 1988). Optional observation adds pressure
practice without making every session a mock (Beilock 2001).

The `practice-day` skill routes the printed schedule. The interviewer closes
each editor rep with one fix and `just practice-finish`; an optional non-editor
rep closes once with `just rep-finish`.

## Video Shelf

| Need | Watch |
|------|-------|
| First-principles warm-up | [MIT 6.006 Lecture 1, Algorithmic Thinking and Peak Finding](https://www.youtube.com/watch?v=HtSuA80QTyo) |
| BFS / graph traversal miss | [MIT 6.006 Lecture 13, Breadth-First Search](https://www.youtube.com/watch?v=s-CYnVz-uh4) |
| Dynamic programming miss | [MIT 6.006 Lecture 19, Dynamic Programming I](https://www.youtube.com/watch?v=OQ5jsbhAv_M) |
| Graph depth beyond pattern memory | [William Fiset Graph Theory Playlist](https://www.youtube.com/playlist?list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93P) |
| Course-schedule/toposort walkthrough | [NeetCode: Course Schedule](https://www.youtube.com/watch?v=EgI5nU9etnU) |
| Coin-change DP walkthrough | [NeetCode: Coin Change](https://www.youtube.com/watch?v=H9bfqozjoqs) |
| Think-aloud mock interview | [Life at Google: How to solve a Google coding interview question](https://www.youtube.com/watch?v=Ti5vfu9arXQ) |
| Classic whiteboard interview shape | [How to: Work at Google - Example Coding/Engineering Interview](https://www.youtube.com/watch?v=XKu_SEDAykw) |

Watch with a job: pause after the problem statement, run CLARP yourself, then
compare. If the video becomes entertainment, close it and do another cold rep.

### Watch a real interview narrated (think-aloud demos)

For observed-practice prep, study *how* strong candidates keep reasoning visible,
take hints, and recover when stuck. Every URL was confirmed live. Watch one,
then do your own recorded rep in the same shape.

| Need | Watch |
|------|-------|
| The canonical think-out-loud arc (restate → example → approach → code → analyze) | [How to: Work at Google: Example Coding Interview](https://www.youtube.com/watch?v=XKu_SEDAykw) (Life at Google) |
| Continuous narration in a real mock | [Mock Google Coding Interview with a Meta Intern](https://www.youtube.com/watch?v=46dZH7LDbf8) (NeetCode) |
| Coached intake ritual + verbalizing | [Google Coding Interview With A High School Student](https://www.youtube.com/watch?v=qz9tKlF431k) (Clément Mihailescu) |
| Getting stuck and recovering gracefully | [Google Coding Interview With A Normal Software Engineer](https://www.youtube.com/watch?v=rw4s4M3hFfs) (Clément Mihailescu) |
| Authentic anonymous mock + hint-taking | [Python interview with an interviewing.io engineer](https://www.youtube.com/watch?v=mDYOy7k8kOQ) (interviewing.io) |
| Meta-skills: communicate, manage getting stuck | [How To Pass Your Coding Interviews](https://www.youtube.com/watch?v=z3h0JGANLoI) (Nick White + Clément Mihailescu) |
| Early-career structured intake | [Mock Coding Interview with a Student](https://www.youtube.com/watch?v=jfg5WMYqA48) (Cracking FAANG) |
| Brute-force-then-optimize aloud, from the CtCI author | [Cracking the Coding Interview: Gayle Laakmann McDowell](https://www.youtube.com/watch?v=aClxtDcdpsQ) (Dice) |

## Research Backing

| Practice rule | Source |
|---------------|--------|
| Four hours is a ceiling for effortful deliberate practice, not a minimum to pad with passive study. | [Ericsson, Krampe, and Tesch-Romer, 1993, deliberate practice](https://gwern.net/doc/psychology/writing/1993-ericsson.pdf) |
| Verbalized reasoning is useful process data. In practice: say the next inference, not a polished lecture. | [Ericsson and Simon, 1980, verbal reports](https://acs.ist.psu.edu/ist597/papers/ericssonS80.pdf) |
| Think-aloud is a separate skill from solving; practice should simulate speaking while solving. | [Daryanto et al., 2025, technical-interview think-aloud practice](https://arxiv.org/pdf/2507.14418v1) |
| Spoken reasoning traces expose process, not just final answers. That is why tape review matters. | [Wurgaft et al., 2025, scaling the think-aloud method](https://arxiv.org/pdf/2505.23931v1) |
| Whiteboard interviews under observation can increase stress and cognitive load; practice should include a camera or person. | [Behroozi et al., 2020, technical-interview stress](https://par.nsf.gov/servlets/purl/10196170) |
| Technical interviewers evaluate communication and walkthrough quality, not just code arrival. | [Ford et al., 2017, interviewer expectations](https://www.microsoft.com/en-us/research/publication/the-tech-talk-balance-what-technical-interviewers-expect-from-technical-candidates/) |
| Retrieval beats rereading for durable memory. Cold reps are not assessment theater; they are learning. | [Roediger and Karpicke, 2006, test-enhanced learning](https://pubmed.ncbi.nlm.nih.gov/16507066/) |
| Interleaving helps when the task is choosing a strategy from the prompt, not repeating a known pattern block. | [Interleaved practice study, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589969/) |
| Worked examples help early, but only as a bridge back to active solving. | [MIT Teaching + Learning Lab on worked examples](https://tll.mit.edu/teaching-resources/how-people-learn/worked-examples/) |
| Writing worries before a high-pressure test can reduce intrusive thoughts. | [Ramirez and Beilock, 2011, PubMed](https://pubmed.ncbi.nlm.nih.gov/21233387/) |
| Reappraising stress arousal can improve performance-relevant stress responses. | [Jamieson, Nock, and Mendes, 2012, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3410434/) |
| Interviewers explicitly advise structured preparation and clear discussion of your role, work, and problem solving. | [Google Careers interview tips](https://www.google.com/about/careers/applications/interview-tips/) |
| Pressure hurts most on under-practiced, working-memory-heavy problems. So over-practice core patterns to automaticity, and rehearse under the exact social-evaluative condition (camera/person). | [Beilock and Carr, 2001, choking under pressure](https://doi.org/10.1037/0096-3445.130.4.701) |
| Reappraising nerves *as excitement* ("I'm excited") outperforms trying to calm down. Use a one-second opener before the room. | [Brooks, 2014, get excited](https://doi.org/10.1037/a0035325) |
| Coding interviews score explicit dimensions: communication, problem-solving, technical competency, and testing. Silence and unexplained work cost you directly, independent of the final answer. | [Tech Interview Handbook, coding rubrics](https://www.techinterviewhandbook.org/coding-interview-rubrics/) |
| Taking a hint is a positive signal, and a single nervous round is statistically normal even for strong candidates. Talk to keep the process visible, not to sound polished. *(The hint statistic reflects candidates' desire to advance, a rapport proxy, not a literal hire vote.)* | [interviewing.io, what the best interviews have in common](https://interviewing.io/blog/best-technical-interviews-common) |

## What Not To Do

- Do not watch broad playlists before you have a logged miss.
- Do not drill one topic for four hours unless the interview is explicitly about
  that topic. Mixed draws are closer to the real task.
- Do not optimize for silent speed. Optimize for clarify -> plan -> implement ->
  trace -> complexity while interrupted.
- Do not let the public packet absorb employer-specific prep. People, panels,
  clearance facts, and private sponsor context belong in downstream overlays.
