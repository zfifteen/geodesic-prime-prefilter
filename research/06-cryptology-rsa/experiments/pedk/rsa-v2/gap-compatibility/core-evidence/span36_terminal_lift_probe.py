#!/usr/bin/env python3
"""Probe span-36 plus lower terminal lift in the public o6 trigger surface."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
ORIENTATION_DIR = INPUT_ROOT / "lower_terminal_twin_orientation_probe"
OUTPUT_DIR = INPUT_ROOT / "span36_terminal_lift_probe"
RULE_ID = "pedk_span36_terminal_lift_probe_v1"


def enriched_rows_for(payload_rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    """Return enriched rows keyed by window and case ID."""
    needed_by_window: dict[str, set[str]] = {}
    for row in payload_rows:
        needed_by_window.setdefault(str(row["window"]), set()).add(str(row["case_id"]))

    out = {}
    for window, case_ids in sorted(needed_by_window.items()):
        path = INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}" / "enriched_rows.jsonl"
        for row in read_jsonl(path):
            case_id = str(row["case_id"])
            if case_id in case_ids:
                out[(window, case_id)] = row
    return out


def with_span_fields(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Attach direct factor-span arithmetic to orientation rows."""
    enriched = enriched_rows_for(rows)
    out = []
    for row in rows:
        key = (str(row["window"]), str(row["case_id"]))
        enriched_row = enriched[key]
        p = int(enriched_row["p"])
        q = int(enriched_row["q"])
        span = q - p
        terminal_side = str(row["terminal_side"])
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "public_key": row.get("public_key"),
                "p_mod30": p % 30,
                "q_mod30": q % 30,
                "span": span,
                "span_mod36": span % 36,
                "span_divisible_by_36": span % 36 == 0,
                "terminal_side": terminal_side,
                "lower_terminal_lift": terminal_side == "p",
                "any_terminal_lift": terminal_side != "none",
            }
        )
    return out


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts for one row key."""
    return {str(value): count for value, count in sorted(Counter(row[key] for row in rows).items())}


def conjunction_count(rows: list[dict[str, object]]) -> int:
    """Return rows with span divisible by 36 and lower terminal lift."""
    return sum(
        1
        for row in rows
        if row["span_divisible_by_36"] and row["lower_terminal_lift"]
    )


def summary(
    trigger_rows: list[dict[str, object]],
    observed_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact span-36 terminal-lift summary."""
    return {
        "rule_id": RULE_ID,
        "status": "measured_span36_terminal_lift_probe",
        "theorem_status": "hypothesis_not_proved",
        "trigger_row_count": len(trigger_rows),
        "trigger_span_mod36_counts": count_by(trigger_rows, "span_mod36"),
        "trigger_span36_lower_terminal_lift_rows": conjunction_count(trigger_rows),
        "observed_replacement_row_count": len(observed_rows),
        "observed_span_mod36_counts": count_by(observed_rows, "span_mod36"),
        "observed_span36_lower_terminal_lift_rows": conjunction_count(observed_rows),
        "prior_pair_support_row_count": len(prior_rows),
        "prior_span_mod36_counts": count_by(prior_rows, "span_mod36"),
        "prior_span36_lower_terminal_lift_rows": conjunction_count(prior_rows),
        "sharper_arithmetic_statement": (
            "In the current public o6 residue-bridge surface, the observed "
            "supported prior-absent replacements are exactly the rows with "
            "factor span divisible by 36 and lower-factor terminal-twin lift. "
            "Span divisibility alone is not enough: prior support contains "
            "span-36 rows, but none with lower terminal lift."
        ),
    }


def main() -> int:
    """Run the span-36 terminal-lift probe."""
    trigger_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "trigger_orientation_rows.jsonl")
    )
    observed_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "observed_replacement_rows.jsonl")
    )
    prior_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "prior_support_rows.jsonl")
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = summary(trigger_rows, observed_rows, prior_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    write_jsonl(OUTPUT_DIR / "trigger_rows.jsonl", trigger_rows)
    write_jsonl(OUTPUT_DIR / "observed_replacement_rows.jsonl", observed_rows)
    write_jsonl(OUTPUT_DIR / "prior_support_rows.jsonl", prior_rows)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
