#!/usr/bin/env python3
"""Surface markdown paths mentioning RH-facing keywords not yet in FINDINGS_INDEX.

Usage (from repo root):
  python3 research/19-rh-corpus/scripts/scan_rh_references.py

Prints candidate paths for manual review. Does not modify FINDINGS_INDEX.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
INDEX = REPO / "research/19-rh-corpus/FINDINGS_INDEX.md"
PATTERNS = re.compile(
    r"Riemann|RH\b|critical line|pole placement|source-to-spectral|zeta compression|Re\(s\)",
    re.I,
)
SKIP_DIRS = {
    ".git",
    ".lake",
    "node_modules",
    "__pycache__",
    "lake-packages",
    "lean_packages",
}
SKIP_GLOBS = ("**/19-rh-corpus/**",)


def indexed_paths() -> set[str]:
    text = INDEX.read_text(encoding="utf-8")
    return set(re.findall(r"`([^`]+\.(?:md|lean|html|json|txt|py))`", text))


def rg_candidates() -> list[str]:
    cmd = [
        "rg",
        "-l",
        r"Riemann|RH\b|critical line|pole placement|source-to-spectral",
        "--glob",
        "*.md",
        "--glob",
        "!research/19-rh-corpus/**",
        str(REPO),
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return []
    paths = []
    for line in out.stdout.splitlines():
        p = Path(line.strip())
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            rel = p.relative_to(REPO).as_posix()
        except ValueError:
            continue
        paths.append(rel)
    return sorted(set(paths))


def main() -> None:
    known = indexed_paths()
    candidates = rg_candidates()
    print("# RH reference scan (candidates not verbatim in FINDINGS_INDEX paths)\n")
    novel = [p for p in candidates if p not in known and not any(k in p for k in known)]
    if not novel:
        print("No unlisted paths from ripgrep (or rg unavailable). Review FINDINGS_INDEX manually.")
        return
    for p in novel[:80]:
        print(f"- {p}")
    if len(novel) > 80:
        print(f"\n... and {len(novel) - 80} more")


if __name__ == "__main__":
    main()