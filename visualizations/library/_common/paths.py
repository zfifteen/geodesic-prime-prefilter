"""Path anchors for the plot library."""

from __future__ import annotations

from pathlib import Path

LIBRARY_ROOT = Path(__file__).resolve().parents[1]
VISUALIZATIONS_ROOT = LIBRARY_ROOT.parent
REPO_ROOT = VISUALIZATIONS_ROOT.parent
ENTRIES_DIR = LIBRARY_ROOT / "entries"
FIXTURES_DIR = LIBRARY_ROOT / "fixtures"
OUT_ROOT = LIBRARY_ROOT / "out"
CATALOG_PATH = LIBRARY_ROOT / "catalog.json"
SCRIPTS_DIR = VISUALIZATIONS_ROOT / "scripts"
GALLERY_ROOT = VISUALIZATIONS_ROOT / "gallery"


def gallery_root() -> Path:
    return GALLERY_ROOT


def out_dir_for(entry_id: str) -> Path:
    path = OUT_ROOT / entry_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def entry_dir(entry_id: str) -> Path:
    return ENTRIES_DIR / entry_id
