#!/usr/bin/env python3
"""Load catalog + per-entry metadata for the plot library."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VIS = Path(__file__).resolve().parents[1]
LIBRARY = VIS / "library"
ENTRIES = LIBRARY / "entries"
CATALOG = LIBRARY / "catalog.json"


def load_catalog() -> dict[str, Any]:
    with CATALOG.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_entry(entry_id: str) -> dict[str, Any]:
    path = ENTRIES / entry_id / "entry.json"
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("id") != entry_id:
        raise ValueError(f"entry id mismatch: folder={entry_id} json={data.get('id')}")
    data["_dir"] = str(path.parent)
    caption = path.parent / "caption.md"
    data["_caption_path"] = str(caption) if caption.is_file() else None
    data["_caption"] = caption.read_text(encoding="utf-8") if caption.is_file() else ""
    return data


def load_all_entries() -> list[dict[str, Any]]:
    cat = load_catalog()
    entries = []
    for eid in cat["entries"]:
        entries.append(load_entry(eid))
    return entries


def discover_orphan_entries() -> list[str]:
    """Entry folders that exist on disk but are missing from catalog.json."""
    cat_ids = set(load_catalog()["entries"])
    orphans = []
    if not ENTRIES.is_dir():
        return orphans
    for path in sorted(ENTRIES.iterdir()):
        if path.is_dir() and (path / "entry.json").is_file() and path.name not in cat_ids:
            orphans.append(path.name)
    return orphans
