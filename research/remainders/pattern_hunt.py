"""Thin CLI: stream JSONL, write partition + extended JSON."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pattern_hunt_core import (
    aggregate_cells,
    record_features,
    run_extended_analysis,
    structural_laws,
)


def stream_features(jsonl_path: Path, *, max_records: int | None = None) -> list[dict[str, Any]]:
    feats: list[dict[str, Any]] = []
    with jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            feats.append(record_features(json.loads(line)))
            if max_records is not None and len(feats) >= max_records:
                break
    return feats


def run_probe(
    jsonl: Path,
    partition_out: Path,
    extended_out: Path | None = None,
    *,
    max_records: int | None = None,
    surface_label: str = "pattern_hunt_surface_max_p_400000",
) -> dict[str, Any]:
    feats = stream_features(jsonl, max_records=max_records)
    agg = aggregate_cells(feats)
    ext_path = extended_out or partition_out.parent / "pattern_extended_analysis.json"
    payload: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_jsonl": str(jsonl.resolve()),
        "surface_label": surface_label,
        "repro_command": (
            f"python research/remainders/pattern_hunt.py --jsonl {jsonl} "
            f"--output {partition_out} --extended-output {ext_path}"
        ),
        "partition_keys": ["p_mod_30", "position_bin", "gap_regime"],
        "joint_features": ["zero_pattern_code", "primorial_level", "mod210_class", "k_offset_bin"],
        "summary": agg,
        "structural_laws": structural_laws(agg),
    }
    partition_out.parent.mkdir(parents=True, exist_ok=True)
    partition_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    ext = run_extended_analysis(feats)
    ext_payload = {
        "timestamp_utc": payload["timestamp_utc"],
        "source_jsonl": payload["source_jsonl"],
        "surface_label": surface_label,
        "repro_command": payload["repro_command"],
        "analysis": ext,
    }
    ext_path.write_text(json.dumps(ext_payload, indent=2), encoding="utf-8")
    payload["extended_analysis_path"] = str(ext_path.resolve())
    return payload


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Partition-first remainder pattern hunt")
    ap.add_argument("--jsonl", type=Path, default=here / "output/pattern_hunt_surface/raw_records.jsonl")
    ap.add_argument("--output", type=Path, default=here / "correlations/investigation/pattern_partition_summary.json")
    ap.add_argument(
        "--extended-output",
        type=Path,
        default=here / "correlations/investigation/pattern_extended_analysis.json",
    )
    ap.add_argument("--max-records", type=int, default=None)
    ap.add_argument("--no-extended", action="store_true")
    args = ap.parse_args()

    if not args.jsonl.is_file():
        print(f"Missing JSONL: {args.jsonl}", file=sys.stderr)
        return 1

    ext_path = None if args.no_extended else args.extended_output
    result = run_probe(args.jsonl, args.output, ext_path, max_records=args.max_records)
    print(
        json.dumps(
            {
                "records": result["summary"]["record_count"],
                "cells": result["summary"]["cell_count"],
                "laws": len(result["structural_laws"]),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())