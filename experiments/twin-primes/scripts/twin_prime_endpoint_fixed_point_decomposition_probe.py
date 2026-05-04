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
LOW_COMPLEXITY_COFACTOR_FAMILIES = frozenset({"fixed_point", "semiprime_distinct"})
PRIME_POWER_TAIL_FAMILIES = frozenset(
    {"prime_square", "prime_cube", "prime_power", "two_prime_power_family"}
)


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


def reduced_obstruction_family(cofactor_family: str | None) -> str:
    """Return the obstruction family after stripping the least factor."""
    if cofactor_family is None:
        return "endpoint_fixed_point"
    if cofactor_family == "fixed_point":
        return "least_factor_times_fixed_point_cofactor"
    if cofactor_family == "semiprime_distinct":
        return "least_factor_times_semiprime_cofactor"
    return "least_factor_times_higher_cofactor"


def second_strip_family(second_remainder_family: str | None) -> str:
    """Return the obstruction family after stripping a second factor."""
    if second_remainder_family is None:
        return "not_second_stripped"
    if second_remainder_family == "fixed_point":
        return "second_factor_times_fixed_point_remainder"
    if second_remainder_family == "semiprime_distinct":
        return "second_factor_times_semiprime_remainder"
    return "second_factor_times_higher_remainder"


def third_strip_family(third_remainder_family: str | None) -> str:
    """Return the obstruction family after stripping a third factor."""
    if third_remainder_family is None:
        return "not_third_stripped"
    if third_remainder_family == "fixed_point":
        return "third_factor_times_fixed_point_remainder"
    if third_remainder_family == "semiprime_distinct":
        return "third_factor_times_semiprime_remainder"
    return "third_factor_times_higher_remainder"


