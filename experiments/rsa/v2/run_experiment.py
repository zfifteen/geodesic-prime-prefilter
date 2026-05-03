#!/usr/bin/env python3
"""Run the RSA v2 PGS-first reciprocal anchor-surface experiment."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import gmpy2


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)


RULE_ID = "pgs_first_reciprocal_anchor_surface_v1"
SMALL_REGIME_MAX_BITS = 50
BALANCE_BAND = gmpy2.mpz(2)
PGS_ENDPOINT_RADIUS = 16
RULE_X_CANDIDATE_BOUND = 128
DEFAULT_CHUNK_WIDTH = 1_000_000
DEFAULT_MAX_LOWER_ENDPOINTS = 100_000
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})


@dataclass(frozen=True)
class LadderCase:
    """One public modulus rung."""

    case_id: str
    bits: int
    n: gmpy2.mpz


@dataclass(frozen=True)
class LocalLock:
    """One local PGSPG reset state around a public endpoint."""

    value: gmpy2.mpz
    previous_endpoint: gmpy2.mpz | None
    reset_endpoint: gmpy2.mpz | None
    reset_gap_offset: int | None
    carrier_w: gmpy2.mpz | None
    carrier_d: int | None
    lock_carrier_offset: int | None
    lock_carrier_d: int | None
    lower_d_threat_offset: int | None
    tail_after_reset_offsets: tuple[int, ...]
    reset_deadline_kind: str | None
    reset_deadline_offset: int | None
    reset_deadline_value: gmpy2.mpz | None
    reset_deadline_margin: int | None
    reset_signature: str | None
    locked: bool


@dataclass(frozen=True)
class AnchorRow:
    """One two-sided PGS endpoint/reset survivor row."""

    rank: int
    x: gmpy2.mpz
    y: gmpy2.mpz
    lower_lock: LocalLock
    upper_lock: LocalLock
    lower_transported_deadline_width: int | None
    upper_transported_deadline_width: int | None


def mpz_to_int(value: gmpy2.mpz) -> int:
    """Convert one GMP coordinate for the current exact small-regime backend."""
    return int(value)


def case_supported_by_interval_backend(case: LadderCase) -> bool:
    """Return whether the current exact interval backend supports one rung."""
    return SMALL_REGIME_MAX_BITS >= case.bits


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


def wheel_open(value: gmpy2.mpz) -> bool:
    """Return whether one integer is open under the fixed 30-wheel."""
    return int(value % 30) in WHEEL_OPEN_RESIDUES_MOD30


def balance_bounds(center: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Return the public balanced factor interval."""
    # Dividing the square-root center gives the lower balanced endpoint.
    lower = center // BALANCE_BAND
    # Multiplying the square-root center gives the upper balanced endpoint.
    upper = center * BALANCE_BAND
    return lower, upper


