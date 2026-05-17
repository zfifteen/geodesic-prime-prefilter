#!/usr/bin/env python3
"""Probe lower-factor orientation of terminal-twin lift in public o6 triggers."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from public_o6_residue_bridge_probe import trigger_rows
from slot_factor_public_quotient_test import read_jsonl
from terminal_twin_lift_probe import OUTPUT_DIR as TERMINAL_TWIN_OUTPUT_DIR
from terminal_twin_lift_probe import left_bridge_records


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "lower_terminal_twin_orientation_probe"
RULE_ID = "pedk_lower_terminal_twin_orientation_probe_v1"


def enriched_row(window: str, case_id: str) -> dict[str, object]:
    """Return one enriched row by window and case ID."""
    for row in read_jsonl(
        INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}" / "enriched_rows.jsonl"
    ):
        if row["case_id"] == case_id:
            return row
    raise ValueError(f"missing enriched row: {window} {case_id}")


def terminal_side_value(row: dict[str, object]) -> str:
    """Return which factor sides have terminal-twin lift."""
    sides = [
        record["side"]
        for record in left_bridge_records(row)
        if record["terminal_twin_lift"]
    ]
    return "|".join(sides) if sides else "none"


def lower_terminal_residue(row: dict[str, object]) -> int | None:
    """Return the lower factor residue when the lower side has terminal lift."""
    for record in left_bridge_records(row):
        if record["side"] == "p" and record["terminal_twin_lift"]:
            return int(row["p"]) % 30
    return None


def trigger_orientation_rows() -> list[dict[str, object]]:
    """Return orientation rows for all public o6 residue-bridge trigger rows."""
    out = []
    for row in trigger_rows():
        enriched = enriched_row(str(row["window"]), str(row["case_id"]))
        records = left_bridge_records(enriched)
        terminal_records = [
            record for record in records if record["terminal_twin_lift"]
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "public_key": row["public_key"],
                "factor_residue_pair_mod30": row["factor_residue_pair_mod30"],
                "terminal_side": terminal_side_value(enriched),
                "p_mod30": int(enriched["p"]) % 30,
                "q_mod30": int(enriched["q"]) % 30,
                "lower_terminal_residue_mod30": lower_terminal_residue(enriched),
                "p_less_than_q": int(enriched["p"]) < int(enriched["q"]),
                "terminal_records": terminal_records,
                "left_bridge_records": records,
            }
        )
    return out


def observed_replacement_rows() -> list[dict[str, object]]:
    """Return observed replacement rows from the terminal-twin probe."""
    out = []
    for row in read_jsonl(TERMINAL_TWIN_OUTPUT_DIR / "observed_replacement_rows.jsonl"):
        enriched = enriched_row(str(row["window"]), str(row["case_id"]))
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "public_key": row["public_key"],
                "terminal_side": terminal_side_value(enriched),
                "p_mod30": int(enriched["p"]) % 30,
                "q_mod30": int(enriched["q"]) % 30,
                "lower_terminal_residue_mod30": lower_terminal_residue(enriched),
                "p_less_than_q": int(enriched["p"]) < int(enriched["q"]),
                "terminal_records": [
                    record
                    for record in left_bridge_records(enriched)
                    if record["terminal_twin_lift"]
                ],
            }
        )
    return out


def prior_support_rows() -> list[dict[str, object]]:
    """Return prior support rows from the terminal-twin probe."""
    out = []
    for row in read_jsonl(TERMINAL_TWIN_OUTPUT_DIR / "prior_pair_support_rows.jsonl"):
        terminal_records = [
            record
            for record in row["left_bridge_records"]
            if record["terminal_twin_lift"]
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "pair_identity_key": row["pair_identity_key"],
                "terminal_side": (
                    "|".join(record["side"] for record in terminal_records)
                    if terminal_records
                    else "none"
                ),
                "terminal_records": terminal_records,
            }
        )
    return out


def summary(
    trigger_rows_payload: list[dict[str, object]],
    observed_rows_payload: list[dict[str, object]],
    prior_rows_payload: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact lower-terminal orientation summary."""
    trigger_lower_terminal = [
        row for row in trigger_rows_payload
        if row["lower_terminal_residue_mod30"] is not None
    ]
    observed_lower_terminal = [
        row for row in observed_rows_payload
        if row["lower_terminal_residue_mod30"] is not None
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_lower_terminal_twin_orientation_probe",
        "theorem_status": "hypothesis_not_proved",
        "trigger_rres_o4_row_count": len(trigger_rows_payload),
        "trigger_terminal_side_counts": dict(
            sorted(Counter(row["terminal_side"] for row in trigger_rows_payload).items())
        ),
        "trigger_p_less_than_q_false_count": sum(
            1 for row in trigger_rows_payload if not row["p_less_than_q"]
        ),
        "trigger_lower_terminal_residue_counts": dict(
            sorted(
                Counter(
                    row["lower_terminal_residue_mod30"]
                    for row in trigger_lower_terminal
                ).items()
            )
        ),
        "trigger_lower_terminal_residue_by_public_key": {
            public_key: dict(sorted(counts.items()))
            for public_key, counts in sorted(
                {
                    public_key: Counter(
                        row["lower_terminal_residue_mod30"]
                        for row in trigger_lower_terminal
                        if row["public_key"] == public_key
                    )
                    for public_key in {
                        row["public_key"] for row in trigger_rows_payload
                    }
                }.items()
            )
        },
        "observed_replacement_row_count": len(observed_rows_payload),
        "observed_replacement_terminal_side_counts": dict(
            sorted(Counter(row["terminal_side"] for row in observed_rows_payload).items())
        ),
        "observed_replacement_p_less_than_q_false_count": sum(
            1 for row in observed_rows_payload if not row["p_less_than_q"]
        ),
        "observed_replacement_lower_terminal_residue_counts": dict(
            sorted(
                Counter(
                    row["lower_terminal_residue_mod30"]
                    for row in observed_lower_terminal
                ).items()
            )
        ),
        "observed_replacement_lower_terminal_residue_by_public_key": {
            public_key: dict(sorted(counts.items()))
            for public_key, counts in sorted(
                {
                    public_key: Counter(
                        row["lower_terminal_residue_mod30"]
                        for row in observed_lower_terminal
                        if row["public_key"] == public_key
                    )
                    for public_key in {
                        row["public_key"] for row in observed_rows_payload
                    }
                }.items()
            )
        },
        "prior_pair_support_row_count": len(prior_rows_payload),
        "prior_pair_support_terminal_side_counts": dict(
            sorted(Counter(row["terminal_side"] for row in prior_rows_payload).items())
        ),
        "sharper_arithmetic_statement": (
            "In the public o6 residue-bridge trigger rows, terminal-twin lift "
            "is lower-factor oriented: every terminal-twin trigger row includes "
            "the p side, and the observed supported prior-absent replacements "
            "have terminal-twin lift on p only, with lower residue 13 for the "
            "o4-even/o6-mid/o4-odd trigger and lower residue 19 for the "
            "o4-odd/o6-early/o6-odd trigger."
        ),
    }


def main() -> int:
    """Run the lower terminal-twin orientation probe."""
    triggers = trigger_orientation_rows()
    observed = observed_replacement_rows()
    prior = prior_support_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(triggers, observed, prior))
    write_jsonl(OUTPUT_DIR / "trigger_orientation_rows.jsonl", triggers)
    write_jsonl(OUTPUT_DIR / "observed_replacement_rows.jsonl", observed)
    write_jsonl(OUTPUT_DIR / "prior_support_rows.jsonl", prior)
    print(json.dumps(summary(triggers, observed, prior), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
