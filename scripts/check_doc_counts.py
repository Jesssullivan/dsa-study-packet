"""CI guard: fail if hand-typed doc counts drift from the code SSOT.

The public docs are allowed to avoid counts entirely. If they do state a count,
it must match the source tree; the generated `just catalog` surface must always
match.
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import catalog  # noqa: E402
from core42 import CORE_42  # noqa: E402

NUMBER_WORD = {
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
}


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
    ("docs/index.md", "core problems", "drills"),
    ("docs/index.md", "core algorithms", "drills"),
    ("docs/index.md", "Concept Modules", "concepts"),
    ("docs/index.md", "Reference Sheets", "sheets"),
    ("README.md", "core problems", "drills"),
    ("README.md", "Reference Sheets", "sheets"),
]
WORD_CHECKS = [
    ("docs/reference/index.md", "sheets"),
    ("docs/printables.md", "sheets"),
]


def main() -> int:
    c = ssot_counts()
    fails: list[str] = []

    catalog_counts = {
        "drills": catalog.core_count(),
        "impls": catalog.implementation_count(),
        "concepts": catalog.concept_count(),
        "sheets": catalog.reference_sheet_count(),
    }
    if catalog_counts != c:
        fails.append(f"just catalog counts {catalog_counts} but SSOT = {c}")

    for rel, kw, key in DIGIT_CHECKS:
        text = (ROOT / rel).read_text()
        want = c[key]
        for m in re.finditer(rf"(\d+)\s+{re.escape(kw)}", text):
            if int(m.group(1)) != want:
                fails.append(f'{rel}: says "{m.group(1)} {kw}" but SSOT = {want}')

    for rel, key in WORD_CHECKS:
        text = (ROOT / rel).read_text()
        want = c[key]
        for value, word in NUMBER_WORD.items():
            if value == want:
                continue
            if re.search(
                rf"\b{word}\b[^\n.]*\b(sheets|handouts)\b",
                text,
                re.IGNORECASE,
            ):
                fails.append(
                    f'{rel}: says "{word}" sheets/handouts but SSOT = {want}'
                )

    if fails:
        print("Doc-count drift (docs disagree with the code SSOT):", file=sys.stderr)
        for f in fails:
            print(f"  {f}", file=sys.stderr)
        print(f"  SSOT counts: {c}", file=sys.stderr)
        return 1

    print(f"Doc count guard passed; generated catalog matches SSOT: {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
