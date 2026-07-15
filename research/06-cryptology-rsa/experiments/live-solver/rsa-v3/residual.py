"""Residual taxonomy helpers for A1."""

from __future__ import annotations

from typing import Any, Mapping

TAXONOMY: dict[str, str] = {
    "unresolved_by_missing_lower_certificate": "No lower chamber-reset certificate at start anchor",
    "unresolved_by_endpoint_chain_boundary": "Walk exhausted lower balance without closure",
    "unresolved_by_endpoint_chain_cycle": "Repeated anchor in chain walk",
    "unresolved_by_certificate_pair_not_closed": "Transport present but no reset or deadline closure",
    "unresolved_by_reciprocal_carrier_misalignment": "GWR-carrier floor transport bound failed",
    "unresolved_by_first_tail_misalignment": "First-tail reciprocal proximity failed",
    "unresolved_by_joint_cell_C1T2L1": (
        "Joint residual cell C1T2L1: dual-gap D holds with loose carrier rank "
        "(delta_c > tight band 20), hard first-tail miss (rank 2), and weak lower lock"
    ),
    "unresolved_by_lower_lock_misalignment": "Lower lock dominance failed",
    "unresolved_by_profile_count_mismatch": "Active/unresolved profile counts mismatched",
    "unresolved_by_gwr_carrier_fields_absent": "Carrier fields required for GWR closure were missing",
    "unresolved_by_instrumentation_limit": "Large-bit instrumentation hit max_steps or bootstrap limit",
}

RESOLVED_PREFIX = "endpoint_class_by_"


def is_resolved_status(status: str) -> bool:
    return str(status).startswith(RESOLVED_PREFIX)


def is_known_residual(code: str) -> bool:
    return code in TAXONOMY


def coerce_residual_code(code: str | None) -> str:
    """Map unknown or empty residual codes to a taxonomy-safe instrumentation residual.

    Resolve paths must never raise on novel v2 residual labels; they map here.
    """
    if code is None or not str(code).strip():
        return "unresolved_by_instrumentation_limit"
    text = str(code)
    if text in TAXONOMY:
        return text
    if text.startswith("endpoint_class_by_"):
        # Mis-tagged resolved status is not a residual; force honest unresolved.
        return "unresolved_by_certificate_pair_not_closed"
    return "unresolved_by_instrumentation_limit"


def build_residual_row(
    *,
    case_id: str,
    bits: int,
    n_value: str,
    residual_code: str,
    step_index: int | None,
    stage: str,
    lower_present: bool,
    upper_present: bool,
    diagnostics: Mapping[str, Any] | None = None,
    rule_id: str,
    algorithm_version: str,
) -> dict[str, Any]:
    """Build one residual ledger row with required diagnostics."""
    if residual_code not in TAXONOMY:
        raise ValueError(f"unknown residual code: {residual_code}")
    return {
        "case_id": case_id,
        "bits": bits,
        "N": str(n_value),
        "residual_code": residual_code,
        "residual_meaning": TAXONOMY[residual_code],
        "step_index": step_index,
        "stage": stage,
        "lower_certificate_present": lower_present,
        "upper_certificate_present": upper_present,
        "diagnostics": dict(diagnostics or {}),
        "rule_id": rule_id,
        "algorithm_version": algorithm_version,
    }
