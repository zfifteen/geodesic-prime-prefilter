#!/usr/bin/env python3
"""Measure whether the public boundary-drop field is already in the live rows."""

from __future__ import annotations

import json
from pathlib import Path


CASE_ORDER = (
    "rsa_v2_40bit_static_001",
    "rsa_v2_50bit_static_001",
    "rsa_v2_64bit_static_001",
)

ROOT = Path(__file__).resolve().parents[2]
TRACK_DIR = Path(__file__).resolve().parent
SURVIVOR_PATH = (
    ROOT
    / "research"
    / "06-cryptology-rsa"
    / "experiments"
    / "live-solver"
    / "rsa-v2"
    / "output"
    / "survivor_rows.jsonl"
)
OUTPUT_PATH = TRACK_DIR / "2026-05-20-boundary-drop-admissibility-probe.json"


def load_survivor_rows() -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for line in SURVIVOR_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[str(row["case_id"])] = row
    missing = [case_id for case_id in CASE_ORDER if case_id not in rows]
    if missing:
        raise RuntimeError(f"missing survivor rows: {missing}")
    return rows


def selected_cell(row: dict[str, object]) -> tuple[int, int, str]:
    status = str(row["public_closure_status"])
    if status == "endpoint_class_by_reciprocal_deadline_signature_correction":
        return (
            int(str(row["corrected_lower_endpoint"])),
            int(str(row["corrected_upper_endpoint"])),
            "emitted_deadline_signature_endpoint_cell",
        )
    if status in {
        "endpoint_class_by_mutual_certificate_closure",
        "unresolved_by_reciprocal_carrier_misalignment",
    }:
        return (
            int(str(row["lower_reset_endpoint"])),
            int(str(row["upper_reset_endpoint"])),
            "mutual_reset_endpoint_cell",
        )
    raise RuntimeError(f"unexpected status for boundary-drop probe: {status}")


def boundary_drop_row(row: dict[str, object]) -> dict[str, object]:
    n_value = int(str(row["N"]))
    lower, upper, cell_source = selected_cell(row)

    t_lower = n_value // lower
    t_upper = n_value // upper
    t_minus_one_lower = (n_value - 1) // lower
    t_minus_one_upper = (n_value - 1) // upper

    lower_boundary_drop = t_lower - t_minus_one_lower
    upper_boundary_drop = t_upper - t_minus_one_upper
    mutual_floor_closure = t_lower == upper and t_upper == lower
    boundary_drop_closure = lower_boundary_drop == 1 and upper_boundary_drop == 1
    promoted_by_boundary_drop = mutual_floor_closure and boundary_drop_closure

    current_field_names = set(row.keys())
    current_rows_export_boundary_drop = any(
        "minus_one" in name or "boundary_drop" in name or "n_minus_1" in name
        for name in current_field_names
    )

    return {
        "case_id": row["case_id"],
        "bits": row["bits"],
        "public_closure_status": row["public_closure_status"],
        "cell_source": cell_source,
        "endpoint_cell_lower": str(lower),
        "endpoint_cell_upper": str(upper),
        "T_N_lower": str(t_lower),
        "T_N_upper": str(t_upper),
        "T_N_minus_1_lower": str(t_minus_one_lower),
        "T_N_minus_1_upper": str(t_minus_one_upper),
        "lower_boundary_drop": lower_boundary_drop,
        "upper_boundary_drop": upper_boundary_drop,
        "mutual_floor_closure": mutual_floor_closure,
        "boundary_drop_closure": boundary_drop_closure,
        "promoted_by_boundary_drop": promoted_by_boundary_drop,
        "current_rows_export_boundary_drop": current_rows_export_boundary_drop,
        "audit_only_residual": str(n_value - lower * upper),
    }


def main() -> None:
    rows = load_survivor_rows()
    measured_rows = [boundary_drop_row(rows[case_id]) for case_id in CASE_ORDER]
    payload = {
        "probe": "boundary_drop_admissibility_probe",
        "status": "ADVANCE",
        "inference_boundary": (
            "The probe measures T_N and T_{N-1} floor-cell boundary behavior for "
            "already emitted or already rejected public endpoint cells. The "
            "audit_only_residual field is not used to promote an endpoint."
        ),
        "bridge_lemma": (
            "If a public endpoint cell (L,U) has floor(N/L)=U and floor(N/U)=L, "
            "then floor((N-1)/L)=U-1 and floor((N-1)/U)=L-1 proves N=LU."
        ),
        "current_certificate_contract_finding": (
            "The live survivor rows do not export a boundary-drop or N-minus-one "
            "transport certificate field. Admitting it is a new public endpoint-cell "
            "promotion rule unless the transported certificate law derives it."
        ),
        "rows": measured_rows,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
