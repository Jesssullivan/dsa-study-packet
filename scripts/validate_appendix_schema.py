"""CI guard: validate reference-sheets/appendix-topics.json.

The appendix is authored as structured data and rendered into the booklet by
gen_booklet._gen_appendix_pages(). A malformed entry (missing section_title,
wrong field types, over-wide table rows) would silently break LaTeX rendering;
this validates the structure the renderer relies on.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "reference-sheets" / "appendix-topics.json"


def _check_topic(index: int, topic: Any, errs: list[str]) -> None:
    where = f"topic[{index}]"
    if not isinstance(topic, dict):
        errs.append(f"{where}: must be an object")
        return

    title = topic.get("section_title")
    if not isinstance(title, str) or not title.strip():
        errs.append(f"{where}: section_title must be a non-empty string")
    where = title if isinstance(title, str) and title.strip() else where

    if "summary" in topic and not isinstance(topic["summary"], str):
        errs.append(f"{where}: summary must be a string")

    for key in ("key_points", "pitfalls"):
        if key in topic:
            val = topic[key]
            if not isinstance(val, list) or any(not isinstance(x, str) for x in val):
                errs.append(f"{where}: {key} must be a list of strings")

    for tbl in topic.get("tables", []) or []:
        header = tbl.get("header") if isinstance(tbl, dict) else None
        rows = tbl.get("rows") if isinstance(tbl, dict) else None
        if not isinstance(header, list) or not isinstance(rows, list):
            errs.append(f"{where}: each table needs a list 'header' and list 'rows'")
            continue
        ncol = len(header)
        for row in rows:
            if not isinstance(row, list):
                errs.append(f"{where}: table row must be a list")
            elif len(row) > ncol:
                errs.append(f"{where}: table row has {len(row)} cells > header {ncol}")

    for cb in topic.get("code_blocks", []) or []:
        if not isinstance(cb, dict) or not isinstance(cb.get("code"), str):
            errs.append(f"{where}: each code_block needs a string 'code'")


def main() -> int:
    if not DATA.exists():
        print(f"{DATA} missing", file=sys.stderr)
        return 1
    try:
        topics = json.loads(DATA.read_text())
    except json.JSONDecodeError as exc:
        print(f"appendix-topics.json invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(topics, list) or not topics:
        print("appendix-topics.json must be a non-empty list", file=sys.stderr)
        return 1

    errs: list[str] = []
    for i, topic in enumerate(topics):
        _check_topic(i, topic, errs)

    if errs:
        print("appendix-topics.json validation FAILED:", file=sys.stderr)
        for line in errs:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"appendix-topics.json valid ({len(topics)} topics).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
