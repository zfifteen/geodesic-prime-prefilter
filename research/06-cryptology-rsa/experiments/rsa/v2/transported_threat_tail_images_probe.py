#!/usr/bin/env python3
"""Emit transported threat/tail interval-position diagnostics for RSA v2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from run_experiment import (  # noqa: E402
    LadderCase,
    PGSCertificate,
    load_cases,
    pgs_certificate,
    previous_endpoint,
)


RULE_ID = "transported_threat_tail_images_v1"
DEFAULT_MEASURED_ROWS = 256
POSITION_FIELDS = (
    "threat_image_position",
    "tail_image_position",
    "induced_threat_position",
    "induced_tail_position",
)
BROAD_REGIME_NUMERATOR = 9
BROAD_REGIME_DENOMINATOR = 10


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def prior_endpoint_chain(start: gmpy2.mpz, measured_rows: int) -> list[gmpy2.mpz]:
    """Return a measurement-only chain of public previous endpoints."""
    if measured_rows < 1:
        raise ValueError("measured_rows must be positive")
    anchors: list[gmpy2.mpz] = []
    current = gmpy2.mpz(start)
    for _index in range(measured_rows):
        anchors.append(current)
        next_anchor = previous_endpoint(current - 1)
        if next_anchor is None:
            break
        current = next_anchor
    return anchors


def opposite_anchor_for(n_value: gmpy2.mpz, certificate: PGSCertificate) -> gmpy2.mpz | None:
    """Return the public opposite-side anchor induced by transported reset image."""
    image = n_value // certificate.reset_endpoint
    return previous_endpoint(image)


def threat_value(certificate: PGSCertificate) -> gmpy2.mpz | None:
    """Return the public lower-divisor threat coordinate when present."""
    if certificate.lower_d_threat_offset is None:
        return None
    return certificate.anchor + certificate.lower_d_threat_offset


def first_tail_offset(certificate: PGSCertificate) -> int | None:
    """Return the first public tail offset after reset when present."""
    if not certificate.tail_after_reset_offsets:
        return None
    return int(certificate.tail_after_reset_offsets[0])


def first_tail_value(certificate: PGSCertificate) -> gmpy2.mpz | None:
    """Return the first public tail coordinate after reset when present."""
    offset = first_tail_offset(certificate)
    if offset is None:
        return None
    return certificate.anchor + offset


def transport_image(n_value: gmpy2.mpz, value: gmpy2.mpz | None) -> gmpy2.mpz | None:
    """Return the reciprocal floor image for one public coordinate."""
    if value is None:
        return None
    return n_value // value


def interval_position(value: gmpy2.mpz | None, certificate: PGSCertificate | None) -> str:
    """Return one coordinate position against an induced reset-deadline interval."""
    if value is None or certificate is None or certificate.reset_deadline_value is None:
        return "missing"
    if certificate.reset_deadline_value < certificate.reset_endpoint:
        raise ValueError("certificate reset-deadline interval is inverted")
    if value < certificate.reset_endpoint:
        return "before_upper_reset"
    if value <= certificate.reset_deadline_value:
        return "inside_upper_interval"
    return "after_upper_deadline"


def public_row(case: LadderCase, source_certificate: PGSCertificate) -> dict[str, object]:
    """Return one public transported threat/tail diagnostic row."""
    induced_anchor = opposite_anchor_for(case.n, source_certificate)
    induced_certificate = None if induced_anchor is None else pgs_certificate(induced_anchor)

    source_threat_value = threat_value(source_certificate)
    source_tail_offset = first_tail_offset(source_certificate)
    source_tail_value = first_tail_value(source_certificate)
    threat_image = transport_image(case.n, source_threat_value)
    tail_image = transport_image(case.n, source_tail_value)

    induced_threat_value = None if induced_certificate is None else threat_value(induced_certificate)
    induced_tail_offset = None if induced_certificate is None else first_tail_offset(induced_certificate)
    induced_tail_value = None if induced_certificate is None else first_tail_value(induced_certificate)

    threat_position = interval_position(threat_image, induced_certificate)
    tail_position = interval_position(tail_image, induced_certificate)
    induced_threat_position = interval_position(induced_threat_value, induced_certificate)
    induced_tail_position = interval_position(induced_tail_value, induced_certificate)
    position_signature = "|".join(
        (
            threat_position,
            tail_position,
            induced_threat_position,
            induced_tail_position,
        )
    )

    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "source_anchor": str(source_certificate.anchor),
        "source_reset_endpoint": str(source_certificate.reset_endpoint),
        "source_reset_deadline_value": str(source_certificate.reset_deadline_value),
        "source_lower_d_threat_offset": source_certificate.lower_d_threat_offset,
        "source_tail_after_reset_offset": source_tail_offset,
        "source_threat_value": None if source_threat_value is None else str(source_threat_value),
        "source_tail_value": None if source_tail_value is None else str(source_tail_value),
        "transported_threat_image": None if threat_image is None else str(threat_image),
        "transported_tail_image": None if tail_image is None else str(tail_image),
        "induced_anchor": None if induced_anchor is None else str(induced_anchor),
        "induced_reset_endpoint": (
            None if induced_certificate is None else str(induced_certificate.reset_endpoint)
        ),
        "induced_reset_deadline_value": (
            None
            if induced_certificate is None or induced_certificate.reset_deadline_value is None
            else str(induced_certificate.reset_deadline_value)
        ),
        "induced_lower_d_threat_offset": (
            None if induced_certificate is None else induced_certificate.lower_d_threat_offset
        ),
        "induced_tail_after_reset_offset": induced_tail_offset,
        "induced_threat_value": (
            None if induced_threat_value is None else str(induced_threat_value)
        ),
        "induced_tail_value": None if induced_tail_value is None else str(induced_tail_value),
        "threat_image_position": threat_position,
        "tail_image_position": tail_position,
        "induced_threat_position": induced_threat_position,
        "induced_tail_position": induced_tail_position,
        "position_signature": position_signature,
    }


def case_rows(case: LadderCase, measured_rows: int) -> list[dict[str, object]]:
    """Return public transported threat/tail rows for one modulus case."""
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []
    rows: list[dict[str, object]] = []
    for anchor in prior_endpoint_chain(first_anchor, measured_rows):
        certificate = pgs_certificate(anchor)
        if certificate is None:
            continue
        rows.append(public_row(case, certificate))
    return rows


def count_values(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    """Return deterministic counts for one row field."""
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row[field])
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def field_summary(rows: list[dict[str, object]], field: str) -> dict[str, object]:
    """Return constant and broad-regime diagnostics for one position field."""
    counts = count_values(rows, field)
    row_count = len(rows)
    if not counts:
        return {
            "field": field,
            "counts": {},
            "unique_count": 0,
            "dominant_value": None,
            "dominant_count": 0,
            "is_constant": False,
            "is_broad_regime": False,
        }
    dominant_value, dominant_count = max(
        counts.items(),
        key=lambda item: (item[1], item[0]),
    )
    is_constant = len(counts) == 1
    is_broad = dominant_count * BROAD_REGIME_DENOMINATOR >= (
        row_count * BROAD_REGIME_NUMERATOR
    )
    return {
        "field": field,
        "counts": counts,
        "unique_count": len(counts),
        "dominant_value": dominant_value,
        "dominant_count": dominant_count,
        "dominant_fraction": f"{dominant_count}/{row_count}",
        "is_constant": is_constant,
        "is_broad_regime": is_broad,
    }


def summarize(rows: list[dict[str, object]], measured_rows: int) -> dict[str, object]:
    """Return falsification-oriented summary counts for sidecar rows."""
    cases = sorted({str(row["case_id"]) for row in rows})
    position_summaries = [field_summary(rows, field) for field in POSITION_FIELDS]
    constant_fields = [
        str(item["field"])
        for item in position_summaries
        if item["is_constant"]
    ]
    broad_fields = [
        str(item["field"])
        for item in position_summaries
        if item["is_broad_regime"]
    ]
    case_summaries = []
    for case_id in cases:
        case_rows_for_id = [row for row in rows if row["case_id"] == case_id]
        case_summaries.append(
            {
                "case_id": case_id,
                "row_count": len(case_rows_for_id),
                "position_signature_counts": count_values(
                    case_rows_for_id,
                    "position_signature",
                ),
                "position_field_summaries": [
                    field_summary(case_rows_for_id, field)
                    for field in POSITION_FIELDS
                ],
            }
        )

    diagnostic_status = (
        "positions_constant_or_broad_regime_only"
        if set(broad_fields) == set(POSITION_FIELDS)
        else "positions_have_multiple_regimes"
    )
    return {
        "rule_id": RULE_ID,
        "measured_rows_per_case": measured_rows,
        "case_count": len(cases),
        "cases": cases,
        "row_count": len(rows),
        "position_fields": list(POSITION_FIELDS),
        "broad_regime_threshold": {
            "numerator": BROAD_REGIME_NUMERATOR,
            "denominator": BROAD_REGIME_DENOMINATOR,
        },
        "constant_position_fields": constant_fields,
        "broad_regime_position_fields": broad_fields,
        "diagnostic_status": diagnostic_status,
        "position_signature_counts": count_values(rows, "position_signature"),
        "position_field_summaries": position_summaries,
        "case_summaries": case_summaries,
    }


def run_probe(
    cases_path: Path,
    measured_rows: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Run the public transported threat/tail image probe."""
    cases = load_cases(cases_path)
    rows: list[dict[str, object]] = []
    for case in cases:
        rows.extend(case_rows(case, measured_rows))
    return rows, summarize(rows, measured_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Emit public transported threat/tail image diagnostics."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=THIS_DIR / "fixtures" / "ladder_cases.jsonl",
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
        default=THIS_DIR / "output" / "transported_threat_tail_images",
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
