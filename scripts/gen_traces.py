"""Generate algorithm-visualizer traces (SSOT frame data) into docs/assets/traces/.

Each trace narrates an algorithm on a FIXED input as frames the generic player
(docs/assets/js/visualizer.js) renders. Every trace carries a `verify` block;
tests/test_traces.py runs the REAL implementation on the same input and asserts
the narrated result matches — so a narration cannot drift from the code.

Adding an algorithm = adding a trace function here (data), not touching the player.
Run: python scripts/gen_traces.py   (or `just traces`)
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "traces"


def _frame(caption: str, structures: list[dict]) -> dict:
    return {"caption": caption, "structures": structures}


def trace_binary_search() -> dict:
    nums = [1, 3, 4, 7, 9, 11, 15, 20]
    target = 11
    frames: list[dict] = []

    def window(extra: dict | None = None) -> dict:
        s = {
            "name": "nums",
            "kind": "array",
            "data": list(nums),
            "highlight": [],
            "pointers": {"lo": lo, "hi": hi},
        }
        if extra:
            s["pointers"].update(extra.get("pointers", {}))
            s["highlight"] = extra.get("highlight", [])
        return s

    lo, hi, result = 0, len(nums) - 1, -1
    frames.append(_frame(
        f"Search for {target} in a sorted array. Window lo={lo}, hi={hi}.",
        [window(), {"name": "state", "kind": "vars", "data": {"target": target}}],
    ))
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        frames.append(_frame(
            f"mid = {mid}; compare nums[{mid}] = {nums[mid]} with target {target}.",
            [window({"pointers": {"mid": mid}, "highlight": [mid]}),
             {"name": "state", "kind": "vars", "data": {"target": target}}],
        ))
        if nums[mid] == target:
            result = mid
            frames.append(_frame(
                f"nums[{mid}] == {target} — found at index {mid}.",
                [{"name": "nums", "kind": "array", "data": list(nums),
                  "highlight": [mid], "pointers": {"mid": mid}}],
            ))
            break
        if nums[mid] < target:
            lo = mid + 1
            frames.append(_frame(
                f"nums[{mid}] < {target} — discard left half, search right (lo={lo}).",
                [window()],
            ))
        else:
            hi = mid - 1
            frames.append(_frame(
                f"nums[{mid}] > {target} — discard right half, search left (hi={hi}).",
                [window()],
            ))

    return {
        "algorithm": "binary_search",
        "title": "Binary Search",
        "input": f"nums={nums}, target={target}",
        "result": result,
        "verify": {
            "import": "algo.searching.binary_search",
            "func": "binary_search",
            "args": [nums, target],
            "expected": result,
        },
        "frames": frames,
    }


TRACES: dict[str, Callable[[], dict]] = {
    "binary_search": trace_binary_search,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in TRACES.items():
        trace = fn()
        (OUT / f"{name}.json").write_text(json.dumps(trace, indent=2))
        print(f"wrote {name}.json ({len(trace['frames'])} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
