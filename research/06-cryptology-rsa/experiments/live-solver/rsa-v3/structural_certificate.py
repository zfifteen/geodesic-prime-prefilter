"""Structural certificate package builder for A1."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


SCHEMA_ID = "pgs_structural_certificate_v3"
ALGORITHM_VERSION = "pgs_rsa_endpoint_resolver_v3.1"
RULE_ID = "reciprocal_pgs_gwr_carrier_transport_v3"

FORBIDDEN_PUBLIC_KEYS = frozenset(
    {
        "p",
        "q",
        "factor",
        "factors",
        "audit_status",
        "audit_label",
        "confidence",
        "is_factor",
        "factor_found",
    }
)


def canonical_json(payload: Mapping[str, Any]) -> str:
    """Canonical JSON for hashing (sorted keys, compact separators)."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def content_hash(payload: Mapping[str, Any]) -> str:
    """SHA-256 content hash over payload without content_hash field."""
    body = {k: v for k, v in payload.items() if k != "content_hash"}
    digest = hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _side_cert_from_v2_prefix(pair_json: Mapping[str, Any], prefix: str) -> dict[str, Any] | None:
    """Build one side certificate dict from v2 pair_to_json fields."""
    anchor = pair_json.get(f"{prefix}_anchor")
    reset = pair_json.get(f"{prefix}_reset_endpoint")
    if anchor is None and reset is None:
        return None
    return {
        "anchor": None if anchor is None else str(anchor),
        "reset_endpoint": None if reset is None else str(reset),
        "gap_offset": pair_json.get(f"{prefix}_gap_offset"),
        "candidate_bound": pair_json.get(f"{prefix}_candidate_bound"),
        "active_count": pair_json.get(f"{prefix}_active_count"),
        "resolved_count": pair_json.get(f"{prefix}_resolved_count"),
        "unresolved_count": pair_json.get(f"{prefix}_unresolved_count"),
        "closed_offsets_before_q": pair_json.get(f"{prefix}_closed_offsets_before_q") or [],
        "carrier_w": pair_json.get(f"{prefix}_carrier_w"),
        "carrier_d": pair_json.get(f"{prefix}_carrier_d"),
        "lock_carrier_offset": pair_json.get(f"{prefix}_lock_carrier_offset"),
        "lock_carrier_d": pair_json.get(f"{prefix}_lock_carrier_d"),
        "lower_d_threat_offset": pair_json.get(f"{prefix}_d_threat_offset"),
        "tail_after_reset_offsets": pair_json.get(f"{prefix}_tail_after_reset_offsets") or [],
        "reset_deadline_value": pair_json.get(f"{prefix}_reset_deadline_value"),
        "reset_deadline_margin": pair_json.get(f"{prefix}_reset_deadline_margin"),
        "reset_signature": pair_json.get(f"{prefix}_reset_signature"),
    }


def assert_no_forbidden_public_fields(payload: Mapping[str, Any], path: str = "$") -> None:
    """Raise ValueError if forbidden audit/factor fields appear."""
    for key, value in payload.items():
        if key in FORBIDDEN_PUBLIC_KEYS:
            raise ValueError(f"forbidden public field {path}.{key}")
        if isinstance(value, dict):
            assert_no_forbidden_public_fields(value, f"{path}.{key}")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    assert_no_forbidden_public_fields(item, f"{path}.{key}[{i}]")


