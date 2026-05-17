#!/usr/bin/env python3
"""Audit the mod-30 residue bridge for the public o6 terminal-twin triggers."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import pair_identity_key, public_key
from directional_boundary_gate_surface import boundary_index_from_pair_key
from slot_factor_public_quotient_test import read_jsonl
from terminal_twin_lift_probe import has_terminal_twin_lift


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "public_o6_residue_bridge_probe"
RULE_ID = "pedk_public_o6_residue_bridge_probe_v1"
BLOCKED_RESIDUES_MOD30 = {0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27}
FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
ALLOWED_RESIDUES_MOD30 = (1, 7, 11, 13, 17, 19, 23, 29)


def first_open_offset_for_residue(residue: int) -> int:
    """Return the first wheel-open offset after one mod-30 residue."""
    for offset in FIRST_OPEN_OFFSETS:
        if (residue + offset) % 30 not in BLOCKED_RESIDUES_MOD30:
            return offset
    raise ValueError(f"no first-open offset for residue {residue}")


def wheel_o4_residues() -> tuple[int, ...]:
    """Return endpoint residues whose first right-open offset is 4."""
    return tuple(
        residue
        for residue in ALLOWED_RESIDUES_MOD30
        if first_open_offset_for_residue(residue) == 4
    )


def residue_pairs_for_product(
    residues: tuple[int, ...],
    product_residue: int,
) -> list[tuple[int, int]]:
    """Return ordered residue pairs with the requested product residue."""
    return [
        (left, right)
        for left in residues
        for right in residues
        if (left * right) % 30 == product_residue
    ]


def enriched_rows() -> list[dict[str, object]]:
    """Return all enriched rows in the current output tree."""
    rows = []
    for path in sorted(INPUT_ROOT.glob("enriched_multiplication_map_corpus_*/enriched_rows.jsonl")):
        window = path.parent.name.replace("enriched_multiplication_map_corpus_", "")
        for row in read_jsonl(path):
            row = dict(row)
            row["window"] = window
            rows.append(row)
    return rows


def trigger_public_keys() -> set[str]:
    """Return the two public keys from the terminal-twin trigger probe."""
    rows = read_jsonl(
        INPUT_ROOT
        / "public_o6_terminal_twin_trigger_probe"
        / "public_trigger_rows.jsonl"
    )
    return {str(row["public_key"]) for row in rows}


def trigger_rows() -> list[dict[str, object]]:
    """Return observed rows matching the trigger public keys and Rres=o4|o4."""
    keys = trigger_public_keys()
    out = []
    for row in enriched_rows():
        pair_key = pair_identity_key(row)
        if public_key(row) not in keys:
            continue
        if boundary_index_from_pair_key(pair_key, "right_residues") != "Rres=o4|o4":
            continue
        p_residue = int(row["p"]) % 30
        q_residue = int(row["q"]) % 30
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "public_key": public_key(row),
                "N_mod30": int(row["N"]) % 30,
                "p_mod30": p_residue,
                "q_mod30": q_residue,
                "factor_residue_pair_mod30": f"{p_residue}|{q_residue}",
                "has_terminal_twin_lift": has_terminal_twin_lift(row),
                "pair_identity_key": pair_key,
            }
        )
    out.sort(
        key=lambda row: (
            str(row["public_key"]),
            str(row["window"]),
            str(row["case_id"]),
        )
    )
    return out


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact residue bridge summary."""
    o4_residues = wheel_o4_residues()
    product_pairs = residue_pairs_for_product(o4_residues, 7)
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_o6_residue_bridge_probe",
        "theorem_status": "hypothesis_not_proved",
        "wheel_o4_residues": list(o4_residues),
        "o4_residue_pairs_with_product_7": [
            f"{left}|{right}" for left, right in product_pairs
        ],
        "trigger_rres_o4_row_count": len(rows),
        "trigger_N_mod30_counts": dict(
            sorted(Counter(row["N_mod30"] for row in rows).items())
        ),
        "trigger_factor_residue_pair_counts": dict(
            sorted(Counter(row["factor_residue_pair_mod30"] for row in rows).items())
        ),
        "trigger_terminal_twin_lift_count": sum(
            1 for row in rows if row["has_terminal_twin_lift"]
        ),
        "trigger_terminal_twin_lift_by_public_key": dict(
            sorted(
                Counter(
                    row["public_key"]
                    for row in rows
                    if row["has_terminal_twin_lift"]
                ).items()
            )
        ),
        "trigger_public_key_counts": dict(
            sorted(Counter(row["public_key"] for row in rows).items())
        ),
        "sharper_arithmetic_statement": (
            "For the two public o6 trigger keys, every observed Rres=o4|o4 "
            "row has N mod 30 = 7. Since the endpoint residues with first "
            "right-open offset 4 are 7, 13, and 19, the only ordered o4|o4 "
            "factor residue pairs with product 7 are 13|19 and 19|13."
        ),
    }


def main() -> int:
    """Run the public o6 residue bridge probe."""
    rows = trigger_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows))
    write_jsonl(OUTPUT_DIR / "trigger_rows.jsonl", rows)
    print(json.dumps(summary(rows), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
