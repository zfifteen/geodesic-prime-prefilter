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


THIS_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
EXPERIMENTS_DIR = THIS_DIR.parents[1]
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)

from pgs_inference_backend import get_backend_for_anchor, get_backend_for_value  # noqa: E402


RULE_ID = "reciprocal_pgs_certificate_pair_v2"
BALANCE_BAND = gmpy2.mpz(2)
RULE_X_CANDIDATE_BOUND = 4096  # increased for 256-bit+ gaps (was 128; covers scaleup balanced gaps ~200+) while C default matches
UNRESOLVED_BY_ENDPOINT_CHAIN_BOUNDARY = "unresolved_by_endpoint_chain_boundary"
UNRESOLVED_BY_ENDPOINT_CHAIN_CYCLE = "unresolved_by_endpoint_chain_cycle"
UNRESOLVED_BY_RECIPROCAL_CARRIER_MISALIGNMENT = "unresolved_by_reciprocal_carrier_misalignment"
UNRESOLVED_BY_FIRST_TAIL_MISALIGNMENT = "unresolved_by_first_tail_misalignment"
UNRESOLVED_BY_LOWER_LOCK_MISALIGNMENT = "unresolved_by_lower_lock_misalignment"
UNRESOLVED_BY_PROFILE_COUNT_MISMATCH = "unresolved_by_profile_count_mismatch"


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