def reciprocal_floor(n_value: gmpy2.mpz, x_value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the public reciprocal coordinate for one lower endpoint."""
    # The floor reciprocal maps a lower endpoint to the opposite side of N.
    return n_value // x_value


def endpoint_values_descending(
    lower: gmpy2.mpz,
    upper: gmpy2.mpz,
    chunk_width: int,
    max_endpoints: int,
) -> tuple[list[gmpy2.mpz], bool]:
    """Return public endpoints while walking down from the square-root side."""
    endpoints: list[gmpy2.mpz] = []
    cursor = mpz_to_int(upper)
    floor = mpz_to_int(lower)
    while cursor >= floor and len(endpoints) < max_endpoints:
        # The chunk lower bound moves the endpoint walk left in PGS space.
        chunk_lo = max(floor, cursor - chunk_width + 1)
        # The chunk upper bound is exclusive for interval divisor-count measurement.
        chunk_hi = cursor + 1
        counts = divisor_counts_segment(chunk_lo, chunk_hi)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                endpoints.append(gmpy2.mpz(chunk_lo + offset))
                if len(endpoints) == max_endpoints:
                    break
        cursor = chunk_lo - 1
    exhausted = cursor >= floor
    return endpoints, exhausted


def exact_endpoint_values(values: list[gmpy2.mpz]) -> set[str]:
    """Return values that are exact endpoints using one measured interval."""
    if not values:
        return set()
    # The minimum reciprocal value fixes the left edge of the endpoint field.
    lo = min(mpz_to_int(value) for value in values)
    # The maximum reciprocal value fixes the right edge of the endpoint field.
    hi = max(mpz_to_int(value) for value in values) + 1
    counts = divisor_counts_segment(lo, hi)
    endpoints: set[str] = set()
    for value in values:
        if int(counts[mpz_to_int(value) - lo]) == 2:
            endpoints.add(str(value))
    return endpoints


def previous_endpoint(value: gmpy2.mpz) -> gmpy2.mpz | None:
    """Return the previous public endpoint before one value."""
    hi = mpz_to_int(value)
    while hi > 2:
        # The backward PGSPG chunk finds the prior endpoint anchor.
        lo = max(2, hi - RULE_X_CANDIDATE_BOUND)
        counts = divisor_counts_segment(lo, hi)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return gmpy2.mpz(lo + offset)
        hi = lo
    return None


@lru_cache(maxsize=200_000)
def local_lock_int(value: int) -> LocalLock:
    """Return the local PGSPG reset lock for one known endpoint value."""
    value_mpz = gmpy2.mpz(value)
    anchor = previous_endpoint(value_mpz)
    certificate = None
    if anchor is not None:
        certificate = pgs_chamber_reset_state_certificate(
            mpz_to_int(anchor),
            RULE_X_CANDIDATE_BOUND,
        )
    reset = None if certificate is None else gmpy2.mpz(int(certificate["q"]))
    locked = reset == value_mpz
    carrier_w = None
    if certificate is not None and certificate["carrier_w"] is not None:
        carrier_w = gmpy2.mpz(int(certificate["carrier_w"]))
    tail_offsets = (
        ()
        if certificate is None
        else tuple(int(offset) for offset in certificate["tail_after_reset_offsets"])
    )
    reset_gap = None if certificate is None else int(certificate["gap_offset"])
    threat_offset = (
        None
        if certificate is None or certificate["lower_d_threat_offset"] is None
        else int(certificate["lower_d_threat_offset"])
    )
    deadline_options: list[tuple[int, str]] = []
    if tail_offsets:
        deadline_options.append((tail_offsets[0], "tail"))
    if threat_offset is not None:
        deadline_options.append((threat_offset, "threat"))
    if not deadline_options and reset_gap is not None:
        deadline_options.append((RULE_X_CANDIDATE_BOUND, "bound"))
    deadline_offset = None
    deadline_kind = None
    if deadline_options:
        deadline_offset, deadline_kind = min(deadline_options)
    deadline_value = None
    if anchor is not None and deadline_offset is not None:
        # Adding the deadline offset gives the next local reset boundary.
        deadline_value = anchor + deadline_offset
    deadline_margin = None
    if reset_gap is not None and deadline_offset is not None:
        # Subtracting the reset offset measures remaining reset freedom.
        deadline_margin = deadline_offset - reset_gap
    signature = None
    if certificate is not None:
        signature = (
            f"carrier_d={certificate['carrier_d']};"
            f"lock_carrier_d={certificate['lock_carrier_d']};"
            f"threat={threat_offset is not None};"
            f"deadline={deadline_kind}"
        )
    return LocalLock(
        value=value_mpz,
        previous_endpoint=anchor,
        reset_endpoint=reset,
        reset_gap_offset=reset_gap,
        carrier_w=carrier_w,
        carrier_d=None if certificate is None or certificate["carrier_d"] is None else int(certificate["carrier_d"]),
        lock_carrier_offset=None if certificate is None or certificate["lock_carrier_offset"] is None else int(certificate["lock_carrier_offset"]),
        lock_carrier_d=None if certificate is None or certificate["lock_carrier_d"] is None else int(certificate["lock_carrier_d"]),
        lower_d_threat_offset=threat_offset,
        tail_after_reset_offsets=tail_offsets,
        reset_deadline_kind=deadline_kind,
        reset_deadline_offset=deadline_offset,
        reset_deadline_value=deadline_value,
        reset_deadline_margin=deadline_margin,
        reset_signature=signature,
        locked=bool(locked),
    )


def local_lock(value: gmpy2.mpz) -> LocalLock:
    """Return the cached local PGSPG reset lock for one known endpoint."""
    return local_lock_int(mpz_to_int(value))


def transported_deadline_width(n_value: gmpy2.mpz, lock: LocalLock) -> int | None:
    """Return the reciprocal width of one reset-to-deadline interval."""
    if lock.reset_endpoint is None or lock.reset_deadline_value is None:
        return None
    # Mapping the reset endpoint through N gives its opposite-side image.
    reset_image = n_value // lock.reset_endpoint
    # Mapping the reset deadline through N gives the transported deadline image.
    deadline_image = n_value // lock.reset_deadline_value
    return abs(mpz_to_int(reset_image - deadline_image))


def pgs_anchor_rows(
    case: LadderCase,
    max_lower_endpoints: int,
    chunk_width: int,
) -> tuple[list[AnchorRow], dict[str, object]]:
    """Return the PGS-first reciprocal anchor surface for one public case."""
    # The integer square root orients the lower and upper sides; it is not a gate.
    center = gmpy2.isqrt(case.n)
    lower_balance, upper_balance = balance_bounds(center)
    lower_endpoints, budget_exhausted = endpoint_values_descending(
        lower_balance,
        center,
        chunk_width,
        max_lower_endpoints,
    )
    reciprocal_balance = 0
    reciprocal_wheel = 0
    endpoint_pair_rows: list[tuple[gmpy2.mpz, gmpy2.mpz]] = []

    for x_value in lower_endpoints:
        # The reciprocal floor gives the public opposite-side coordinate.
        y_value = reciprocal_floor(case.n, x_value)
        if not center <= y_value <= upper_balance:
            continue
        reciprocal_balance += 1
        if not wheel_open(y_value):
            continue
        reciprocal_wheel += 1
        endpoint_pair_rows.append((x_value, y_value))

    reciprocal_endpoint_values = exact_endpoint_values(
        [y_value for _x_value, y_value in endpoint_pair_rows]
    )
    two_endpoint_rows = [
        (x_value, y_value)
        for x_value, y_value in endpoint_pair_rows
        if str(y_value) in reciprocal_endpoint_values
    ]

    rows: list[AnchorRow] = []
    upper_locked_rows = 0
    for x_value, y_value in two_endpoint_rows:
        lower_lock = local_lock(x_value)
        upper_lock = local_lock(y_value)
        if upper_lock.locked:
            upper_locked_rows += 1
        if not (lower_lock.locked and upper_lock.locked):
            continue
        rows.append(
            AnchorRow(
                rank=0,
                x=x_value,
                y=y_value,
                lower_lock=lower_lock,
                upper_lock=upper_lock,
                lower_transported_deadline_width=transported_deadline_width(case.n, lower_lock),
                upper_transported_deadline_width=transported_deadline_width(case.n, upper_lock),
            )
        )

    ranked = sorted(
        rows,
        key=lambda row: (abs(mpz_to_int(row.x - center)), mpz_to_int(row.x)),
    )
    ranked_rows = [
        AnchorRow(
            rank=index,
            x=row.x,
            y=row.y,
            lower_lock=row.lower_lock,
            upper_lock=row.upper_lock,
            lower_transported_deadline_width=row.lower_transported_deadline_width,
            upper_transported_deadline_width=row.upper_transported_deadline_width,
        )
        for index, row in enumerate(ranked, start=1)
    ]
    counts: dict[str, object] = {
        "center": str(center),
        "balance_lower": str(lower_balance),
        "balance_upper": str(upper_balance),
        "max_lower_endpoints": max_lower_endpoints,
        "lower_pgs_endpoints_seen": len(lower_endpoints),
        "lower_endpoint_walk_budget_exhausted": budget_exhausted,
        "lowest_endpoint_seen": None if not lower_endpoints else str(lower_endpoints[-1]),
        "reciprocal_balance_rows": reciprocal_balance,
        "reciprocal_wheel_rows": reciprocal_wheel,
        "reciprocal_endpoint_rows": len(two_endpoint_rows),
        "upper_locked_rows": upper_locked_rows,
        "two_sided_pgs_lock_rows": len(ranked_rows),
    }
    return ranked_rows, counts


def lock_to_json(lock: LocalLock, prefix: str) -> dict[str, object]:
    """Return local-lock fields with one side prefix."""
    return {
        f"{prefix}_previous_endpoint": None if lock.previous_endpoint is None else str(lock.previous_endpoint),
        f"{prefix}_reset_endpoint": None if lock.reset_endpoint is None else str(lock.reset_endpoint),
        f"{prefix}_reset_gap_offset": lock.reset_gap_offset,
        f"{prefix}_carrier_w": None if lock.carrier_w is None else str(lock.carrier_w),
        f"{prefix}_carrier_d": lock.carrier_d,
        f"{prefix}_lock_carrier_offset": lock.lock_carrier_offset,
        f"{prefix}_lock_carrier_d": lock.lock_carrier_d,
        f"{prefix}_d_threat_offset": lock.lower_d_threat_offset,
        f"{prefix}_tail_after_reset_offsets": list(lock.tail_after_reset_offsets),
        f"{prefix}_reset_deadline_kind": lock.reset_deadline_kind,
        f"{prefix}_reset_deadline_offset": lock.reset_deadline_offset,
        f"{prefix}_reset_deadline_value": None if lock.reset_deadline_value is None else str(lock.reset_deadline_value),
        f"{prefix}_reset_deadline_margin": lock.reset_deadline_margin,
        f"{prefix}_reset_signature": lock.reset_signature,
    }


def anchor_to_json(case: LadderCase, row: AnchorRow) -> dict[str, object]:
    """Return one two-sided anchor row as JSON-safe public fields."""
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rank": row.rank,
        "x": str(row.x),
        "y": str(row.y),
        "lower_transported_deadline_width": row.lower_transported_deadline_width,
        "upper_transported_deadline_width": row.upper_transported_deadline_width,
        "resolver_status": "transported_deadline_invariant_not_derived",
        "rule_id": RULE_ID,
    }
    payload.update(lock_to_json(row.lower_lock, "lower"))
    payload.update(lock_to_json(row.upper_lock, "upper"))
    return payload


def result_row(case: LadderCase, anchors: list[AnchorRow]) -> dict[str, object]:
    """Return unresolved inference until the transported invariant is derived."""
    reason = (
        "no_two_sided_pgs_lock"
        if not anchors
        else "transported_deadline_invariant_not_derived"
    )
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "status": "unresolved",
        "unresolved_reason": reason,
        "rule_id": RULE_ID,
    }


def summary_row(case: LadderCase, counts: dict[str, object], anchors: list[AnchorRow]) -> dict[str, object]:
    """Return one public funnel summary row."""
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "balance_band": str(BALANCE_BAND),
        **counts,
        "ordered_survivors": len(anchors),
        "unordered_survivors": len({tuple(sorted((str(row.x), str(row.y)))) for row in anchors}),
        "resolver_status": "transported_deadline_invariant_not_derived",
        "rule_id": RULE_ID,
    }


def run_cases(
    cases: list[LadderCase],
    max_lower_endpoints: int,
    chunk_width: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Run every public case through the same PGS-first surface."""
    results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    survivor_payloads: list[dict[str, object]] = []
    for case in cases:
        if not case_supported_by_interval_backend(case):
            empty_counts: dict[str, object] = {
                "small_regime_max_bits": SMALL_REGIME_MAX_BITS,
                "interval_backend_status": "gmp_interval_backend_required",
                "two_sided_pgs_lock_rows": 0,
            }
            results.append(
                {
                    "case_id": case.case_id,
                    "bits": case.bits,
                    "N": str(case.n),
                    "status": "unresolved",
                    "unresolved_reason": "gmp_interval_backend_required",
                    "rule_id": RULE_ID,
                }
            )
            summaries.append(summary_row(case, empty_counts, []))
            continue
        anchors, counts = pgs_anchor_rows(case, max_lower_endpoints, chunk_width)
        results.append(result_row(case, anchors))
        summaries.append(summary_row(case, counts, anchors))
        survivor_payloads.extend(anchor_to_json(case, row) for row in anchors)
    return results, summaries, survivor_payloads


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the RSA v2 PGS-first experiment.")
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
        help="Directory for inference_rows.jsonl, survivor_rows.jsonl, and summary.json.",
    )
    parser.add_argument(
        "--max-lower-endpoints",
        type=int,
        default=DEFAULT_MAX_LOWER_ENDPOINTS,
        help="PGS endpoint-walk budget from the square-root side.",
    )
    parser.add_argument(
        "--chunk-width",
        type=int,
        default=DEFAULT_CHUNK_WIDTH,
        help="Public endpoint-walk chunk width.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the official experiment."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cases = load_cases(args.cases)
    results, summaries, survivors = run_cases(
        cases,
        args.max_lower_endpoints,
        args.chunk_width,
    )
    write_jsonl(args.output_dir / "inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", survivors)
    write_json(args.output_dir / "summary.json", {"cases": summaries})
    print(json.dumps({"cases": summaries}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
