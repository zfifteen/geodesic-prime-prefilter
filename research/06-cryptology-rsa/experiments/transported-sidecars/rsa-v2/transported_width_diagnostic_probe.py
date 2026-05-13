#!/usr/bin/env python3
"""Measure public symmetric reset-to-deadline transported width diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = THIS_DIR.parents[1]
LIVE_SOLVER_DIR = EXPERIMENTS_DIR / "live-solver" / "rsa-v2"
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
for import_dir in (THIS_DIR, LIVE_SOLVER_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from run_experiment import (  # noqa: E402
    LadderCase,
    PGSCertificate,
    load_cases,
    pgs_certificate,
    previous_endpoint,
)
from transported_exclusion_debt_probe import prior_endpoint_chain  # noqa: E402


RULE_ID = "transported_width_diagnostic_v1"
DEFAULT_MEASURED_ROWS = 256


@dataclass(frozen=True)
class WidthFields:
    """One public reset-to-deadline width comparison in both directions."""

    source_width: int
    source_transported_width: int
    induced_width: int
    induced_transported_width: int
    source_to_induced_delta_abs: int
    induced_to_source_delta_abs: int
    exact_source_to_induced_width_match: bool
    exact_induced_to_source_width_match: bool
    exact_symmetric_width_match: bool
    carrier_tolerance: int
    carrier_source_to_induced_width_match: bool
    carrier_induced_to_source_width_match: bool
    carrier_symmetric_width_match: bool


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def certificate_width(certificate: PGSCertificate) -> int:
    """Return the public source-side reset-to-deadline width."""
    if certificate.reset_deadline_value is None:
        raise ValueError("certificate missing reset_deadline_value")
    return abs(int(certificate.reset_deadline_value - certificate.reset_endpoint))


def transported_width(n_value: gmpy2.mpz, certificate: PGSCertificate) -> int:
    """Return the public transported reset-to-deadline width."""
    if certificate.reset_deadline_value is None:
        raise ValueError("certificate missing reset_deadline_value")
    reset_image = n_value // certificate.reset_endpoint
    deadline_image = n_value // certificate.reset_deadline_value
    return abs(int(deadline_image - reset_image))


def deadline_kind(certificate: PGSCertificate) -> str | None:
    """Return the public reset-deadline kind encoded in the certificate signature."""
    if certificate.reset_signature is None:
        return None
    for part in certificate.reset_signature.split(";"):
        if part.startswith("deadline="):
            return part.split("=", 1)[1]
    return None


def interval_position(value: gmpy2.mpz, left: gmpy2.mpz, right: gmpy2.mpz) -> str:
    """Return one coordinate's position relative to a closed transported interval."""
    lo = min(left, right)
    hi = max(left, right)
    if value < lo:
        return "below"
    if value > hi:
        return "above"
    return "inside"


def frontier_class(
    n_value: gmpy2.mpz,
    source_certificate: PGSCertificate,
    opposite_certificate: PGSCertificate,
) -> tuple[object, ...]:
    """Return the documented static frontier-class tuple for one direction."""
    transport_reset = n_value // source_certificate.reset_endpoint
    if source_certificate.reset_deadline_value is None:
        raise ValueError("source certificate missing reset_deadline_value")
    transport_deadline = n_value // source_certificate.reset_deadline_value
    return (
        interval_position(
            opposite_certificate.reset_endpoint,
            transport_reset,
            transport_deadline,
        ),
        interval_position(
            opposite_certificate.reset_deadline_value,
            transport_reset,
            transport_deadline,
        ),
        deadline_kind(opposite_certificate),
        opposite_certificate.carrier_d,
        opposite_certificate.lock_carrier_d,
        opposite_certificate.lower_d_threat_offset is not None,
        bool(opposite_certificate.tail_after_reset_offsets),
    )