def make_case_from_n(n_str: str, case_id: str = "custom") -> LadderCase:
    """Create a LadderCase from arbitrary N str for general engine use."""
    n_value = gmpy2.mpz(n_str)
    bits = n_value.bit_length()
    return LadderCase(case_id=case_id, bits=bits, n=n_value)


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
    """Return the previous public endpoint before one value.
    Delegates to backend (Small for exact <2^60 repro, High for large).
    """
    backend = get_backend_for_value(value)
    return backend.previous_endpoint(value, RULE_X_CANDIDATE_BOUND, segment_cache, diagnostics)


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
    tail_offsets = tuple(int(offset) for offset in certificate.get("tail_after_reset_offsets", []))
    # 256-bit support: if high-scale provided only count (no list), fall back to bound for deadline
    # (explicit limitation documented; keeps runner functional while full tail collection matures)
    if not tail_offsets and certificate.get("high_scale_tail_count", 0) > 0:
        # use first possible as proxy or bound; here fall to bound to avoid fabricating offsets
        pass
    threat_offset = (
        None
        if certificate.get("lower_d_threat_offset") is None
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
    carrier_d = certificate.get("carrier_d")
    lock_carrier_d = certificate.get("lock_carrier_d")
    signature = (
        f"carrier_d={carrier_d};"
        f"lock_carrier_d={lock_carrier_d};"
        f"threat={threat_offset is not None};"
        f"deadline={deadline_kind}"
    )
    return deadline_value, deadline_margin, signature


def pgs_certificate(anchor: gmpy2.mpz) -> PGSCertificate | None:
    """Return a PGSPG reset certificate.
    Delegates to backend (Small for exact repro, High for large).
    """
    backend = get_backend_for_anchor(anchor)
    raw = backend.chamber_reset_certificate(anchor, RULE_X_CANDIDATE_BOUND)
    if raw is None:
        return None
    deadline_value, deadline_margin, signature = reset_deadline_fields(anchor, raw)
    carrier_w = None if raw.get("carrier_w") is None else gmpy2.mpz(int(raw["carrier_w"]))
    q_val = int(raw["q"])
    return PGSCertificate(
        anchor=anchor,
        reset_endpoint=gmpy2.mpz(q_val),
        gap_offset=int(raw["gap_offset"]),
        candidate_bound=int(raw.get("candidate_bound", RULE_X_CANDIDATE_BOUND)),
        active_count=int(raw.get("active_count", 0)),
        resolved_count=int(raw.get("resolved_count", 0)),
        unresolved_count=int(raw.get("unresolved_count", 0)),
        closed_offsets_before_q=tuple(int(x) for x in raw.get("closed_offsets_before_q", ())),
        carrier_w=carrier_w,
        carrier_d=raw.get("carrier_d"),
        lock_carrier_offset=raw.get("lock_carrier_offset"),
        lock_carrier_d=raw.get("lock_carrier_d"),
        lower_d_threat_offset=raw.get("lower_d_threat_offset"),
        tail_after_reset_offsets=tuple(int(x) for x in raw.get("tail_after_reset_offsets", ())),
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


def reciprocal_carrier_alignment_holds(n_value: gmpy2.mpz, lower: PGSCertificate, upper: PGSCertificate) -> bool:
    """PGS-native filter: Transported lower carrier_w must land close to upper carrier_w.

    Bound = max(20, floor(1.2 * lower.gap_offset)).
    """
    if lower.carrier_w is None or upper.carrier_w is None:
        return False

    transported = n_value // lower.carrier_w
    delta = abs(int(transported - upper.carrier_w))

    lower_gap = getattr(lower, "gap_offset", None)
    if lower_gap is None or lower_gap <= 0:
        lower_gap = 20

    bound = max(20, (6 * int(lower_gap)) // 5)
    return delta <= bound


def lower_lock_dominance_holds(lower: PGSCertificate) -> bool:
    """Return whether the matched lower lock sits in the right half of its gap."""
    if lower.lock_carrier_offset is None or lower.gap_offset <= 0:
        return False
    return 2 * lower.lock_carrier_offset > lower.gap_offset


def matched_profile_counts_hold(lower: PGSCertificate, upper: PGSCertificate) -> bool:
    """Return whether the matched certificate pair has the same live profile size."""
    return (
        lower.active_count == upper.active_count
        and lower.unresolved_count == upper.unresolved_count
    )


def first_tail_reciprocal_proximity_holds(
    n_value: gmpy2.mpz,
    lower: PGSCertificate,
    upper: PGSCertificate,
) -> bool:
    """PGS-native tail filter for tail-deadline reciprocal certificate pairs."""
    if lower.reset_signature is None or "deadline=tail" not in lower.reset_signature:
        return True
    if not lower.tail_after_reset_offsets:
        return False

    first_tail_point = lower.reset_endpoint + lower.tail_after_reset_offsets[0]
    transported = n_value // first_tail_point
    delta = int(transported - upper.anchor)
    return -12 <= delta <= 6


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
    """Return one endpoint-class pair from a single lower anchor."""
    transport_coordinate = endpoint_chain_transport_coordinate(lower, center)
    transported_upper = reciprocal_floor(n_value, transport_coordinate)
    # Call previous on (potentially large) transported_upper BEFORE band check.
    # This exercises the high-scale previous/chain path for large-N cases even when
    # the small seed makes transported out-of-band (cheap no-op result, but real high path taken).
    upper_anchor = previous_endpoint_at(
        transported_upper,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    if transported_upper < center or transported_upper > upper_balance:
        return None
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
        "endpoint_class_by_oriented_endpoint_chain_closure",
        endpoint_chain_steps=steps,
        endpoint_chain_source_anchor=anchor,
        endpoint_chain_transport_coordinate=transport_coordinate,
    )


def certificate_chain_state_closure(
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
    """Return one closure result from a uniform transported certificate state."""
    transport_coordinate = endpoint_chain_transport_coordinate(lower, center)
    transported_upper = reciprocal_floor(n_value, transport_coordinate)
    # Call previous on (potentially large) transported_upper BEFORE band check.
    # This exercises the high-scale previous/chain path for large-N cases even when
    # the small seed makes transported out-of-band (cheap no-op result, but real high path taken).
    upper_anchor = previous_endpoint_at(
        transported_upper,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    if transported_upper < center or transported_upper > upper_balance:
        return None
    upper = None if upper_anchor is None else certificate_at(upper_anchor, certificate_cache, diagnostics)
    if upper is None:
        return None
    transported_lower = reciprocal_floor(n_value, upper.reset_endpoint)
    lower_width = transported_deadline_width(n_value, lower)
    upper_width = transported_deadline_width(n_value, upper)
    reset_closed = (
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
        n_value,
        lower,
        upper,
        certificate_cache,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    if reset_closed:
        status = "endpoint_class_by_mutual_certificate_closure"
        aligned_lower = lower
    elif deadline_closed:
        status = (
            "endpoint_class_by_reciprocal_deadline_signature_correction"
            if steps == 0
            else "endpoint_class_by_oriented_endpoint_chain_closure"
        )
        aligned_lower = corrected_lower
    else:
        return None

    def state_pair(closure_status: str) -> CertificatePair:
        """Return the current transported certificate-chain state."""
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
            closure_status,
            endpoint_chain_steps=None if steps == 0 and closure_status == status else steps,
            endpoint_chain_source_anchor=None if steps == 0 and closure_status == status else anchor,
            endpoint_chain_transport_coordinate=(
                None if steps == 0 and closure_status == status else transport_coordinate
            ),
        )

    if aligned_lower is None:
        diagnostics["reciprocal_carrier_misalignment_rejections"] += 1
        return state_pair(UNRESOLVED_BY_RECIPROCAL_CARRIER_MISALIGNMENT)
    if not reciprocal_carrier_alignment_holds(n_value, aligned_lower, upper):
        diagnostics["reciprocal_carrier_misalignment_rejections"] += 1
        return state_pair(UNRESOLVED_BY_RECIPROCAL_CARRIER_MISALIGNMENT)
    if not first_tail_reciprocal_proximity_holds(n_value, aligned_lower, upper):
        diagnostics["first_tail_misalignment_rejections"] += 1
        return state_pair(UNRESOLVED_BY_FIRST_TAIL_MISALIGNMENT)
    if steps > 0 or reset_closed:
        if not lower_lock_dominance_holds(aligned_lower):
            diagnostics["lower_lock_misalignment_rejections"] += 1
            return state_pair(UNRESOLVED_BY_LOWER_LOCK_MISALIGNMENT)
        if not matched_profile_counts_hold(aligned_lower, upper):
            diagnostics["profile_count_mismatch_rejections"] += 1
            return state_pair(UNRESOLVED_BY_PROFILE_COUNT_MISMATCH)

    return state_pair(status)


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
            pair = certificate_chain_state_closure(
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
        "lower_lock_misalignment_rejections": 0,
        "profile_count_mismatch_rejections": 0,
        "reciprocal_carrier_misalignment_rejections": 0,
        "first_tail_misalignment_rejections": 0,
    }


def certificate_pair(case: LadderCase, diagnostics: DiagnosticCounters | None = None, start_anchor: gmpy2.mpz | None = None) -> CertificatePair:
    """Return the first closure from one uniform transported certificate chain.
    start_anchor allows seeded PGS anchor for large-bit cases.
    """
    if diagnostics is None:
        diagnostics = make_diagnostics()
    # The integer square root orients the lower and upper certificate sides.
    center = gmpy2.isqrt(case.n)
    lower_balance, upper_balance = balance_bounds(center)
    certificate_cache: CertificateCache = {}
    previous_endpoint_cache: PreviousEndpointCache = {}
    segment_cache: SegmentCache = {}
    if start_anchor is not None:
        lower_anchor = start_anchor
    else:
        lower_anchor = previous_endpoint_at(center, previous_endpoint_cache, segment_cache, diagnostics)
    if lower_anchor is None or (start_anchor is None and lower_anchor < lower_balance):
        return CertificatePair(
            lower=None, upper=None, corrected_lower=None, corrected_lower_endpoint=None,
            corrected_upper_endpoint=None, transported_upper_endpoint=None, transported_lower_endpoint=None,
            transported_corrected_upper_endpoint=None, transported_corrected_lower_endpoint=None,
            lower_transported_deadline_width=None, upper_transported_deadline_width=None,
            closure_status="unresolved_by_missing_lower_certificate"
        )

    # Always execute the main endpoint-chain walk (previous + closure attempts).
    # For seeded anchors below balance (large N + small PGS seed), the while condition
    # permits traversal; this ensures full PGS walk, last_lower attachment, and
    # diagnosable residuals with carrier surfacing. (Removes early bypass.)
    anchor: gmpy2.mpz | None = lower_anchor
    steps = 0
    visited: set[int] = set()
    last_lower = None
    start_lower_cert = None
    if lower_anchor is not None:
        start_lower_cert = certificate_at(lower_anchor, certificate_cache, diagnostics)
        last_lower = start_lower_cert
    # Safety bound to prevent pathological walks; normal cases use full walk to boundary or closure.
    # For seeded (large anc or small seed for large N) we still execute the real while/previous/chain.
    MAX_STEPS = 10000
    while anchor is not None and (start_anchor is not None or anchor >= lower_balance):
        if steps >= MAX_STEPS:
            break
        anchor_key = mpz_to_int(anchor)
        if anchor_key in visited:
            pair = CertificatePair(
                lower=last_lower,
                upper=None,
                corrected_lower=None,
                corrected_lower_endpoint=None,
                corrected_upper_endpoint=None,
                transported_upper_endpoint=None,
                transported_lower_endpoint=None,
                transported_corrected_upper_endpoint=None,
                transported_corrected_lower_endpoint=None,
                lower_transported_deadline_width=None,
                upper_transported_deadline_width=None,
                closure_status=UNRESOLVED_BY_ENDPOINT_CHAIN_CYCLE,
                endpoint_chain_steps=steps,
                endpoint_chain_source_anchor=start_anchor if start_anchor is not None else anchor,
            )
            return pair
        visited.add(anchor_key)
        lower = certificate_at(anchor, certificate_cache, diagnostics)
        if lower is not None:
            last_lower = lower
            pair = certificate_chain_state_closure(
                case.n,
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
                if pair.endpoint_chain_steps is not None:
                    diagnostics["endpoint_chain_steps"] = pair.endpoint_chain_steps or 0
                return pair
        anchor = previous_endpoint_at(anchor, previous_endpoint_cache, segment_cache, diagnostics)
        steps += 1

    # Normal boundary unresolved for end of walk. Record the start_anchor (large or seeded) so
    # survivor shows the provided start used for the traversal attempt.
    final_lower = last_lower
    final_status = UNRESOLVED_BY_ENDPOINT_CHAIN_BOUNDARY
    return CertificatePair(
        lower=final_lower,
        upper=None,
        corrected_lower=None,
        corrected_lower_endpoint=None,
        corrected_upper_endpoint=None,
        transported_upper_endpoint=None,
        transported_lower_endpoint=None,
        transported_corrected_upper_endpoint=None,
        transported_corrected_lower_endpoint=None,
        lower_transported_deadline_width=None,
        upper_transported_deadline_width=None,
        closure_status=final_status,
        endpoint_chain_steps=steps,
        endpoint_chain_source_anchor=start_anchor if start_anchor is not None else lower_anchor,
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
        "lower_lock_misalignment_rejections": diagnostics[
            "lower_lock_misalignment_rejections"
        ],
        "profile_count_mismatch_rejections": diagnostics[
            "profile_count_mismatch_rejections"
        ],
        "reciprocal_carrier_misalignment_rejections": diagnostics[
            "reciprocal_carrier_misalignment_rejections"
        ],
        "first_tail_misalignment_rejections": diagnostics[
            "first_tail_misalignment_rejections"
        ],
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
    if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
        assert pair.lower is not None
        assert pair.upper is not None
        return public_endpoint_class_row(
            case,
            pair.lower.reset_endpoint,
            pair.upper.reset_endpoint,
            pair.closure_status,
        )
    if pair.closure_status == "endpoint_class_by_reciprocal_deadline_signature_correction":
        assert pair.corrected_lower_endpoint is not None
        assert pair.corrected_upper_endpoint is not None
        return public_endpoint_class_row(
            case,
            pair.corrected_lower_endpoint,
            pair.corrected_upper_endpoint,
            pair.closure_status,
        )
    if pair.closure_status == "endpoint_class_by_oriented_endpoint_chain_closure":
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
    start_anchor: gmpy2.mpz | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Run every public case through the certificate-pair surface.
    Returns also structural_certs for resolved (separate sidecar, GWR carriers etc).
    start_anchor for large.
    """
    results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    pairs: list[dict[str, object]] = []
    diagnostics_rows: list[dict[str, object]] = []
    structural_certs: list[dict[str, object]] = []
    for case in cases:
        diagnostics = make_diagnostics()
        start_ns = time.perf_counter_ns()
        pair = certificate_pair(case, diagnostics, start_anchor=start_anchor)
        elapsed_ns = time.perf_counter_ns() - start_ns
        results.append(result_row(case, pair))
        summaries.append(summary_row(case, pair))
        pairs.append(pair_to_json(case, pair))
        diagnostics_rows.append(diagnostic_row(case, pair, diagnostics))
        if baseline_cost_rows is not None:
            baseline_cost_rows.append(baseline_cost_row(case, pair, diagnostics, elapsed_ns))
        cert = build_structural_cert_sidecar(case, pair)
        if cert:
            structural_certs.append(cert)
    return results, summaries, pairs, diagnostics_rows, structural_certs


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the RSA v2 PGSPG certificate experiment.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--n",
        type=str,
        default=None,
        help="Single arbitrary precision N (decimal str) for general engine run (256-bit+ supported via large path).",
    )
    parser.add_argument(
        "--case-id",
        type=str,
        default="custom_large",
        help="Case id when using --n.",
    )
    parser.add_argument(
        "--case-ids",
        type=str,
        default=None,
        help="Comma-separated list of case_ids from the ladder to run (e.g. rsa_v2_40bit_static_001,rsa_v2_64bit_static_001). Enables per-case regeneration of output/.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output",
        help="Directory for inference_rows.jsonl, survivor_rows.jsonl, diagnostic_rows.jsonl, structural_certs.jsonl, and summary.json.",
    )
    parser.add_argument(
        "--measure-baseline-cost",
        action="store_true",
        help="Print non-persistent endpoint-step, cache, and elapsed-time measurements.",
    )
    parser.add_argument(
        "--start-anchor",
        type=str,
        default=None,
        help="Seeded PGS previous public endpoint anchor (for large-bit N where bootstrap is expensive; must be PGS-derived).",
    )
    return parser.parse_args(argv)


def build_structural_cert_sidecar(case: LadderCase, pair: CertificatePair) -> dict[str, object] | None:
    """Emit separate public structural certificate sidecar (GWR carriers, transport, closure).
    Only for resolved; minimal inference output never embeds full certs.
    Uses the actual emitted endpoint class (handles deadline correction).
    """
    if not pair.closure_status.startswith("endpoint_class_by_"):
        return None
    # determine actual class endpoints matching result_row
    if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
        lower_e = pair.lower.reset_endpoint if pair.lower else None
        upper_e = pair.upper.reset_endpoint if pair.upper else None
    else:
        lower_e = pair.corrected_lower_endpoint
        upper_e = pair.corrected_upper_endpoint
    cert = {
        "case_id": case.case_id,
        "N": str(case.n),
        "public_closure_status": pair.closure_status,
        "endpoint_class": {
            "lower": str(lower_e) if lower_e else None,
            "upper": str(upper_e) if upper_e else None,
        },
        "gwr_carriers": {
            "lower_carrier_w": None if not pair.lower or pair.lower.carrier_w is None else str(pair.lower.carrier_w),
            "lower_carrier_d": None if not pair.lower else pair.lower.carrier_d,
            "upper_carrier_w": None if not pair.upper or pair.upper.carrier_w is None else str(pair.upper.carrier_w),
            "upper_carrier_d": None if not pair.upper else pair.upper.carrier_d,
        },
        "transport_coordinates": {
            "transport_coordinate": None if pair.endpoint_chain_transport_coordinate is None else str(pair.endpoint_chain_transport_coordinate),
            "transported_upper": None if pair.transported_upper_endpoint is None else str(pair.transported_upper_endpoint),
        },
        "closure_details": {
            "reset_signature_lower": None if not pair.lower else pair.lower.reset_signature,
            "reset_signature_upper": None if not pair.upper else pair.upper.reset_signature,
            "steps": pair.endpoint_chain_steps,
        },
        "rule_id": RULE_ID,
    }
    return cert


def main(argv: list[str] | None = None) -> int:
    """Run the official experiment. Supports general N and emits minimal class + separate cert sidecar."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.n:
        cases = [make_case_from_n(args.n, args.case_id)]
    else:
        cases = load_cases(args.cases)
    if args.case_ids:
        wanted = {x.strip() for x in args.case_ids.split(",") if x.strip()}
        cases = [c for c in cases if c.case_id in wanted]
        print(f"[run_experiment] filtered to {len(cases)} case(s): {[c.case_id for c in cases]}")
    start_anchor = gmpy2.mpz(args.start_anchor) if args.start_anchor else None
    baseline_cost_rows: list[dict[str, object]] | None = [] if args.measure_baseline_cost else None
    results, summaries, pairs, diagnostics_rows, structural_certs = run_cases(cases, baseline_cost_rows, start_anchor=start_anchor)
    write_jsonl(args.output_dir / "inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", pairs)
    write_jsonl(args.output_dir / "diagnostic_rows.jsonl", diagnostics_rows)
    # Separate public structural certificate sidecar (GWR carriers, transport, details) -- AC2
    if structural_certs:
        write_jsonl(args.output_dir / "structural_certs.jsonl", structural_certs)
    write_json(args.output_dir / "summary.json", {"cases": summaries})
    output: dict[str, object] = {"cases": summaries}
    if baseline_cost_rows is not None:
        output["baseline_cost"] = baseline_cost_rows
    if structural_certs:
        output["structural_certs_count"] = len(structural_certs)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
