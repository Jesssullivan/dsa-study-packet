"""Clean-checkout contracts for the cache-compatible Bazel front door."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _write_executable(path: Path, body: str) -> None:
    path.write_text(f"#!/bin/sh\nset -eu\n{body}\n")
    path.chmod(0o755)


@pytest.mark.parametrize(
    ("recipe", "targets", "bazel_action"),
    [
        ("remote-compile", (), "build //:booklet"),
        ("remote-build", ("//...",), "build //..."),
        ("remote-test", ("//:booklet_smoke",), "test //:booklet_smoke"),
        ("remote-test", ("//...",), "test //..."),
    ],
)
def test_remote_frontdoors_generate_before_bazel(
    tmp_path: Path,
    recipe: str,
    targets: tuple[str, ...],
    bazel_action: str,
) -> None:
    (tmp_path / "justfile").write_text((ROOT / "justfile").read_text())
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    trace = tmp_path / "trace"
    fake_bazel = bin_dir / "bazel"
    _write_executable(
        bin_dir / "uv",
        'printf "uv %s\\n" "$*" >> "$TRACE"',
    )
    _write_executable(
        fake_bazel,
        'printf "bazel %s\\n" "$*" >> "$TRACE"',
    )
    env = {
        **os.environ,
        "BAZEL_BIN": str(fake_bazel),
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "TRACE": str(trace),
    }

    completed = subprocess.run(
        [
            "just",
            "--justfile",
            str(tmp_path / "justfile"),
            "--working-directory",
            str(tmp_path),
            recipe,
            *targets,
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert completed.returncode == 0, completed.stderr
    assert trace.read_text().splitlines() == [
        "uv run python scripts/gen_booklet.py",
        f"bazel {bazel_action}",
    ]
