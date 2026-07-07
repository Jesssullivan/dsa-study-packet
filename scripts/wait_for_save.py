"""Block until a file is saved, then exit — the rung-2 turn-taking primitive.

Kind by construction: reacts to a save event only, never inspects keystrokes
or the editor buffer. The candidate's save is the explicit "your turn" signal.

Exit codes: 0 = save detected · 2 = timeout (candidate stepped away) · 1 = error.

Re-stats the PATH (not a held descriptor) each poll, so atomic saves
(temp-file + rename, as VS Code and vim do) are seen: the path picks up the
new inode/mtime. Compares mtime+size+inode, not a content hash — a dirty save
with unchanged content still bumps mtime and still means "your turn".
"""

from __future__ import annotations

import argparse
import os
import sys
import time

Snapshot = tuple[int, int, int] | None


def snap(path: str) -> Snapshot:
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return None
    return (st.st_mtime_ns, st.st_size, st.st_ino)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="seconds to wait before giving up (keep under any harness cap)",
    )
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    base = snap(args.file)
    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        time.sleep(args.interval)
        current = snap(args.file)
        if current is not None and current != base:
            print(args.file)
            return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
