#!/usr/bin/env python3
"""
Regenerate committed output/ ONLY by executing shipped runner logic.

- Supports --case-ids to run subset (enables one-at-a-time for large cases).
- Wipes target output dir.
- Uses the exact same load_cases + run_cases + writers as run_experiment.py.
- Never hand-edits or "rich patches" the rows.

After running this, committed output/ will match what certificate_pair produces today.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

import gmpy2

THIS_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
EXPERIMENTS_DIR = THIS_DIR.parents[1]
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
SOURCE_DIR = ROOT / "src" / "python"

if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from run_experiment import (  # noqa: E402
    LadderCase,
    load_cases,
    run_cases,
    write_json,
    write_jsonl,
    DATA_LADDER_DIR as RUNNER_DATA_LADDER,
)

def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--case-ids", type=str, default=None,
                   help="Comma separated case_ids to include. Default: all in fixtures.")
    p.add_argument("--output-dir", type=Path, default=THIS_DIR / "output",
                   help="Target output dir to (re)generate (will be wiped).")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)

    cases_path = DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl"
    all_cases = load_cases(cases_path)

    if args.case_ids:
        wanted = {x.strip() for x in args.case_ids.split(",") if x.strip()}
        cases = [c for c in all_cases if c.case_id in wanted]
    else:
        cases = all_cases

    print(f"[rebuild] regenerating {len(cases)} case(s) into {args.output_dir}")

    # Wipe
    if args.output_dir.exists():
        for f in args.output_dir.glob("*.jsonl"):
            f.unlink()
        for f in args.output_dir.glob("summary.json"):
            f.unlink()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Run shipped logic exactly
    results, summaries, pairs, diagnostics_rows, structural_certs = run_cases(cases)

    write_jsonl(args.output_dir / "inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", pairs)
    write_jsonl(args.output_dir / "diagnostic_rows.jsonl", diagnostics_rows)
    if structural_certs:
        write_jsonl(args.output_dir / "structural_certs.jsonl", structural_certs)

    summary_obj = {"cases": summaries}
    if structural_certs:
        summary_obj["structural_certs_count"] = len(structural_certs)
    write_json(args.output_dir / "summary.json", summary_obj)

    print("[rebuild] done. Wrote:", list(args.output_dir.glob("*")))
    return 0

if __name__ == "__main__":
    sys.exit(main())
