---
title: Printables
---

# Printables

Everything in this packet that is meant to leave the screen and land on paper.
Use this page when you want to study away from a keyboard, or to assemble the
stack of sheets you carry into an interview.

!!! abstract "Two artifacts, one rule"
    There are exactly two printable surfaces here:

    1. **The full booklet** — one self-contained PDF with the decision trees,
       pattern tables, every algorithm (docstring + code), and the appendix.
    2. **The reference sheets** — compact handouts you can fan out
       on a desk.

    The rule: **bring the latest packet.** Both artifacts are *generated* from
    the source code and notes, so regenerate before any study block or interview
    loop with `just packet` (and `just pdf-all` for the sheets). The committed
    copies drift the moment you add an algorithm or edit a note.

---

## The full booklet

The single "bring everything" artifact, built fresh by `just packet`. It is the
most complete offline view of the repo.

[:material-download: Download the full booklet (PDF)](assets/booklet.pdf){ .md-button .md-button--primary }
[:material-eye: View it inline](assets/booklet.pdf){ .md-button }

**What's inside, in order:**

| Section | Contents |
|---------|----------|
| Title page + table of contents | Navigable structure for the whole packet |
| Decision trees & pattern pages | Problem-signal → pattern recognition, lifted from the reference sheets |
| One page per algorithm | Module docstring (problem, approach, complexity) plus the full code listing, for every implementation in `src/algo/` |
| Appendix | Interview topics that round out whiteboard coverage — concurrency, hashing internals, amortized analysis, recursion → iteration, numeric pitfalls — rendered compile-safely from `reference-sheets/appendix-topics.json` |

!!! note "Why the page count moves"
    The booklet emits **one page per algorithm**, so its length tracks the repo.
    Add a drill and the next `just packet` build is a page or two longer. Treat
    the current build as a snapshot, not a fixed page count — always reprint from
    a fresh build rather than reusing an old PDF.

<div markdown class="pdf-viewer">
<iframe src="assets/booklet.pdf" width="100%" height="800px" style="border: 1px solid #ccc; border-radius: 8px;"></iframe>
</div>

---

## Reference sheets

Focused handouts. Each links to the rendered page below; the same source
markdown (`reference-sheets/*.md`) compiles to standalone PDFs with
`just pdf-all`.

| # | Sheet | One-line description |
|---|-------|----------------------|
| 01 | [Python Standard Library](reference/01-python-stdlib.md) | `collections`, `itertools`, `functools`, `bisect`, `heapq` — the built-ins you reach for first |
| 02 | [Data Structures](reference/02-data-structures.md) | Operations and Big-O for every Python built-in type, plus trees, graphs, and heaps |
| 03 | [Algorithm Templates](reference/03-algorithm-templates.md) | Copy-ready templates: binary search, BFS/DFS, sliding window, backtracking, DP, and more |
| 04 | [Big-O Complexity](reference/04-big-o-complexity.md) | Time complexities ranked, input-size rules of thumb, amortized analysis |
| 05 | [Common Patterns](reference/05-common-patterns.md) | The compact problem-signal → pattern table — what to try first |
| 06 | [System Design](reference/06-system-design.md) | Load balancing, caching, message queues, database scaling, API design |
| 07 | [Interview Day Guide](reference/07-interview-day-guide.md) | Day-of logistics, communication framework, timing strategy, and what to have open |
| 08 | [Cross-Reference Guide](reference/08-cross-reference-guide.md) | Master lookup: problem description → implementation, decision tree, keyword cheat sheet |
| 09 | [Python 3.14 & Modern Patterns](reference/09-python-314-and-modern-patterns.md) | PEP 750 t-strings, PEP 649 lazy annotations, PEP 695 type syntax, Hypothesis, advanced typing |
| 10 | [Whiteboard Performance & Panic Protocol](reference/10-whiteboard-performance-protocol.md) | CLARP, panic recovery, collaboration scripts, self-review rubric |
| 11 | [14-Day Whiteboard Ramp](reference/11-14-day-whiteboard-ramp.md) | Day-by-day four-hour study loop for board + IDE practice |

