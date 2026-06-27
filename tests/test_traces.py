"""Anti-drift guard for visualizer traces.

Each trace narrates an algorithm; this asserts the narrated final result equals
the real implementation's output on the same input, so a trace cannot silently
diverge from the code it visualizes.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS))

import gen_traces  # noqa: E402


def test_traces_registered() -> None:
    assert gen_traces.TRACES, "no visualizer traces registered"


def test_each_trace_matches_implementation() -> None:
    for name, build in gen_traces.TRACES.items():
        trace = build()
        assert trace.get("frames"), f"{name}: trace has no frames"
        v = trace["verify"]
        impl = getattr(importlib.import_module(v["import"]), v["func"])
        assert impl(*v["args"]) == v["expected"], f"{name}: narration drifted from implementation"
