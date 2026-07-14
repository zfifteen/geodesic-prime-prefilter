#!/usr/bin/env python3
"""Lint catalog entries for status and claim-language discipline."""

from __future__ import annotations

import sys
from pathlib import Path

VIS = Path(__file__).resolve().parents[1]
LIBRARY = VIS / "library"
REPO = VIS.parent
sys.path.insert(0, str(LIBRARY))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog_lib import discover_orphan_entries, load_all_entries, load_catalog  # noqa: E402
from _common.status import iter_status_issues, normalize_status  # noqa: E402


def main() -> int:
    cat = load_catalog()
    entries = load_all_entries()
    issues = list(iter_status_issues(entries))

    for entry in entries:
        eid = entry["id"]
        script = Path(entry["_dir"]) / entry.get("script", "demo.py")
        if not script.is_file():
            issues.append(f"{eid}: missing script {script.name}")
        for out_name in entry.get("outputs", ["plot.png"]):
            if not out_name:
                issues.append(f"{eid}: empty output name")
        if entry.get("kind") == "legacy-wrap":
            rel = entry.get("legacy_source")
            if not rel:
                issues.append(f"{eid}: legacy-wrap requires legacy_source")
            else:
                src = REPO / rel
                if not src.is_file():
                    issues.append(f"{eid}: legacy_source missing: {rel}")
        try:
            normalize_status(str(entry["status"]))
        except ValueError as exc:
            issues.append(f"{eid}: {exc}")

    for orphan in discover_orphan_entries():
        issues.append(f"orphan entry folder not in catalog.json: {orphan}")

    for eid in cat["entries"]:
        if not (LIBRARY / "entries" / eid / "entry.json").is_file():
            issues.append(f"catalog lists missing entry: {eid}")

    if issues:
        print("LINT FAIL")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print(f"LINT OK ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
