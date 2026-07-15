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
        filled = block[0] != seed or len(block) > 1
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
