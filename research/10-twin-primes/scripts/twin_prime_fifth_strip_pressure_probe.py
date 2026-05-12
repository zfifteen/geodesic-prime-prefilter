#!/usr/bin/env python3
"""Pressure-test the fifth factor strip on one focused fifth layer."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

from sympy import factorint


ROOT = Path(__file__).resolve().parents[3]
ENDPOINT_PROBE_PATH = Path(__file__).with_name("twin_prime_endpoint_fixed_point_decomposition_probe.py")
DEFAULT_INPUT = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "output"
    / "twin_prime_fourth_strip_pressure_probe"
    / "fifth_layer_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "output"
    / "twin_prime_fifth_strip_pressure_probe"
)
DEFAULT_SCALE = 10**18


def load_endpoint_probe():
    """Load the experiment-local endpoint decomposition helpers."""
    spec = importlib.util.spec_from_file_location(
        "twin_prime_endpoint_fixed_point_decomposition_probe",
        ENDPOINT_PROBE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load endpoint decomposition probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENDPOINT_PROBE = load_endpoint_probe()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run fifth-strip pressure on a focused fifth-layer surface.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def factorization(n: int) -> list[tuple[int, int]]:
    """Return exact factorization for post-decision decomposition."""
    return [(int(prime), int(exp)) for prime, exp in sorted(factorint(int(n)).items())]


def fifth_strip_terminal(fifth_remainder_family: str) -> str:
    """Return the terminal class after the fifth strip."""
    if fifth_remainder_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES:
        return f"fifth_strip_{fifth_remainder_family}"
    if ENDPOINT_PROBE.is_prime_power_tail(fifth_remainder_family):
        return f"fifth_strip_prime_power_tail_{fifth_remainder_family}"
    return "sixth_layer_multi_prime"


def is_fifth_strip_accounted(fifth_remainder_family: str) -> bool:
    """Return whether the fifth strip reaches the known terminal grammar."""
    return (
        fifth_remainder_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES
        or ENDPOINT_PROBE.is_prime_power_tail(fifth_remainder_family)
    )


def load_fifth_layer_rows(path: Path, scale: int) -> list[dict[str, str]]:
    """Load the fifth-layer rows for one scale."""
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["scale"]) == int(scale):
                if row["fourth_remainder_family"] != "multi_prime_family":
                    raise ValueError(f"non-fifth-layer family for q={row['q']}")
                if row["fourth_strip_accounted"] != "False":
                    raise ValueError(f"accounted row found in fifth-layer input for q={row['q']}")
                rows.append(row)
    if not rows:
        raise ValueError(f"no fifth-layer rows found for scale={scale}")
    return rows


def fifth_strip_row(row: dict[str, str]) -> dict[str, object]:
    """Return one fifth-strip decomposition row."""
    fourth_remainder = int(row["fourth_remainder"])
    factors = factorization(fourth_remainder)
    fifth_factor = factors[0][0]
    fifth_remainder = fourth_remainder // fifth_factor
    fifth_remainder_factors = factorization(fifth_remainder)
    fifth_remainder_tau = ENDPOINT_PROBE.tau_from_factors(fifth_remainder_factors)
    fifth_remainder_family = ENDPOINT_PROBE.endpoint_family(
        fifth_remainder_factors,
        fifth_remainder_tau,
    )
    terminal = fifth_strip_terminal(fifth_remainder_family)
    accounted = is_fifth_strip_accounted(fifth_remainder_family)
    return {
        "scale": int(row["scale"]),
        "q": int(row["q"]),
        "candidate": int(row["candidate"]),
        "factor_signature": row["factor_signature"],
        "fourth_factor": int(row["fourth_factor"]),
        "fourth_remainder": fourth_remainder,
        "fifth_factor": fifth_factor,
        "fifth_remainder": fifth_remainder,
        "fifth_remainder_tau": fifth_remainder_tau,
        "fifth_remainder_family": fifth_remainder_family,
        "fifth_remainder_signature": ENDPOINT_PROBE.factor_signature(fifth_remainder_factors),
        "fifth_strip_terminal": terminal,
        "fifth_strip_accounted": accounted,
    }


def count_by(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    """Return grouped counts for one field."""
    counts: dict[object, int] = {}
    for row in rows:
        value = row[field]
        counts[value] = counts.get(value, 0) + 1
    return [
        {field: value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], str(item[0])))
    ]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return summary metrics for fifth-strip pressure."""
    accounted = [row for row in rows if bool(row["fifth_strip_accounted"])]
    sixth_layer = [row for row in rows if not bool(row["fifth_strip_accounted"])]
    low_complexity = [
        row
        for row in rows
        if row["fifth_remainder_family"] in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES
    ]
    prime_power_tail = [
        row
        for row in rows
        if ENDPOINT_PROBE.is_prime_power_tail(str(row["fifth_remainder_family"]))
    ]
    return {
        "scale": int(rows[0]["scale"]),
        "input_fifth_layer_count": len(rows),
        "fifth_strip_low_complexity_count": len(low_complexity),
        "fifth_strip_prime_power_tail_count": len(prime_power_tail),
        "fifth_strip_accounted_count": len(accounted),
        "sixth_layer_count": len(sixth_layer),
        "fifth_strip_compression_rate": len(accounted) / len(rows),
        "fifth_remainder_family_distribution": count_by(rows, "fifth_remainder_family"),
        "fifth_strip_terminal_distribution": count_by(rows, "fifth_strip_terminal"),
        "sixth_layer_family_distribution": count_by(sixth_layer, "fifth_remainder_family"),
        "grammar_disposition": "CLOSED" if not sixth_layer else "SIXTH_LAYER_FOUND",
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the focused fifth-strip probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_rows = load_fifth_layer_rows(args.input, args.scale)
    rows = [fifth_strip_row(row) for row in source_rows]
    summary = summarize(rows)
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "fourth_factor",
        "fourth_remainder",
        "fifth_factor",
        "fifth_remainder",
        "fifth_remainder_tau",
        "fifth_remainder_family",
        "fifth_remainder_signature",
        "fifth_strip_terminal",
        "fifth_strip_accounted",
    ]
    sixth_layer_rows = [row for row in rows if not bool(row["fifth_strip_accounted"])]
    write_csv(args.output_dir / "fifth_strip_rows.csv", rows, fields)
    write_csv(args.output_dir / "sixth_layer_rows.csv", sixth_layer_rows, fields)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
