"""Fail if private prep material leaks into the public packet tree.

This public guard enforces *structural* rules only: secret-shaped content and
secret-file paths that are never public-safe, regardless of whose they are.
Name-specific tripwires (employers, panels, private repo names) are enforced
from the private downstream repo, which scans this tree with its own marker
list — so the public guard cannot itself disclose what it guards against.
"""

from __future__ import annotations

import os
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

# Tracked dotenv files are never public-safe; documented examples are.
ALLOWED_ENV_BASENAMES = frozenset({".env.example", ".env.sample", ".env.template"})

FORBIDDEN_CONTENT = (
    ("old Codespaces token name", re.compile(re.escape("GH_" + "CODESPACES_TOKEN"))),
    ("age recipient", re.compile(r"\bage1[0-9a-z]{58}\b")),
    ("age secret key", re.compile(r"AGE-SECRET-KEY-1[0-9A-Z]+")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
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
    # A tracked symlink's git blob is its target string, not the target's
    # contents (which may be a directory, e.g. .agents/skills/* skill
    # symlinks) — read the link itself so this stays a structural check.
    if path.is_symlink():
        return os.readlink(path)
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

        basename = lowered.rsplit("/", 1)[-1]
        if (
            basename == ".env" or basename.startswith(".env.")
        ) and basename not in ALLOWED_ENV_BASENAMES:
            failures.append(f"{rel}: tracked dotenv file is not public-safe")

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
