#!/usr/bin/env python3
"""Run the RSA v2 reciprocal PGS deadline-lock experiment."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
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


RULE_ID = "reciprocal_pgs_deadline_lock_v1"
CHAMBER_RADIUS = gmpy2.mpz(1024)
BALANCE_BAND = gmpy2.mpz(2)
PGS_ENDPOINT_RADIUS = 16
RULE_X_CANDIDATE_BOUND = 128
RECURSIVE_DEPTH = 4
DEADLINE_WIDTH_TOLERANCE = 1
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})


@dataclass(frozen=True)
class LadderCase:
    """One public modulus rung."""

    case_id: str
    bits: int
    n: gmpy2.mpz


@dataclass(frozen=True)
class CandidateRow:
    """One public chamber coordinate and its reciprocal floor coordinate."""

    x: gmpy2.mpz
    y: gmpy2.mpz


@dataclass(frozen=True)
class LocalLock:
    """One local PGSPG reset state around a candidate endpoint."""

    value: gmpy2.mpz
    nearest_endpoint: gmpy2.mpz | None
    nearest_endpoint_distance: int | None
    previous_endpoint: gmpy2.mpz | None
    reset_endpoint: gmpy2.mpz | None
    reset_gap_offset: int | None
    active_count: int | None
    resolved_count: int | None
    unresolved_count: int | None
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
class SurvivorRow:
    """One ordered survivor row after the public PGS checks."""

    rank: int
    x: gmpy2.mpz
    y: gmpy2.mpz
    lower_lock: LocalLock
    upper_lock: LocalLock
    recursive_rounds_locked: int
    deadline_locked: bool
    deadline_lock_reason: str
    lower_transported_deadline_width: int | None
    upper_transported_deadline_width: int | None


def mpz_to_int(value: gmpy2.mpz) -> int:
    """Convert one GMP integer for existing local PGSPG helper calls."""
    return int(value)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


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
    """Return whether one integer sits in a residue class open to endpoints."""
    return int(value % 30) in WHEEL_OPEN_RESIDUES_MOD30


def candidate_band(n_value: gmpy2.mpz) -> list[gmpy2.mpz]:
    """Return the full public chamber around the integer square root of N."""
    # The integer square root gives the public center of the semiprime chamber.
    center = gmpy2.isqrt(n_value)
    # The fixed radius defines the lower side of the public chamber.
    lower = center - CHAMBER_RADIUS
    # The fixed radius defines the upper side of the public chamber.
    upper = center + CHAMBER_RADIUS
    return [lower + offset for offset in range(mpz_to_int(upper - lower) + 1)]


def balance_bounds(center: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Return the global balance interval around the square-root center."""
    # Division by the balance band gives the smallest accepted balanced endpoint.
    lower = center // BALANCE_BAND
    # Multiplication by the balance band gives the largest accepted balanced endpoint.
    upper = center * BALANCE_BAND
    return lower, upper


