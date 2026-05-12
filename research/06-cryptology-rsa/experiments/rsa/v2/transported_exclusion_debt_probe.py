#!/usr/bin/env python3
"""Emit public transported exclusion-debt rows for RSA v2 certificates."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
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


RULE_ID = "transported_exclusion_debt_v1"
DEFAULT_MEASURED_ROWS = 256
DEFAULT_RECURSIVE_DEPTH = 4


@dataclass(frozen=True)
class DebtFields:
    """One public GWR/NLSC exclusion-debt measurement."""

    prefix_debt: int
    suffix_debt: int
    debt: int
    transport_reset_image: gmpy2.mpz
    transport_deadline_image: gmpy2.mpz
    transport_width: int
    balance: int


@dataclass(frozen=True)
class LedgerFields:
    """One public transported GWR/NLSC exclusion-ledger measurement."""

    source_carrier_value: gmpy2.mpz
    source_transport_carrier_image: gmpy2.mpz
    transported_prefix_lo: gmpy2.mpz
    transported_prefix_hi: gmpy2.mpz
    transported_suffix_lo: gmpy2.mpz
    transported_suffix_hi: gmpy2.mpz
    induced_carrier_value: gmpy2.mpz | None
    induced_lower_threat_value: gmpy2.mpz | None
    induced_carrier_in_prefix_zone: bool
    induced_carrier_in_suffix_zone: bool
    induced_threat_before_transported_deadline: bool
    induced_threat_in_committed_zone: bool
    ledger_prefix_elimination: bool
    ledger_suffix_elimination: bool
    ledger_threat_ceiling_elimination: bool
    ledger_eliminated: bool
    ledger_survivor: bool


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


def deadline_offset(certificate: PGSCertificate) -> int:
    """Return the public reset-deadline offset from the certificate anchor."""
    if certificate.reset_deadline_value is None:
        raise ValueError("certificate missing reset_deadline_value")
    return int(certificate.reset_deadline_value - certificate.anchor)


def debt_fields(n_value: gmpy2.mpz, certificate: PGSCertificate) -> DebtFields:
    """Return transported exclusion-debt fields for one public certificate."""
    if certificate.lock_carrier_offset is None or certificate.lock_carrier_d is None:
        raise ValueError("certificate missing carrier lock fields")
    if certificate.reset_deadline_value is None:
        raise ValueError("certificate missing reset_deadline_value")

    carrier_offset = int(certificate.lock_carrier_offset)
    carrier_d = int(certificate.lock_carrier_d)
    reset_deadline_offset = deadline_offset(certificate)
    prefix_debt = max(0, carrier_offset - 1) * max(0, carrier_d - 2)
    suffix_debt = max(0, reset_deadline_offset - carrier_offset) * max(0, carrier_d - 3)
    debt = prefix_debt + suffix_debt
    transport_reset_image = n_value // certificate.reset_endpoint
    transport_deadline_image = n_value // certificate.reset_deadline_value
    transport_width = int(transport_reset_image - transport_deadline_image)
    balance = transport_width - debt
    return DebtFields(
        prefix_debt=prefix_debt,
        suffix_debt=suffix_debt,
        debt=debt,
        transport_reset_image=transport_reset_image,
        transport_deadline_image=transport_deadline_image,
        transport_width=transport_width,
        balance=balance,
    )


def carrier_value(certificate: PGSCertificate) -> gmpy2.mpz:
    """Return the public selected carrier coordinate for one certificate."""
    if certificate.carrier_w is not None:
        return certificate.carrier_w
    if certificate.lock_carrier_offset is None:
        raise ValueError("certificate missing carrier coordinate")
    return certificate.anchor + certificate.lock_carrier_offset


def lower_threat_value(certificate: PGSCertificate) -> gmpy2.mpz | None:
    """Return the first later lower-divisor threat coordinate, when present."""
    if certificate.lower_d_threat_offset is None:
        return None
    return certificate.anchor + certificate.lower_d_threat_offset


def in_closed_interval(value: gmpy2.mpz, left: gmpy2.mpz, right: gmpy2.mpz) -> bool:
    """Return whether one coordinate is inside the closed interval."""
    lo = min(left, right)
    hi = max(left, right)
    return lo <= value <= hi


def ledger_fields(
    n_value: gmpy2.mpz,
    source_certificate: PGSCertificate,
    induced_certificate: PGSCertificate | None,
    source_debt: DebtFields,
) -> LedgerFields:
    """Return transported exclusion-ledger fields for one public certificate pair."""
    if source_certificate.lock_carrier_d is None:
        raise ValueError("source certificate missing lock carrier divisor count")

    source_carrier_value = carrier_value(source_certificate)
    source_transport_carrier_image = n_value // source_carrier_value
    transported_prefix_lo = source_debt.transport_reset_image
    transported_prefix_hi = source_transport_carrier_image
    transported_suffix_lo = source_debt.transport_deadline_image
    transported_suffix_hi = source_debt.transport_reset_image

    if induced_certificate is None or induced_certificate.lock_carrier_d is None:
        return LedgerFields(
            source_carrier_value=source_carrier_value,
            source_transport_carrier_image=source_transport_carrier_image,
            transported_prefix_lo=transported_prefix_lo,
            transported_prefix_hi=transported_prefix_hi,
            transported_suffix_lo=transported_suffix_lo,
            transported_suffix_hi=transported_suffix_hi,
            induced_carrier_value=None,
            induced_lower_threat_value=None,
            induced_carrier_in_prefix_zone=False,
            induced_carrier_in_suffix_zone=False,
            induced_threat_before_transported_deadline=False,
            induced_threat_in_committed_zone=False,
            ledger_prefix_elimination=False,
            ledger_suffix_elimination=False,
            ledger_threat_ceiling_elimination=False,
            ledger_eliminated=False,
            ledger_survivor=False,
        )

    induced_carrier_value = carrier_value(induced_certificate)
    induced_threat_value = lower_threat_value(induced_certificate)
    in_prefix = in_closed_interval(
        induced_carrier_value,
        transported_prefix_lo,
        transported_prefix_hi,
    )
    in_suffix = in_closed_interval(
        induced_carrier_value,
        transported_suffix_lo,
        transported_suffix_hi,
    )
    prefix_elimination = (
        in_prefix
        and induced_certificate.lock_carrier_d <= source_certificate.lock_carrier_d
    )
    suffix_elimination = (
        in_suffix
        and induced_certificate.lock_carrier_d < source_certificate.lock_carrier_d
    )
    threat_before_deadline = (
        induced_threat_value is not None
        and induced_threat_value < source_debt.transport_deadline_image
    )
    threat_in_committed_zone = (
        induced_threat_value is not None
        and in_closed_interval(
            induced_threat_value,
            transported_suffix_lo,
            transported_suffix_hi,
        )
    )
    threat_ceiling_elimination = (
        (threat_before_deadline or threat_in_committed_zone)
        and induced_certificate.lock_carrier_d <= source_certificate.lock_carrier_d
    )
    eliminated = prefix_elimination or suffix_elimination or threat_ceiling_elimination
    return LedgerFields(
        source_carrier_value=source_carrier_value,
        source_transport_carrier_image=source_transport_carrier_image,
        transported_prefix_lo=transported_prefix_lo,
        transported_prefix_hi=transported_prefix_hi,
        transported_suffix_lo=transported_suffix_lo,
        transported_suffix_hi=transported_suffix_hi,
        induced_carrier_value=induced_carrier_value,
        induced_lower_threat_value=induced_threat_value,
        induced_carrier_in_prefix_zone=in_prefix,
        induced_carrier_in_suffix_zone=in_suffix,
        induced_threat_before_transported_deadline=threat_before_deadline,
        induced_threat_in_committed_zone=threat_in_committed_zone,
        ledger_prefix_elimination=prefix_elimination,
        ledger_suffix_elimination=suffix_elimination,
        ledger_threat_ceiling_elimination=threat_ceiling_elimination,
        ledger_eliminated=eliminated,
        ledger_survivor=not eliminated,
    )


def phase(value: int) -> str:
    """Return the sign phase for one transported debt balance."""
    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def opposite_anchor_for(n_value: gmpy2.mpz, certificate: PGSCertificate) -> gmpy2.mpz | None:
    """Return the public opposite-side anchor induced by transported reset image."""
    image = n_value // certificate.reset_endpoint
    return previous_endpoint(image)


def next_lower_anchor_for(
    n_value: gmpy2.mpz,
    upper_certificate: PGSCertificate | None,
) -> gmpy2.mpz | None:
    """Return the next lower anchor induced by the opposite reset image."""
    if upper_certificate is None:
        return None
    transported_lower = n_value // upper_certificate.reset_endpoint
    lower_endpoint = previous_endpoint(transported_lower)
    if lower_endpoint is None:
        return None
    return previous_endpoint(lower_endpoint - 1)


def public_row(
    case: LadderCase,
    source_certificate: PGSCertificate,
    previous_source_balance: int | None,
) -> dict[str, object]:
    """Return one public transported exclusion-debt sidecar row."""
    source_debt = debt_fields(case.n, source_certificate)
    induced_anchor = opposite_anchor_for(case.n, source_certificate)
    induced_certificate = None if induced_anchor is None else pgs_certificate(induced_anchor)
    induced_debt = None if induced_certificate is None else debt_fields(case.n, induced_certificate)
    source_ledger = ledger_fields(
        case.n,
        source_certificate,
        induced_certificate,
        source_debt,
    )
    next_lower_anchor = next_lower_anchor_for(case.n, induced_certificate)
    prior_anchor = previous_endpoint(source_certificate.anchor - 1)

    balance_delta = None if induced_debt is None else source_debt.balance - induced_debt.balance
    width_expansion = (
        None
        if induced_debt is None
        else induced_debt.transport_width - source_debt.transport_width
    )
    debt_contraction = (
        None
        if induced_debt is None
        else source_debt.debt - induced_debt.debt
    )
    balance_step_delta = (
        None
        if previous_source_balance is None
        else source_debt.balance - previous_source_balance
    )
    fixed_cycle = (
        induced_certificate is not None
        and next_lower_anchor is not None
        and next_lower_anchor == source_certificate.anchor
    )
    local_descent = (
        prior_anchor is not None
        and next_lower_anchor is not None
        and next_lower_anchor == prior_anchor
    )
    positive_debt_shock = (
        balance_step_delta is not None
        and balance_step_delta > 0
    )
    nonlocal_debt_shock = positive_debt_shock and not local_descent
    local_width_debt_signal = (
        local_descent
        and width_expansion is not None
        and debt_contraction is not None
        and width_expansion > debt_contraction
    )

    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "source_anchor": str(source_certificate.anchor),
        "source_reset_endpoint": str(source_certificate.reset_endpoint),
        "source_reset_deadline_value": str(source_certificate.reset_deadline_value),
        "source_reset_deadline_offset": deadline_offset(source_certificate),
        "source_lock_carrier_offset": source_certificate.lock_carrier_offset,
        "source_lock_carrier_d": source_certificate.lock_carrier_d,
        "source_prefix_debt": source_debt.prefix_debt,
        "source_suffix_debt": source_debt.suffix_debt,
        "source_debt": source_debt.debt,
        "source_transport_reset_image": str(source_debt.transport_reset_image),
        "source_transport_deadline_image": str(source_debt.transport_deadline_image),
        "source_transport_width": source_debt.transport_width,
        "source_balance": source_debt.balance,
        "source_balance_phase": phase(source_debt.balance),
        "source_balance_step_delta": balance_step_delta,
        "source_carrier_value": str(source_ledger.source_carrier_value),
        "source_transport_carrier_image": str(source_ledger.source_transport_carrier_image),
        "transported_prefix_lo": str(source_ledger.transported_prefix_lo),
        "transported_prefix_hi": str(source_ledger.transported_prefix_hi),
        "transported_suffix_lo": str(source_ledger.transported_suffix_lo),
        "transported_suffix_hi": str(source_ledger.transported_suffix_hi),
        "induced_anchor": None if induced_anchor is None else str(induced_anchor),
        "induced_reset_endpoint": (
            None if induced_certificate is None else str(induced_certificate.reset_endpoint)
        ),
        "induced_reset_deadline_value": (
            None if induced_certificate is None else str(induced_certificate.reset_deadline_value)
        ),
        "induced_lock_carrier_offset": (
            None if induced_certificate is None else induced_certificate.lock_carrier_offset
        ),
        "induced_lock_carrier_d": (
            None if induced_certificate is None else induced_certificate.lock_carrier_d
        ),
        "induced_debt": None if induced_debt is None else induced_debt.debt,
        "induced_transport_width": (
            None if induced_debt is None else induced_debt.transport_width
        ),
        "induced_balance": None if induced_debt is None else induced_debt.balance,
        "induced_balance_phase": None if induced_debt is None else phase(induced_debt.balance),
        "induced_carrier_value": (
            None
            if source_ledger.induced_carrier_value is None
            else str(source_ledger.induced_carrier_value)
        ),
        "induced_lower_threat_value": (
            None
            if source_ledger.induced_lower_threat_value is None
            else str(source_ledger.induced_lower_threat_value)
        ),
        "induced_carrier_in_prefix_zone": source_ledger.induced_carrier_in_prefix_zone,
        "induced_carrier_in_suffix_zone": source_ledger.induced_carrier_in_suffix_zone,
        "induced_threat_before_transported_deadline": (
            source_ledger.induced_threat_before_transported_deadline
        ),
        "induced_threat_in_committed_zone": source_ledger.induced_threat_in_committed_zone,
        "balance_delta": balance_delta,
        "balance_delta_abs": None if balance_delta is None else abs(balance_delta),
        "width_expansion": width_expansion,
        "debt_contraction": debt_contraction,
        "next_lower_anchor": None if next_lower_anchor is None else str(next_lower_anchor),
        "fixed_cycle": fixed_cycle,
        "local_descent_collapse": local_descent,
        "positive_debt_shock": positive_debt_shock,
        "nonlocal_debt_shock": nonlocal_debt_shock,
        "local_width_debt_signal": local_width_debt_signal,
        "ledger_prefix_elimination": source_ledger.ledger_prefix_elimination,
        "ledger_suffix_elimination": source_ledger.ledger_suffix_elimination,
        "ledger_threat_ceiling_elimination": source_ledger.ledger_threat_ceiling_elimination,
        "ledger_eliminated": source_ledger.ledger_eliminated,
        "ledger_survivor": source_ledger.ledger_survivor,
    }


def annotate_frontier_state(row: dict[str, object], seen_induced_anchors: set[str]) -> None:
    """Attach public frontier novelty fields to one sidecar row."""
    induced_anchor = row["induced_anchor"]
    stale_state = induced_anchor is None or str(induced_anchor) in seen_induced_anchors
    row["frontier_new_transport_state"] = not stale_state
    row["ledger_stale_transport_state"] = stale_state
    row["ledger_effective_survivor"] = (
        row["ledger_survivor"] and row["frontier_new_transport_state"]
    )
    if induced_anchor is not None:
        seen_induced_anchors.add(str(induced_anchor))


def case_rows(case: LadderCase, measured_rows: int) -> list[dict[str, object]]:
    """Return public exclusion-debt rows for one modulus case."""
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []
    rows: list[dict[str, object]] = []
    previous_balance: int | None = None
    seen_induced_anchors: set[str] = set()
    for anchor in prior_endpoint_chain(first_anchor, measured_rows):
        certificate = pgs_certificate(anchor)
        if certificate is None:
            continue
        row = public_row(case, certificate, previous_balance)
        annotate_frontier_state(row, seen_induced_anchors)
        previous_balance = int(row["source_balance"])
        rows.append(row)
    return rows


def recursive_case_rows(
    case: LadderCase,
    measured_rows: int,
    recursive_depth: int,
) -> list[dict[str, object]]:
    """Return recursive public exclusion-ledger rows for one modulus case."""
    if recursive_depth < 1:
        return []
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []

    source_anchors = prior_endpoint_chain(first_anchor, measured_rows)
    seen_induced_anchors: set[str] = set()
    seen_source_anchors: set[str] = set()
    rows: list[dict[str, object]] = []

    for depth in range(recursive_depth):
        layer_source_keys = {str(anchor) for anchor in source_anchors}
        seen_source_anchors.update(layer_source_keys)
        next_anchors: list[gmpy2.mpz] = []

        for anchor in source_anchors:
            certificate = pgs_certificate(anchor)
            if certificate is None:
                continue
            row = public_row(case, certificate, None)
            annotate_frontier_state(row, seen_induced_anchors)
            induced_anchor = row["induced_anchor"]
            cycle_state = (
                induced_anchor is not None
                and str(induced_anchor) in seen_source_anchors
            )
            row["recursion_depth"] = depth
            row["ledger_recursive_cycle_state"] = cycle_state
            row["ledger_recursive_survivor"] = (
                row["ledger_effective_survivor"] and not cycle_state
            )
            rows.append(row)
            if row["ledger_recursive_survivor"] and induced_anchor is not None:
                next_anchors.append(gmpy2.mpz(str(induced_anchor)))

        if not next_anchors:
            break
        source_anchors = next_anchors

    return rows


def summarize_recursive(
    recursive_rows: list[dict[str, object]],
    recursive_depth: int,
) -> dict[str, object]:
    """Return recursive transported-ledger contraction counts."""
    layer_summaries = []
    depths = sorted({int(row["recursion_depth"]) for row in recursive_rows})
    for depth in depths:
        layer_rows = [row for row in recursive_rows if int(row["recursion_depth"]) == depth]
        layer_summaries.append(
            {
                "recursion_depth": depth,
                "row_count": len(layer_rows),
                "ledger_eliminated_count": sum(
                    1 for row in layer_rows if row["ledger_eliminated"]
                ),
                "ledger_stale_transport_state_count": sum(
                    1 for row in layer_rows if row["ledger_stale_transport_state"]
                ),
                "ledger_recursive_cycle_state_count": sum(
                    1 for row in layer_rows if row["ledger_recursive_cycle_state"]
                ),
                "ledger_recursive_survivor_count": sum(
                    1 for row in layer_rows if row["ledger_recursive_survivor"]
                ),
            }
        )
    case_layer_summaries = []
    case_ids = sorted({str(row["case_id"]) for row in recursive_rows})
    for case_id in case_ids:
        case_rows = [row for row in recursive_rows if str(row["case_id"]) == case_id]
        for depth in sorted({int(row["recursion_depth"]) for row in case_rows}):
            layer_rows = [
                row
                for row in case_rows
                if int(row["recursion_depth"]) == depth
            ]
            case_layer_summaries.append(
                {
                    "case_id": case_id,
                    "recursion_depth": depth,
                    "row_count": len(layer_rows),
                    "ledger_eliminated_count": sum(
                        1 for row in layer_rows if row["ledger_eliminated"]
                    ),
                    "ledger_stale_transport_state_count": sum(
                        1 for row in layer_rows if row["ledger_stale_transport_state"]
                    ),
                    "ledger_recursive_cycle_state_count": sum(
                        1 for row in layer_rows if row["ledger_recursive_cycle_state"]
                    ),
                    "ledger_recursive_survivor_count": sum(
                        1 for row in layer_rows if row["ledger_recursive_survivor"]
                    ),
                }
            )

    return {
        "recursive_depth_limit": recursive_depth,
        "recursive_row_count": len(recursive_rows),
        "recursive_layer_count": len(layer_summaries),
        "recursive_layer_summaries": layer_summaries,
        "recursive_case_layer_summaries": case_layer_summaries,
        "recursive_final_survivor_count": (
            0
            if not layer_summaries
            else int(layer_summaries[-1]["ledger_recursive_survivor_count"])
        ),
    }


def summarize(
    rows: list[dict[str, object]],
    measured_rows: int,
    recursive_rows: list[dict[str, object]],
    recursive_depth: int,
) -> dict[str, object]:
    """Return falsification-oriented summary counts for sidecar rows."""
    cases = sorted({str(row["case_id"]) for row in rows})
    phase_change_count = 0
    previous_by_case: dict[str, str] = {}
    for row in rows:
        case_id = str(row["case_id"])
        current_phase = str(row["source_balance_phase"])
        previous_phase = previous_by_case.get(case_id)
        if previous_phase is not None and previous_phase != current_phase:
            phase_change_count += 1
        previous_by_case[case_id] = current_phase

    broad_phase_counts: dict[str, int] = {}
    for row in rows:
        key = str(row["source_balance_phase"])
        broad_phase_counts[key] = broad_phase_counts.get(key, 0) + 1
    case_summaries = []
    for case_id in cases:
        case_rows = [row for row in rows if row["case_id"] == case_id]
        case_summaries.append(
            {
                "case_id": case_id,
                "row_count": len(case_rows),
                "ledger_prefix_elimination_count": sum(
                    1 for row in case_rows if row["ledger_prefix_elimination"]
                ),
                "ledger_suffix_elimination_count": sum(
                    1 for row in case_rows if row["ledger_suffix_elimination"]
                ),
                "ledger_threat_ceiling_elimination_count": sum(
                    1 for row in case_rows if row["ledger_threat_ceiling_elimination"]
                ),
                "ledger_eliminated_count": sum(
                    1 for row in case_rows if row["ledger_eliminated"]
                ),
                "ledger_stale_transport_state_count": sum(
                    1 for row in case_rows if row["ledger_stale_transport_state"]
                ),
                "ledger_survivor_count": sum(
                    1 for row in case_rows if row["ledger_survivor"]
                ),
                "ledger_effective_survivor_count": sum(
                    1 for row in case_rows if row["ledger_effective_survivor"]
                ),
            }
        )

    summary = {
        "rule_id": RULE_ID,
        "measured_rows_per_case": measured_rows,
        "case_count": len(cases),
        "cases": cases,
        "case_summaries": case_summaries,
        "row_count": len(rows),
        "phase_counts": broad_phase_counts,
        "phase_change_count": phase_change_count,
        "zero_balance_count": sum(1 for row in rows if row["source_balance"] == 0),
        "positive_debt_shock_count": sum(1 for row in rows if row["positive_debt_shock"]),
        "nonlocal_debt_shock_count": sum(1 for row in rows if row["nonlocal_debt_shock"]),
        "local_width_debt_signal_count": sum(
            1 for row in rows if row["local_width_debt_signal"]
        ),
        "fixed_cycle_count": sum(1 for row in rows if row["fixed_cycle"]),
        "local_descent_collapse_count": sum(
            1 for row in rows if row["local_descent_collapse"]
        ),
        "missing_induced_certificate_count": sum(
            1 for row in rows if row["induced_anchor"] is None
        ),
        "ledger_prefix_elimination_count": sum(
            1 for row in rows if row["ledger_prefix_elimination"]
        ),
        "ledger_suffix_elimination_count": sum(
            1 for row in rows if row["ledger_suffix_elimination"]
        ),
        "ledger_threat_ceiling_elimination_count": sum(
            1 for row in rows if row["ledger_threat_ceiling_elimination"]
        ),
        "ledger_eliminated_count": sum(1 for row in rows if row["ledger_eliminated"]),
        "ledger_stale_transport_state_count": sum(
            1 for row in rows if row["ledger_stale_transport_state"]
        ),
        "ledger_survivor_count": sum(1 for row in rows if row["ledger_survivor"]),
        "ledger_effective_survivor_count": sum(
            1 for row in rows if row["ledger_effective_survivor"]
        ),
    }
    summary.update(summarize_recursive(recursive_rows, recursive_depth))
    return summary


def run_probe(
    cases_path: Path,
    measured_rows: int,
    recursive_depth: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the public transported exclusion-debt probe."""
    cases = load_cases(cases_path)
    rows: list[dict[str, object]] = []
    recursive_rows: list[dict[str, object]] = []
    for case in cases:
        rows.extend(case_rows(case, measured_rows))
        recursive_rows.extend(recursive_case_rows(case, measured_rows, recursive_depth))
    return rows, recursive_rows, summarize(rows, measured_rows, recursive_rows, recursive_depth)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Emit public transported exclusion-debt rows.")
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
        default=THIS_DIR / "output" / "transported_exclusion_debt",
        help="Directory for debt_rows.jsonl, recursive_rows.jsonl, and summary.json.",
    )
    parser.add_argument(
        "--recursive-depth",
        type=int,
        default=DEFAULT_RECURSIVE_DEPTH,
        help="Measurement-only recursive transported-ledger depth limit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, recursive_rows, summary = run_probe(
        args.cases,
        args.measured_rows,
        args.recursive_depth,
    )
    write_jsonl(args.output_dir / "debt_rows.jsonl", rows)
    write_jsonl(args.output_dir / "recursive_rows.jsonl", recursive_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