def is_prime_power_tail(third_remainder_family: str | None) -> bool:
    """Return whether the third remainder is prime-power tail material."""
    return third_remainder_family in PRIME_POWER_TAIL_FAMILIES


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
    second_factor = None
    second_factor_mod30 = None
    second_remainder = None
    second_remainder_mod30 = None
    second_remainder_tau = None
    second_remainder_family = None
    third_factor = None
    third_factor_mod30 = None
    third_remainder = None
    third_remainder_mod30 = None
    third_remainder_tau = None
    third_remainder_family = None
    if not endpoint_is_fixed:
        least_factor = factors[0][0]
        cofactor = candidate // least_factor
        cofactor_factors = factorization(cofactor)
        cofactor_tau = tau_from_factors(cofactor_factors)
        cofactor_family = endpoint_family(cofactor_factors, cofactor_tau)
        if cofactor_family not in LOW_COMPLEXITY_COFACTOR_FAMILIES:
            second_factor = cofactor_factors[0][0]
            second_factor_mod30 = second_factor % 30
            second_remainder = cofactor // second_factor
            second_remainder_mod30 = second_remainder % 30
            second_remainder_factors = factorization(second_remainder)
            second_remainder_tau = tau_from_factors(second_remainder_factors)
            second_remainder_family = endpoint_family(
                second_remainder_factors,
                second_remainder_tau,
            )
            if second_remainder_family not in LOW_COMPLEXITY_COFACTOR_FAMILIES:
                third_factor = second_remainder_factors[0][0]
                third_factor_mod30 = third_factor % 30
                third_remainder = second_remainder // third_factor
                third_remainder_mod30 = third_remainder % 30
                third_remainder_factors = factorization(third_remainder)
                third_remainder_tau = tau_from_factors(third_remainder_factors)
                third_remainder_family = endpoint_family(
                    third_remainder_factors,
                    third_remainder_tau,
                )
    reduced_family = reduced_obstruction_family(cofactor_family)
    second_family = second_strip_family(second_remainder_family)
    third_family = third_strip_family(third_remainder_family)

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
        "cofactor_mod30": None if cofactor is None else cofactor % 30,
        "cofactor_tau": cofactor_tau,
        "cofactor_family": cofactor_family,
        "reduced_obstruction_family": reduced_family,
        "low_complexity_cofactor_obstruction": cofactor_family in LOW_COMPLEXITY_COFACTOR_FAMILIES,
        "higher_cofactor_obstruction": (
            cofactor_family is not None and cofactor_family not in LOW_COMPLEXITY_COFACTOR_FAMILIES
        ),
        "second_factor": second_factor,
        "second_factor_mod30": second_factor_mod30,
        "second_remainder": second_remainder,
        "second_remainder_mod30": second_remainder_mod30,
        "second_remainder_tau": second_remainder_tau,
        "second_remainder_family": second_remainder_family,
        "second_strip_family": second_family,
        "second_strip_low_complexity_remainder": (
            second_remainder_family in LOW_COMPLEXITY_COFACTOR_FAMILIES
        ),
        "third_factor": third_factor,
        "third_factor_mod30": third_factor_mod30,
        "third_remainder": third_remainder,
        "third_remainder_mod30": third_remainder_mod30,
        "third_remainder_tau": third_remainder_tau,
        "third_remainder_family": third_remainder_family,
        "third_strip_family": third_family,
        "third_strip_low_complexity_remainder": (
            third_remainder_family in LOW_COMPLEXITY_COFACTOR_FAMILIES
        ),
        "third_strip_prime_power_tail": is_prime_power_tail(third_remainder_family),
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
    low_complexity_obstructed = [
        row
        for row in obstructed
        if bool(row["low_complexity_cofactor_obstruction"])
    ]
    higher_cofactor_obstructed = [
        row
        for row in obstructed
        if bool(row["higher_cofactor_obstruction"])
    ]
    second_strip_low_complexity = [
        row
        for row in higher_cofactor_obstructed
        if bool(row["second_strip_low_complexity_remainder"])
    ]
    second_strip_higher = [
        row
        for row in higher_cofactor_obstructed
        if row["second_strip_family"] == "second_factor_times_higher_remainder"
    ]
    third_strip_low_complexity = [
        row
        for row in second_strip_higher
        if bool(row["third_strip_low_complexity_remainder"])
    ]
    third_strip_higher = [
        row
        for row in second_strip_higher
        if row["third_strip_family"] == "third_factor_times_higher_remainder"
    ]
    third_strip_prime_power_tail = [
        row
        for row in third_strip_higher
        if bool(row["third_strip_prime_power_tail"])
    ]
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
        "low_complexity_cofactor_obstruction_count": len(low_complexity_obstructed),
        "low_complexity_cofactor_obstruction_rate": (
            len(low_complexity_obstructed) / len(obstructed) if obstructed else 0.0
        ),
        "higher_cofactor_obstruction_count": len(higher_cofactor_obstructed),
        "second_strip_low_complexity_remainder_count": len(second_strip_low_complexity),
        "second_strip_low_complexity_remainder_rate": (
            len(second_strip_low_complexity) / len(higher_cofactor_obstructed)
            if higher_cofactor_obstructed
            else 0.0
        ),
        "second_strip_higher_remainder_count": len(second_strip_higher),
        "third_strip_low_complexity_remainder_count": len(third_strip_low_complexity),
        "third_strip_low_complexity_remainder_rate": (
            len(third_strip_low_complexity) / len(second_strip_higher)
            if second_strip_higher
            else 0.0
        ),
        "third_strip_higher_remainder_count": len(third_strip_higher),
        "third_strip_prime_power_tail_count": len(third_strip_prime_power_tail),
        "third_strip_prime_power_tail_rate": (
            len(third_strip_prime_power_tail) / len(third_strip_higher)
            if third_strip_higher
            else 0.0
        ),
        "endpoint_family_distribution": count_by(rows, "endpoint_family"),
        "obstruction_family_distribution": count_by(obstructed, "endpoint_family"),
        "reduced_obstruction_family_distribution": count_by(obstructed, "reduced_obstruction_family"),
        "second_strip_family_distribution": count_by(higher_cofactor_obstructed, "second_strip_family"),
        "second_remainder_family_distribution": count_by(higher_cofactor_obstructed, "second_remainder_family"),
        "third_strip_family_distribution": count_by(second_strip_higher, "third_strip_family"),
        "third_remainder_family_distribution": count_by(second_strip_higher, "third_remainder_family"),
        "third_strip_prime_power_tail_distribution": count_by(
            third_strip_prime_power_tail,
            "third_remainder_family",
            "factor_signature",
        ),
        "tau_candidate_distribution": count_by(rows, "tau_candidate"),
        "least_factor_distribution": count_by(obstructed, "least_factor")[:50],
        "least_factor_low_complexity_distribution": count_by(
            low_complexity_obstructed,
            "least_factor",
            "cofactor_family",
        )[:50],
        "least_factor_residue_distribution": count_by(obstructed, "least_factor_mod30"),
        "candidate_cofactor_residue_distribution": count_by(
            obstructed,
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
        ),
        "second_strip_residue_distribution": count_by(
            higher_cofactor_obstructed,
            "cofactor_mod30",
            "second_factor_mod30",
            "second_remainder_mod30",
        ),
        "second_strip_grammar": count_by(
            higher_cofactor_obstructed,
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
            "second_factor_mod30",
            "second_remainder_mod30",
            "second_strip_family",
            "second_factor",
            "second_remainder_family",
        )[:100],
        "third_strip_residue_distribution": count_by(
            second_strip_higher,
            "second_remainder_mod30",
            "third_factor_mod30",
            "third_remainder_mod30",
        ),
        "third_strip_grammar": count_by(
            second_strip_higher,
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
            "second_factor_mod30",
            "second_remainder_mod30",
            "third_factor_mod30",
            "third_remainder_mod30",
            "third_strip_family",
            "third_factor",
            "third_remainder_family",
        )[:100],
        "third_strip_higher_rows": third_strip_higher,
        "cofactor_family_distribution": count_by(obstructed, "cofactor_family"),
        "compact_obstruction_grammar": count_by(
            obstructed,
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
            "reduced_obstruction_family",
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
        "cofactor_mod30",
        "cofactor_tau",
        "cofactor_family",
        "reduced_obstruction_family",
        "low_complexity_cofactor_obstruction",
        "higher_cofactor_obstruction",
        "second_factor",
        "second_factor_mod30",
        "second_remainder",
        "second_remainder_mod30",
        "second_remainder_tau",
        "second_remainder_family",
        "second_strip_family",
        "second_strip_low_complexity_remainder",
        "third_factor",
        "third_factor_mod30",
        "third_remainder",
        "third_remainder_mod30",
        "third_remainder_tau",
        "third_remainder_family",
        "third_strip_family",
        "third_strip_low_complexity_remainder",
        "third_strip_prime_power_tail",
    ]
    grammar_fields = [
        "candidate_mod30",
        "least_factor_mod30",
        "cofactor_mod30",
        "reduced_obstruction_family",
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
    write_csv(
        args.output_dir / "second_strip_grammar_rows.csv",
        summary["second_strip_grammar"],
        [
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
            "second_factor_mod30",
            "second_remainder_mod30",
            "second_strip_family",
            "second_factor",
            "second_remainder_family",
            "count",
        ],
    )
    write_csv(
        args.output_dir / "third_strip_grammar_rows.csv",
        summary["third_strip_grammar"],
        [
            "candidate_mod30",
            "least_factor_mod30",
            "cofactor_mod30",
            "second_factor_mod30",
            "second_remainder_mod30",
            "third_factor_mod30",
            "third_remainder_mod30",
            "third_strip_family",
            "third_factor",
            "third_remainder_family",
            "count",
        ],
    )
    write_csv(
        args.output_dir / "third_strip_higher_rows.csv",
        summary["third_strip_higher_rows"],
        row_fields,
    )
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
