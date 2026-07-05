"""CI guard: fail if hand-typed doc counts drift from the code SSOT.

Same spirit as check_public_boundary.py — a cheap gate so the site's stated
counts (core drills, reference sheets, concept modules) can never silently
disagree with the source tree. Fix the doc text (or the SSOT) when this fails.
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from core42 import CORE_42  # noqa: E402

NUMBER_WORD = {9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen"}


def ssot_counts() -> dict[str, int]:
    algo = [f for f in glob.glob(str(ROOT / "src/algo/**/*.py"), recursive=True) if "__init__" not in f]
    concepts = [f for f in glob.glob(str(ROOT / "src/concepts/*.py")) if "__init__" not in f]
    sheets = glob.glob(str(ROOT / "reference-sheets/[0-9]*.md"))
    return {
        "drills": sum(len(v) for v in CORE_42.values()),
        "impls": len(algo),
        "concepts": len(concepts),
        "sheets": len(sheets),
    }

# (relative file, keyword anchoring the count, kind, ssot key)
DIGIT_CHECKS = [
    ("docs/index.md", "core drills", "drills"),
    ("docs/index.md", "core algorithms", "drills"),
    ("docs/index.md", "Concept Modules", "concepts"),
    ("docs/index.md", "Reference Sheets", "sheets"),
]
WORD_CHECKS = [
    ("docs/reference/index.md", "sheets"),
    ("docs/printables.md", "sheets"),
]


def main() -> int:
    c = ssot_counts()
    fails: list[str] = []

    for rel, kw, key in DIGIT_CHECKS:
        text = (ROOT / rel).read_text()
        want = c[key]
        m = re.search(rf"(\d+)\s+{re.escape(kw)}", text)
        if not m:
            fails.append(f'{rel}: no "<n> {kw}" phrase found (SSOT expects {want})')
        elif int(m.group(1)) != want:
            fails.append(f'{rel}: says "{m.group(1)} {kw}" but SSOT = {want}')

    for rel, key in WORD_CHECKS:
        text = (ROOT / rel).read_text()
        want = c[key]
        word = NUMBER_WORD.get(want, str(want))
        if not re.search(rf"\b{word}\b", text, re.IGNORECASE):
            fails.append(f'{rel}: expected the word "{word}" (SSOT sheets = {want}); count drifted')

    if fails:
        print("Doc-count drift (docs disagree with the code SSOT):", file=sys.stderr)
        for f in fails:
            print(f"  {f}", file=sys.stderr)
        print(f"  SSOT counts: {c}", file=sys.stderr)
        return 1

    print(f"Doc counts consistent with SSOT: {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
