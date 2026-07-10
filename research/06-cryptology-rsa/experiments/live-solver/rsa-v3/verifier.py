#!/usr/bin/env python3
"""Standalone structural certificate verifier (A1 FR-CERT-02/03).

Fails closed. Never uses classical factor APIs to repair a certificate.

Semantic checks (all resolved closure rules):
- required fields and schema
- no forbidden audit/factor keys
- content_hash integrity
- endpoint_class matches the closed endpoints for the named closure rule
- reciprocal floor transport: floor(N / lower) == upper and floor(N / upper) == lower
  on the closed endpoint pair
- reset signatures equal on the aligned lower certificate and upper certificate
- transport images consistent with floor maps when present
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from structural_certificate import (
    FORBIDDEN_PUBLIC_KEYS,
    SCHEMA_ID,
    content_hash,
)


REQUIRED_TOP = (
    "schema",
    "algorithm_version",
    "rule_id",
    "case_id",
    "bits",
    "N",
    "center",
    "closure_status",
    "endpoint_class",
    "transport",
    "gwr_carrier_closure",
    "content_hash",
)

RESOLVED_PREFIX = "endpoint_class_by_"
MUTUAL = "endpoint_class_by_mutual_certificate_closure"
DEADLINE = "endpoint_class_by_reciprocal_deadline_signature_correction"
CHAIN = "endpoint_class_by_oriented_endpoint_chain_closure"


def _scan_forbidden(payload: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FORBIDDEN_PUBLIC_KEYS:
                errors.append(f"forbidden field {path}.{key}")
            errors.extend(_scan_forbidden(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for i, item in enumerate(payload):
            errors.extend(_scan_forbidden(item, f"{path}[{i}]"))
    return errors


def _as_int(value: Any, label: str, errors: list[str]) -> int | None:
    if value is None or value == "":
        errors.append(f"{label} is missing")
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        errors.append(f"{label} is not an integer string: {value!r}")
        return None


def _try_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _closed_endpoint_pair(
    cert: dict[str, Any],
    closure: str,
    errors: list[str],
) -> tuple[int | None, int | None]:
    """Return the closed lower/upper endpoints implied by the closure rule."""
    transport = cert.get("transport") or {}
    lower_cert = cert.get("lower_certificate") or {}
    upper_cert = cert.get("upper_certificate") or {}
    corrected = cert.get("corrected_lower_certificate") or {}
    endpoint = cert.get("endpoint_class") or {}

    if closure == MUTUAL:
        lower = _try_int(lower_cert.get("reset_endpoint"))
        upper = _try_int(upper_cert.get("reset_endpoint"))
        if lower is None:
            errors.append("mutual closure missing lower_certificate.reset_endpoint")
        if upper is None:
            errors.append("mutual closure missing upper_certificate.reset_endpoint")
        return lower, upper

    if closure in (DEADLINE, CHAIN):
        lower = _try_int(transport.get("corrected_lower_endpoint"))
        upper = _try_int(transport.get("corrected_upper_endpoint"))
        if lower is None:
            lower = _try_int(corrected.get("reset_endpoint"))
        if upper is None:
            upper = _try_int(upper_cert.get("reset_deadline_value"))
        if lower is None:
            lower = _try_int(endpoint.get("lower"))
        if upper is None:
            upper = _try_int(endpoint.get("upper"))
        if lower is None:
            errors.append("deadline/chain closure missing closed lower endpoint")
        if upper is None:
            errors.append("deadline/chain closure missing closed upper endpoint")
        return lower, upper

    lower = _try_int(endpoint.get("lower"))
    upper = _try_int(endpoint.get("upper"))
    if lower is None or upper is None:
        errors.append("resolved certificate missing endpoint_class endpoints")
    return lower, upper


def _aligned_lower_signature(cert: dict[str, Any], closure: str) -> Any:
    """Signature side used for GWR/deadline alignment checks."""
    if closure == MUTUAL:
        lower_cert = cert.get("lower_certificate") or {}
        return lower_cert.get("reset_signature")
    corrected = cert.get("corrected_lower_certificate") or {}
    if corrected.get("reset_signature") is not None:
        return corrected.get("reset_signature")
    lower_cert = cert.get("lower_certificate") or {}
    return lower_cert.get("reset_signature")


def _check_resolved_semantics(cert: dict[str, Any], errors: list[str]) -> None:
    """Semantic fail-closed checks for any endpoint_class_by_* certificate."""
    closure = str(cert.get("closure_status") or "")
    if not closure.startswith(RESOLVED_PREFIX):
        return

    n_value = _as_int(cert.get("N"), "N", errors)
    if n_value is None or n_value <= 0:
        if n_value is not None:
            errors.append("N must be positive")
        return

    endpoint = cert.get("endpoint_class")
    if not isinstance(endpoint, dict):
        return

    class_lower = _as_int(endpoint.get("lower"), "endpoint_class.lower", errors)
    class_upper = _as_int(endpoint.get("upper"), "endpoint_class.upper", errors)
    closed_lower, closed_upper = _closed_endpoint_pair(cert, closure, errors)

    # endpoint_class must match the closed endpoints for the named rule.
    if (
        class_lower is not None
        and closed_lower is not None
        and class_lower != closed_lower
    ):
        errors.append(
            f"endpoint_class.lower {class_lower} != closed lower endpoint {closed_lower}"
        )
    if (
        class_upper is not None
        and closed_upper is not None
        and class_upper != closed_upper
    ):
        errors.append(
            f"endpoint_class.upper {class_upper} != closed upper endpoint {closed_upper}"
        )

    # Reciprocal floor transport on the public closed pair (class endpoints if present).
    lower_ep = class_lower if class_lower is not None else closed_lower
    upper_ep = class_upper if class_upper is not None else closed_upper
    if lower_ep is not None and upper_ep is not None:
        if lower_ep <= 0 or upper_ep <= 0:
            errors.append("closed endpoints must be positive")
        else:
            if n_value // lower_ep != upper_ep:
                errors.append(
                    f"floor transport failed: floor(N/lower)={n_value // lower_ep} != upper={upper_ep}"
                )
            if n_value // upper_ep != lower_ep:
                errors.append(
                    f"floor transport failed: floor(N/upper)={n_value // upper_ep} != lower={lower_ep}"
                )

    # Signature equality under the named closure rule (aligned lower vs upper).
    upper_cert = cert.get("upper_certificate") or {}
    lower_sig = _aligned_lower_signature(cert, closure)
    upper_sig = upper_cert.get("reset_signature")
    if lower_sig is None or upper_sig is None:
        errors.append("aligned lower and upper reset_signature are required for resolved class")
    elif lower_sig != upper_sig:
        errors.append("aligned lower and upper reset_signature do not match")

    # Transport images, when present, must equal floor maps of the stated coordinates.
    transport = cert.get("transport") or {}
    tu = transport.get("transported_upper_endpoint")
    tl = transport.get("transported_lower_endpoint")
    coord = transport.get("endpoint_chain_transport_coordinate")
    lower_cert = cert.get("lower_certificate") or {}
    upper_reset = upper_cert.get("reset_endpoint")

    if coord is not None and tu is not None:
        c = _as_int(coord, "transport.endpoint_chain_transport_coordinate", errors)
        tui = _as_int(tu, "transport.transported_upper_endpoint", errors)
        if c is not None and tui is not None and c > 0 and n_value // c != tui:
            errors.append(
                f"transport.transported_upper_endpoint {tui} != floor(N/coord)={n_value // c}"
            )

    if upper_reset is not None and tl is not None:
        ur = _as_int(upper_reset, "upper_certificate.reset_endpoint", errors)
        tli = _as_int(tl, "transport.transported_lower_endpoint", errors)
        if ur is not None and tli is not None and ur > 0 and n_value // ur != tli:
            errors.append(
                f"transport.transported_lower_endpoint {tli} != floor(N/upper.reset)={n_value // ur}"
            )

    # Deadline / chain correction transport consistency when both corrected fields exist.
    if closure in (DEADLINE, CHAIN):
        cl = transport.get("corrected_lower_endpoint")
        cu = transport.get("corrected_upper_endpoint")
        tcl = transport.get("transported_corrected_lower_endpoint")
        tcu = transport.get("transported_corrected_upper_endpoint")
        cli = _as_int(cl, "transport.corrected_lower_endpoint", errors) if cl is not None else None
        cui = _as_int(cu, "transport.corrected_upper_endpoint", errors) if cu is not None else None
        if cli is not None and cui is not None and cli > 0 and cui > 0:
            if n_value // cli != cui:
                errors.append(
                    f"corrected pair floor failed: floor(N/corrected_lower)={n_value // cli} != corrected_upper={cui}"
                )
            if n_value // cui != cli:
                errors.append(
                    f"corrected pair floor failed: floor(N/corrected_upper)={n_value // cui} != corrected_lower={cli}"
                )
        if tcu is not None and cli is not None and cli > 0:
            tcui = _as_int(tcu, "transport.transported_corrected_upper_endpoint", errors)
            if tcui is not None and n_value // cli != tcui:
                errors.append(
                    "transport.transported_corrected_upper_endpoint inconsistent with floor(N/corrected_lower)"
                )
        if tcl is not None and cui is not None and cui > 0:
            tcli = _as_int(tcl, "transport.transported_corrected_lower_endpoint", errors)
            if tcli is not None and n_value // cui != tcli:
                errors.append(
                    "transport.transported_corrected_lower_endpoint inconsistent with floor(N/corrected_upper)"
                )


def verify_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    """Verify one structural certificate. Returns report dict with ok bool."""
    errors: list[str] = []
    if not isinstance(cert, dict):
        return {"ok": False, "errors": ["certificate is not an object"]}

    for key in REQUIRED_TOP:
        if key not in cert:
            errors.append(f"missing required field {key}")

    if cert.get("schema") != SCHEMA_ID:
        errors.append(f"schema must be {SCHEMA_ID}")

    endpoint = cert.get("endpoint_class")
    if not isinstance(endpoint, dict):
        errors.append("endpoint_class must be object")
    else:
        if "lower" not in endpoint or "upper" not in endpoint:
            errors.append("endpoint_class requires lower and upper")
        if not endpoint.get("lower") or not endpoint.get("upper"):
            errors.append("endpoint_class lower/upper must be non-empty")

    errors.extend(_scan_forbidden(cert))

    # Content hash integrity
    expected = content_hash(cert)
    actual = cert.get("content_hash")
    if actual != expected:
        errors.append(f"content_hash mismatch: got {actual}, expected {expected}")

    _check_resolved_semantics(cert, errors)

    return {
        "ok": not errors,
        "case_id": cert.get("case_id"),
        "errors": errors,
        "content_hash": cert.get("content_hash"),
    }


def verify_path(path: Path) -> dict[str, Any]:
    """Verify a JSONL file of certificates or a single JSON certificate."""
    text = path.read_text(encoding="utf-8").strip()
    reports: list[dict[str, Any]] = []
    if not text:
        return {"ok": False, "count": 0, "accepted": 0, "rejected": 0, "reports": []}
    if path.suffix == ".jsonl" or "\n" in text:
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        rows = [json.loads(text)]
    for row in rows:
        reports.append(verify_certificate(row))
    accepted = sum(1 for r in reports if r["ok"])
    rejected = len(reports) - accepted
    return {
        "ok": rejected == 0 and accepted > 0,
        "count": len(reports),
        "accepted": accepted,
        "rejected": rejected,
        "reports": reports,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify A1 structural certificates.")
    parser.add_argument("--certs", type=Path, required=True, help="Certificate JSON or JSONL path.")
    parser.add_argument("--report", type=Path, default=None, help="Optional report JSON path.")
    args = parser.parse_args(argv)
    report = verify_path(args.certs)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("ok", "count", "accepted", "rejected")}, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
