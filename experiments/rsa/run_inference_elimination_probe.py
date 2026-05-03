#!/usr/bin/env python3
"""Toy RSA survivor funnel focused on inference-only elimination.

This script knows only ``N`` and structural search parameters. It does not store
hidden factors or run exact factor certification.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import gmpy2
import sympy
from sympy import factorint, nextprime, prevprime, randprime


RSA_CASES_PATH = Path("experiments/rsa/rsa_cases.json")
SUMMARY_PATH = Path("experiments/rsa/inference_elimination_probe.csv")
SURVIVOR_PATH = Path("experiments/rsa/inference_elimination_survivors.jsonl")
WHEEL_PRIMES = (2, 3, 5, 7)
PGS_CHAMBER_RADIUS = 16
PGS_ENDPOINT_TOLERANCE = 0
RULE_X_CANDIDATE_BOUND = 128
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})
STATUS_REJECTED = "REJECTED"
STATUS_RESOLVED_SURVIVOR = "RESOLVED_SURVIVOR"
STATUS_UNRESOLVED = "UNRESOLVED"


def generate_rsa_like_skewed_semiprime(target_bits: int, skew_bits: int, max_attempts: int = 500) -> tuple[int, int, int]:
    """
    Generate a high-quality RSA-like skewed semiprime.
    - p and q are strong random primes.
    - Controlled skew |p - q| ≈ 2^skew_bits.
    - N has exactly 'target_bits' bits.
    """
    half_bits = target_bits // 2
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        p = randprime(2**(half_bits - 1), 2**half_bits)
        offset = 1 << skew_bits
        q_candidate = p + offset
        q = nextprime(q_candidate)
        n = p * q
        if n.bit_length() == target_bits:
            return n, p, q
        # Minimal adjustment
        if n.bit_length() < target_bits:
            while n.bit_length() < target_bits and attempts < max_attempts:
                attempts += 1
                q = nextprime(q)
                n = p * q
        else:
            while n.bit_length() > target_bits and attempts < max_attempts:
                attempts += 1
                q = prevprime(q)
                n = p * q
        if n.bit_length() == target_bits:
            return n, p, q
    raise ValueError(f"Failed to generate {target_bits}-bit semiprime after {max_attempts} attempts")


def save_rsa_cases():
    """Generate all cases and save them to a shared JSON file for both probe and audit."""
    cases = []
    for case_id, bits, skew_bits, radius, balance_band in [
        ("rsa_like_60bit_skew_14", 60, 14, 16643, 2),
        ("rsa_like_80bit_skew_16", 80, 16, 65806, 2),
        ("rsa_like_100bit_skew_18", 100, 18, 262467, 2),
        ("rsa_like_125bit_skew_18", 126, 18, 262422, 2),
        ("rsa_like_150bit_skew_20", 150, 20, 1048877, 2),
        ("rsa_like_180bit_skew_22", 180, 22, 4194587, 2),
        ("rsa_like_200bit_skew_24", 200, 24, 16777628, 2),
        # Add future rungs here
    ]:
        n, p, q = generate_rsa_like_skewed_semiprime(bits, skew_bits)
        cases.append({
            "case_id": case_id,
            "n": n,
            "p": p,
            "q": q,
            "radius": radius,
            "balance_band": balance_band,
        })
    with RSA_CASES_PATH.open("w") as f:
        json.dump(cases, f, indent=2)
    print("Generated and saved rsa_cases.json")


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


@dataclass(frozen=True)
class DivisorField:
    counts: dict[int, int]

    def count(self, value: int) -> int:
        return self.counts[value]

    def is_endpoint(self, value: int) -> bool:
        return self.counts[value] == 2


def load_toy_cases():
    if not RSA_CASES_PATH.exists():
        save_rsa_cases()
    with RSA_CASES_PATH.open() as f:
        data = json.load(f)
    return tuple(
        ToyCase(
            case["case_id"],
            case["n"],
            case["radius"],
            case["balance_band"],
        )
        for case in data
    )


TOY_CASES = load_toy_cases()


@lru_cache(maxsize=2_000_000)
def divisor_count_exact_value(value: int) -> int:
    """Return the exact divisor count for one integer."""
    if value < 1:
        raise ValueError("value must be at least 1")
    gmp_value = gmpy2.mpz(value)
    total = 1
    for exponent in factorint(gmp_value).values():
        total *= int(exponent) + 1
    return total


def build_divisor_field(intervals: list[tuple[int, int]]) -> DivisorField:
    """Build exact divisor counts for the union of half-open intervals."""
    values: set[int] = set()
    for lo, hi in intervals:
        if lo < 1:
            raise ValueError("lo must be at least 1")
        if hi <= lo:
            raise ValueError("hi must be larger than lo")
        values.update(range(lo, hi))
    return DivisorField(
        {value: divisor_count_exact_value(value) for value in sorted(values)}
    )


def candidate_region(n: int, radius: int) -> range:
    """Return the deterministic candidate region around sqrt(N)."""
    center = math.isqrt(n)
    lo = max(2, center - radius)
    hi = center + radius
    return range(lo, hi + 1)


def wheel_admissible(value: int) -> bool:
    """Return whether value can be a prime endpoint under the fixed wheel."""
    return all(value == prime or value % prime != 0 for prime in WHEEL_PRIMES)


def endpoint_query_values(
    n: int,
    candidates: range,
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
    intervals = [
        (max(2, value - chamber_radius), value + chamber_radius + 1)
        for value in sorted(values)
    ]
    divisor_field = build_divisor_field(intervals)
    nearest_by_value: dict[int, tuple[int | None, int | None]] = {}

    for value in sorted(values):
        lo = max(2, value - chamber_radius)
        hi = value + chamber_radius + 1
        endpoints = [
            candidate
            for candidate in range(lo, hi)
            if divisor_field.is_endpoint(candidate)
        ]
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
    """Return count of endpoint-field construction failures."""
    return sum(1 for value in values if value not in endpoint_field.nearest_by_value)


def endpoint_mode(endpoint_values: set[int], chamber_radius: int) -> str:
    """Return the endpoint mode used by one case."""
    return "batched_exact_gmp_divisor_field"


def rule_x_mode(endpoint_values: set[int]) -> str:
    """Return the Rule X mode used by one case."""
    return "batched_exact_gmp_chamber_reset"


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
    endpoint_field: EndpointField,
) -> tuple[int | None, int | None]:
    """Return the nearest divisor-count endpoint inside a local chamber."""
    return endpoint_field.nearest_by_value[value]


def admissible_offsets(p: int, candidate_bound: int) -> list[int]:
    """Return wheel-open boundary offsets inside the chamber."""
    return [
        offset
        for offset in range(1, candidate_bound + 1)
        if (p + offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30
    ]


def pgs_chamber_reset_state_certificate_from_field(
    p: int,
    candidate_bound: int,
    divisor_field: DivisorField,
) -> dict[str, object] | None:
    """Return the first GWR/NLSC chamber-reset survivor."""
    offset_set = set(admissible_offsets(p, candidate_bound))
    candidate_states: list[dict[str, object]] = []
    carrier_offset: int | None = None
    carrier_d: int | None = None
    unresolved_count = 0

    for offset in range(1, candidate_bound + 1):
        n = p + offset
        divisor_count = divisor_field.count(n)
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
            divisor_count = divisor_field.count(p + offset)
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


def build_previous_anchor_map(values: set[int]) -> dict[int, int | None]:
    """Build previous endpoint anchors for all Rule X query values."""
    anchors: dict[int, int | None] = {}
    pending = {value: value for value in values}

    while pending:
        intervals = [
            (max(2, hi - RULE_X_CANDIDATE_BOUND), hi)
            for hi in pending.values()
        ]
        divisor_field = build_divisor_field(intervals)
        next_pending: dict[int, int] = {}
        for value, hi in pending.items():
            lo = max(2, hi - RULE_X_CANDIDATE_BOUND)
            anchor = None
            for candidate in range(hi - 1, lo - 1, -1):
                if divisor_field.is_endpoint(candidate):
                    anchor = candidate
                    break
            if anchor is not None:
                anchors[value] = anchor
            elif lo == 2:
                anchors[value] = None
            else:
                next_pending[value] = lo
        pending = next_pending

    return anchors


def build_rule_x_answers(
    values: set[int],
) -> dict[int, tuple[bool | None, int | None, int | None]]:
    """Build Rule X answers from one batched chamber-reset field."""
    anchors = build_previous_anchor_map(values)
    chamber_keys = {
        (anchor, max(RULE_X_CANDIDATE_BOUND, value - anchor))
        for value, anchor in anchors.items()
        if anchor is not None
    }
    intervals = [
        (anchor + 1, anchor + candidate_bound + 1)
        for anchor, candidate_bound in sorted(chamber_keys)
    ]
    divisor_field = build_divisor_field(intervals) if intervals else DivisorField({})
    endpoints: dict[tuple[int, int], int | None] = {}
    for anchor, candidate_bound in sorted(chamber_keys):
        certificate = pgs_chamber_reset_state_certificate_from_field(
            anchor,
            candidate_bound,
            divisor_field,
        )
        endpoints[(anchor, candidate_bound)] = (
            None if certificate is None else int(certificate["q"])
        )

    answers: dict[int, tuple[bool | None, int | None, int | None]] = {}
    for value, anchor in anchors.items():
        if anchor is None:
            answers[value] = (None, None, None)
            continue
        candidate_bound = max(RULE_X_CANDIDATE_BOUND, value - anchor)
        endpoint = endpoints[(anchor, candidate_bound)]
        if endpoint is None:
            answers[value] = (None, anchor, None)
            continue
        answers[value] = (endpoint == value, anchor, endpoint)
    return answers


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
    if p_distance != PGS_ENDPOINT_TOLERANCE:
        return candidate_state(
            d, q_floor, True, "pgs_candidate_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
        )
    if q_distance != PGS_ENDPOINT_TOLERANCE:
        return candidate_state(
            d, q_floor, True, "pgs_cofactor_endpoint_incompatible",
            p_hat, p_distance, q_hat, q_distance,
        )

    return candidate_state(
        d, q_floor, False, "survived",
        p_hat, p_distance, q_hat, q_distance,
        None, None, None, None,
    )


def apply_rule_x(
    state: CandidateState,
    rule_x_answers: dict[int, tuple[bool | None, int | None, int | None]],
) -> CandidateState:
    """Apply batched Rule X answers to one PGS survivor."""
    if state.eliminated:
        return state

    p_rule_x_ok, p_anchor, p_rule_x_hat = rule_x_answers[state.d]
    if p_rule_x_ok is None:
        return candidate_state(
            state.d, state.q_floor, False, "rule_x_candidate_unresolved",
            state.pgs_p_hat, state.pgs_p_distance,
            state.pgs_q_hat, state.pgs_q_distance,
            p_anchor, p_rule_x_hat, None, None,
        )
    if not p_rule_x_ok:
        return candidate_state(
            state.d, state.q_floor, True, "rule_x_candidate_endpoint_incompatible",
            state.pgs_p_hat, state.pgs_p_distance,
            state.pgs_q_hat, state.pgs_q_distance,
            p_anchor, p_rule_x_hat, None, None,
        )

    q_rule_x_ok, q_anchor, q_rule_x_hat = rule_x_answers[state.q_floor]
    if q_rule_x_ok is None:
        return candidate_state(
            state.d, state.q_floor, False, "rule_x_cofactor_unresolved",
            state.pgs_p_hat, state.pgs_p_distance,
            state.pgs_q_hat, state.pgs_q_distance,
            p_anchor, p_rule_x_hat, q_anchor, q_rule_x_hat,
        )
    if not q_rule_x_ok:
        return candidate_state(
            state.d, state.q_floor, True, "rule_x_cofactor_endpoint_incompatible",
            state.pgs_p_hat, state.pgs_p_distance,
            state.pgs_q_hat, state.pgs_q_distance,
            p_anchor, p_rule_x_hat, q_anchor, q_rule_x_hat,
        )

    return candidate_state(
        state.d, state.q_floor, False, "survived",
        state.pgs_p_hat, state.pgs_p_distance,
        state.pgs_q_hat, state.pgs_q_distance,
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
    pgs_survivors: list[CandidateState] = []
    reason_counts: Counter[str] = Counter()
    all_reason_counts: Counter[str] = Counter()
    eliminated_count = 0
    for d in candidates:
        state = infer_elimination(n, d, sqrt_n, case.balance_band, endpoint_field)
        if state.eliminated:
            reason_counts[state.reason] += 1
            all_reason_counts[state.reason] += 1
            eliminated_count += 1
        else:
            pgs_survivors.append(state)

    rule_x_values = {
        value
        for state in pgs_survivors
        for value in (state.d, state.q_floor)
    }
    rule_x_answers = build_rule_x_answers(rule_x_values)
    states: list[CandidateState] = []
    for state in pgs_survivors:
        final_state = apply_rule_x(state, rule_x_answers)
        all_reason_counts[final_state.reason] += 1
        if final_state.eliminated:
            reason_counts[final_state.reason] += 1
            eliminated_count += 1
        else:
            states.append(final_state)
    ranked = rank_survivors(states, sqrt_n)

    generated = len(candidates)
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
        "rule_x_unresolved": all_reason_counts["rule_x_candidate_unresolved"]
        + all_reason_counts["rule_x_cofactor_unresolved"],
        "resolved_survivors": all_reason_counts["survived"],
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

    print(
        "case_id,bits,generated,post_wheel,pgs_rule_x_rejected,"
        "rule_x_unresolved,resolved_survivors,survivors,"
        "computation_displacement,pgs_reduction"
    )
    for row in summaries:
        post_wheel = (
            int(row["generated"])
            - int(row["balance_rejected"])
            - int(row["wheel_rejected"])
        )
        pgs_rule_rejected = int(row["pgs_chamber_rejected"]) + int(row["rule_x_rejected"])
        pgs_reduction = pgs_rule_rejected / post_wheel if post_wheel else 0.0
        print(
            f"{row['case_id']},{row['bits']},{row['generated']},{post_wheel},"
            f"{pgs_rule_rejected},{row['rule_x_unresolved']},"
            f"{row['resolved_survivors']},{row['survivors']},"
            f"{row['computation_displacement']},"
            f"{pgs_reduction:.6f}"
        )
    print(f"wrote {SUMMARY_PATH}")
    print(f"wrote {SURVIVOR_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
