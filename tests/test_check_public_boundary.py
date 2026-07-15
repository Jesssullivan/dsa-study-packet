"""Working-tree edge cases for the public-boundary guard."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_public_boundary import (  # type: ignore[import-not-found]
    read_text,
)


def test_pending_tracked_deletion_has_no_content_to_scan(tmp_path: Path) -> None:
    assert read_text(tmp_path / "deleted-file") is None
