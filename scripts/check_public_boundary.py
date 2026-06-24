"""Fail if private prep material leaks into the public packet tree."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()

FORBIDDEN_PATH_SUFFIXES = (
    ".sops.yaml",
    ".sops.yml",
    ".sops.json",
)

FORBIDDEN_CONTENT = (
    ("old Codespaces token name", re.compile(re.escape("GH_" + "CODESPACES_TOKEN"))),
    (
        "old age recipient",
        re.compile(
            re.escape(
                "age1" + "wc2s9pfju7haufdw0at0pm2cxx9rs9qmj80nf0nzy82w0fr0gp3skzfgds"
            )
        ),
    ),
    ("legacy ASI repo name", re.compile(re.escape("DSA-study-" + "ASI"))),
    ("private resume repo name", re.compile(r"\bspear[_-]resumes\b")),
    ("private MITRE marker", re.compile(r"\bMITRE\b")),
    ("private SCEPTER marker", re.compile(r"\bSCEPTER\b")),
    ("private ASI marker", re.compile(r"\bASI\b")),
    ("private CRA marker", re.compile(r"\bCRA\b")),
    ("private STR marker", re.compile(r"\bSTR\b")),
)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [path for path in result.stdout.decode().split("\0") if path]


def read_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode()
    except UnicodeDecodeError:
        return None


def main() -> int:
    failures: list[str] = []

    for rel in tracked_files():
        lowered = rel.lower()
        if lowered.endswith(FORBIDDEN_PATH_SUFFIXES):
            failures.append(f"{rel}: tracked SOPS secret file is not public-safe")

        if rel == SELF:
            continue

        text = read_text(ROOT / rel)
        if text is None:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern in FORBIDDEN_CONTENT:
                if pattern.search(line):
                    failures.append(f"{rel}:{line_no}: {label}: {line.strip()}")

    if failures:
        print("Public boundary check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("Public boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
