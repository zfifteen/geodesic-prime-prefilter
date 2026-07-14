#!/usr/bin/env python3
"""Run all (or filtered) plot library demos."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

VIS = Path(__file__).resolve().parents[1]
LIBRARY = VIS / "library"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog_lib import load_all_entries, load_catalog  # noqa: E402


def resolve_python() -> str:
    venv_py = LIBRARY / ".venv" / "bin" / "python"
    if venv_py.is_file():
        return str(venv_py)
    return sys.executable


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", type=int, default=None, help="Only entries with this tier")
    parser.add_argument("--id", action="append", default=[], help="Only these entry ids")
    parser.add_argument("--python", default=None, help="Python interpreter override")
    args = parser.parse_args()

    py = args.python or resolve_python()
    entries = load_all_entries()
    if args.id:
        wanted = set(args.id)
        entries = [e for e in entries if e["id"] in wanted]
    if args.tier is not None:
        entries = [e for e in entries if int(e.get("tier", 99)) == args.tier]

    if not entries:
        print("No entries selected", file=sys.stderr)
        return 1

    failures = []
    for entry in entries:
        eid = entry["id"]
        script = Path(entry["_dir"]) / entry.get("script", "demo.py")
        print(f"==> {eid}")
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        proc = subprocess.run([py, str(script)], cwd=str(script.parent), env=env)
        if proc.returncode != 0:
            failures.append(eid)
            print(f"FAIL {eid} exit={proc.returncode}", file=sys.stderr)
        else:
            out = LIBRARY / "out" / eid / "plot.png"
            if not out.is_file():
                failures.append(eid)
                print(f"FAIL {eid} missing {out}", file=sys.stderr)
            else:
                print(f"OK   {out}")

    print()
    if failures:
        print(f"DONE with failures: {', '.join(failures)}")
        return 1
    print(f"DONE ok ({len(entries)} entries)")
    cat = load_catalog()
    print(f"catalog version {cat.get('version')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
