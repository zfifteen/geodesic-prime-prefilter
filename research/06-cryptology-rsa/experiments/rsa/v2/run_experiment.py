#!/usr/bin/env python3
"""Run the RSA v2 reciprocal PGSPG certificate-pair experiment."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import gmpy2


ROOT = Path(__file__).resolve().parents[5]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)


RULE_ID = "reciprocal_pgs_certificate_pair_v2"
BALANCE_BAND = gmpy2.mpz(2)
RULE_X_CANDIDATE_BOUND = 128


@dataclass(frozen=True)
class LadderCase:
    """One public modulus rung."""

    case_id: str
    bits: int
    n: gmpy2.mpz


@dataclass(frozen=True)
class PGSCertificate:
    """One PGSPG reset certificate derived from a public previous endpoint."""

    anchor: gmpy2.mpz
    reset_endpoint: gmpy2.mpz
    gap_offset: int
    candidate_bound: int
    active_count: int
    resolved_count: int
    unresolved_count: int
    closed_offsets_before_q: tuple[int, ...]
    carrier_w: gmpy2.mpz | None
    carrier_d: int | None
    lock_carrier_offset: int | None
    lock_carrier_d: int | None
    lower_d_threat_offset: int | None
    tail_after_reset_offsets: tuple[int, ...]
    reset_deadline_value: gmpy2.mpz | None
    reset_deadline_margin: int | None
    reset_signature: str | None


CertificateCache = dict[int, PGSCertificate | None]
PreviousEndpointCache = dict[int, gmpy2.mpz | None]
SegmentCache = dict[tuple[int, int], object]
DiagnosticCounters = dict[str, int]


@dataclass(frozen=True)
class CertificatePair:
    """One reciprocal pair of lower and upper PGSPG certificates."""

    lower: PGSCertificate | None
    upper: PGSCertificate | None
    corrected_lower: PGSCertificate | None
    corrected_lower_endpoint: gmpy2.mpz | None
    corrected_upper_endpoint: gmpy2.mpz | None
    transported_upper_endpoint: gmpy2.mpz | None
    transported_lower_endpoint: gmpy2.mpz | None
    transported_corrected_upper_endpoint: gmpy2.mpz | None
    transported_corrected_lower_endpoint: gmpy2.mpz | None
    lower_transported_deadline_width: int | None
    upper_transported_deadline_width: int | None
    closure_status: str
    endpoint_chain_steps: int | None = None
    endpoint_chain_source_anchor: gmpy2.mpz | None = None
    endpoint_chain_transport_coordinate: gmpy2.mpz | None = None


def mpz_to_int(value: gmpy2.mpz) -> int:
    """Convert one GMP coordinate for the current exact small-regime backend."""
    return int(value)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def load_cases(path: Path) -> list[LadderCase]:
    """Load public ladder cases without hidden fields."""
    cases: list[LadderCase] = []
    for row in read_jsonl(path):
        if "p" in row or "q" in row:
            raise ValueError("public case rows must not contain audit-only endpoints")
        n_value = gmpy2.mpz(str(row["N"]))
        cases.append(
            LadderCase(
                case_id=str(row["case_id"]),
                bits=int(row["bits"]),
                n=n_value,
            )
        )
    return cases


def balance_bounds(center: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Return the public balanced factor interval."""
    # Dividing the square-root center gives the lower balanced endpoint.
    lower = center // BALANCE_BAND
    # Multiplying the square-root center gives the upper balanced endpoint.
    upper = center * BALANCE_BAND
    return lower, upper


