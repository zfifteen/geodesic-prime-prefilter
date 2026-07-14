"""Save plot outputs and sidecar metadata."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import out_dir_for


def _git_head(repo_root: Path) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def save_figure(
    fig: Any,
    entry_id: str,
    *,
    filename: str = "plot.png",
    dpi: int = 160,
    meta: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> Path:
    """Save a matplotlib figure and write meta.json beside it."""
    out_dir = out_dir_for(entry_id)
    path = out_dir / filename
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    payload = {
        "entry_id": entry_id,
        "filename": filename,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dpi": dpi,
    }
    if repo_root is not None:
        head = _git_head(repo_root)
        if head:
            payload["git_head"] = head
    if meta:
        payload.update(meta)
    (out_dir / "meta.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def copy_legacy_asset(
    source: Path,
    entry_id: str,
    *,
    filename: str = "plot.png",
    meta: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> Path:
    """Copy a committed legacy PNG into library out/ and write meta."""
    import shutil

    if not source.is_file():
        raise FileNotFoundError(f"Legacy asset missing: {source}")
    out_dir = out_dir_for(entry_id)
    dest = out_dir / filename
    shutil.copy2(source, dest)
    payload = {
        "entry_id": entry_id,
        "filename": filename,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "provenance": "legacy-copy",
        "source": str(source),
    }
    if repo_root is not None:
        head = _git_head(repo_root)
        if head:
            payload["git_head"] = head
    if meta:
        payload.update(meta)
    (out_dir / "meta.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest
