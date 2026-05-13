#!/usr/bin/env python3
"""Measure whether public PGS endpoint classes remove Shor order work."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = THIS_DIR.parents[1]
LIVE_SOLVER_DIR = EXPERIMENTS_DIR / "live-solver" / "rsa-v2"
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
for import_dir in (THIS_DIR, LIVE_SOLVER_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from run_experiment import (  # noqa: E402
    LadderCase,
    certificate_pair,
    load_cases,
    write_json,
    write_jsonl,
)


RULE_ID = "pgs_shor_order_entropy_probe_v1"
BASES = (2, 3, 5, 7, 11, 13, 17, 19)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "shor_order_entropy_probe"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_audit_factors(path: Path) -> dict[str, tuple[gmpy2.mpz, gmpy2.mpz]]:
    """Load downstream audit endpoints by case id."""
    factors: dict[str, tuple[gmpy2.mpz, gmpy2.mpz]] = {}
    for row in read_jsonl(path):
        factors[str(row["case_id"])] = (gmpy2.mpz(str(row["p"])), gmpy2.mpz(str(row["q"])))
    return factors


def lcm(left: int, right: int) -> int:
    """Return the least common multiple of two positive integers."""
    return left // math.gcd(left, right) * right


def factor_integer(value: int) -> dict[int, int]:
    """Return a deterministic trial-division factorization for audit integers."""
    if value < 1:
        raise ValueError("value must be positive")
    remaining = value
    factors: dict[int, int] = {}
    while remaining % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        remaining //= 2
    divisor = 3
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor += 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def multiplicative_order(base: int, modulus: int, exponent_bound: int) -> int | None:
    """Return the base order modulo modulus using one supplied exponent bound."""
    if math.gcd(base, modulus) != 1:
        return None
    order = exponent_bound
    for prime, exponent in factor_integer(exponent_bound).items():
        for _ in range(exponent):
            candidate = order // prime
            if pow(base, candidate, modulus) != 1:
                break
            order = candidate
    return order


def endpoint_class(pair) -> tuple[str, gmpy2.mpz | None, gmpy2.mpz | None]:
    """Return the public endpoint class emitted by the reciprocal PGS surface."""
    if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
        if pair.lower is None or pair.upper is None:
            raise ValueError("resolved mutual closure missing certificates")
        return pair.closure_status, pair.lower.reset_endpoint, pair.upper.reset_endpoint
    if pair.closure_status == "endpoint_class_by_reciprocal_deadline_signature_correction":
        return pair.closure_status, pair.corrected_lower_endpoint, pair.corrected_upper_endpoint
    if pair.closure_status == "endpoint_class_by_oriented_endpoint_chain_closure":
        return pair.closure_status, pair.corrected_lower_endpoint, pair.corrected_upper_endpoint
    return pair.closure_status, None, None


def public_row(case: LadderCase) -> tuple[dict[str, object], tuple[gmpy2.mpz, gmpy2.mpz] | None]:
    """Return one public PGS order-entropy row and optional endpoint class."""
    pair = certificate_pair(case)
    status, lower_endpoint, upper_endpoint = endpoint_class(pair)
    baseline_phase_bits = 2 * case.bits
    endpoint_class_present = lower_endpoint is not None and upper_endpoint is not None
    pgs_candidate_lambda_bits = None
    if endpoint_class_present:
        pgs_candidate_lambda_bits = lcm(int(lower_endpoint - 1), int(upper_endpoint - 1)).bit_length()
    row = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "source_rule_id": "reciprocal_pgs_certificate_pair_v2",
        "baseline_phase_bits": baseline_phase_bits,
        "pgs_public_closure_status": status,
        "pgs_endpoint_class_present": endpoint_class_present,
        "pgs_lower_endpoint_class": None if lower_endpoint is None else str(lower_endpoint),
        "pgs_upper_endpoint_class": None if upper_endpoint is None else str(upper_endpoint),
        "pgs_candidate_lambda_bits": pgs_candidate_lambda_bits,
        "public_inference_role": (
            "PGS supplies a public endpoint class before Shor order finding"
            if endpoint_class_present
            else "PGS returns unresolved before Shor order finding"
        ),
    }
    if lower_endpoint is None or upper_endpoint is None:
        return row, None
    return row, (lower_endpoint, upper_endpoint)


def order_vector(n_value: int, exponent_bound: int) -> dict[str, int | None]:
    """Return fixed-base orders for one modulus and exponent bound."""
    vector: dict[str, int | None] = {}
    for base in BASES:
        vector[str(base)] = multiplicative_order(base, n_value, exponent_bound)
    return vector


def audit_row(
    case: LadderCase,
    public_endpoint_class: tuple[gmpy2.mpz, gmpy2.mpz] | None,
    audit_factors: tuple[gmpy2.mpz, gmpy2.mpz],
) -> dict[str, object]:
    """Return downstream Shor-order audit metrics after public rows exist."""
    p_value, q_value = audit_factors
    actual_lambda = lcm(int(p_value - 1), int(q_value - 1))
    actual_orders = order_vector(int(case.n), actual_lambda)
    endpoint_match = False
    candidate_lambda = None
    candidate_orders = None
    residual_phase_bits = 2 * case.bits
    quantum_work_status = "ordinary_shor_order_finding_still_required"

    if public_endpoint_class is not None:
        lower_endpoint, upper_endpoint = public_endpoint_class
        endpoint_match = (
            {int(lower_endpoint), int(upper_endpoint)} == {int(p_value), int(q_value)}
        )
        candidate_lambda = lcm(int(lower_endpoint - 1), int(upper_endpoint - 1))
        candidate_orders = order_vector(int(case.n), candidate_lambda)
        if endpoint_match and candidate_orders == actual_orders:
            residual_phase_bits = 0
            quantum_work_status = "order_finding_removed_by_public_pgs_endpoint_class"
        else:
            quantum_work_status = "public_pgs_endpoint_class_failed_audit"

    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "audit_role": "downstream_only_after_public_endpoint_class",
        "audit_endpoint_match": endpoint_match,
        "actual_lambda_bits": actual_lambda.bit_length(),
        "actual_lambda_divisor_count": divisor_count_from_factorization(
            factor_integer(actual_lambda)
        ),
        "actual_order_by_base": actual_orders,
        "candidate_lambda_bits": None if candidate_lambda is None else candidate_lambda.bit_length(),
        "candidate_order_by_base": candidate_orders,
        "baseline_phase_bits": 2 * case.bits,
        "residual_phase_bits_after_pgs": residual_phase_bits,
        "phase_bits_removed_by_pgs": (2 * case.bits) - residual_phase_bits,
        "quantum_work_status": quantum_work_status,
    }


def divisor_count_from_factorization(factors: dict[int, int]) -> int:
    """Return the divisor count implied by one prime factorization."""
    total = 1
    for exponent in factors.values():
        total *= exponent + 1
    return total


def svg_bar_chart(rows: list[dict[str, object]]) -> str:
    """Return a small inline SVG phase-bit collapse chart."""
    width = 760
    row_height = 54
    top = 52
    left = 190
    chart_width = 500
    height = top + row_height * len(rows) + 42
    max_bits = max(int(row["baseline_phase_bits"]) for row in rows) if rows else 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="24" y="30" font-family="Arial" font-size="18" font-weight="700" fill="#111827">PGS order-entropy collapse before Shor</text>',
        '<text x="24" y="48" font-family="Arial" font-size="12" fill="#475569">Blue is ordinary phase bits. Green is residual phase bits after public PGS endpoint class.</text>',
    ]
    for index, row in enumerate(rows):
        y = top + index * row_height
        baseline = int(row["baseline_phase_bits"])
        residual = int(row["residual_phase_bits_after_pgs"])
        baseline_width = int(chart_width * baseline / max_bits)
        residual_width = int(chart_width * residual / max_bits)
        label = f"{row['case_id']} ({row['bits']}-bit)"
        parts.extend(
            [
                f'<text x="24" y="{y + 18}" font-family="Arial" font-size="12" fill="#111827">{label}</text>',
                f'<rect x="{left}" y="{y}" width="{baseline_width}" height="18" rx="3" fill="#2563eb"/>',
                f'<rect x="{left}" y="{y + 24}" width="{residual_width}" height="18" rx="3" fill="#16a34a"/>',
                f'<text x="{left + baseline_width + 8}" y="{y + 14}" font-family="Arial" font-size="12" fill="#1e3a8a">{baseline}</text>',
                f'<text x="{left + residual_width + 8}" y="{y + 38}" font-family="Arial" font-size="12" fill="#166534">{residual}</text>',
            ]
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def run_probe(
    cases: list[LadderCase],
    audit_factors: dict[str, tuple[gmpy2.mpz, gmpy2.mpz]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the public sidecar and downstream order audit."""
    public_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []
    for case in cases:
        row, endpoints = public_row(case)
        public_rows.append(row)
        if case.case_id in audit_factors:
            audit_rows.append(audit_row(case, endpoints, audit_factors[case.case_id]))
    removed_count = sum(
        1
        for row in audit_rows
        if row["quantum_work_status"] == "order_finding_removed_by_public_pgs_endpoint_class"
    )
    summary = {
        "rule_id": RULE_ID,
        "case_count": len(cases),
        "audit_row_count": len(audit_rows),
        "order_finding_removed_count": removed_count,
        "unresolved_before_shor_count": sum(
            1 for row in public_rows if not row["pgs_endpoint_class_present"]
        ),
        "total_baseline_phase_bits": sum(int(row["baseline_phase_bits"]) for row in audit_rows),
        "total_residual_phase_bits_after_pgs": sum(
            int(row["residual_phase_bits_after_pgs"]) for row in audit_rows
        ),
        "status": (
            "mixed_public_pgs_collapse"
            if removed_count and removed_count < len(audit_rows)
            else "public_pgs_collapse_absent"
            if removed_count == 0
            else "public_pgs_collapse_complete"
        ),
    }
    return public_rows, audit_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the PGS/Shor order-entropy probe.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--factors",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "audit_factors.jsonl",
        help="Audit-only factor rows JSONL path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for public, audit, summary, and SVG artifacts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the probe and write LF-terminated artifacts."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cases = load_cases(args.cases)
    audit_factors = load_audit_factors(args.factors)
    public_rows, audit_rows, summary = run_probe(cases, audit_factors)
    write_jsonl(args.output_dir / "public_order_entropy_rows.jsonl", public_rows)
    write_jsonl(args.output_dir / "audit_order_entropy_rows.jsonl", audit_rows)
    write_json(args.output_dir / "summary.json", summary)
    (args.output_dir / "phase_bit_collapse.svg").write_text(
        svg_bar_chart(audit_rows),
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
