#!/usr/bin/env python3
"""Audit the endpoint meaning of factor-left gap records."""

from __future__ import annotations

import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import gmpy2

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROOT = next(
    parent
    for parent in THIS_DIR.parents
    if (parent / "src" / "python").exists() and (parent / "research").exists()
)
LIVE_SOLVER_DIR = (
    ROOT / "research" / "06-cryptology-rsa" / "experiments" / "live-solver" / "rsa-v2"
)
if str(LIVE_SOLVER_DIR) not in sys.path:
    sys.path.insert(0, str(LIVE_SOLVER_DIR))

from run_experiment import previous_endpoint  # noqa: E402


INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "factor_left_gap_semantics_audit"
RULE_ID = "pedk_factor_left_gap_semantics_audit_v1"


@lru_cache(maxsize=None)
def immediate_left_endpoint(factor: int) -> int:
    """Return the immediate PGS endpoint before one factor coordinate."""
    immediate_left = previous_endpoint(gmpy2.mpz(factor - 1))
    if immediate_left is None:
        raise ValueError(f"no immediate left endpoint for {factor}")
    return int(immediate_left)


def endpoint_record(row: dict[str, object], side: str) -> dict[str, object]:
    """Return the factor-left endpoint audit record for one side."""
    factor = int(row[side])
    immediate_left = immediate_left_endpoint(factor)
    stored_width = int(row[f"{side}_left_gap_width"])
    stored_left_endpoint = factor - stored_width
    stored_winner_offset = int(row[f"{side}_left_winner_offset"])
    stored_winner_value = stored_left_endpoint + stored_winner_offset
    return {
        "side": side,
        "factor": factor,
        "immediate_left_endpoint": immediate_left,
        "factor_minus_immediate_left": factor - immediate_left,
        "stored_left_gap_left_endpoint": stored_left_endpoint,
        "stored_left_gap_width": stored_width,
        "stored_left_gap_right_endpoint": stored_left_endpoint + stored_width,
        "stored_left_winner_offset": stored_winner_offset,
        "stored_left_winner_value": stored_winner_value,
        "stored_left_winner_d": row[f"{side}_left_winner_d"],
        "stored_left_winner_phase": row[f"{side}_left_winner_phase"],
        "stored_left_gap_contains_immediate_left_endpoint": (
            stored_left_endpoint < immediate_left < factor
        ),
        "stored_left_winner_is_immediate_left_endpoint": (
            stored_winner_value == immediate_left
        ),
        "stored_left_winner_distance_from_factor": factor - stored_winner_value,
    }


def enriched_rows() -> list[dict[str, object]]:
    """Return all enriched multiplication-map rows in the current output tree."""
    rows = []
    for path in sorted(INPUT_ROOT.glob("enriched_multiplication_map_corpus_*/enriched_rows.jsonl")):
        window = path.parent.name.replace("enriched_multiplication_map_corpus_", "")
        for row in read_jsonl(path):
            row = dict(row)
            row["window"] = window
            rows.append(row)
    return rows


def reentry_cases() -> set[tuple[str, str]]:
    """Return load-match reentry case IDs from the previous focused probe."""
    path = INPUT_ROOT / "shared_load_reentry_cell_probe" / "load_match_observed_forward_rows.jsonl"
    return {
        (str(row["window"]), str(row["case_id"]))
        for row in read_jsonl(path)
    }


def audit_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return factor-left endpoint audit records for all rows."""
    out = []
    reentry = reentry_cases()
    for row in rows:
        for side in ("p", "q"):
            record = endpoint_record(row, side)
            record.update(
                {
                    "rule_id": RULE_ID,
                    "window": row["window"],
                    "case_id": row["case_id"],
                    "public_gwr_side": row["public_gwr_side"],
                    "is_load_match_reentry_case": (
                        (str(row["window"]), str(row["case_id"])) in reentry
                    ),
                }
            )
            out.append(record)
    out.sort(
        key=lambda row: (
            not bool(row["is_load_match_reentry_case"]),
            str(row["window"]),
            str(row["case_id"]),
            str(row["side"]),
        )
    )
    return out


def count_where(rows: list[dict[str, object]], key: str) -> int:
    """Return the number of rows where a boolean field is true."""
    return sum(1 for row in rows if row[key])


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact factor-left endpoint semantics audit summary."""
    reentry = [row for row in rows if row["is_load_match_reentry_case"]]
    reentry_very_late = [
        row for row in reentry if row["stored_left_winner_phase"] == "very_late"
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_factor_left_gap_semantics_audit",
        "theorem_status": "hypothesis_not_proved",
        "audit_status": "factor_left_record_is_second_previous_to_factor_span",
        "factor_side_record_count": len(rows),
        "stored_left_gap_contains_immediate_left_endpoint_count": count_where(
            rows,
            "stored_left_gap_contains_immediate_left_endpoint",
        ),
        "stored_left_winner_is_immediate_left_endpoint_count": count_where(
            rows,
            "stored_left_winner_is_immediate_left_endpoint",
        ),
        "stored_left_winner_distance_from_factor_counts": dict(
            sorted(
                Counter(
                    row["stored_left_winner_distance_from_factor"]
                    for row in rows
                ).items()
            )
        ),
        "load_match_reentry_factor_side_record_count": len(reentry),
        "load_match_reentry_very_late_left_record_count": len(reentry_very_late),
        "load_match_reentry_very_late_left_winner_is_immediate_left_endpoint_count": count_where(
            reentry_very_late,
            "stored_left_winner_is_immediate_left_endpoint",
        ),
        "load_match_reentry_very_late_factor_minus_immediate_left_counts": dict(
            sorted(
                Counter(
                    row["factor_minus_immediate_left"]
                    for row in reentry_very_late
                ).items()
            )
        ),
        "sharper_arithmetic_statement": (
            "The measured load-match very_late left records are immediate-left "
            "endpoint records: the selected point two before the factor is the "
            "previous PGS endpoint itself."
        ),
    }


def main() -> int:
    """Run the factor-left gap semantics audit."""
    rows = audit_rows(enriched_rows())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows))
    write_jsonl(OUTPUT_DIR / "audit_rows.jsonl", rows)
    write_jsonl(
        OUTPUT_DIR / "load_match_reentry_rows.jsonl",
        [row for row in rows if row["is_load_match_reentry_case"]],
    )
    print(json.dumps(summary(rows), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
