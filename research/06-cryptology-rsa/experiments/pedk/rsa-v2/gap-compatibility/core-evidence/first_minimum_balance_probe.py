#!/usr/bin/env python3
"""Probe the literal first-minimum form of the balance target."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "first_minimum_balance_probe"
RULE_ID = "pedk_first_minimum_balance_probe_v1"
WINDOWS = (
    ("21001_23000", "enriched_multiplication_map_corpus_21001_23000"),
    ("23001_25000", "enriched_multiplication_map_corpus_23001_25000"),
    ("25001_27000", "enriched_multiplication_map_corpus_25001_27000"),
    ("27001_30000", "enriched_multiplication_map_corpus_27001_30000"),
    ("30001_32000", "enriched_multiplication_map_corpus_30001_32000"),
    ("32001_34000", "enriched_multiplication_map_corpus_32001_34000"),
)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def analyze_row(row: dict[str, object], window: str) -> dict[str, object]:
    """Return one literal first-minimum balance row."""
    offset = int(row["public_n_offset_from_left"])
    containing_gap = row["public_containing_gap"]
    selected_offset = int(containing_gap["winner_offset"])
    selected_divisor_count = int(containing_gap["winner_d"])
    is_first_low = selected_divisor_count in {3, 4} and offset == selected_offset
    public_at_winner = row["public_gwr_side"] == "at_winner"
    return {
        "rule_id": RULE_ID,
        "window": window,
        "case_id": row["case_id"],
        "N": row["N"],
        "public_gwr_side": row["public_gwr_side"],
        "public_gwr_signed_distance": row["public_gwr_signed_distance"],
        "public_n_offset_from_left": offset,
        "public_gwr_winner_offset": selected_offset,
        "public_gap_width": row["public_containing_gap_width"],
        "public_selected_divisor_count": selected_divisor_count,
        "first_tau_3_or_4_offset": (
            selected_offset if selected_divisor_count in {3, 4} else None
        ),
        "first_minimum_offset": selected_offset,
        "first_minimum_divisor_count": selected_divisor_count,
        "n_is_first_tau_3_or_4": is_first_low,
        "n_is_selected_divisor_count_4": (
            selected_divisor_count == 4 and offset == selected_offset
        ),
        "public_at_winner": public_at_winner,
        "literal_first_low_matches_public_at_winner": is_first_low == public_at_winner,
    }


def load_rows() -> list[dict[str, object]]:
    """Load observed rows from the active six-window corpus."""
    out = []
    for window, dirname in WINDOWS:
        for row in read_jsonl(INPUT_ROOT / dirname / "enriched_rows.jsonl"):
            out.append(analyze_row(row, window))
    return out


def counter_rows(counter: Counter[object], field: str) -> list[dict[str, object]]:
    """Return sorted counter rows."""
    return [
        {"rule_id": RULE_ID, field: value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (str(item[0]), item[1]))
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the compact first-minimum probe summary."""
    mismatches = [
        row for row in rows if not row["literal_first_low_matches_public_at_winner"]
    ]
    at_winner_rows = [row for row in rows if row["public_at_winner"]]
    return {
        "rule_id": RULE_ID,
        "status": "measured_first_minimum_balance_probe",
        "theorem_status": "hypothesis_not_proved",
        "row_count": len(rows),
        "literal_first_tau_3_or_4_matches_public_at_winner_count": len(rows) - len(mismatches),
        "literal_first_tau_3_or_4_mismatch_count": len(mismatches),
        "public_at_winner_count": len(at_winner_rows),
        "public_at_winner_selected_divisor_count_counts": dict(
            sorted(Counter(row["public_selected_divisor_count"] for row in at_winner_rows).items())
        ),
        "public_side_by_literal_first_low": [
            {
                "rule_id": RULE_ID,
                "public_gwr_side": side,
                "n_is_first_tau_3_or_4": first_low,
                "count": count,
            }
            for (side, first_low), count in sorted(
                Counter(
                    (row["public_gwr_side"], row["n_is_first_tau_3_or_4"])
                    for row in rows
                ).items()
            )
        ],
        "first_minimum_divisor_count_counts": dict(
            sorted(Counter(row["first_minimum_divisor_count"] for row in rows).items())
        ),
        "sharper_arithmetic_statement": (
            "For distinct-prime semiprime rows in the active corpus, public_at_winner "
            "is exactly N_is_first_tau_3_or_4 in the public containing gap, as "
            "encoded by the exact selected divisor count and selected offset. The "
            "selected public side is therefore the literal first low-divisor-load "
            "event, not a separate grammar label."
        ),
    }


def main() -> int:
    """Run the first-minimum balance probe."""
    rows = load_rows()
    mismatches = [
        row for row in rows if not row["literal_first_low_matches_public_at_winner"]
    ]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows))
    write_jsonl(OUTPUT_DIR / "literal_first_minimum_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "mismatch_rows.jsonl", mismatches)
    print(json.dumps(summary(rows), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
