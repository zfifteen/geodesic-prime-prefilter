#!/usr/bin/env python3
"""Probe local chamber-reset horizon truncation vs global endpoint-chain extension.

The probe walks the same modulus-link cases as scale_pgs_chain_modulus_link.py,
but instruments every chain step with chamber-reset certificate fields and NLSC
threat-horizon rows. It checks whether local truncation, global chain extension,
and modulus-link closure align on deterministic semiprime cases.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_predictor.gpe_nlsc_selector import (  # noqa: E402
    oracle_nlsc_selector_row,
)
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    DEFAULT_CANDIDATE_BOUND,
    pgs_chamber_reset_state_certificate,
)

CHAIN_STEP_BUDGET = 64
PGS_CANDIDATE_BOUND = 4096


@dataclass(frozen=True)
class ScaleCase:
    """One deterministic semiprime case with a PGS chain seed."""

    label: str
    n: int
    seed: int
    expected_upper_endpoint: int
    expected_lower_endpoint: int


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


LOCAL_CANDIDATE_BOUND = DEFAULT_CANDIDATE_BOUND
GLOBAL_CANDIDATE_BOUND = PGS_CANDIDATE_BOUND


@dataclass(frozen=True)
class ChamberStepRecord:
    """One instrumented chamber-reset step on the endpoint chain."""

    step_index: int
    anchor_p: int
    emitted_q: int
    gap_offset: int
    candidate_bound: int
    lock_carrier_d: int | None
    lower_d_threat_offset: int | None
    local_horizon_used: int
    local_truncation_active: bool
    local_truncation_safe: bool
    local_bound_sufficient: bool
    carrier_w: int | None
    winner_divisor_class: int | None
    nlsc_threat_horizon: int | None
    nlsc_square_ceiling_margin: int | None
    nlsc_horizon_contains_q: bool | None
    local_threat_le_nlsc_margin: bool | None
    transported_floor: int
    transported_in_locked_set: bool
    reciprocal_floor_closes: bool
    modulus_link_residual_if_pair: int | None


@dataclass(frozen=True)
class AlignmentCaseResult:
    """Alignment summary for one modulus-link walk."""

    label: str
    modulus: int
    seed: int
    expected_upper: int
    expected_lower: int
    chain_candidate_bound: int
    closure_step: int | None
    closure_upper: int | None
    closure_lower: int | None
    modulus_link_zero: bool | None
    audit_match: bool | None
    all_local_truncation_safe: bool
    all_local_bound_sufficient: bool
    all_nlsc_horizon_contains_q: bool
    d4_steps: int
    unresolved_steps: int
    skipped_floor_closures: int
    stop_reason: str
    steps: tuple[ChamberStepRecord, ...]


def chamber_certificate(
    anchor_p: int,
    candidate_bound: int,
) -> dict[str, object] | None:
    """Return one chamber-reset certificate or None when unresolved."""
    return pgs_chamber_reset_state_certificate(int(anchor_p), int(candidate_bound))


def nlsc_fields(anchor_p: int) -> tuple[int | None, int | None, int | None]:
    """Return (winner_d, threat_horizon, square_ceiling_margin) when available."""
    try:
        row = oracle_nlsc_selector_row(int(anchor_p))
    except Exception:
        return None, None, None
    return (
        row.winner_divisor_class,
        row.threat_horizon,
        row.square_ceiling_margin,
    )


def local_horizon_used(
    gap_offset: int,
    threat_offset: int | None,
    candidate_bound: int,
) -> int:
    """Return the effective local horizon consumed before emission."""
    if threat_offset is not None:
        return min(gap_offset, threat_offset)
    return min(gap_offset, candidate_bound)


def instrument_chain_walk(
    case: ScaleCase,
    candidate_bound: int = GLOBAL_CANDIDATE_BOUND,
    step_budget: int = CHAIN_STEP_BUDGET,
) -> AlignmentCaseResult:
    """Walk one modulus-link case with per-step chamber instrumentation."""
    modulus = int(case.n)
    current = int(case.seed)
    locked_endpoints: set[int] = {current}
    steps: list[ChamberStepRecord] = []
    skipped_floor_closures = 0
    closure_step: int | None = None
    closure_upper: int | None = None
    closure_lower: int | None = None
    stop_reason = "step_budget_exhausted"

    for step_index in range(1, step_budget + 1):
        cert = chamber_certificate(current, candidate_bound)
        if cert is None:
            steps.append(
                ChamberStepRecord(
                    step_index=step_index,
                    anchor_p=current,
                    emitted_q=-1,
                    gap_offset=-1,
                    candidate_bound=candidate_bound,
                    lock_carrier_d=None,
                    lower_d_threat_offset=None,
                    local_horizon_used=0,
                    local_truncation_active=False,
                    local_truncation_safe=False,
                    local_bound_sufficient=False,
                    carrier_w=None,
                    winner_divisor_class=None,
                    nlsc_threat_horizon=None,
                    nlsc_square_ceiling_margin=None,
                    nlsc_horizon_contains_q=None,
                    local_threat_le_nlsc_margin=None,
                    transported_floor=modulus // current if current else 0,
                    transported_in_locked_set=False,
                    reciprocal_floor_closes=False,
                    modulus_link_residual_if_pair=None,
                )
            )
            stop_reason = "chamber_unresolved"
            break

        gap_offset = int(cert["gap_offset"])
        threat_offset = cert.get("lower_d_threat_offset")
        threat_offset_int = None if threat_offset is None else int(threat_offset)
        emitted_q = int(cert["q"])
        lock_carrier_d = cert.get("lock_carrier_d")
        lock_carrier_d_int = None if lock_carrier_d is None else int(lock_carrier_d)
        carrier_w = cert.get("carrier_w")
        carrier_w_int = None if carrier_w is None else int(carrier_w)

        winner_d, threat_horizon, square_margin = nlsc_fields(current)
        nlsc_contains_q = None
        local_threat_le_margin = None
        if winner_d == 4 and threat_horizon is not None:
            nlsc_contains_q = emitted_q <= threat_horizon
            if square_margin is not None:
                local_threat_le_margin = (
                    threat_offset_int is None
                    or threat_offset_int <= square_margin
                )

        truncation_active = threat_offset_int is not None
        truncation_safe = threat_offset_int is None or gap_offset <= threat_offset_int
        bound_sufficient = gap_offset <= candidate_bound

        anchor_p = current
        transported = modulus // anchor_p
        transported_locked = transported in locked_endpoints
        reciprocal = reciprocal_floor_closes(modulus, anchor_p, transported)
        residual_if_pair = None
        if transported_locked and reciprocal:
            lower = min(anchor_p, transported)
            upper = max(anchor_p, transported)
            residual_if_pair = modulus_link_residual(modulus, lower, upper)

        steps.append(
            ChamberStepRecord(
                step_index=step_index,
                anchor_p=current,
                emitted_q=emitted_q,
                gap_offset=gap_offset,
                candidate_bound=candidate_bound,
                lock_carrier_d=lock_carrier_d_int,
                lower_d_threat_offset=threat_offset_int,
                local_horizon_used=local_horizon_used(
                    gap_offset,
                    threat_offset_int,
                    candidate_bound,
                ),
                local_truncation_active=truncation_active,
                local_truncation_safe=truncation_safe,
                local_bound_sufficient=bound_sufficient,
                carrier_w=carrier_w_int,
                winner_divisor_class=winner_d,
                nlsc_threat_horizon=threat_horizon,
                nlsc_square_ceiling_margin=square_margin,
                nlsc_horizon_contains_q=nlsc_contains_q,
                local_threat_le_nlsc_margin=local_threat_le_margin,
                transported_floor=transported,
                transported_in_locked_set=transported_locked,
                reciprocal_floor_closes=reciprocal,
                modulus_link_residual_if_pair=residual_if_pair,
            )
        )

        current = emitted_q
        locked_endpoints.add(current)

        if not transported_locked or not reciprocal:
            continue
        lower = min(anchor_p, transported)
        upper = max(anchor_p, transported)
        residual = modulus_link_residual(modulus, lower, upper)
        if residual != 0:
            skipped_floor_closures += 1
            continue

        closure_step = step_index
        closure_upper = upper
        closure_lower = lower
        stop_reason = "modulus_link_zero_locked"
        break

    resolved_steps = [step for step in steps if step.emitted_q > 0]
    d4_steps = sum(1 for step in resolved_steps if step.winner_divisor_class == 4)
    unresolved_steps = sum(1 for step in steps if step.emitted_q <= 0)

    all_trunc_safe = all(step.local_truncation_safe for step in resolved_steps)
    all_bound_suff = all(step.local_bound_sufficient for step in resolved_steps)
    nlsc_steps = [
        step
        for step in resolved_steps
        if step.nlsc_horizon_contains_q is not None
    ]
    all_nlsc = all(step.nlsc_horizon_contains_q for step in nlsc_steps)

    modulus_link_zero = None
    audit_match = None
    if closure_upper is not None and closure_lower is not None:
        modulus_link_zero = (
            modulus_link_residual(modulus, closure_lower, closure_upper) == 0
        )
        audit_match = (
            closure_upper == case.expected_upper_endpoint
            and closure_lower == case.expected_lower_endpoint
        )

    return AlignmentCaseResult(
        label=case.label,
        modulus=modulus,
        seed=case.seed,
        expected_upper=case.expected_upper_endpoint,
        expected_lower=case.expected_lower_endpoint,
        chain_candidate_bound=candidate_bound,
        closure_step=closure_step,
        closure_upper=closure_upper,
        closure_lower=closure_lower,
        modulus_link_zero=modulus_link_zero,
        audit_match=audit_match,
        all_local_truncation_safe=all_trunc_safe,
        all_local_bound_sufficient=all_bound_suff,
        all_nlsc_horizon_contains_q=all_nlsc,
        d4_steps=d4_steps,
        unresolved_steps=unresolved_steps,
        skipped_floor_closures=skipped_floor_closures,
        stop_reason=stop_reason,
        steps=tuple(steps),
    )


def compare_local_vs_global_bounds(case: ScaleCase) -> dict[str, object]:
    """Check whether the production local bound still closes the same modulus link."""
    global_result = instrument_chain_walk(case, candidate_bound=GLOBAL_CANDIDATE_BOUND)
    local_result = instrument_chain_walk(case, candidate_bound=LOCAL_CANDIDATE_BOUND)
    return {
        "label": case.label,
        "modulus": case.n,
        "global_bound": GLOBAL_CANDIDATE_BOUND,
        "local_bound": LOCAL_CANDIDATE_BOUND,
        "global_closure_step": global_result.closure_step,
        "local_closure_step": local_result.closure_step,
        "global_audit_match": global_result.audit_match,
        "local_audit_match": local_result.audit_match,
        "bounds_equivalent_on_case": (
            global_result.closure_upper == local_result.closure_upper
            and global_result.closure_lower == local_result.closure_lower
            and global_result.audit_match == local_result.audit_match
        ),
    }


def summarize(results: tuple[AlignmentCaseResult, ...]) -> dict[str, object]:
    """Return aggregate alignment statistics."""
    closed = [result for result in results if result.closure_step is not None]
    return {
        "case_count": len(results),
        "closed_count": len(closed),
        "audit_match_count": sum(1 for result in closed if result.audit_match),
        "all_local_truncation_safe_count": sum(
            1 for result in closed if result.all_local_truncation_safe
        ),
        "all_local_bound_sufficient_count": sum(
            1 for result in closed if result.all_local_bound_sufficient
        ),
        "all_nlsc_horizon_contains_q_count": sum(
            1 for result in closed if result.all_nlsc_horizon_contains_q
        ),
        "total_d4_steps": sum(result.d4_steps for result in closed),
        "total_skipped_floor_closures": sum(
            result.skipped_floor_closures for result in closed
        ),
        "insight": (
            "local chamber-reset truncation and global endpoint-chain extension "
            "align for modulus-link closure when every chain step satisfies "
            "gap_offset <= candidate_bound, gap_offset <= lower_d_threat_offset "
            "(when threat is active), and emitted_q <= S_+(w) on d=4 carriers."
        ),
    }


def run_probe(
    cases: tuple[ScaleCase, ...] = SCALE_CASES,
    candidate_bound: int = GLOBAL_CANDIDATE_BOUND,
    compare_bounds: bool = False,
) -> dict[str, object]:
    """Run the full alignment probe."""
    started = perf_counter()
    results = tuple(
        instrument_chain_walk(case, candidate_bound=candidate_bound)
        for case in cases
    )
    bound_comparison = None
    if compare_bounds:
        bound_comparison = tuple(compare_local_vs_global_bounds(case) for case in cases)
    elapsed = perf_counter() - started
    return {
        "probe_id": "chamber_horizon_alignment_probe_candidate_3",
        "candidate_bound": candidate_bound,
        "local_reference_bound": LOCAL_CANDIDATE_BOUND,
        "global_reference_bound": GLOBAL_CANDIDATE_BOUND,
        "compare_bounds": compare_bounds,
        "elapsed_seconds": elapsed,
        "summary": summarize(results),
        "bound_comparison": bound_comparison,
        "cases": [
            {
                **{
                    key: value
                    for key, value in asdict(result).items()
                    if key != "steps"
                },
                "steps": [asdict(step) for step in result.steps],
            }
            for result in results
        ],
    }


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Probe chamber-reset local truncation vs endpoint-chain extension.",
    )
    parser.add_argument(
        "--candidate-bound",
        type=int,
        default=GLOBAL_CANDIDATE_BOUND,
        help="Per-step chamber-reset candidate bound used on the endpoint chain.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "output" / "alignment_probe.json",
        help="JSON output path.",
    )
    parser.add_argument(
        "--compare-bounds",
        action="store_true",
        help="Also compare LOCAL_CANDIDATE_BOUND=128 vs GLOBAL_CANDIDATE_BOUND.",
    )
    args = parser.parse_args()

    payload = run_probe(
        candidate_bound=int(args.candidate_bound),
        compare_bounds=bool(args.compare_bounds),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    print("Chamber-reset / endpoint-chain horizon alignment probe (candidate 3)")
    print(f"candidate_bound: {args.candidate_bound}")
    print(
        f"closed: {summary['closed_count']}/{summary['case_count']} "
        f"audit_match: {summary['audit_match_count']}"
    )
    print(
        "local_truncation_safe: "
        f"{summary['all_local_truncation_safe_count']}/{summary['closed_count']}"
    )
    print(
        "nlsc_horizon_contains_q: "
        f"{summary['all_nlsc_horizon_contains_q_count']}/{summary['closed_count']}"
    )
    print(f"output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())