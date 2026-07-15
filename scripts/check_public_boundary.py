"""Fail if private prep material leaks into the public packet tree.

This public guard enforces *structural* rules only: secret-shaped content and
secret-file paths that are never public-safe, regardless of whose they are.
Name-specific tripwires (employers, panels, private repo names) are enforced
from the private downstream repo, which scans this tree with its own marker
list, so the public guard cannot itself disclose what it guards against.
"""

from __future__ import annotations

import io
import os
import re
import subprocess
import sys
from collections import defaultdict
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


def tracked_index_texts() -> dict[str, tuple[str, ...]]:
    """Return every text blob currently present in the Git index by path.

    Reading the index separately matters when a staged file differs from, or
    has been deleted from, the working tree. ``git cat-file --batch`` keeps the
    guard fast while still handling symlink blobs and conflicted index stages.
    """
    result = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    paths: list[str] = []
    entries: list[tuple[str, str]] = []
    for raw_entry in result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        metadata, raw_path = raw_entry.split(b"\t", 1)
        mode, object_id, _stage = metadata.decode("ascii").split()
        rel = os.fsdecode(raw_path)
        paths.append(rel)
        # A gitlink points at a commit, not a file blob. Keep its path for the
        # structural rules, but there is no file content for this guard to read.
        if mode != "160000":
            entries.append((rel, object_id))

    texts: defaultdict[str, list[str]] = defaultdict(list)
    for rel in paths:
        texts[rel]
    if not entries:
        return {rel: tuple(versions) for rel, versions in texts.items()}

    blobs = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        check=True,
        input="".join(f"{object_id}\n" for _, object_id in entries).encode(),
        stdout=subprocess.PIPE,
    ).stdout
    stream = io.BytesIO(blobs)
    for (rel, expected_id) in entries:
        header = stream.readline().decode("ascii").rstrip("\n").split()
        if len(header) != 3 or header[0] != expected_id or header[1] != "blob":
            raise RuntimeError(f"unexpected git cat-file response for {rel}")
        size = int(header[2])
        data = stream.read(size)
        if len(data) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated git cat-file response for {rel}")
        text = decode_text(data)
        if text is not None and text not in texts[rel]:
            texts[rel].append(text)

    return {rel: tuple(versions) for rel, versions in texts.items()}


def decode_text(data: bytes) -> str | None:
    if b"\0" in data:
        return None
    try:
        return data.decode()
    except UnicodeDecodeError:
        return None


def read_text(path: Path) -> str | None:
    # A tracked symlink's git blob is its target string, not the target's
    # contents (which may be a directory, e.g. .agents/skills/* skill
    # symlinks). Read the link itself so this stays a structural check.
    if path.is_symlink():
        return os.readlink(path)
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        # The caller scans the index separately, so a missing working-tree
        # copy does not omit staged or committed content.
        return None
    return decode_text(data)


def main() -> int:
    failures: list[str] = []

    for rel, index_texts in tracked_index_texts().items():
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

        working_text = read_text(ROOT / rel)
        versions = list(index_texts)
        if working_text is not None and working_text not in versions:
            versions.append(working_text)

        for text in versions:
            for line_no, line in enumerate(text.splitlines(), start=1):
                for label, pattern in FORBIDDEN_CONTENT:
                    if pattern.search(line):
                        failure = f"{rel}:{line_no}: {label}: {line.strip()}"
                        if failure not in failures:
                            failures.append(failure)

    if failures:
        print("Public boundary check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print("Public boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