def reciprocal_floor(n_value: gmpy2.mpz, value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the public reciprocal floor coordinate for one value."""
    # The floor reciprocal transports one public coordinate to the opposite side of N.
    return n_value // value


def divisor_counts_window(
    lo: int,
    hi: int,
    segment_cache: SegmentCache | None = None,
    diagnostics: DiagnosticCounters | None = None,
) -> object:
    """Return one case-local cached exact divisor-count segment."""
    if diagnostics is not None:
        diagnostics["divisor_segment_lookups"] += 1
    if segment_cache is None:
        if diagnostics is not None:
            diagnostics["divisor_segment_calls"] += 1
        return divisor_counts_segment(lo, hi)
    key = (lo, hi)
    if key not in segment_cache:
        if diagnostics is not None:
            diagnostics["divisor_segment_calls"] += 1
        segment_cache[key] = divisor_counts_segment(lo, hi)
    return segment_cache[key]


def previous_endpoint(
    value: gmpy2.mpz,
    segment_cache: SegmentCache | None = None,
    diagnostics: DiagnosticCounters | None = None,
) -> gmpy2.mpz | None:
    """Return the previous public endpoint before one value."""
    hi = mpz_to_int(value)
    while hi > 2:
        # The backward PGSPG chunk finds the prior endpoint anchor.
        lo = max(2, hi - RULE_X_CANDIDATE_BOUND)
        counts = divisor_counts_window(lo, hi, segment_cache, diagnostics)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return gmpy2.mpz(lo + offset)
        hi = lo
    return None


def previous_endpoint_at(
    value: gmpy2.mpz,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> gmpy2.mpz | None:
    """Return one case-local cached previous public endpoint."""
    diagnostics["previous_endpoint_lookups"] += 1
    key = mpz_to_int(value)
    if key not in previous_endpoint_cache:
        diagnostics["previous_endpoint_calls"] += 1
        previous_endpoint_cache[key] = previous_endpoint(value, segment_cache, diagnostics)
    return previous_endpoint_cache[key]


def reset_deadline_fields(
    anchor: gmpy2.mpz,
    certificate: dict[str, object],
) -> tuple[gmpy2.mpz | None, int | None, str | None]:
    """Return reset-deadline value, margin, and signature for one certificate."""
    tail_offsets = tuple(int(offset) for offset in certificate["tail_after_reset_offsets"])
    threat_offset = (
        None
        if certificate["lower_d_threat_offset"] is None
        else int(certificate["lower_d_threat_offset"])
    )
    deadline_options: list[tuple[int, str]] = []
    if tail_offsets:
        deadline_options.append((tail_offsets[0], "tail"))
    if threat_offset is not None:
        deadline_options.append((threat_offset, "threat"))
    if not deadline_options:
        deadline_options.append((RULE_X_CANDIDATE_BOUND, "bound"))
    deadline_offset, deadline_kind = min(deadline_options)
    # Adding the local deadline offset gives the next reset boundary.
    deadline_value = anchor + deadline_offset
    # Subtracting the reset offset measures remaining reset freedom.
    deadline_margin = deadline_offset - int(certificate["gap_offset"])
    signature = (
        f"carrier_d={certificate['carrier_d']};"
        f"lock_carrier_d={certificate['lock_carrier_d']};"
        f"threat={threat_offset is not None};"
        f"deadline={deadline_kind}"
    )
    return deadline_value, deadline_margin, signature


def pgs_certificate(anchor: gmpy2.mpz) -> PGSCertificate | None:
    """Return a PGSPG reset certificate for one public previous endpoint."""
    raw = pgs_chamber_reset_state_certificate(
        mpz_to_int(anchor),
        RULE_X_CANDIDATE_BOUND,
    )
    if raw is None:
        return None
    deadline_value, deadline_margin, signature = reset_deadline_fields(anchor, raw)
    carrier_w = None if raw["carrier_w"] is None else gmpy2.mpz(int(raw["carrier_w"]))
    return PGSCertificate(
        anchor=anchor,
        reset_endpoint=gmpy2.mpz(int(raw["q"])),
        gap_offset=int(raw["gap_offset"]),
        candidate_bound=int(raw["candidate_bound"]),
        active_count=int(raw["active_count"]),
        resolved_count=int(raw["resolved_count"]),
        unresolved_count=int(raw["unresolved_count"]),
        closed_offsets_before_q=tuple(int(offset) for offset in raw["closed_offsets_before_q"]),
        carrier_w=carrier_w,
        carrier_d=None if raw["carrier_d"] is None else int(raw["carrier_d"]),
        lock_carrier_offset=None if raw["lock_carrier_offset"] is None else int(raw["lock_carrier_offset"]),
        lock_carrier_d=None if raw["lock_carrier_d"] is None else int(raw["lock_carrier_d"]),
        lower_d_threat_offset=None if raw["lower_d_threat_offset"] is None else int(raw["lower_d_threat_offset"]),
        tail_after_reset_offsets=tuple(int(offset) for offset in raw["tail_after_reset_offsets"]),
        reset_deadline_value=deadline_value,
        reset_deadline_margin=deadline_margin,
        reset_signature=signature,
    )


def certificate_at(
    anchor: gmpy2.mpz,
    certificate_cache: CertificateCache,
    diagnostics: DiagnosticCounters,
) -> PGSCertificate | None:
    """Return one case-local cached PGSPG certificate."""
    diagnostics["certificate_lookups"] += 1
    key = mpz_to_int(anchor)
    if key not in certificate_cache:
        diagnostics["certificate_builds"] += 1
        certificate_cache[key] = pgs_certificate(anchor)
    return certificate_cache[key]


def transported_deadline_width(n_value: gmpy2.mpz, certificate: PGSCertificate | None) -> int | None:
    """Return the reciprocal width of one reset-to-deadline interval."""
    if certificate is None or certificate.reset_deadline_value is None:
        return None
    # Transporting the reset endpoint gives the opposite-side reset image.
    reset_image = n_value // certificate.reset_endpoint
    # Transporting the deadline gives the opposite-side deadline image.
    deadline_image = n_value // certificate.reset_deadline_value
    return abs(mpz_to_int(reset_image - deadline_image))


def deadline_correction_closes(
    n_value: gmpy2.mpz,
    lower: PGSCertificate,
    upper: PGSCertificate,
    certificate_cache: CertificateCache,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> tuple[PGSCertificate | None, gmpy2.mpz | None, gmpy2.mpz | None, gmpy2.mpz | None, gmpy2.mpz | None, bool]:
    """Return whether the public upper deadline closes one corrected endpoint."""
    diagnostics["closure_attempts"] += 1
    if upper.reset_deadline_value is None:
        return None, None, None, None, None, False
    # The failed upper reset transports back to the lower side of the chamber.
    corrected_lower_image = reciprocal_floor(n_value, upper.reset_endpoint)
    # The previous public endpoint before that image is the corrected lower anchor.
    corrected_lower_endpoint = previous_endpoint_at(corrected_lower_image, previous_endpoint_cache, segment_cache, diagnostics)
    if corrected_lower_endpoint is None:
        return None, None, None, None, None, False
    corrected_lower = certificate_at(corrected_lower_endpoint, certificate_cache, diagnostics)
    if corrected_lower is None:
        return None, corrected_lower_endpoint, None, None, None, False
    corrected_upper_endpoint = upper.reset_deadline_value
    # The correction must move outward from the original reset pair, not relabel it.
    outward_correction = (
        corrected_lower_endpoint < lower.anchor
        and corrected_upper_endpoint > upper.reset_endpoint
    )
    transported_corrected_upper = reciprocal_floor(n_value, corrected_lower_endpoint)
    transported_corrected_lower = reciprocal_floor(n_value, corrected_upper_endpoint)
    closed = (
        outward_correction
        and transported_corrected_upper == corrected_upper_endpoint
        and transported_corrected_lower == corrected_lower_endpoint
        and corrected_lower.reset_signature == upper.reset_signature
    )
    return (
        corrected_lower,
        corrected_lower_endpoint,
        corrected_upper_endpoint,
        transported_corrected_upper,
        transported_corrected_lower,
        closed,
    )


def endpoint_chain_transport_coordinate(lower: PGSCertificate, center: gmpy2.mpz) -> gmpy2.mpz:
    """Return the lower coordinate transported during endpoint-chain traversal."""
    return lower.reset_endpoint if lower.reset_endpoint <= center else lower.anchor


def endpoint_chain_step_closure(
    n_value: gmpy2.mpz,
    center: gmpy2.mpz,
    upper_balance: gmpy2.mpz,
    anchor: gmpy2.mpz,
    steps: int,
    lower: PGSCertificate,
    certificate_cache: CertificateCache,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> CertificatePair | None:
    """Return one resolved endpoint-chain pair from a single lower anchor."""
    transport_coordinate = endpoint_chain_transport_coordinate(lower, center)
    transported_upper = reciprocal_floor(n_value, transport_coordinate)
    if transported_upper < center or transported_upper > upper_balance:
        return None
    upper_anchor = previous_endpoint_at(
        transported_upper,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    upper = None if upper_anchor is None else certificate_at(upper_anchor, certificate_cache, diagnostics)
    if upper is None:
        return None
    transported_lower = reciprocal_floor(n_value, upper.reset_endpoint)
    (
        corrected_lower,
        corrected_lower_endpoint,
        corrected_upper_endpoint,
        transported_corrected_upper,
        transported_corrected_lower,
        deadline_closed,
    ) = deadline_correction_closes(
        n_value,
        lower,
        upper,
        certificate_cache,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    if not deadline_closed:
        return None
    return CertificatePair(
        lower,
        upper,
        corrected_lower,
        corrected_lower_endpoint,
        corrected_upper_endpoint,
        transported_upper,
        transported_lower,
        transported_corrected_upper,
        transported_corrected_lower,
        transported_deadline_width(n_value, lower),
        transported_deadline_width(n_value, upper),
        "resolved_by_oriented_endpoint_chain_closure",
        endpoint_chain_steps=steps,
        endpoint_chain_source_anchor=anchor,
        endpoint_chain_transport_coordinate=transport_coordinate,
    )


def endpoint_chain_closure(
    n_value: gmpy2.mpz,
    center: gmpy2.mpz,
    lower_balance: gmpy2.mpz,
    upper_balance: gmpy2.mpz,
    start_anchor: gmpy2.mpz,
    certificate_cache: CertificateCache,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> CertificatePair | None:
    """Return the first oriented endpoint-chain deadline closure."""
    anchor: gmpy2.mpz | None = start_anchor
    steps = 0
    while anchor is not None and anchor >= lower_balance:
        lower = certificate_at(anchor, certificate_cache, diagnostics)
        if lower is not None:
            pair = endpoint_chain_step_closure(
                n_value,
                center,
                upper_balance,
                anchor,
                steps,
                lower,
                certificate_cache,
                previous_endpoint_cache,
                segment_cache,
                diagnostics,
            )
            if pair is not None:
                return pair
        anchor = previous_endpoint_at(anchor, previous_endpoint_cache, segment_cache, diagnostics)
        steps += 1
    return None


def make_diagnostics() -> DiagnosticCounters:
    """Return empty counters for one public case."""
    return {
        "previous_endpoint_lookups": 0,
        "previous_endpoint_calls": 0,
        "certificate_lookups": 0,
        "certificate_builds": 0,
        "divisor_segment_lookups": 0,
        "divisor_segment_calls": 0,
        "endpoint_chain_steps": 0,
        "closure_attempts": 0,
    }


def certificate_pair(case: LadderCase, diagnostics: DiagnosticCounters | None = None) -> CertificatePair:
    """Return the reciprocal certificate pair from square-root orientation."""
    if diagnostics is None:
        diagnostics = make_diagnostics()
    # The integer square root orients the lower and upper certificate sides.
    center = gmpy2.isqrt(case.n)
    lower_balance, upper_balance = balance_bounds(center)
    certificate_cache: CertificateCache = {}
    previous_endpoint_cache: PreviousEndpointCache = {}
    segment_cache: SegmentCache = {}
    lower_anchor = previous_endpoint_at(center, previous_endpoint_cache, segment_cache, diagnostics)
    if lower_anchor is None or lower_anchor < lower_balance:
        return CertificatePair(None, None, None, None, None, None, None, None, None, None, "unresolved_by_missing_lower_certificate")

    lower = certificate_at(lower_anchor, certificate_cache, diagnostics)
    if lower is None:
        return CertificatePair(None, None, None, None, None, None, None, None, None, None, "unresolved_by_missing_lower_certificate")

    if lower.reset_endpoint > center:
        endpoint_chain_pair = endpoint_chain_closure(
            case.n,
            center,
            lower_balance,
            upper_balance,
            lower_anchor,
            certificate_cache,
            previous_endpoint_cache,
            segment_cache,
            diagnostics,
        )
        if endpoint_chain_pair is not None:
            diagnostics["endpoint_chain_steps"] = endpoint_chain_pair.endpoint_chain_steps or 0
            return endpoint_chain_pair
        return CertificatePair(
            lower,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            transported_deadline_width(case.n, lower),
            None,
            "unresolved_by_reset_endpoint_crosses_orientation",
        )

    transported_upper = reciprocal_floor(case.n, lower.reset_endpoint)
    if transported_upper < center or transported_upper > upper_balance:
        return CertificatePair(
            lower,
            None,
            None,
            None,
            None,
            transported_upper,
            None,
            None,
            None,
            transported_deadline_width(case.n, lower),
            None,
            "unresolved_by_certificate_pair_not_closed",
        )
    upper_anchor = previous_endpoint_at(transported_upper, previous_endpoint_cache, segment_cache, diagnostics)
    if upper_anchor is None:
        return CertificatePair(
            lower,
            None,
            None,
            None,
            None,
            transported_upper,
            None,
            None,
            None,
            transported_deadline_width(case.n, lower),
            None,
            "unresolved_by_missing_upper_certificate",
        )
    upper = certificate_at(upper_anchor, certificate_cache, diagnostics)
    if upper is None:
        return CertificatePair(
            lower,
            None,
            None,
            None,
            None,
            transported_upper,
            None,
            None,
            None,
            transported_deadline_width(case.n, lower),
            None,
            "unresolved_by_missing_upper_certificate",
        )

    transported_lower = reciprocal_floor(case.n, upper.reset_endpoint)
    lower_width = transported_deadline_width(case.n, lower)
    upper_width = transported_deadline_width(case.n, upper)
    closed = (
        transported_upper == upper.reset_endpoint
        and transported_lower == lower.reset_endpoint
        and lower.reset_signature == upper.reset_signature
    )
    (
        corrected_lower,
        corrected_lower_endpoint,
        corrected_upper_endpoint,
        transported_corrected_upper,
        transported_corrected_lower,
        deadline_closed,
    ) = deadline_correction_closes(
        case.n,
        lower,
        upper,
        certificate_cache,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    status = "unresolved_by_certificate_pair_not_closed"
    if closed:
        status = "resolved_by_mutual_certificate_closure"
    elif deadline_closed:
        status = "resolved_by_reciprocal_deadline_signature_correction"
    else:
        endpoint_chain_pair = endpoint_chain_closure(
            case.n,
            center,
            lower_balance,
            upper_balance,
            lower_anchor,
            certificate_cache,
            previous_endpoint_cache,
            segment_cache,
            diagnostics,
        )
        if endpoint_chain_pair is not None:
            diagnostics["endpoint_chain_steps"] = endpoint_chain_pair.endpoint_chain_steps or 0
            return endpoint_chain_pair
    return CertificatePair(
        lower,
        upper,
        corrected_lower,
        corrected_lower_endpoint,
        corrected_upper_endpoint,
        transported_upper,
        transported_lower,
        transported_corrected_upper,
        transported_corrected_lower,
        lower_width,
        upper_width,
        status,
    )


def diagnostic_row(case: LadderCase, pair: CertificatePair, diagnostics: DiagnosticCounters) -> dict[str, object]:
    """Return one public performance diagnostic sidecar row."""
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "public_closure_status": pair.closure_status,
        "previous_endpoint_lookups": diagnostics["previous_endpoint_lookups"],
        "previous_endpoint_calls": diagnostics["previous_endpoint_calls"],
        "certificate_lookups": diagnostics["certificate_lookups"],
        "certificate_builds": diagnostics["certificate_builds"],
        "divisor_segment_lookups": diagnostics["divisor_segment_lookups"],
        "divisor_segment_calls": diagnostics["divisor_segment_calls"],
        "endpoint_chain_steps": diagnostics["endpoint_chain_steps"],
        "closure_attempts": diagnostics["closure_attempts"],
    }


def baseline_cost_row(
    case: LadderCase,
    pair: CertificatePair,
    diagnostics: DiagnosticCounters,
    elapsed_ns: int,
) -> dict[str, object]:
    """Return one non-persistent baseline-cost measurement row."""
    cache_lookups = (
        diagnostics["previous_endpoint_lookups"]
        + diagnostics["certificate_lookups"]
        + diagnostics["divisor_segment_lookups"]
    )
    cache_misses = (
        diagnostics["previous_endpoint_calls"]
        + diagnostics["certificate_builds"]
        + diagnostics["divisor_segment_calls"]
    )
    cache_hits = cache_lookups - cache_misses
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "public_closure_status": pair.closure_status,
        "endpoint_chain_steps": diagnostics["endpoint_chain_steps"],
        "cache_lookups": cache_lookups,
        "cache_misses": cache_misses,
        "cache_hit_rate": 0.0 if cache_lookups == 0 else cache_hits / cache_lookups,
        "elapsed_ms": elapsed_ns / 1_000_000,
    }


def certificate_to_json(certificate: PGSCertificate | None, prefix: str) -> dict[str, object]:
    """Return JSON-safe certificate fields with one side prefix."""
    if certificate is None:
        return {
            f"{prefix}_anchor": None,
            f"{prefix}_reset_endpoint": None,
            f"{prefix}_reset_signature": None,
        }
    return {
        f"{prefix}_anchor": str(certificate.anchor),
        f"{prefix}_reset_endpoint": str(certificate.reset_endpoint),
        f"{prefix}_gap_offset": certificate.gap_offset,
        f"{prefix}_candidate_bound": certificate.candidate_bound,
        f"{prefix}_active_count": certificate.active_count,
        f"{prefix}_resolved_count": certificate.resolved_count,
        f"{prefix}_unresolved_count": certificate.unresolved_count,
        f"{prefix}_closed_offsets_before_q": list(certificate.closed_offsets_before_q),
        f"{prefix}_carrier_w": None if certificate.carrier_w is None else str(certificate.carrier_w),
        f"{prefix}_carrier_d": certificate.carrier_d,
        f"{prefix}_lock_carrier_offset": certificate.lock_carrier_offset,
        f"{prefix}_lock_carrier_d": certificate.lock_carrier_d,
        f"{prefix}_d_threat_offset": certificate.lower_d_threat_offset,
        f"{prefix}_tail_after_reset_offsets": list(certificate.tail_after_reset_offsets),
        f"{prefix}_reset_deadline_value": None if certificate.reset_deadline_value is None else str(certificate.reset_deadline_value),
        f"{prefix}_reset_deadline_margin": certificate.reset_deadline_margin,
        f"{prefix}_reset_signature": certificate.reset_signature,
    }


def pair_to_json(case: LadderCase, pair: CertificatePair) -> dict[str, object]:
    """Return one reciprocal certificate pair as JSON-safe public fields."""
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "public_closure_status": pair.closure_status,
        "transported_upper_endpoint": None if pair.transported_upper_endpoint is None else str(pair.transported_upper_endpoint),
        "transported_lower_endpoint": None if pair.transported_lower_endpoint is None else str(pair.transported_lower_endpoint),
        "corrected_lower_endpoint": None if pair.corrected_lower_endpoint is None else str(pair.corrected_lower_endpoint),
        "corrected_upper_endpoint": None if pair.corrected_upper_endpoint is None else str(pair.corrected_upper_endpoint),
        "transported_corrected_upper_endpoint": None if pair.transported_corrected_upper_endpoint is None else str(pair.transported_corrected_upper_endpoint),
        "transported_corrected_lower_endpoint": None if pair.transported_corrected_lower_endpoint is None else str(pair.transported_corrected_lower_endpoint),
        "lower_transported_deadline_width": pair.lower_transported_deadline_width,
        "upper_transported_deadline_width": pair.upper_transported_deadline_width,
        "endpoint_chain_steps": pair.endpoint_chain_steps,
        "endpoint_chain_source_anchor": None if pair.endpoint_chain_source_anchor is None else str(pair.endpoint_chain_source_anchor),
        "endpoint_chain_transport_coordinate": None if pair.endpoint_chain_transport_coordinate is None else str(pair.endpoint_chain_transport_coordinate),
        "rule_id": RULE_ID,
    }
    payload.update(certificate_to_json(pair.lower, "lower"))
    payload.update(certificate_to_json(pair.upper, "upper"))
    payload.update(certificate_to_json(pair.corrected_lower, "corrected_lower"))
    return payload


def public_endpoint_class_row(
    case: LadderCase,
    lower: gmpy2.mpz,
    upper: gmpy2.mpz,
    public_closure_status: str,
) -> dict[str, object]:
    """Return one public endpoint-class row without factor-shaped fields."""
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "status": "public_endpoint_class_found",
        "public_structure_found": True,
        "endpoint_class_lower": str(lower),
        "endpoint_class_upper": str(upper),
        "public_closure_status": public_closure_status,
        "rule_id": RULE_ID,
    }


def result_row(case: LadderCase, pair: CertificatePair) -> dict[str, object]:
    """Return public endpoint-class status from certificate closure only."""
    if pair.closure_status == "resolved_by_mutual_certificate_closure":
        assert pair.lower is not None
        assert pair.upper is not None
        return public_endpoint_class_row(
            case,
            pair.lower.reset_endpoint,
            pair.upper.reset_endpoint,
            pair.closure_status,
        )
    if pair.closure_status == "resolved_by_reciprocal_deadline_signature_correction":
        assert pair.corrected_lower_endpoint is not None
        assert pair.corrected_upper_endpoint is not None
        return public_endpoint_class_row(
            case,
            pair.corrected_lower_endpoint,
            pair.corrected_upper_endpoint,
            pair.closure_status,
        )
    if pair.closure_status == "resolved_by_oriented_endpoint_chain_closure":
        assert pair.corrected_lower_endpoint is not None
        assert pair.corrected_upper_endpoint is not None
        return public_endpoint_class_row(
            case,
            pair.corrected_lower_endpoint,
            pair.corrected_upper_endpoint,
            pair.closure_status,
        )
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "status": "unresolved",
        "public_structure_found": False,
        "unresolved_reason": pair.closure_status,
        "rule_id": RULE_ID,
    }


def summary_row(case: LadderCase, pair: CertificatePair) -> dict[str, object]:
    """Return one public certificate-pair summary row."""
    # The integer square root is the public orientation coordinate.
    center = gmpy2.isqrt(case.n)
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "center": str(center),
        "balance_band": str(BALANCE_BAND),
        "public_closure_status": pair.closure_status,
        "lower_certificate_present": pair.lower is not None,
        "upper_certificate_present": pair.upper is not None,
        "corrected_lower_certificate_present": pair.corrected_lower is not None,
        "endpoint_chain_steps": pair.endpoint_chain_steps,
        "rule_id": RULE_ID,
    }


def run_cases(
    cases: list[LadderCase],
    baseline_cost_rows: list[dict[str, object]] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Run every public case through the certificate-pair surface."""
    results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    pairs: list[dict[str, object]] = []
    diagnostics_rows: list[dict[str, object]] = []
    for case in cases:
        diagnostics = make_diagnostics()
        start_ns = time.perf_counter_ns()
        pair = certificate_pair(case, diagnostics)
        elapsed_ns = time.perf_counter_ns() - start_ns
        results.append(result_row(case, pair))
        summaries.append(summary_row(case, pair))
        pairs.append(pair_to_json(case, pair))
        diagnostics_rows.append(diagnostic_row(case, pair, diagnostics))
        if baseline_cost_rows is not None:
            baseline_cost_rows.append(baseline_cost_row(case, pair, diagnostics, elapsed_ns))
    return results, summaries, pairs, diagnostics_rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the RSA v2 PGSPG certificate experiment.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parent / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "output",
        help="Directory for inference_rows.jsonl, survivor_rows.jsonl, diagnostic_rows.jsonl, and summary.json.",
    )
    parser.add_argument(
        "--measure-baseline-cost",
        action="store_true",
        help="Print non-persistent endpoint-step, cache, and elapsed-time measurements.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the official experiment."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cases = load_cases(args.cases)
    baseline_cost_rows: list[dict[str, object]] | None = [] if args.measure_baseline_cost else None
    results, summaries, pairs, diagnostics_rows = run_cases(cases, baseline_cost_rows)
    write_jsonl(args.output_dir / "inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", pairs)
    write_jsonl(args.output_dir / "diagnostic_rows.jsonl", diagnostics_rows)
    write_json(args.output_dir / "summary.json", {"cases": summaries})
    output: dict[str, object] = {"cases": summaries}
    if baseline_cost_rows is not None:
        output["baseline_cost"] = baseline_cost_rows
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
