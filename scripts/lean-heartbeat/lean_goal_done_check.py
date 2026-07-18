#!/usr/bin/env python3
"""Decide whether the PGS Lean hourly heartbeat should disable."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STATE = Path(__file__).resolve().parent / "LEAN_HEARTBEAT_STATE.md"
DONE_FILE = REPO / "lean-4" / "LEAN_PROGRAM_DONE.md"
PGS = REPO / "lean-4" / "PGS"


def state_enabled() -> bool:
    if not STATE.is_file():
        return True
    text = STATE.read_text(encoding="utf-8")
    m = re.search(r"(?im)^\s*enabled\s*:\s*(true|false)\s*$", text)
    if not m:
        return True
    return m.group(1).lower() == "true"


def owner_done() -> bool:
    return DONE_FILE.is_file()


def count_sorry() -> int:
    if not PGS.is_dir():
        return -1
    n = 0
    for path in sorted(PGS.glob("*.lean")):
        for line in path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s == "sorry" or s.startswith("sorry ") or s.startswith("sorry--"):
                n += 1
    return n


def main() -> int:
    """Exit 0 => disable heartbeat. Exit 1 => keep running. Exit 2 => error."""
    if not state_enabled():
        print("DISABLE reason=state_enabled_false")
        return 0
    if owner_done():
        print(f"DISABLE reason=owner_done_file path={DONE_FILE}")
        return 0
    sorry = count_sorry()
    print(f"KEEP sorry_count={sorry} owner_done=false state_enabled=true")
    if sorry == 0:
        print(
            "NOTE: zero sorry in PGS/*.lean — candidate progress; "
            "still need full DoD + lean-4/LEAN_PROGRAM_DONE.md before disable"
        )
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
