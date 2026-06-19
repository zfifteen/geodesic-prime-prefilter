#!/usr/bin/env python3
"""Print human-readable summary from prefix-state L_FCL probe output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    print(f"Regime: {summary['regime']}")
    print(f"Gaps: {summary['gaps_total']}")
    print(f"L0 match rate: {summary['l0_match_rate']}")
    print(f"Semantic audit pass: {summary['semantic_audit_pass']}")
    print(f"Any law mismatch count: {summary['any_law_mismatch_count']}")
    print(f"Any law early support count: {summary['any_law_early_support_count']}")
    for law_id, report in summary.get("law_reports", {}).items():
        print(
            f"{law_id}: early_fire={report['early_fire_count']} "
            f"mismatch={report['mismatch_count']} "
            f"falsified_as_predictor={report['falsified_as_predictor']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())