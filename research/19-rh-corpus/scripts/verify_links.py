#!/usr/bin/env python3
"""Verify every relative markdown link under research/19-rh-corpus/."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "research" / "19-rh-corpus"
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def main() -> int:
    broken: list[tuple[str, str]] = []
    checked = 0

    for md in sorted(CORPUS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(2).strip().split()[0]
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if target.endswith("/"):
                broken.append((str(md.relative_to(ROOT)), target))
                continue
            resolved = (md.parent / target).resolve()
            checked += 1
            if not resolved.exists():
                broken.append((str(md.relative_to(ROOT)), target))

    print(f"Checked {checked} file links under {CORPUS.relative_to(ROOT)}/")
    if broken:
        print(f"BROKEN: {len(broken)}")
        for src, target in broken:
            print(f"  {src} -> {target}")
        return 1

    print("OK — all links resolve to existing files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())