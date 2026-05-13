#!/usr/bin/env python3
"""Run OECC_RECURSIVE_V2 beside the linear OECC baseline."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from run_experiment import (  # noqa: E402
    CertificateCache,
    CertificatePair,
    DiagnosticCounters,
    LadderCase,
    PGSCertificate,
    PreviousEndpointCache,
    SegmentCache,
    balance_bounds,
    baseline_cost_row,
    certificate_at,
    endpoint_chain_step_closure,
    endpoint_chain_transport_coordinate,
    load_cases,
    make_diagnostics,
    pair_to_json,
    previous_endpoint_at,
    reciprocal_floor,
    result_row,
    summary_row,
    write_json,
    write_jsonl,
)


IMPLEMENTATION_LABEL = "OECC_RECURSIVE_V2"
UNRESOLVED_BY_RECURSIVE_CYCLE = "unresolved_by_recursive_cycle"
UNRESOLVED_BY_RECURSIVE_BALANCE_BOUNDARY = "unresolved_by_recursive_balance_boundary"


@dataclass(frozen=True)
class RecursiveOpenState:
    """One unresolved recursive step with the next lower anchor."""

    next_anchor: gmpy2.mpz | None
    status: str


@dataclass(frozen=True)
class RecursiveRun:
    """One OECC_RECURSIVE_V2 case result."""

    pair: CertificatePair | None
    closure_status: str
    recursion_steps: int
    visited_anchor_count: int
    elapsed_ns: int
    diagnostics: DiagnosticCounters


def previous_lower_anchor(
    anchor: gmpy2.mpz,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> gmpy2.mpz | None:
    """Return the prior public lower endpoint before one anchor."""
    return previous_endpoint_at(anchor, previous_endpoint_cache, segment_cache, diagnostics)


def recursive_jump_anchor(
    n_value: gmpy2.mpz,
    lower_balance: gmpy2.mpz,
    anchor: gmpy2.mpz,
    upper: PGSCertificate,
    corrected_lower_anchor: gmpy2.mpz | None,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> gmpy2.mpz | None:
    """Return the greatest public recursive jump anchor below the current anchor."""
    candidates: list[gmpy2.mpz | None] = [corrected_lower_anchor]
    if corrected_lower_anchor is not None:
        candidates.append(
            previous_endpoint_at(
                corrected_lower_anchor,
                previous_endpoint_cache,
                segment_cache,
                diagnostics,
            )
        )
    if upper.reset_deadline_value is not None:
        candidates.append(
            previous_endpoint_at(
                reciprocal_floor(n_value, upper.reset_deadline_value),
                previous_endpoint_cache,
                segment_cache,
                diagnostics,
            )
        )
    candidates.append(
        previous_endpoint_at(
            reciprocal_floor(n_value, upper.reset_endpoint),
            previous_endpoint_cache,
            segment_cache,
            diagnostics,
        )
    )
    kept = [
        candidate
        for candidate in candidates
        if candidate is not None and lower_balance <= candidate < anchor
    ]
    if not kept:
        return previous_lower_anchor(anchor, previous_endpoint_cache, segment_cache, diagnostics)
    return max(kept)


def recursive_step(
    case: LadderCase,
    center: gmpy2.mpz,
    lower_balance: gmpy2.mpz,
    upper_balance: gmpy2.mpz,
    anchor: gmpy2.mpz,
    steps: int,
    certificate_cache: CertificateCache,
    previous_endpoint_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
    diagnostics: DiagnosticCounters,
) -> CertificatePair | RecursiveOpenState:
    """Resolve or advance one recursive lower-anchor state."""
    lower = certificate_at(anchor, certificate_cache, diagnostics)
    if lower is None:
        return RecursiveOpenState(
            previous_lower_anchor(anchor, previous_endpoint_cache, segment_cache, diagnostics),
            "open_by_missing_lower_certificate",
        )

    pair = endpoint_chain_step_closure(
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
        return pair

    transport_coordinate = endpoint_chain_transport_coordinate(lower, center)
    transported_upper = reciprocal_floor(case.n, transport_coordinate)
    if transported_upper < center or transported_upper > upper_balance:
        return RecursiveOpenState(
            previous_lower_anchor(anchor, previous_endpoint_cache, segment_cache, diagnostics),
            "open_by_upper_transport_outside_balance",
        )

    upper_anchor = previous_endpoint_at(
        transported_upper,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    upper = None if upper_anchor is None else certificate_at(upper_anchor, certificate_cache, diagnostics)
    if upper is None:
        return RecursiveOpenState(
            previous_lower_anchor(anchor, previous_endpoint_cache, segment_cache, diagnostics),
            "open_by_missing_upper_certificate",
        )

    corrected_lower_anchor = previous_endpoint_at(
        reciprocal_floor(case.n, upper.reset_endpoint),
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    return RecursiveOpenState(
        recursive_jump_anchor(
            case.n,
            lower_balance,
            anchor,
            upper,
            corrected_lower_anchor,
            previous_endpoint_cache,
            segment_cache,
            diagnostics,
        ),
        "open_by_recursive_jump",
    )


def recursive_pair(case: LadderCase) -> RecursiveRun:
    """Return one OECC_RECURSIVE_V2 side-by-side result."""
    diagnostics = make_diagnostics()
    start_ns = time.perf_counter_ns()
    center = gmpy2.isqrt(case.n)
    lower_balance, upper_balance = balance_bounds(center)
    certificate_cache: CertificateCache = {}
    previous_endpoint_cache: PreviousEndpointCache = {}
    segment_cache: SegmentCache = {}
    anchor = previous_endpoint_at(center, previous_endpoint_cache, segment_cache, diagnostics)
    visited: set[int] = set()
    steps = 0

    while anchor is not None and anchor >= lower_balance:
        anchor_key = int(anchor)
        if anchor_key in visited:
            return RecursiveRun(
                None,
                UNRESOLVED_BY_RECURSIVE_CYCLE,
                steps,
                len(visited),
                time.perf_counter_ns() - start_ns,
                diagnostics,
            )
        visited.add(anchor_key)
        state = recursive_step(
            case,
            center,
            lower_balance,
            upper_balance,
            anchor,
            steps,
            certificate_cache,
            previous_endpoint_cache,
            segment_cache,
            diagnostics,
        )
        if isinstance(state, CertificatePair):
            diagnostics["endpoint_chain_steps"] = state.endpoint_chain_steps or 0
            return RecursiveRun(
                state,
                state.closure_status,
                steps,
                len(visited),
                time.perf_counter_ns() - start_ns,
                diagnostics,
            )
        anchor = state.next_anchor
        steps += 1

    return RecursiveRun(
        None,
        UNRESOLVED_BY_RECURSIVE_BALANCE_BOUNDARY,
        steps,
        len(visited),
        time.perf_counter_ns() - start_ns,
        diagnostics,
    )


def unresolved_pair_row(case: LadderCase, run: RecursiveRun) -> dict[str, object]:
    """Return one JSON-safe unresolved recursive row."""
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "implementation_label": IMPLEMENTATION_LABEL,
        "closure_status": run.closure_status,
        "recursion_steps": run.recursion_steps,
        "visited_anchor_count": run.visited_anchor_count,
        "rule_id": IMPLEMENTATION_LABEL,
    }


def recursive_result_row(case: LadderCase, run: RecursiveRun) -> dict[str, object]:
    """Return one inference-shaped recursive result row."""
    if run.pair is None:
        return {
            "case_id": case.case_id,
            "bits": case.bits,
            "N": str(case.n),
            "status": "unresolved",
            "unresolved_reason": run.closure_status,
            "implementation_label": IMPLEMENTATION_LABEL,
            "rule_id": IMPLEMENTATION_LABEL,
        }
    row = result_row(case, run.pair)
    row["implementation_label"] = IMPLEMENTATION_LABEL
    row["rule_id"] = IMPLEMENTATION_LABEL
    return row


def recursive_pair_row(case: LadderCase, run: RecursiveRun) -> dict[str, object]:
    """Return one recursive certificate-pair sidecar row."""
    if run.pair is None:
        return unresolved_pair_row(case, run)
    row = pair_to_json(case, run.pair)
    row["implementation_label"] = IMPLEMENTATION_LABEL
    row["rule_id"] = IMPLEMENTATION_LABEL
    row["recursion_steps"] = run.recursion_steps
    row["visited_anchor_count"] = run.visited_anchor_count
    return row


def recursive_summary_row(case: LadderCase, run: RecursiveRun) -> dict[str, object]:
    """Return one recursive summary row."""
    if run.pair is None:
        return {
            "case_id": case.case_id,
            "bits": case.bits,
            "N": str(case.n),
            "implementation_label": IMPLEMENTATION_LABEL,
            "closure_status": run.closure_status,
            "recursion_steps": run.recursion_steps,
            "visited_anchor_count": run.visited_anchor_count,
            "rule_id": IMPLEMENTATION_LABEL,
        }
    row = summary_row(case, run.pair)
    row["implementation_label"] = IMPLEMENTATION_LABEL
    row["rule_id"] = IMPLEMENTATION_LABEL
    row["recursion_steps"] = run.recursion_steps
    row["visited_anchor_count"] = run.visited_anchor_count
    return row


def recursive_diagnostic_row(case: LadderCase, run: RecursiveRun) -> dict[str, object]:
    """Return one recursive diagnostic sidecar row."""
    row = baseline_cost_row(case, run.pair, run.diagnostics, run.elapsed_ns) if run.pair is not None else {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": IMPLEMENTATION_LABEL,
        "closure_status": run.closure_status,
        "endpoint_chain_steps": run.diagnostics["endpoint_chain_steps"],
        "cache_lookups": (
            run.diagnostics["previous_endpoint_lookups"]
            + run.diagnostics["certificate_lookups"]
            + run.diagnostics["divisor_segment_lookups"]
        ),
        "cache_misses": (
            run.diagnostics["previous_endpoint_calls"]
            + run.diagnostics["certificate_builds"]
            + run.diagnostics["divisor_segment_calls"]
        ),
        "cache_hit_rate": 0.0,
        "elapsed_ms": run.elapsed_ns / 1_000_000,
    }
    row["implementation_label"] = IMPLEMENTATION_LABEL
    row["rule_id"] = IMPLEMENTATION_LABEL
    row["recursion_steps"] = run.recursion_steps
    row["visited_anchor_count"] = run.visited_anchor_count
    return row


def run_cases(cases: list[LadderCase]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Run public cases through OECC_RECURSIVE_V2 sidecar inference."""
    results: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    pairs: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    for case in cases:
        run = recursive_pair(case)
        results.append(recursive_result_row(case, run))
        summaries.append(recursive_summary_row(case, run))
        pairs.append(recursive_pair_row(case, run))
        diagnostics.append(recursive_diagnostic_row(case, run))
    return results, summaries, pairs, diagnostics


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run OECC_RECURSIVE_V2 beside OECC_LINEAR_V1.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=THIS_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "recursive_v2",
        help="Directory for recursive_v2 sidecar outputs.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the recursive side-by-side experiment."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results, summaries, pairs, diagnostics = run_cases(load_cases(args.cases))
    write_jsonl(args.output_dir / "recursive_inference_rows.jsonl", results)
    write_jsonl(args.output_dir / "recursive_pair_rows.jsonl", pairs)
    write_jsonl(args.output_dir / "recursive_diagnostic_rows.jsonl", diagnostics)
    write_json(args.output_dir / "summary.json", {"cases": summaries})
    print(json.dumps({"cases": summaries}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
