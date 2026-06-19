#!/usr/bin/env python3
"""Merge gap-probe and exclusion-probe summaries into FINDINGS inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(gap_summary: dict, excl_summary: dict | None) -> dict:
    report = {
        "harness": {
            "f0_match_rate": gap_summary.get("f0_match_rate"),
            "f1_match_rate": gap_summary.get("f1_match_rate"),
            "f2rx_match_rate": gap_summary.get("f2rx_match_rate"),
            "regime": gap_summary.get("regime"),
            "gaps_total": gap_summary.get("gaps_total"),
        },
        "tier_a": {
            "supported": gap_summary.get("f1_match_rate") == 1.0,
            "audit_tau2_f1_fail": gap_summary.get("audit_tau2_f1_fail", 0),
        },
        "tier_b": {
            "expected_pass": (
                gap_summary.get("f2rx_match_rate") == 1.0
                and gap_summary.get("f1_match_rate") == gap_summary.get("f2rx_match_rate")
            ),
            "audit_tau2_f2rx_fail": gap_summary.get("audit_tau2_f2rx_fail", 0),
        },
        "prefix_forcing": {
            "prefix_none_at_gap_minus_1_rate": gap_summary.get(
                "prefix_none_at_gap_minus_1_rate"
            ),
            "decision_offset_eq_gap_rate": gap_summary.get(
                "decision_offset_eq_gap_rate"
            ),
        },
    }
    if excl_summary:
        report["tier_c"] = {
            "unique_resolved_survivor_count": excl_summary.get(
                "unique_resolved_survivor_count"
            ),
            "no_unique_boundary_count": excl_summary.get("no_unique_boundary_count"),
            "true_boundary_rejected_count": excl_summary.get(
                "true_boundary_rejected_count"
            ),
            "unique_survivor_match_rate": excl_summary.get(
                "unique_survivor_match_rate"
            ),
            "row_count": excl_summary.get("row_count"),
            "supported": excl_summary.get("unique_resolved_survivor_count", 0) > 0,
            "unresolved": excl_summary.get("unique_resolved_survivor_count", 0) == 0,
        }
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap-summary", type=Path, required=True)
    parser.add_argument("--excl-summary", type=Path, default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENT_DIR / "output" / "merged_report.json",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    gap_summary = load_json(args.gap_summary)
    excl_summary = load_json(args.excl_summary) if args.excl_summary else None
    report = build_report(gap_summary, excl_summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())