def build_structural_certificate(
    *,
    case_id: str,
    bits: int,
    n_value: str,
    center: str,
    closure_status: str,
    endpoint_lower: str,
    endpoint_upper: str,
    pair_json: Mapping[str, Any],
    gwr_predicate_map: Mapping[str, Any],
    step_index: int | None,
    git_commit: str | None,
) -> dict[str, Any]:
    """Build a versioned structural certificate package for a resolved class."""
    package: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "algorithm_version": ALGORITHM_VERSION,
        "rule_id": RULE_ID,
        "git_commit": git_commit,
        "case_id": case_id,
        "bits": int(bits),
        "N": str(n_value),
        "center": str(center),
        "step_index": step_index,
        "closure_status": closure_status,
        "endpoint_class": {
            "lower": str(endpoint_lower),
            "upper": str(endpoint_upper),
        },
        "lower_certificate": _side_cert_from_v2_prefix(pair_json, "lower"),
        "upper_certificate": _side_cert_from_v2_prefix(pair_json, "upper"),
        "corrected_lower_certificate": _side_cert_from_v2_prefix(pair_json, "corrected_lower"),
        "transport": {
            "endpoint_chain_transport_coordinate": pair_json.get(
                "endpoint_chain_transport_coordinate"
            ),
            "transported_upper_endpoint": pair_json.get("transported_upper_endpoint"),
            "transported_lower_endpoint": pair_json.get("transported_lower_endpoint"),
            "corrected_lower_endpoint": pair_json.get("corrected_lower_endpoint"),
            "corrected_upper_endpoint": pair_json.get("corrected_upper_endpoint"),
            "transported_corrected_upper_endpoint": pair_json.get(
                "transported_corrected_upper_endpoint"
            ),
            "transported_corrected_lower_endpoint": pair_json.get(
                "transported_corrected_lower_endpoint"
            ),
        },
        "gwr_carrier_closure": dict(gwr_predicate_map),
    }
    assert_no_forbidden_public_fields(package)
    package["content_hash"] = content_hash(package)
    return package


def rehash_certificate(cert: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy with content_hash recomputed over the body."""
    out = json.loads(json.dumps(cert))
    out["content_hash"] = content_hash(out)
    return out


def mutate_certificate_for_tests(
    cert: Mapping[str, Any],
    mutation: str,
    *,
    rehash: bool = True,
) -> dict[str, Any]:
    """Produce a deliberately broken certificate for fail-closed verifier tests.

    Semantic mutations (floor, signature, endpoint_class) rehash by default so
    the verifier must reject on structure, not only on a stale content_hash.
    Use mutation=\"bad_hash\" or rehash=False to test hash integrity alone.
    """
    broken = json.loads(json.dumps(cert))
    transport = broken.setdefault("transport", {})
    endpoint = broken.setdefault("endpoint_class", {})

    if mutation == "floor_equality":
        # Break reciprocal floor on the closed endpoint pair while keeping schema intact.
        # Prefer mutating endpoint_class so floor(N/lower)!=upper fails for every rule.
        if endpoint.get("upper") is not None:
            try:
                endpoint["upper"] = str(int(endpoint["upper"]) + 1)
            except (TypeError, ValueError):
                endpoint["upper"] = "1"
        if transport.get("corrected_upper_endpoint") is not None:
            try:
                transport["corrected_upper_endpoint"] = str(
                    int(transport["corrected_upper_endpoint"]) + 1
                )
            except (TypeError, ValueError):
                transport["corrected_upper_endpoint"] = "1"
        if transport.get("transported_upper_endpoint") is not None:
            try:
                transport["transported_upper_endpoint"] = str(
                    int(transport["transported_upper_endpoint"]) + 7
                )
            except (TypeError, ValueError):
                transport["transported_upper_endpoint"] = "1"
    elif mutation == "signature":
        # Break aligned signature equality without relying on magic token lists.
        upper = broken.get("upper_certificate") or {}
        upper["reset_signature"] = str(upper.get("reset_signature") or "") + "|broken"
        broken["upper_certificate"] = upper
        corrected = broken.get("corrected_lower_certificate")
        if isinstance(corrected, dict) and corrected.get("reset_signature") is not None:
            # Keep corrected sig as original so mismatch is lower-aligned vs upper.
            pass
        lower = broken.get("lower_certificate") or {}
        if lower.get("reset_signature") is not None and not isinstance(corrected, dict):
            # Mutual path: leave lower intact, upper already broken.
            pass
    elif mutation == "endpoint_class":
        # Diverges endpoint_class from closed certificate endpoints.
        if endpoint.get("lower") is not None:
            try:
                endpoint["lower"] = str(int(endpoint["lower"]) + 11)
            except (TypeError, ValueError):
                endpoint["lower"] = "999"
    elif mutation == "missing_field":
        broken.pop("endpoint_class", None)
        rehash = False  # missing required field; hash optional
    elif mutation == "bad_hash":
        broken["content_hash"] = "sha256:" + ("0" * 64)
        rehash = False
    else:
        raise ValueError(f"unknown mutation {mutation}")

    if rehash and "content_hash" in broken:
        broken = rehash_certificate(broken)
    return broken