!!! success "Download the sheet PDFs"
    Every sheet is served here as a print-ready PDF, rebuilt on each deploy from
    the same source markdown. Grab the ones you want:

    - [01 — Python Standard Library](assets/sheets/01-python-stdlib.pdf)
    - [02 — Data Structures](assets/sheets/02-data-structures.pdf)
    - [03 — Algorithm Templates](assets/sheets/03-algorithm-templates.pdf)
    - [04 — Big-O Complexity](assets/sheets/04-big-o-complexity.pdf)
    - [05 — Common Patterns](assets/sheets/05-common-patterns.pdf)
    - [06 — System Design](assets/sheets/06-system-design.pdf)
    - [07 — Interview Day Guide](assets/sheets/07-interview-day-guide.pdf)
    - [08 — Cross-Reference Guide](assets/sheets/08-cross-reference-guide.pdf)
    - [09 — Python 3.14 & Modern Patterns](assets/sheets/09-python-314-and-modern-patterns.pdf)
    - [10 — Whiteboard Performance & Panic Protocol](assets/sheets/10-whiteboard-performance-protocol.pdf)
    - [11 — 14-Day Whiteboard Ramp](assets/sheets/11-14-day-whiteboard-ramp.pdf)

    Building locally? `just pdf-all` writes the same set to
    `reference-sheets/pdf/`, and `just pdf <file>` converts a single sheet.

---

## Build it yourself

=== "Full booklet"

    ```bash
    just packet
    # → booklet.pdf  and  docs/assets/booklet.pdf (refreshed)
    ```

    Regenerates `booklet.tex` from current code and notes, compiles it with
    `tectonic`, and refreshes the copy embedded in this site.

=== "All reference sheets"

    ```bash
    just pdf-all
    # → reference-sheets/pdf/*.pdf
    ```

    Converts every `reference-sheets/*.md` to PDF via pandoc + tectonic.

=== "One sheet"

    ```bash
    just pdf reference-sheets/07-interview-day-guide.md
    # → reference-sheets/07-interview-day-guide.pdf
    ```

---

## Print tips

!!! tip "Make the paper work for you"
    - **Duplex (double-sided).** The booklet is one algorithm per page, so
      double-siding puts two related algorithms on each sheet and roughly halves
      the stack. Set the binding edge to long-edge for a booklet feel.
    - **Sheets are sized to print clean.** Several are explicitly paginated
      (stdlib and data structures are 2 pages, algorithm templates is 4) so each
      handout lands on whole sheets — print the sheets you want as a duplex set.
    - **Grayscale is fine.** PDFs use colored links for screen reading; nothing
      depends on color on paper.
    - **Reprint, don't reuse.** Run `just packet` (and `just pdf-all`) right
      before printing so the paper matches the current code.

### Recommended desk stack

The [Interview Day Guide](reference/07-interview-day-guide.md) prescribes a
print order. Put these on the desk, top to bottom:

1. **07 — Interview Day Guide** (top, for quick pattern lookup)
2. **01 — Python Standard Library**
3. **03 — Algorithm Templates**
4. **05 — Common Patterns**
5. **04 — Big-O Complexity**
6. **06 — System Design** (for a system-design round)

The full booklet sits beside the stack as the deep-reference fallback when a
sheet is not enough.

---

## Related

- [Interview Day Guide](reference/07-interview-day-guide.md) — the day-of runbook, including the print list above
- [When to Use What](guide/when-to-use-what.md) — the decision tree mapping problem signals to patterns
- [Cross-Reference Guide](reference/08-cross-reference-guide.md) — pattern → implementation lookup
- [Source of Truth](guide/source-of-truth.md) — how these artifacts are generated and kept reproducible
