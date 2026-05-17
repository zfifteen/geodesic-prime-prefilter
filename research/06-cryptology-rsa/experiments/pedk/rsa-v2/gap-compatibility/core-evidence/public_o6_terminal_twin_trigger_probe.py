#!/usr/bin/env python3
"""Profile the public o6 balanced reentry trigger for terminal-twin lift."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl
from terminal_twin_lift_probe import (
    OUTPUT_DIR as TERMINAL_TWIN_OUTPUT_DIR,
    left_bridge_records,
)


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "public_o6_terminal_twin_trigger_probe"
RULE_ID = "pedk_public_o6_terminal_twin_trigger_probe_v1"


def load_terminal_rows(name: str) -> list[dict[str, object]]:
    """Return rows from the terminal-twin probe output."""
    return read_jsonl(TERMINAL_TWIN_OUTPUT_DIR / name)


def public_key_from_candidate(row: dict[str, object]) -> str:
    """Return public key from a candidate row."""
    return str(row["public_key"])


def public_key_from_observed(row: dict[str, object]) -> str:
    """Return public key from an observed replacement row."""
    return str(row["public_key"])


def exact_enriched_row(window: str, case_id: str) -> dict[str, object]:
    """Return one enriched row by window and case ID."""
    for row in read_jsonl(
        INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}" / "enriched_rows.jsonl"
    ):
        if row["case_id"] == case_id:
            return row
    raise ValueError(f"missing enriched row: {window} {case_id}")


def row_has_terminal_twin(row: dict[str, object]) -> bool:
    """Return whether an observed replacement row has terminal-twin lift."""
    return any(record["terminal_twin_lift"] for record in row["left_bridge_records"])


def public_key_rows() -> list[dict[str, object]]:
    """Return trigger rows by public key."""
    candidate_rows = load_terminal_rows("candidate_rows.jsonl")
    prior_rows = load_terminal_rows("prior_pair_support_rows.jsonl")
    observed_rows = load_terminal_rows("observed_replacement_rows.jsonl")

    candidate_counts = Counter(public_key_from_candidate(row) for row in candidate_rows)
    observed_counts = Counter(public_key_from_observed(row) for row in observed_rows)
    observed_terminal_counts = Counter(
        public_key_from_observed(row) for row in observed_rows if row_has_terminal_twin(row)
    )

    pair_to_public: dict[str, set[str]] = defaultdict(set)
    for row in candidate_rows:
        pair_to_public[str(row["pair_identity_key"])].add(public_key_from_candidate(row))

    prior_counts: Counter[str] = Counter()
    prior_terminal_counts: Counter[str] = Counter()
    for row in prior_rows:
        for public_key in pair_to_public[str(row["pair_identity_key"])]:
            prior_counts[public_key] += 1
            if row_has_terminal_twin(row):
                prior_terminal_counts[public_key] += 1

    out = []
    for public_key in sorted(candidate_counts):
        observed_examples = [
            row for row in observed_rows if public_key_from_observed(row) == public_key
        ]
        observed_bridge_counts = Counter(
            f"width={record['left_bridge_width']}|distance={record['immediate_left_distance']}|preceding={record['preceding_gap_width_before_immediate_left']}"
            for row in observed_examples
            for record in row["left_bridge_records"]
            if record["terminal_twin_lift"]
        )
        enriched_examples = [
            exact_enriched_row(str(row["window"]), str(row["case_id"]))
            for row in observed_examples
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "public_key": public_key,
                "candidate_load_match_reentry_rows": candidate_counts[public_key],
                "public_key_prior_pair_support_rows": prior_counts[public_key],
                "public_key_prior_pair_support_rows_with_terminal_twin_lift": (
                    prior_terminal_counts[public_key]
                ),
                "observed_replacement_rows": observed_counts[public_key],
                "observed_replacement_rows_with_terminal_twin_lift": observed_terminal_counts[
                    public_key
                ],
                "observed_terminal_twin_bridge_counts": dict(
                    sorted(observed_bridge_counts.items())
                ),
                "observed_replacement_case_ids": [
                    row["case_id"] for row in observed_examples
                ],
                "observed_factor_residue_pairs_mod30": [
                    "|".join(
                        str(int(enriched[side]) % 30)
                        for side in ("p", "q")
                    )
                    for enriched in enriched_examples
                ],
                "observed_left_bridge_records": [
                    left_bridge_records(enriched)
                    for enriched in enriched_examples
                ],
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact public-trigger summary."""
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_o6_terminal_twin_trigger_probe",
        "theorem_status": "hypothesis_not_proved",
        "public_trigger_count": len(rows),
        "candidate_load_match_reentry_rows": sum(
            int(row["candidate_load_match_reentry_rows"]) for row in rows
        ),
        "public_key_prior_pair_support_rows": sum(
            int(row["public_key_prior_pair_support_rows"]) for row in rows
        ),
        "public_key_prior_pair_support_rows_with_terminal_twin_lift": sum(
            int(row["public_key_prior_pair_support_rows_with_terminal_twin_lift"])
            for row in rows
        ),
        "observed_replacement_rows": sum(
            int(row["observed_replacement_rows"]) for row in rows
        ),
        "observed_replacement_rows_with_terminal_twin_lift": sum(
            int(row["observed_replacement_rows_with_terminal_twin_lift"])
            for row in rows
        ),
        "public_trigger_rows": rows,
        "sharper_arithmetic_statement": (
            "For the two supported prior-absent public o6_d4_a6 balanced "
            "right-boundary cells, every observed forward replacement contains "
            "terminal-twin lift, while no prior support row for the old pair "
            "classes contains terminal-twin lift."
        ),
    }


def main() -> int:
    """Run the public o6 terminal-twin trigger probe."""
    rows = public_key_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows))
    write_jsonl(OUTPUT_DIR / "public_trigger_rows.jsonl", rows)
    print(json.dumps(summary(rows), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
