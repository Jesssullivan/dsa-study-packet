"""Presence-gate an editor-practice scaffold: which sections are filled, and is
coding still locked?

Working-tree agent tool only. NEVER wire into `just lint` or CI: the scaffold
deliberately contains `raise NotImplementedError`, which `check_no_stubs.py`
rightly rejects in committed code.

Presence, not correctness: a section counts as "filled" when the candidate
changed its seed line or wrote anything beneath it. The content is the
interviewer's to read, not this script's to judge.

Usage:
    python scripts/scaffold_status.py src/algo/arrays/two_sum.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_solution import LOCK_SENTINEL, SCAFFOLD_SEEDS

PLACEHOLDERS = frozenset({"answer", "fill here", "placeholder", "tbd", "todo"})


def _meaningful_comment(text: str) -> bool:
    normalized = text.removeprefix("#").strip().lower()
    return (
        any(character.isalnum() for character in normalized)
        and normalized not in PLACEHOLDERS
    )


def section_status(
    text: str,
    seeds: tuple[str, ...] = SCAFFOLD_SEEDS,
    lock_sentinel: str = LOCK_SENTINEL,
) -> dict[str, str]:
    labels = tuple(seed.split(":", 1)[0].removeprefix("# ") for seed in seeds)
    lines = [line.strip() for line in text.splitlines()]
    markers = tuple(f"# {label}:" for label in labels)
    status: dict[str, str] = {}
    for label, seed, marker in zip(labels, seeds, markers, strict=True):
        starts = [i for i, line in enumerate(lines) if line.startswith(marker)]
        if not starts:
            status[label] = "missing"
            continue
        start = starts[0]
        block = [lines[start]]
        for line in lines[start + 1 :]:
            if line.startswith(markers) or line == lock_sentinel:
                break
            # Once the candidate unlocks, executable code follows the final
            # marker. It is not evidence that the final reasoning comment was
            # filled in.
            if line and not line.startswith("#"):
                break
            if line:
                block.append(line)
        seed_text = seed.removeprefix(marker).strip()
        prompt_text = block[0].removeprefix(marker).strip()
        inline_answer = prompt_text != seed_text and _meaningful_comment(prompt_text)
        continuation_answer = any(_meaningful_comment(line) for line in block[1:])
        filled = inline_answer or continuation_answer
        status[label] = "filled" if filled else "empty"
    return status


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <source_file>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        return 1
    text = path.read_text()
    for label, state in section_status(text).items():
        print(f"{label}: {state}")
    print(f"lock: {'locked' if LOCK_SENTINEL in text else 'unlocked'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