def width_fields(
    n_value: gmpy2.mpz,
    source_certificate: PGSCertificate,
    induced_certificate: PGSCertificate,
) -> WidthFields:
    """Return public exact and carrier-tolerant symmetric width fields."""
    if source_certificate.carrier_d is None:
        raise ValueError("source certificate missing carrier_d")
    if induced_certificate.carrier_d is None:
        raise ValueError("induced certificate missing carrier_d")

    source_width = certificate_width(source_certificate)
    source_transport = transported_width(n_value, source_certificate)
    induced_width = certificate_width(induced_certificate)
    induced_transport = transported_width(n_value, induced_certificate)
    source_delta = abs(source_transport - induced_width)
    induced_delta = abs(induced_transport - source_width)
    exact_source_match = source_delta <= 1
    exact_induced_match = induced_delta <= 1
    tolerance = max(source_certificate.carrier_d, induced_certificate.carrier_d)
    carrier_source_match = source_delta <= tolerance
    carrier_induced_match = induced_delta <= tolerance
    return WidthFields(
        source_width=source_width,
        source_transported_width=source_transport,
        induced_width=induced_width,
        induced_transported_width=induced_transport,
        source_to_induced_delta_abs=source_delta,
        induced_to_source_delta_abs=induced_delta,
        exact_source_to_induced_width_match=exact_source_match,
        exact_induced_to_source_width_match=exact_induced_match,
        exact_symmetric_width_match=exact_source_match and exact_induced_match,
        carrier_tolerance=tolerance,
        carrier_source_to_induced_width_match=carrier_source_match,
        carrier_induced_to_source_width_match=carrier_induced_match,
        carrier_symmetric_width_match=carrier_source_match and carrier_induced_match,
    )


def induced_certificate_for(
    n_value: gmpy2.mpz,
    source_certificate: PGSCertificate,
) -> tuple[gmpy2.mpz | None, PGSCertificate | None]:
    """Return the public opposite certificate induced by reset floor transport."""
    induced_anchor = previous_endpoint(n_value // source_certificate.reset_endpoint)
    if induced_anchor is None:
        return None, None
    return induced_anchor, pgs_certificate(induced_anchor)


def public_row(case: LadderCase, source_certificate: PGSCertificate) -> dict[str, object]:
    """Return one public symmetric width diagnostic row."""
    induced_anchor, induced_certificate = induced_certificate_for(case.n, source_certificate)
    base: dict[str, object] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "source_anchor": str(source_certificate.anchor),
        "source_reset_endpoint": str(source_certificate.reset_endpoint),
        "source_reset_deadline_value": str(source_certificate.reset_deadline_value),
        "source_carrier_d": source_certificate.carrier_d,
        "source_lock_carrier_d": source_certificate.lock_carrier_d,
        "induced_anchor": None if induced_anchor is None else str(induced_anchor),
        "induced_reset_endpoint": (
            None if induced_certificate is None else str(induced_certificate.reset_endpoint)
        ),
        "induced_reset_deadline_value": (
            None if induced_certificate is None else str(induced_certificate.reset_deadline_value)
        ),
        "induced_carrier_d": None if induced_certificate is None else induced_certificate.carrier_d,
        "induced_lock_carrier_d": (
            None if induced_certificate is None else induced_certificate.lock_carrier_d
        ),
    }
    if induced_certificate is None:
        base.update(
            {
                "source_width": certificate_width(source_certificate),
                "source_transported_width": transported_width(case.n, source_certificate),
                "induced_width": None,
                "induced_transported_width": None,
                "source_to_induced_delta_abs": None,
                "induced_to_source_delta_abs": None,
                "exact_source_to_induced_width_match": False,
                "exact_induced_to_source_width_match": False,
                "exact_symmetric_width_match": False,
                "carrier_tolerance": None,
                "carrier_source_to_induced_width_match": False,
                "carrier_induced_to_source_width_match": False,
                "carrier_symmetric_width_match": False,
                "static_frontier_class_match": False,
                "source_frontier_class": None,
                "induced_frontier_class": None,
            }
        )
        return base

    fields = width_fields(case.n, source_certificate, induced_certificate)
    source_class = frontier_class(case.n, source_certificate, induced_certificate)
    induced_class = frontier_class(case.n, induced_certificate, source_certificate)
    base.update(
        {
            "source_width": fields.source_width,
            "source_transported_width": fields.source_transported_width,
            "induced_width": fields.induced_width,
            "induced_transported_width": fields.induced_transported_width,
            "source_to_induced_delta_abs": fields.source_to_induced_delta_abs,
            "induced_to_source_delta_abs": fields.induced_to_source_delta_abs,
            "exact_source_to_induced_width_match": fields.exact_source_to_induced_width_match,
            "exact_induced_to_source_width_match": fields.exact_induced_to_source_width_match,
            "exact_symmetric_width_match": fields.exact_symmetric_width_match,
            "carrier_tolerance": fields.carrier_tolerance,
            "carrier_source_to_induced_width_match": fields.carrier_source_to_induced_width_match,
            "carrier_induced_to_source_width_match": fields.carrier_induced_to_source_width_match,
            "carrier_symmetric_width_match": fields.carrier_symmetric_width_match,
            "static_frontier_class_match": source_class == induced_class,
            "source_frontier_class": list(source_class),
            "induced_frontier_class": list(induced_class),
        }
    )
    return base


