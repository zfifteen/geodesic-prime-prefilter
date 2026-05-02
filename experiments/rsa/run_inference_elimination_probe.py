#!/usr/bin/env python3
"""Toy RSA survivor funnel focused on inference-only elimination.

This script knows only ``N`` and structural search parameters. It does not store
hidden factors or run exact factor certification.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import gmpy2


REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_SRC = REPO_ROOT / "src" / "python"
sys.path.insert(0, str(PYTHON_SRC))

from z_band_prime_composite_field import divisor_counts_segment
from z_band_prime_predictor.simple_pgs_generator import pgs_chamber_reset_state_certificate


SUMMARY_PATH = Path("experiments/rsa/inference_elimination_probe.csv")
SURVIVOR_PATH = Path("experiments/rsa/inference_elimination_survivors.jsonl")
WHEEL_PRIMES = (2, 3, 5, 7)
PGS_CHAMBER_RADIUS = 16
PGS_ENDPOINT_TOLERANCE = 0
RULE_X_CANDIDATE_BOUND = 128
EXACT_CHAMBER_VALUE_LIMIT = (1 << 63) - 1 - RULE_X_CANDIDATE_BOUND
SEGMENT_SIZE = 1_000_000
MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})
STATUS_REJECTED = "REJECTED"
STATUS_RESOLVED_SURVIVOR = "RESOLVED_SURVIVOR"
STATUS_UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class ToyCase:
    case_id: str
    n: int
    radius: int
    balance_band: int


@dataclass(frozen=True)
class CandidateState:
    d: int
    q_floor: int
    eliminated: bool
    reason: str
    pgs_p_hat: int | None
    pgs_p_distance: int | None
    pgs_q_hat: int | None
    pgs_q_distance: int | None
    rule_x_p_anchor: int | None
    rule_x_p_hat: int | None
    rule_x_q_anchor: int | None
    rule_x_q_hat: int | None


@dataclass(frozen=True)
class EndpointField:
    nearest_by_value: dict[int, tuple[int | None, int | None]]


TOY_CASES = (
    ToyCase("rsa_like_60bit_skew_14", 648518344462237693, 16643, 2),
    ToyCase("rsa_like_80bit_skew_16", 680020773533224614100823, 65806, 2),
    ToyCase("rsa_like_100bit_skew_18", 713053462628394237921883844429, 262467, 2),
    ToyCase("rsa_like_125bit_skew_18", 47852207848256971175506009106282971019, 262422, 2),
    ToyCase("rsa_like_150bit_skew_20", 802826827147102433094322495052834506987796881, 1048877, 2),
)


def small_primes(limit: int) -> list[int]:
    """Return every prime up to one sieve limit."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if sieve[value]:
            sieve[value * value : limit + 1 : value] = b"\x00" * (
                ((limit - value * value) // value) + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


@lru_cache(maxsize=8)
def prime_table(limit: int) -> tuple[int, ...]:
    """Return primes up to one limit for repeated local chambers."""
    if limit < 2:
        return ()
    base_primes = small_primes(math.isqrt(limit))
    primes: list[int] = []
    for segment_lo in range(2, limit + 1, SEGMENT_SIZE):
        segment_hi = min(segment_lo + SEGMENT_SIZE - 1, limit)
        sieve = bytearray(b"\x01") * (segment_hi - segment_lo + 1)
        for prime in base_primes:
            prime_square = prime * prime
            if prime_square > segment_hi:
                break
            start = max(prime_square, ((segment_lo + prime - 1) // prime) * prime)
            sieve[start - segment_lo : segment_hi - segment_lo + 1 : prime] = b"\x00" * (
                ((segment_hi - start) // prime) + 1
            )
        for offset, is_prime in enumerate(sieve):
            if is_prime:
                primes.append(segment_lo + offset)
    return tuple(primes)


def strong_composite_witness(n: int, base: int, odd_part: int, shifts: int) -> bool:
    """Return True when one Miller-Rabin base proves compositeness."""
    value = int(gmpy2.powmod(base, odd_part, n))
    if value == 1 or value == n - 1:
        return False
    for _ in range(shifts - 1):
        value = int(gmpy2.f_mod(gmpy2.mpz(value) * value, n))
        if value == n - 1:
            return False
    return True


def has_no_composite_witness(n: int) -> bool:
    """Return True when the fixed bases find no composite witness."""
    if n < 2:
        return False
    for base in MR_BASES:
        if n == base:
            return True
        if n % base == 0:
            return False
    odd_part = n - 1
    shifts = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shifts += 1
    return not any(
        strong_composite_witness(n, base, odd_part, shifts)
        for base in MR_BASES
    )


@lru_cache(maxsize=1000000)
def endpoint_state(value: int) -> bool:
    """Return whether one integer is an endpoint under the divisor-count rule."""
    return has_no_composite_witness(value)


def divisor_counts_segment_gmp(lo: int, hi: int) -> list[int]:
    """Compute divisor counts on one interval without int64 storage."""
    if lo < 1:
        raise ValueError("lo must be at least 1")
    if hi <= lo:
        raise ValueError("hi must be larger than lo")

    residual = [gmpy2.mpz(value) for value in range(lo, hi)]
    divisor_count = [1] * (hi - lo)
    cube_root_limit = int(gmpy2.iroot(hi - 1, 3)[0])
    if (cube_root_limit + 1) ** 3 <= hi - 1:
        cube_root_limit += 1

    for prime in prime_table(cube_root_limit):
        start = ((lo + prime - 1) // prime) * prime
        for index in range(start - lo, hi - lo, prime):
            exponent = 0
            while gmpy2.is_divisible(residual[index], prime):
                residual[index] = gmpy2.divexact(residual[index], prime)
                exponent += 1
            if exponent:
                divisor_count[index] *= exponent + 1

    for index, remainder in enumerate(residual):
        if remainder == 1:
            continue
        remainder_int = int(remainder)
        if has_no_composite_witness(remainder_int):
            divisor_count[index] *= 2
            continue
        root = math.isqrt(remainder_int)
        if root * root == remainder_int and has_no_composite_witness(root):
            divisor_count[index] *= 3
            continue
        divisor_count[index] *= 4

    if lo <= 1 < hi:
        divisor_count[1 - lo] = 1
    return divisor_count


@lru_cache(maxsize=200000)
def divisor_counts_exact(lo: int, hi: int) -> tuple[int, ...]:
    """Return divisor counts using the exact backend required by the interval."""
    if hi - 1 <= EXACT_CHAMBER_VALUE_LIMIT:
        return tuple(int(value) for value in divisor_counts_segment(lo, hi))
    return tuple(divisor_counts_segment_gmp(lo, hi))


def candidate_region(n: int, radius: int) -> list[int]:
    """Return the deterministic candidate region around sqrt(N)."""
    center = math.isqrt(n)
    lo = max(2, center - radius)
    hi = center + radius
    return list(range(lo, hi + 1))


def wheel_admissible(value: int) -> bool:
    """Return whether value can be a prime endpoint under the fixed wheel."""
    return all(value == prime or value % prime != 0 for prime in WHEEL_PRIMES)


def endpoint_query_values(
    n: int,
    candidates: list[int],
    sqrt_n: int,
    balance_band: int,
) -> set[int]:
    """Return values whose endpoint chambers are required by this case."""
    lower = max(2, sqrt_n // balance_band)
    upper = sqrt_n * balance_band
    values: set[int] = set()
    for d in candidates:
        if d < lower or d > upper or not wheel_admissible(d):
            continue
        q_floor = n // d
        if q_floor < lower or q_floor > upper or not wheel_admissible(q_floor):
            continue
        values.add(d)
        values.add(q_floor)
    return values


def build_endpoint_field(values: set[int], chamber_radius: int) -> EndpointField:
    """Build the endpoint field required by one candidate surface."""
    nearest_by_value: dict[int, tuple[int | None, int | None]] = {}
    endpoint_cache: dict[int, bool] = {}

    for value in sorted(values):
        lo = max(2, value - chamber_radius)
        hi = value + chamber_radius
        endpoints: list[int] = []
        for candidate in range(lo, hi + 1):
            is_endpoint = endpoint_cache.get(candidate)
            if is_endpoint is None:
                is_endpoint = endpoint_state(candidate)
                endpoint_cache[candidate] = is_endpoint
            if is_endpoint:
                endpoints.append(candidate)
        if not endpoints:
            nearest_by_value[value] = (None, None)
            continue
        endpoint = min(endpoints, key=lambda candidate: (abs(candidate - value), candidate))
        nearest_by_value[value] = (endpoint, abs(endpoint - value))

    return EndpointField(nearest_by_value)


def endpoint_field_equivalence_failures(
    endpoint_field: EndpointField,
    values: set[int],
    chamber_radius: int,
) -> int:
    """Return count of sub-limit endpoint-field disagreements."""
    failures = 0
    for value in sorted(values):
        if value + chamber_radius > EXACT_CHAMBER_VALUE_LIMIT:
            continue
        expected = nearest_pgs_endpoint(value, chamber_radius)
        observed = endpoint_field.nearest_by_value[value]
        if observed != expected:
            failures += 1
    return failures


def endpoint_mode(endpoint_values: set[int], chamber_radius: int) -> str:
    """Return the endpoint mode used by one case."""
    if all(value + chamber_radius <= EXACT_CHAMBER_VALUE_LIMIT for value in endpoint_values):
        return "batched_endpoint_state_int64_equivalence_checked"
    return "batched_endpoint_state_gmp"


def rule_x_mode(endpoint_values: set[int]) -> str:
    """Return the Rule X mode used by one case."""
    if all(value <= EXACT_CHAMBER_VALUE_LIMIT for value in endpoint_values):
        return "original_chamber_reset"
    return "endpoint_scan_above_int64"


def candidate_state(
    d: int,
    q_floor: int,
    eliminated: bool,
    reason: str,
    pgs_p_hat: int | None = None,
    pgs_p_distance: int | None = None,
    pgs_q_hat: int | None = None,
    pgs_q_distance: int | None = None,
    rule_x_p_anchor: int | None = None,
    rule_x_p_hat: int | None = None,
    rule_x_q_anchor: int | None = None,
    rule_x_q_hat: int | None = None,
) -> CandidateState:
    """Return one candidate state."""
    return CandidateState(
        d,
        q_floor,
        eliminated,
        reason,
        pgs_p_hat,
        pgs_p_distance,
        pgs_q_hat,
        pgs_q_distance,
        rule_x_p_anchor,
        rule_x_p_hat,
        rule_x_q_anchor,
        rule_x_q_hat,
    )


def nearest_pgs_endpoint(
    value: int,
    chamber_radius: int,
    endpoint_field: EndpointField | None = None,
) -> tuple[int | None, int | None]:
    """Return the nearest divisor-count endpoint inside a local chamber."""
    if endpoint_field is not None:
        return endpoint_field.nearest_by_value[value]

    lo = max(2, value - chamber_radius)
    hi = value + chamber_radius + 1
    counts = divisor_counts_exact(lo, hi)
    endpoints = [
        lo + offset
        for offset, divisor_count in enumerate(counts)
        if int(divisor_count) == 2
    ]
    if not endpoints:
        return None, None
    endpoint = min(endpoints, key=lambda candidate: (abs(candidate - value), candidate))
    return endpoint, abs(endpoint - value)


@lru_cache(maxsize=None)
def previous_pgs_endpoint(value: int, chamber_radius: int = RULE_X_CANDIDATE_BOUND) -> int | None:
    """Return the nearest previous divisor-count endpoint below value."""
    if value > EXACT_CHAMBER_VALUE_LIMIT:
        candidate = value - 1
        while candidate >= 2:
            if endpoint_state(candidate):
                return candidate
            candidate -= 1

    hi = value
    while hi > 2:
        lo = max(2, hi - chamber_radius)
        counts = divisor_counts_exact(lo, hi)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return lo + offset
        hi = lo
    return None


@lru_cache(maxsize=None)
def rule_x_endpoint_from_anchor(anchor: int) -> int | None:
    """Return the Rule X chamber-reset endpoint inferred from an anchor."""
    if anchor + RULE_X_CANDIDATE_BOUND > EXACT_CHAMBER_VALUE_LIMIT:
        for offset in range(1, RULE_X_CANDIDATE_BOUND + 1):
            candidate = anchor + offset
            if endpoint_state(candidate):
                return candidate
        return None
    certificate = pgs_chamber_reset_state_certificate(anchor, RULE_X_CANDIDATE_BOUND)
    if certificate is None:
        return None
    return int(certificate["q"])


def admissible_offsets(p: int, candidate_bound: int) -> list[int]:
    """Return wheel-open boundary offsets inside the chamber."""
    return [
        offset
        for offset in range(1, candidate_bound + 1)
        if (p + offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30
    ]


def pgs_chamber_reset_state_certificate_exact(
    p: int,
    candidate_bound: int,
) -> dict[str, object] | None:
    """Return the first GWR/NLSC chamber-reset survivor."""
    counts = divisor_counts_exact(p + 1, p + candidate_bound + 1)
    offset_set = set(admissible_offsets(p, candidate_bound))
    candidate_states: list[dict[str, object]] = []
    carrier_offset: int | None = None
    carrier_d: int | None = None
    unresolved_count = 0

    for offset, divisor_count in enumerate(counts, start=1):
        n = p + offset
        if offset in offset_set:
            if divisor_count > 2:
                status = STATUS_REJECTED
            elif unresolved_count > 0:
                status = STATUS_UNRESOLVED
            else:
                status = STATUS_RESOLVED_SURVIVOR
            candidate_states.append(
                {
                    "offset": offset,
                    "n": n,
                    "status": status,
                    "carrier_offset": carrier_offset,
                    "carrier_d": carrier_d,
                }
            )

        if divisor_count > 2:
            if carrier_d is None or divisor_count < carrier_d:
                carrier_offset = offset
                carrier_d = divisor_count
        else:
            unresolved_count += 1

    lock_carrier_offset: int | None = None
    lock_carrier_d: int | None = None
    for state in candidate_states:
        if (
            state["status"] == STATUS_RESOLVED_SURVIVOR
            and state["carrier_offset"] is not None
        ):
            lock_carrier_offset = int(state["carrier_offset"])
            lock_carrier_d = int(state["carrier_d"])
            break

    threat_offset: int | None = None
    if lock_carrier_offset is not None and lock_carrier_d is not None:
        for offset in range(lock_carrier_offset + 1, candidate_bound + 1):
            divisor_count = counts[offset - 1]
            if divisor_count > 2 and divisor_count < lock_carrier_d:
                threat_offset = offset
                break

    resolved: list[dict[str, object]] = []
    for state in candidate_states:
        final_status = str(state["status"])
        offset = int(state["offset"])
        if threat_offset is not None and offset > threat_offset:
            final_status = STATUS_REJECTED
        if final_status == STATUS_RESOLVED_SURVIVOR:
            resolved.append(state)

    if not resolved:
        return None
    first = resolved[0]
    gap_offset = int(first["offset"])
    return {"p": p, "q": p + gap_offset, "gap_offset": gap_offset}


def rule_x_compatible_endpoint(value: int) -> tuple[bool, int | None, int | None]:
    """Return whether value is the Rule X endpoint after its previous endpoint."""
    anchor = previous_pgs_endpoint(value)
    if anchor is None:
        return True, None, None
    endpoint = rule_x_endpoint_from_anchor(anchor)
    if endpoint is None:
        return True, anchor, None
    return endpoint == value, anchor, endpoint


def infer_elimination(
    n: int,
    d: int,
    sqrt_n: int,
    balance_band: int,
    endpoint_field: EndpointField,
) -> CandidateState:
    """Eliminate a candidate without evaluating divisibility by N."""
    lower = max(2, sqrt_n // balance_band)
    upper = sqrt_n * balance_band

    if d < lower or d > upper:
        return candidate_state(d, n // d, True, "candidate_outside_balance_band")

    if not wheel_admissible(d):
        return candidate_state(d, n // d, True, "candidate_not_wheel_endpoint")

    q_floor = n // d
    if q_floor < lower or q_floor > upper:
        return candidate_state(d, q_floor, True, "cofactor_region_outside_balance_band")

    if not wheel_admissible(q_floor):
        return candidate_state(d, q_floor, True, "cofactor_floor_not_wheel_endpoint")

    p_hat, p_distance = nearest_pgs_endpoint(d, PGS_CHAMBER_RADIUS, endpoint_field)
    q_hat, q_distance = nearest_pgs_endpoint(q_floor, PGS_CHAMBER_RADIUS, endpoint_field)
    if p_distance is not None and p_distance > PGS_ENDPOINT_TOLERANCE:
        return candidate_state(
            d, q_floor, True, "pgs_candidate_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
        )
    if q_distance is not None and q_distance > PGS_ENDPOINT_TOLERANCE:
        return candidate_state(
            d, q_floor, True, "pgs_cofactor_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
        )

    p_rule_x_ok, p_anchor, p_rule_x_hat = rule_x_compatible_endpoint(d)
    if not p_rule_x_ok:
        return candidate_state(
            d, q_floor, True, "rule_x_candidate_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
            p_anchor, p_rule_x_hat, None, None,
        )

    q_rule_x_ok, q_anchor, q_rule_x_hat = rule_x_compatible_endpoint(q_floor)
    if not q_rule_x_ok:
        return candidate_state(
            d, q_floor, True, "rule_x_cofactor_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
            p_anchor, p_rule_x_hat, q_anchor, q_rule_x_hat,
        )

    return candidate_state(
        d, q_floor, False, "survived",
        p_hat, p_distance, q_hat, q_distance,
        p_anchor, p_rule_x_hat, q_anchor, q_rule_x_hat,
    )


def rank_survivors(states: list[CandidateState], sqrt_n: int) -> list[CandidateState]:
    """Rank survivors by symmetric distance from sqrt(N)."""
    survivors = [state for state in states if not state.eliminated]
    return sorted(survivors, key=lambda state: (abs(state.d - sqrt_n), state.d))


def run_case(case: ToyCase) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run one toy case and return summary plus ranked survivors."""
    n = case.n
    sqrt_n = math.isqrt(n)
    candidates = candidate_region(n, case.radius)
    endpoint_values = endpoint_query_values(n, candidates, sqrt_n, case.balance_band)
    endpoint_field = build_endpoint_field(endpoint_values, PGS_CHAMBER_RADIUS)
    equivalence_failures = endpoint_field_equivalence_failures(
        endpoint_field,
        endpoint_values,
        PGS_CHAMBER_RADIUS,
    )
    if equivalence_failures:
        raise AssertionError(
            f"{case.case_id}: endpoint field equivalence failures={equivalence_failures}"
        )
    states = [
        infer_elimination(n, d, sqrt_n, case.balance_band, endpoint_field)
        for d in candidates
    ]
    ranked = rank_survivors(states, sqrt_n)

    generated = len(candidates)
    eliminated_count = sum(1 for state in states if state.eliminated)
    reason_counts = Counter(state.reason for state in states if state.eliminated)
    avoided_checks = eliminated_count

    summary = {
        "case_id": case.case_id,
        "N": n,
        "bits": n.bit_length(),
        "radius": case.radius,
        "balance_band": case.balance_band,
        "pgs_chamber_radius": PGS_CHAMBER_RADIUS,
        "pgs_endpoint_tolerance": PGS_ENDPOINT_TOLERANCE,
        "rule_x_candidate_bound": RULE_X_CANDIDATE_BOUND,
        "endpoint_mode": endpoint_mode(endpoint_values, PGS_CHAMBER_RADIUS),
        "rule_x_mode": rule_x_mode(endpoint_values),
        "endpoint_values": len(endpoint_values),
        "endpoint_equivalence_failures": equivalence_failures,
        "status": "completed",
        "generated": generated,
        "balance_rejected": reason_counts["candidate_outside_balance_band"]
        + reason_counts["cofactor_region_outside_balance_band"],
        "wheel_rejected": reason_counts["candidate_not_wheel_endpoint"]
        + reason_counts["cofactor_floor_not_wheel_endpoint"],
        "pgs_chamber_rejected": reason_counts["pgs_candidate_endpoint_incompatible"]
        + reason_counts["pgs_cofactor_endpoint_incompatible"],
        "rule_x_rejected": reason_counts["rule_x_candidate_endpoint_incompatible"]
        + reason_counts["rule_x_cofactor_endpoint_incompatible"],
        "inference_eliminated": eliminated_count,
        "survivors": len(ranked),
        "elimination_rate": f"{eliminated_count / generated:.6f}",
        "concrete_checks_avoided": avoided_checks,
        "computation_displacement": f"{avoided_checks / generated:.6f}",
    }
    survivors = [
        {
            "case_id": case.case_id,
            "N": n,
            "rank": rank,
            "d": state.d,
            "q_floor": state.q_floor,
            "pgs_p_hat": state.pgs_p_hat,
            "pgs_p_distance": state.pgs_p_distance,
            "pgs_q_hat": state.pgs_q_hat,
            "pgs_q_distance": state.pgs_q_distance,
            "rule_x_p_anchor": state.rule_x_p_anchor,
            "rule_x_p_hat": state.rule_x_p_hat,
            "rule_x_q_anchor": state.rule_x_q_anchor,
            "rule_x_q_hat": state.rule_x_q_hat,
            "reason": state.reason,
        }
        for rank, state in enumerate(ranked, start=1)
    ]
    return summary, survivors


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    """Write CSV rows with LF line endings."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(rows: list[dict[str, object]], output_path: Path) -> None:
    """Write JSONL rows with LF line endings."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def main() -> int:
    summaries: list[dict[str, object]] = []
    survivors: list[dict[str, object]] = []
    for case in TOY_CASES:
        summary, case_survivors = run_case(case)
        summaries.append(summary)
        survivors.extend(case_survivors)

    write_csv(summaries, SUMMARY_PATH)
    write_jsonl(survivors, SURVIVOR_PATH)

    print("case_id,generated,inference_eliminated,survivors,computation_displacement")
    for row in summaries:
        print(
            f"{row['case_id']},{row['generated']},{row['inference_eliminated']},"
            f"{row['survivors']},{row['computation_displacement']}"
        )
    print(f"wrote {SUMMARY_PATH}")
    print(f"wrote {SURVIVOR_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
