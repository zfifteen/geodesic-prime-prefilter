#!/usr/bin/env python3
"""
Diagnostic script: Compute reciprocal transport metrics for PGSPG certificates.

This is a read-only analysis tool. It does not modify any runner behavior.
It uses only data already present in survivor_rows.jsonl.

Metrics computed:
- Transported lower carrier_w relative to upper_anchor and upper_carrier_w
- Transported first lower tail point relative to upper_anchor
- Transported lower deadline value relative to upper deadline value
- Basic tightness ratios
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransportMetrics:
    case_id: str
    bits: int
    public_closure_status: str
    endpoint_chain_steps: int

    # Carrier transport
    lower_carrier_w: int
    transported_lower_carrier_w: int
    upper_anchor: int
    upper_carrier_w: int
    carrier_overshoot_above_anchor: int
    carrier_overshoot_above_upper_carrier: int

    # First tail transport
    first_lower_tail_offset: Optional[int]
    first_lower_tail_point: Optional[int]
    transported_first_lower_tail: Optional[int]
    first_tail_delta_from_upper_anchor: Optional[int]

    # Deadline transport
    lower_deadline_value: int
    transported_lower_deadline: int
    upper_deadline_value: int
    deadline_transport_error: int

    # Derived ratios
    carrier_overshoot_to_gap_ratio: Optional[float]
    first_tail_proximity_score: Optional[int]


def load_survivor_rows(path: Path) -> dict[str, dict]:
    """Return survivor rows keyed by public case id."""
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows[r["case_id"]] = r
    return rows


def compute_metrics(case_id: str, row: dict) -> TransportMetrics:
    """Return transport metrics from one survivor row."""
    N = int(row["N"])
    bits = int(row["bits"])
    status = row["public_closure_status"]
    steps = int(row.get("endpoint_chain_steps") or 0)

    # Lower
    lower_carrier_w = int(row["lower_carrier_w"])
    lower_reset_ep = int(row["lower_reset_endpoint"])
    lower_deadline = int(row["lower_reset_deadline_value"])
    lower_tail = [int(x) for x in row.get("lower_tail_after_reset_offsets", []) or []]

    # Upper
    upper_anchor = int(row["upper_anchor"])
    upper_carrier_w = int(row["upper_carrier_w"])
    upper_deadline = int(row["upper_reset_deadline_value"])

    # Transports
    trans_carrier = N // lower_carrier_w
    trans_first_tail = N // (lower_reset_ep + lower_tail[0]) if lower_tail else None
    trans_deadline = N // lower_deadline

    # Deltas
    carrier_above_anchor = trans_carrier - upper_anchor
    carrier_above_upper_carrier = trans_carrier - upper_carrier_w
    first_tail_delta = (trans_first_tail - upper_anchor) if trans_first_tail is not None else None
    deadline_error = trans_deadline - upper_deadline

    # Ratios (avoid division by zero)
    gap_offset = int(row["lower_gap_offset"])
    carrier_ratio = round(carrier_above_anchor / gap_offset, 2) if gap_offset > 0 else None

    return TransportMetrics(
        case_id=case_id,
        bits=bits,
        public_closure_status=status,
        endpoint_chain_steps=steps,
        lower_carrier_w=lower_carrier_w,
        transported_lower_carrier_w=trans_carrier,
        upper_anchor=upper_anchor,
        upper_carrier_w=upper_carrier_w,
        carrier_overshoot_above_anchor=carrier_above_anchor,
        carrier_overshoot_above_upper_carrier=carrier_above_upper_carrier,
        first_lower_tail_offset=lower_tail[0] if lower_tail else None,
        first_lower_tail_point=lower_reset_ep + lower_tail[0] if lower_tail else None,
        transported_first_lower_tail=trans_first_tail,
        first_tail_delta_from_upper_anchor=first_tail_delta,
        lower_deadline_value=lower_deadline,
        transported_lower_deadline=trans_deadline,
        upper_deadline_value=upper_deadline,
        deadline_transport_error=deadline_error,
        carrier_overshoot_to_gap_ratio=carrier_ratio,
        first_tail_proximity_score=None if first_tail_delta is None else abs(first_tail_delta),
    )


def print_table(metrics_list: list[TransportMetrics]) -> None:
    """Print one compact transport-metric table."""
    print("\n" + "=" * 120)
    print("RSA v2 PGSPG Certificate Transport Metrics — Phase 1 Diagnostic")
    print("=" * 120)

    header = (
        f"{'case_id':<28} {'bits':>4} {'status_short':<12} {'steps':>6} | "
        f"{'carrier_overshoot':>16} {'first_tail_delta':>16} {'deadline_err':>12} | "
        f"{'carrier/gap':>10} {'tail_prox':>9}"
    )
    print(header)
    print("-" * 120)

    for m in metrics_list:
        status_short = (
            "deadline_sig" if "deadline" in m.public_closure_status
            else "mutual" if "mutual" in m.public_closure_status
            else m.public_closure_status[:12]
        )

        print(
            f"{m.case_id:<28} {m.bits:>4} {status_short:>12} {m.endpoint_chain_steps:>6} | "
            f"{m.carrier_overshoot_above_anchor:>16} {str(m.first_tail_delta_from_upper_anchor):>16} "
            f"{m.deadline_transport_error:>12} | "
            f"{str(m.carrier_overshoot_to_gap_ratio):>10} {str(m.first_tail_proximity_score):>9}"
        )

    print("-" * 120)
    print("\nLegend:")
    print("  carrier_overshoot : (floor(N / lower.carrier_w) - upper_anchor)")
    print("  first_tail_delta  : (floor(N / first_lower_tail) - upper_anchor)")
    print("  deadline_err      : (floor(N / lower_deadline) - upper_deadline)")
    print("  carrier/gap       : carrier_overshoot / lower_gap_offset")
    print("  tail_prox         : absolute value of first_tail_delta (lower is tighter)")


def evaluate_proposed_predicates(m: TransportMetrics, row: dict) -> dict[str, str]:
    """Evaluate the Phase 2 proposed predicates using the actual lower_gap_offset from the row."""

    results = {}
    lower_gap_offset = int(row.get("lower_gap_offset", 0) or 0)

    # Predicate A: Reciprocal Carrier Alignment
    # Bound = max(20, floor(1.2 * lower_gap_offset))
    bound = max(20, (6 * lower_gap_offset) // 5) if lower_gap_offset > 0 else 20
    actual = abs(m.carrier_overshoot_above_upper_carrier)
    results["A_reciprocal_carrier"] = "PASS" if actual <= bound else "FAIL"
    results["A_bound"] = str(bound)
    results["A_actual"] = str(actual)

    # Predicate B: First Tail Proximity (only when deadline came from tail)
    sig = str(row.get("lower_reset_signature", ""))
    has_tail = bool(row.get("lower_tail_after_reset_offsets"))

    if "deadline=tail" in sig and has_tail and m.first_tail_delta_from_upper_anchor is not None:
        delta = m.first_tail_delta_from_upper_anchor
        results["B_first_tail_proximity"] = "PASS" if -12 <= delta <= 6 else "FAIL"
        results["B_actual_delta"] = str(delta)
    elif "deadline=threat" in sig:
        results["B_first_tail_proximity"] = "N/A (threat-based deadline, no tail)"
    else:
        results["B_first_tail_proximity"] = "N/A"

    return results


def main():
    """Print transport metrics and predicate evaluations for committed ladder rows."""
    base = Path(__file__).parent
    survivor_path = base / "output" / "survivor_rows.jsonl"

    if not survivor_path.exists():
        print(f"ERROR: {survivor_path} not found")
        return

    rows = load_survivor_rows(survivor_path)

    target_cases = [
        "rsa_v2_40bit_static_001",
        "rsa_v2_50bit_static_001",
        "rsa_v2_64bit_static_001",
    ]

    metrics = []
    for cid in target_cases:
        if cid in rows:
            m = compute_metrics(cid, rows[cid])
            metrics.append(m)
        else:
            print(f"Warning: {cid} not found in survivor data")

    print_table(metrics)

    # Phase 2 predicate evaluation
    print("\n\nPHASE 2 PROPOSED PREDICATE EVALUATION")
    print("=" * 120)
    for m in metrics:
        row = rows[m.case_id]
        preds = evaluate_proposed_predicates(m, row)
        print(f"\n{m.case_id} ({m.bits} bit)")
        for name, result in preds.items():
            print(f"  {name}: {result}")


if __name__ == "__main__":
    main()
