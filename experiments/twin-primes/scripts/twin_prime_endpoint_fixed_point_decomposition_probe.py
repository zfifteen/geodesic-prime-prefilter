#!/usr/bin/env python3
"""Decompose endpoint fixed-point hits and obstructions for width-2 chambers."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WIDTH2_PROBE_PATH = Path(__file__).with_name("twin_prime_width2_pgs_generator_probe.py")
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "twin-primes" / "output" / "twin_prime_endpoint_fixed_point_decomposition_probe"
DEFAULT_MAX_RIGHT_PRIME = 1_000_000


def load_width2_probe():
    """Load the experiment-local width-2 generator probe."""
    spec = importlib.util.spec_from_file_location("twin_prime_width2_pgs_generator_probe", WIDTH2_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_width2_pgs_generator_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WIDTH2_PROBE = load_width2_probe()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Decompose q+2 endpoint fixed-point hits and obstructions.",
    )
    parser.add_argument(
        "--max-right-prime",
        type=int,
        default=DEFAULT_MAX_RIGHT_PRIME,
        help="Largest eligible current prime q included in the decomposition.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for summary and CSV artifacts.",
    )
    return parser


def factorization(n: int) -> list[tuple[int, int]]:
    """Return the exact prime-power factorization of n."""
    n = int(n)
    if n < 2:
        raise ValueError("n must be at least 2")

    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            exponent = 0
            while n % divisor == 0:
                n //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors.append((n, 1))
    return factors


def tau_from_factors(factors: list[tuple[int, int]]) -> int:
    """Return divisor count from one factorization."""
    tau = 1
    for _prime, exponent in factors:
        tau *= exponent + 1
    return tau


def factor_signature(factors: list[tuple[int, int]]) -> str:
    """Return a stable factor signature."""
    parts = []
    for prime, exponent in factors:
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def endpoint_family(factors: list[tuple[int, int]], tau_n: int) -> str:
    """Return the endpoint factor family relative to the fixed-point locus."""
    if tau_n == 2:
        return "fixed_point"
    if len(factors) == 1:
        exponent = factors[0][1]
        if exponent == 2:
            return "prime_square"
        if exponent == 3:
            return "prime_cube"
        return "prime_power"
    if len(factors) == 2 and all(exponent == 1 for _prime, exponent in factors):
        return "semiprime_distinct"
    if len(factors) == 2:
        return "two_prime_power_family"
    return "multi_prime_family"


def decomposition_row(row: dict[str, object]) -> dict[str, object]:
    """Return one endpoint fixed-point decomposition row."""
    candidate = int(row["candidate"])
    tau_candidate = int(row["tau_candidate"])
    factors = factorization(candidate)
    factor_tau = tau_from_factors(factors)
    if factor_tau != tau_candidate:
        raise RuntimeError(f"factorization tau mismatch for candidate={candidate}")

    endpoint_is_fixed = tau_candidate == 2
    least_factor = None
    cofactor = None
    cofactor_tau = None
    cofactor_family = None
    if not endpoint_is_fixed:
        least_factor = factors[0][0]
        cofactor = candidate // least_factor
        cofactor_factors = factorization(cofactor)
        cofactor_tau = tau_from_factors(cofactor_factors)
        cofactor_family = endpoint_family(cofactor_factors, cofactor_tau)

    return {
        "q": int(row["q"]),
        "q_mod30": int(row["q"]) % 30,
        "w": int(row["w"]),
        "tau_w": int(row["tau_w"]),
        "candidate": candidate,
        "candidate_mod30": candidate % 30,
        "status": str(row["status"]),
        "endpoint_class": str(row["endpoint_class"]),
        "tau_candidate": tau_candidate,
        "endpoint_fixed_point": endpoint_is_fixed,
        "endpoint_family": endpoint_family(factors, tau_candidate),
        "factor_signature": factor_signature(factors),
        "least_factor": least_factor,
        "least_factor_mod30": None if least_factor is None else least_factor % 30,
        "cofactor": cofactor,
        "cofactor_tau": cofactor_tau,
        "cofactor_family": cofactor_family,
    }


def decomposition_rows(max_right_prime: int) -> list[dict[str, object]]:
    """Return endpoint decomposition rows through one cutoff."""
    records = WIDTH2_PROBE.generated_records(int(max_right_prime))
    audit_rows = WIDTH2_PROBE.audited_rows(records)
    rows = [decomposition_row(row) for row in audit_rows]
    if not rows:
        raise ValueError("no endpoint decomposition rows found")
    return rows


def count_by(rows: list[dict[str, object]], *fields: str) -> list[dict[str, object]]:
    """Return sorted grouped counts for one field tuple."""
    counter = Counter(tuple(row[field] for field in fields) for row in rows)
    output = []
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        payload = {field: value for field, value in zip(fields, key, strict=True)}
        payload["count"] = int(count)
        output.append(payload)
    return output


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return summary metrics for endpoint fixed-point decomposition."""
    fixed = [row for row in rows if row["endpoint_fixed_point"]]
    obstructed = [row for row in rows if not row["endpoint_fixed_point"]]
    status_mismatch = [
        row
        for row in rows
        if (row["status"] == WIDTH2_PROBE.STATUS_UNRESOLVED) != bool(row["endpoint_fixed_point"])
    ]
    return {
        "eligible_anchor_count": len(rows),
        "endpoint_fixed_point_count": len(fixed),
        "endpoint_obstruction_count": len(obstructed),
        "endpoint_fixed_point_rate": len(fixed) / len(rows),
        "status_mismatch_count": len(status_mismatch),
        "endpoint_family_distribution": count_by(rows, "endpoint_family"),
        "obstruction_family_distribution": count_by(obstructed, "endpoint_family"),
        "tau_candidate_distribution": count_by(rows, "tau_candidate"),
        "least_factor_distribution": count_by(obstructed, "least_factor")[:50],
        "cofactor_family_distribution": count_by(obstructed, "cofactor_family"),
        "compact_obstruction_grammar": count_by(
            obstructed,
            "candidate_mod30",
            "endpoint_family",
            "tau_candidate",
            "least_factor",
            "cofactor_family",
        )[:100],
        "audit_status": "PASS" if not status_mismatch else "FAIL",
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the endpoint fixed-point decomposition probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = decomposition_rows(args.max_right_prime)
    summary = summarize(rows)
    row_fields = [
        "q",
        "q_mod30",
        "w",
        "tau_w",
        "candidate",
        "candidate_mod30",
        "status",
        "endpoint_class",
        "tau_candidate",
        "endpoint_fixed_point",
        "endpoint_family",
        "factor_signature",
        "least_factor",
        "least_factor_mod30",
        "cofactor",
        "cofactor_tau",
        "cofactor_family",
    ]
    grammar_fields = [
        "candidate_mod30",
        "endpoint_family",
        "tau_candidate",
        "least_factor",
        "cofactor_family",
        "count",
    ]
    write_csv(args.output_dir / "endpoint_decomposition_rows.csv", rows, row_fields)
    write_csv(
        args.output_dir / "compact_obstruction_grammar_rows.csv",
        summary["compact_obstruction_grammar"],
        grammar_fields,
    )
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
