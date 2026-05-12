#!/usr/bin/env python3
"""Streaming probe for PGS chain traversal through a modulus link.

The anchor is the PGS prime chain, not a classical estimate and not a
modulus-sized interval.

The law chain is:

1. start from a known locked prime endpoint;
2. advance by the repository PGS next-endpoint rule;
3. add each endpoint to the traversed chain state;
4. floor-transport the endpoint through the modulus;
5. require the transported endpoint to already be traversed;
6. require reciprocal floor closure;
7. require zero modulus-link residual.

If the lock chain does not close inside the step budget, the probe raises an
explicit unresolved state.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from z_band_prime_predictor.simple_pgs_generator import emit_record


CHAIN_STEP_BUDGET = 4096
PGS_CANDIDATE_BOUND = 4096


@dataclass(frozen=True)
class ScaleCase:
    """One deterministic semiprime case with a PGS chain seed."""

    label: str
    n: int
    seed: int
    expected_q: int
    expected_p: int


@dataclass(frozen=True)
class WalkResult:
    """Summary of one PGS chain modulus-link walk."""

    n: int
    seed: int
    q: int
    p: int
    chain_steps: int
    locked_endpoint_count: int
    skipped_floor_closures: int
    stop_reason: str


SCALE_CASES = (
    ScaleCase("toy_35", 35, 5, 7, 5),
    ScaleCase("small_77", 77, 5, 11, 7),
    ScaleCase("small_143", 143, 7, 13, 11),
    ScaleCase("small_221", 221, 11, 17, 13),
    ScaleCase("medium_899", 899, 23, 31, 29),
    ScaleCase("large_10403", 10403, 97, 103, 101),
    ScaleCase("large_1022117", 1022117, 997, 1013, 1009),
    ScaleCase("wide_control_15251", 15251, 97, 151, 101),
)


def modulus_link_residual(modulus: int, left_endpoint: int, right_endpoint: int) -> int:
    """Return the modulus-link residual for two chain endpoints."""
    return modulus - left_endpoint * right_endpoint


def reciprocal_floor_closes(modulus: int, endpoint: int, transported: int) -> bool:
    """Return True when floor transport closes in both endpoint directions."""
    if transported < 2:
        return False
    return modulus // transported == endpoint


def pgs_next_endpoint(endpoint: int) -> int:
    """Advance one step on the PGS prime chain."""
    return int(emit_record(endpoint, candidate_bound=PGS_CANDIDATE_BOUND)["q"])


def recursive_chain_modulus_lock(
    modulus: int,
    seed: int,
    step_budget: int = CHAIN_STEP_BUDGET,
) -> WalkResult:
    """Traverse the PGS chain until the modulus link closes on two endpoints."""
    if modulus < 4:
        raise ValueError("modulus must be at least 4")
    if seed < 2:
        raise ValueError("seed must be at least 2")
    if step_budget < 1:
        raise ValueError("step_budget must be positive")

    current = int(seed)
    locked_endpoints: set[int] = {current}
    skipped_floor_closures = 0

    for step in range(1, step_budget + 1):
        current = pgs_next_endpoint(current)
        locked_endpoints.add(current)

        transported = modulus // current
        if transported not in locked_endpoints:
            continue
        if not reciprocal_floor_closes(modulus, current, transported):
            continue

        q = max(current, transported)
        p = min(current, transported)
        if modulus_link_residual(modulus, p, q) != 0:
            skipped_floor_closures += 1
            continue

        return WalkResult(
            n=modulus,
            seed=seed,
            q=q,
            p=p,
            chain_steps=step,
            locked_endpoint_count=len(locked_endpoints),
            skipped_floor_closures=skipped_floor_closures,
            stop_reason="modulus_link_zero_locked",
        )

    raise RuntimeError("PGS chain modulus link did not resolve inside the step budget")


def run_scale_probe(cases: tuple[ScaleCase, ...] = SCALE_CASES) -> tuple[WalkResult, ...]:
    """Run all scale cases through the PGS chain modulus-link walk."""
    return tuple(recursive_chain_modulus_lock(case.n, case.seed) for case in cases)


def main() -> int:
    """Run the scale probe and print deterministic results."""
    print("PGS chain modulus-link streaming probe")
    print("inference_rule: PGS endpoint chain plus modulus-link zero lock")
    print("classical_anchor: none")
    print("interval_table: none")
    print(f"chain_step_budget: {CHAIN_STEP_BUDGET}")
    print(f"pgs_candidate_bound: {PGS_CANDIDATE_BOUND}")
    print()
    print(
        "case,n,seed,selected_q,selected_p,chain_steps,locked_endpoints,"
        "skipped_floor_closures,audit_match,stop_reason,inference_seconds"
    )

    for case in SCALE_CASES:
        walk_start = perf_counter()
        result = recursive_chain_modulus_lock(case.n, case.seed)
        walk_elapsed = perf_counter() - walk_start
        audit_match = result.q == case.expected_q and result.p == case.expected_p
        print(
            f"{case.label},{result.n},{result.seed},{result.q},{result.p},"
            f"{result.chain_steps},{result.locked_endpoint_count},"
            f"{result.skipped_floor_closures},{audit_match},"
            f"{result.stop_reason},{walk_elapsed:.6f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
