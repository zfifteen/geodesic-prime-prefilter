#!/usr/bin/env python3
"""Audit the directed multiplication transport behind endpoint gaps."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_ROOT = THIS_DIR / "output"
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_ROOT / "directed_transport_audit"
RULE_ID = "pedk_directed_transport_audit_v1"

WINDOWS = (
    ("21001_23000", "enriched_multiplication_map_corpus_21001_23000"),
    ("23001_25000", "enriched_multiplication_map_corpus_23001_25000"),
    ("25001_27000", "enriched_multiplication_map_corpus_25001_27000"),
    ("27001_30000", "enriched_multiplication_map_corpus_27001_30000"),
    ("30001_32000", "enriched_multiplication_map_corpus_30001_32000"),
)

RESIDUE_RANK = {"o2": 1, "o4": 2, "o6": 3}
MIDDLE_RESIDUE = "o4"
FIRST_OPEN_RE = re.compile(r"^(o[246])_")
RIGHT_OPEN_OFFSET_BY_ENDPOINT_RESIDUE = {
    1: 6,
    7: 4,
    11: 2,
    13: 4,
    17: 2,
    19: 4,
    23: 6,
    29: 2,
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def first_open_label(value: str) -> str:
    """Return the first-open label from one reduced state."""
    match = FIRST_OPEN_RE.match(value)
    if not match:
        raise ValueError(f"cannot parse first-open label: {value}")
    return match.group(1)


def first_open_offset(value: str) -> int:
    """Return the first-open offset from one reduced state."""
    return int(first_open_label(value)[1:])


def endpoint_residue_step(residue: int) -> int:
    """Return the first right-open offset from an endpoint residue mod 30."""
    return RIGHT_OPEN_OFFSET_BY_ENDPOINT_RESIDUE[residue]


def transport_balance(p_step: int, q_step: int) -> str:
    """Classify the first right-open transport boundary."""
    max_step = max(p_step, q_step)
    if max_step == 2:
        return "shortfall_below_4"
    if max_step == 4:
        return "middle_4_balance"
    if max_step == 6:
        return "overshoot_above_4"
    raise ValueError(f"unknown right-open offset maximum: {max_step}")


def right_boundary_defect(row: dict[str, object]) -> int:
    """Return signed distance from the middle right-boundary residue."""
    p_label = first_open_label(str(row["p_right_reduced_state"]))
    q_label = first_open_label(str(row["q_right_reduced_state"]))
    return max(RESIDUE_RANK[p_label], RESIDUE_RANK[q_label]) - RESIDUE_RANK[MIDDLE_RESIDUE]


def transport_row(row: dict[str, object], window: str) -> dict[str, object]:
    """Return one observed directed transport row."""
    p = int(row["p"])
    q = int(row["q"])
    n = int(row["N"])
    p_step = first_open_offset(str(row["p_right_reduced_state"]))
    q_step = first_open_offset(str(row["q_right_reduced_state"]))
    p_residue_step = endpoint_residue_step(p % 30)
    q_residue_step = endpoint_residue_step(q % 30)
    delta_p = p_step * q
    delta_q = q_step * p
    delta_both = delta_p + delta_q + (p_step * q_step)
    return {
        "rule_id": RULE_ID,
        "window": window,
        "case_id": row["case_id"],
        "public_gwr_side": row["public_gwr_side"],
        "public_containing_exact_type_key": row["public_containing_exact_type_key"],
        "public_n_mod30": n % 30,
        "p_mod30": p % 30,
        "q_mod30": q % 30,
        "p_right_residue": first_open_label(str(row["p_right_reduced_state"])),
        "q_right_residue": first_open_label(str(row["q_right_reduced_state"])),
        "p_right_step": p_step,
        "q_right_step": q_step,
        "p_right_step_from_mod30": p_residue_step,
        "q_right_step_from_mod30": q_residue_step,
        "right_step_matches_endpoint_residue": (
            p_step == p_residue_step and q_step == q_residue_step
        ),
        "right_open_offset_max": max(p_step, q_step),
        "transport_balance": transport_balance(p_step, q_step),
        "right_boundary_defect": right_boundary_defect(row),
        "delta_p_side_mod30": delta_p % 30,
        "delta_q_side_mod30": delta_q % 30,
        "delta_both_side_mod30": delta_both % 30,
        "transport_p_side_mod30": (n + delta_p) % 30,
        "transport_q_side_mod30": (n + delta_q) % 30,
        "transport_both_side_mod30": (n + delta_both) % 30,
    }


def load_rows(input_root: Path) -> list[dict[str, object]]:
    """Load observed at-winner corpus rows."""
    rows = []
    for window, dirname in WINDOWS:
        for row in read_jsonl(input_root / dirname / "enriched_rows.jsonl"):
            if row["public_gwr_side"] != "at_winner":
                continue
            rows.append(transport_row(row, window))
    return rows


def counter_rows(counter: Counter[object], field: str) -> list[dict[str, object]]:
    """Return sorted count rows."""
    return [
        {"rule_id": RULE_ID, field: value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact audit summary."""
    defect_counts = Counter(row["right_boundary_defect"] for row in rows)
    balance_counts = Counter(row["transport_balance"] for row in rows)
    residue_step_mismatches = [
        row for row in rows
        if not row["right_step_matches_endpoint_residue"]
    ]
    transport_counts = Counter(
        (
            row["right_boundary_defect"],
            row["transport_p_side_mod30"],
            row["transport_q_side_mod30"],
            row["transport_both_side_mod30"],
        )
        for row in rows
    )
    return {
        "rule_id": RULE_ID,
        "status": "measured_directed_transport_audit",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "observed_at_winner_row_count": len(rows),
        "right_open_offset_by_endpoint_residue_mod30": RIGHT_OPEN_OFFSET_BY_ENDPOINT_RESIDUE,
        "right_step_endpoint_residue_mismatch_count": len(residue_step_mismatches),
        "defect_counts": dict(sorted(defect_counts.items())),
        "transport_balance_counts": dict(sorted(balance_counts.items())),
        "distinct_transport_key_count": len(transport_counts),
        "top_transport_keys": [
            {
                "right_boundary_defect": key[0],
                "transport_p_side_mod30": key[1],
                "transport_q_side_mod30": key[2],
                "transport_both_side_mod30": key[3],
                "count": count,
            }
            for key, count in transport_counts.most_common(12)
        ],
        "boundary": (
            "This audits directed multiplication transport on observed rows; "
            "it is not the endpoint exclusion rule and not factor recovery."
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Audit directed multiplication transport.")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the audit."""
    args = parse_args(argv)
    rows = load_rows(args.input_root)
    defect_rows = counter_rows(Counter(row["right_boundary_defect"] for row in rows), "right_boundary_defect")
    out_summary = summary(rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", out_summary)
    write_jsonl(args.output_dir / "transport_rows.jsonl", rows)
    write_jsonl(args.output_dir / "defect_count_rows.jsonl", defect_rows)
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