def case_rows(case: LadderCase, measured_rows: int) -> list[dict[str, object]]:
    """Return public symmetric width diagnostic rows for one modulus case."""
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []
    rows: list[dict[str, object]] = []
    for anchor in prior_endpoint_chain(first_anchor, measured_rows):
        certificate = pgs_certificate(anchor)
        if certificate is not None:
            rows.append(public_row(case, certificate))
    return rows


def count(rows: list[dict[str, object]], field: str) -> int:
    """Return the number of rows where one boolean field is true."""
    return sum(1 for row in rows if row[field])


def summarize_case(case_id: str, rows: list[dict[str, object]]) -> dict[str, object]:
    """Return per-case falsification counts for one diagnostic surface."""
    exact_hits = count(rows, "exact_symmetric_width_match")
    carrier_hits = count(rows, "carrier_symmetric_width_match")
    static_hits = count(rows, "static_frontier_class_match")
    return {
        "case_id": case_id,
        "row_count": len(rows),
        "official_unresolved_surface_count": len(rows),
        "missing_induced_certificate_count": sum(
            1 for row in rows if row["induced_anchor"] is None
        ),
        "static_frontier_class_match_count": static_hits,
        "exact_symmetric_width_match_count": exact_hits,
        "carrier_symmetric_width_match_count": carrier_hits,
        "exact_false_positive_against_unresolved_count": exact_hits,
        "carrier_false_positive_against_unresolved_count": carrier_hits,
        "exact_false_positive_against_static_frontier_count": sum(
            1
            for row in rows
            if row["exact_symmetric_width_match"] and row["static_frontier_class_match"]
        ),
        "carrier_false_positive_against_static_frontier_count": sum(
            1
            for row in rows
            if row["carrier_symmetric_width_match"] and row["static_frontier_class_match"]
        ),
    }


def summarize(rows: list[dict[str, object]], measured_rows: int) -> dict[str, object]:
    """Return falsification-oriented summary counts for width diagnostics."""
    case_ids = sorted({str(row["case_id"]) for row in rows})
    case_summaries = [
        summarize_case(case_id, [row for row in rows if row["case_id"] == case_id])
        for case_id in case_ids
    ]
    exact_hits = count(rows, "exact_symmetric_width_match")
    carrier_hits = count(rows, "carrier_symmetric_width_match")
    static_hits = count(rows, "static_frontier_class_match")
    return {
        "rule_id": RULE_ID,
        "measured_rows_per_case": measured_rows,
        "case_count": len(case_ids),
        "cases": case_ids,
        "case_summaries": case_summaries,
        "row_count": len(rows),
        "official_unresolved_surface_count": len(rows),
        "static_frontier_class_match_count": static_hits,
        "exact_symmetric_width_match_count": exact_hits,
        "carrier_symmetric_width_match_count": carrier_hits,
        "exact_false_positive_against_unresolved_count": exact_hits,
        "carrier_false_positive_against_unresolved_count": carrier_hits,
        "exact_false_positive_against_static_frontier_count": sum(
            1
            for row in rows
            if row["exact_symmetric_width_match"] and row["static_frontier_class_match"]
        ),
        "carrier_false_positive_against_static_frontier_count": sum(
            1
            for row in rows
            if row["carrier_symmetric_width_match"] and row["static_frontier_class_match"]
        ),
        "missing_induced_certificate_count": sum(
            1 for row in rows if row["induced_anchor"] is None
        ),
        "diagnostic_status": "diagnostic_only_no_closure_claim",
    }


def run_probe(
    cases_path: Path,
    measured_rows: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Run the public symmetric width diagnostic probe."""
    cases = load_cases(cases_path)
    rows: list[dict[str, object]] = []
    for case in cases:
        rows.extend(case_rows(case, measured_rows))
    return rows, summarize(rows, measured_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Emit public transported width diagnostics.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--measured-rows",
        type=int,
        default=DEFAULT_MEASURED_ROWS,
        help="Measurement-only public frontier rows per case.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "transported_width_diagnostic",
        help="Directory for rows.jsonl and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary = run_probe(args.cases, args.measured_rows)
    write_jsonl(args.output_dir / "rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