def reciprocal_floor(n_value: gmpy2.mpz, x_value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the public reciprocal floor coordinate for one candidate."""
    # The reciprocal floor maps one candidate to its public opposite-side coordinate.
    return n_value // x_value


def public_candidate_funnel(n_value: gmpy2.mpz) -> tuple[list[CandidateRow], dict[str, int]]:
    """Apply the public chamber, balance, wheel, and reciprocal-window filters."""
    # The integer square root fixes the public center for both sides of the chamber.
    center = gmpy2.isqrt(n_value)
    lower_balance, upper_balance = balance_bounds(center)
    candidates = candidate_band(n_value)
    post_balance: list[gmpy2.mpz] = []
    post_wheel: list[CandidateRow] = []
    reciprocal_window: list[CandidateRow] = []

    for x_value in candidates:
        if not lower_balance <= x_value <= upper_balance:
            continue
        post_balance.append(x_value)

        if not wheel_open(x_value):
            continue

        y_value = reciprocal_floor(n_value, x_value)
        if not lower_balance <= y_value <= upper_balance:
            continue
        if not wheel_open(y_value):
            continue
        post_wheel.append(CandidateRow(x_value, y_value))

        if center - CHAMBER_RADIUS <= y_value <= center + CHAMBER_RADIUS:
            reciprocal_window.append(CandidateRow(x_value, y_value))

    return reciprocal_window, {
        "initial_candidate_integers": len(candidates),
        "post_balance_candidates": len(post_balance),
        "post_wheel_candidates": len(post_wheel),
        "reciprocal_window_candidates": len(reciprocal_window),
    }


def nearest_endpoint(value: gmpy2.mpz) -> tuple[gmpy2.mpz | None, int | None]:
    """Return the nearest divisor-count endpoint in a local chamber."""
    # The local endpoint chamber starts a fixed distance left of the candidate.
    lo = max(2, mpz_to_int(value) - PGS_ENDPOINT_RADIUS)
    # The local endpoint chamber ends a fixed distance right of the candidate.
    hi = mpz_to_int(value) + PGS_ENDPOINT_RADIUS + 1
    counts = divisor_counts_segment(lo, hi)
    endpoints = [
        gmpy2.mpz(lo + offset)
        for offset, divisor_count in enumerate(counts)
        if int(divisor_count) == 2
    ]
    if not endpoints:
        return None, None
    # The nearest endpoint measures whether the candidate is itself endpoint-stable.
    endpoint = min(endpoints, key=lambda item: (abs(mpz_to_int(item - value)), mpz_to_int(item)))
    return endpoint, abs(mpz_to_int(endpoint - value))


def previous_endpoint(value: gmpy2.mpz) -> gmpy2.mpz | None:
    """Return the nearest previous divisor-count endpoint below one value."""
    hi = mpz_to_int(value)
    while hi > 2:
        # The backward chunk finds the prior endpoint without using N.
        lo = max(2, hi - RULE_X_CANDIDATE_BOUND)
        counts = divisor_counts_segment(lo, hi)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return gmpy2.mpz(lo + offset)
        hi = lo
    return None


def chamber_reset_certificate(anchor: gmpy2.mpz) -> dict[str, object] | None:
    """Return the PGSPG chamber-reset certificate after one previous endpoint."""
    return pgs_chamber_reset_state_certificate(mpz_to_int(anchor), RULE_X_CANDIDATE_BOUND)


def local_lock(value: gmpy2.mpz) -> LocalLock:
    """Return the local endpoint, reset, and reset-deadline state."""
    endpoint, distance = nearest_endpoint(value)
    anchor = previous_endpoint(value)
    certificate = None if anchor is None else chamber_reset_certificate(anchor)
    reset = None if certificate is None else gmpy2.mpz(int(certificate["q"]))
    locked = endpoint == value and distance == 0 and reset == value
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
        # The reset deadline value is the first local state boundary after reset.
        deadline_value = anchor + deadline_offset
    deadline_margin = None
    if reset_gap is not None and deadline_offset is not None:
        # The reset margin is the local distance from the reset endpoint to the deadline.
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
        value=value,
        nearest_endpoint=endpoint,
        nearest_endpoint_distance=distance,
        previous_endpoint=anchor,
        reset_endpoint=reset,
        reset_gap_offset=reset_gap,
        active_count=None if certificate is None else int(certificate["active_count"]),
        resolved_count=None if certificate is None else int(certificate["resolved_count"]),
        unresolved_count=None if certificate is None else int(certificate["unresolved_count"]),
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


def recursive_lock_rounds(n_value: gmpy2.mpz, x_value: gmpy2.mpz, y_value: gmpy2.mpz) -> int:
    """Return how many reciprocal reset rounds one pair survives."""
    rounds_locked = 0
    current_x = x_value
    current_y = y_value
    for _round_index in range(1, RECURSIVE_DEPTH + 1):
        lower = local_lock(current_x)
        upper = local_lock(current_y)
        if not (lower.locked and upper.locked):
            break
        # The lower side transported through the upper reset must return to the lower reset.
        transported_x = n_value // upper.reset_endpoint
        # The upper side transported through the lower reset must return to the upper reset.
        transported_y = n_value // lower.reset_endpoint
        if transported_x != lower.reset_endpoint or transported_y != upper.reset_endpoint:
            break
        rounds_locked += 1
        current_x = lower.reset_endpoint
        current_y = upper.reset_endpoint
    return rounds_locked


def transported_deadline_width(n_value: gmpy2.mpz, lock: LocalLock) -> int | None:
    """Return how wide one reset interval becomes under the reciprocal map."""
    if lock.reset_endpoint is None or lock.reset_deadline_value is None:
        return None
    # The reciprocal map sends the reset endpoint to the opposite-side coordinate.
    reset_image = n_value // lock.reset_endpoint
    # The reciprocal map sends the reset deadline to the opposite-side deadline image.
    deadline_image = n_value // lock.reset_deadline_value
    return abs(mpz_to_int(reset_image - deadline_image))


def deadline_lock(
    n_value: gmpy2.mpz,
    lower: LocalLock,
    upper: LocalLock,
) -> tuple[bool, str, int | None, int | None]:
    """Return whether two reset states form a reciprocal deadline lock."""
    lower_width = transported_deadline_width(n_value, lower)
    upper_width = transported_deadline_width(n_value, upper)
    if lower.reset_signature != upper.reset_signature:
        return False, "reset_signature_mismatch", lower_width, upper_width
    if lower.reset_deadline_margin != upper.reset_deadline_margin:
        return False, "reset_deadline_margin_mismatch", lower_width, upper_width
    if lower_width is None or upper_width is None:
        return False, "transported_deadline_missing", lower_width, upper_width
    if abs(lower_width - upper_width) > DEADLINE_WIDTH_TOLERANCE:
        return False, "transported_deadline_width_mismatch", lower_width, upper_width
    return True, "reciprocal_deadline_lock", lower_width, upper_width


def survivor_rows(case: LadderCase) -> tuple[list[SurvivorRow], dict[str, int]]:
    """Return all ordered recursive PGS survivors for one public case."""
    candidates, counts = public_candidate_funnel(case.n)
    survivors: list[SurvivorRow] = []
    for row in candidates:
        lower = local_lock(row.x)
        upper = local_lock(row.y)
        if not (lower.locked and upper.locked):
            continue
        rounds = recursive_lock_rounds(case.n, row.x, row.y)
        if rounds != RECURSIVE_DEPTH:
            continue
        deadline_ok, reason, lower_width, upper_width = deadline_lock(case.n, lower, upper)
        survivors.append(
            SurvivorRow(
                rank=0,
                x=row.x,
                y=row.y,
                lower_lock=lower,
                upper_lock=upper,
                recursive_rounds_locked=rounds,
                deadline_locked=deadline_ok,
                deadline_lock_reason=reason,
                lower_transported_deadline_width=lower_width,
                upper_transported_deadline_width=upper_width,
            )
        )
    # The square-root distance ranking keeps the survivor ordering deterministic.
    center = gmpy2.isqrt(case.n)
    ranked = sorted(survivors, key=lambda item: (abs(mpz_to_int(item.x - center)), mpz_to_int(item.x)))
    return [
        SurvivorRow(
            rank=index,
            x=row.x,
            y=row.y,
            lower_lock=row.lower_lock,
            upper_lock=row.upper_lock,
            recursive_rounds_locked=row.recursive_rounds_locked,
            deadline_locked=row.deadline_locked,
            deadline_lock_reason=row.deadline_lock_reason,
            lower_transported_deadline_width=row.lower_transported_deadline_width,
            upper_transported_deadline_width=row.upper_transported_deadline_width,
        )
        for index, row in enumerate(ranked, start=1)
    ], counts


def lock_to_json(lock: LocalLock, prefix: str) -> dict[str, object]:
    """Return public local-lock fields with one side prefix."""
    return {
        f"{prefix}_previous_endpoint": None if lock.previous_endpoint is None else str(lock.previous_endpoint),
        f"{prefix}_reset_endpoint": None if lock.reset_endpoint is None else str(lock.reset_endpoint),
        f"{prefix}_reset_gap_offset": lock.reset_gap_offset,
        f"{prefix}_active_count": lock.active_count,
        f"{prefix}_resolved_count": lock.resolved_count,
        f"{prefix}_unresolved_count": lock.unresolved_count,
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


def survivor_to_json(case: LadderCase, row: SurvivorRow) -> dict[str, object]:
    """Return one ordered survivor as JSON-safe public fields."""
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rank": row.rank,
        "x": str(row.x),
        "y": str(row.y),
        "recursive_rounds_locked": row.recursive_rounds_locked,
        "deadline_locked": row.deadline_locked,
        "deadline_lock_reason": row.deadline_lock_reason,
        "lower_transported_deadline_width": row.lower_transported_deadline_width,
        "upper_transported_deadline_width": row.upper_transported_deadline_width,
        "rule_id": RULE_ID,
    }
    payload.update(lock_to_json(row.lower_lock, "lower"))
    payload.update(lock_to_json(row.upper_lock, "upper"))
    return payload


def result_row(case: LadderCase, survivors: list[SurvivorRow]) -> dict[str, object]:
    """Return the inference result selected by the deadline lock."""
    locked = [row for row in survivors if row.deadline_locked]
    locked_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in locked}
    if len(locked_pairs) != 1:
        reason = "no_reciprocal_deadline_lock" if not locked_pairs else "multiple_reciprocal_deadline_locks"
        return {
            "case_id": case.case_id,
            "bits": case.bits,
            "N": str(case.n),
            "status": "unresolved",
            "unresolved_reason": reason,
            "rule_id": RULE_ID,
        }
    lower, upper = next(iter(locked_pairs))
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "status": "resolved",
        "p": lower,
        "q": upper,
        "rule_id": RULE_ID,
    }


def summary_row(case: LadderCase, counts: dict[str, int], survivors: list[SurvivorRow]) -> dict[str, object]:
    """Return one public funnel summary row."""
    locked = [row for row in survivors if row.deadline_locked]
    survivor_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in survivors}
    locked_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in locked}
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "radius": str(CHAMBER_RADIUS),
        "balance_band": str(BALANCE_BAND),
        **counts,
        "recursive_lock_survivors": len(survivors),
        "ordered_survivors": len(survivors),
        "unordered_survivors": len(survivor_pairs),
        "deadline_lock_ordered_rows": len(locked),
        "deadline_lock_pairs": len(locked_pairs),
        "rule_id": RULE_ID,
    }


def run_cases(cases: list[LadderCase]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Run every public case through the same global solver rule."""
    results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    survivor_payloads: list[dict[str, object]] = []
    for case in cases:
        survivors, counts = survivor_rows(case)
        results.append(result_row(case, survivors))
        summaries.append(summary_row(case, counts, survivors))
        survivor_payloads.extend(survivor_to_json(case, row) for row in survivors)
    return results, summaries, survivor_payloads


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the RSA v2 PGS deadline-lock experiment.")
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the official experiment."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cases = load_cases(args.cases)
    results, summaries, survivors = run_cases(cases)
    write_jsonl(args.output_dir / "inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", survivors)
    write_json(args.output_dir / "summary.json", {"cases": summaries})
    print(json.dumps({"cases": summaries}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
