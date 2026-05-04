#!/usr/bin/env python3
"""Pressure-test the fourth factor strip on one high-scale next layer."""

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
    / "experiments"
    / "twin-primes"
    / "output"
    / "twin_prime_decade_ladder_probe"
    / "next_layer_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "experiments"
    / "twin-primes"
    / "output"
    / "twin_prime_fourth_strip_pressure_probe"
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
        description="Run fourth-strip pressure on a focused next-layer surface.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def factorization(n: int) -> list[tuple[int, int]]:
    """Return exact factorization for post-decision decomposition."""
    return [(int(prime), int(exp)) for prime, exp in sorted(factorint(int(n)).items())]


def fourth_strip_terminal(fourth_remainder_family: str) -> str:
    """Return the terminal class after the fourth strip."""
    if fourth_remainder_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES:
        return f"fourth_strip_{fourth_remainder_family}"
    if ENDPOINT_PROBE.is_prime_power_tail(fourth_remainder_family):
        return f"fourth_strip_prime_power_tail_{fourth_remainder_family}"
    return "fifth_layer_multi_prime"


def is_fourth_strip_accounted(fourth_remainder_family: str) -> bool:
    """Return whether the fourth strip reaches the known terminal grammar."""
    return (
        fourth_remainder_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES
        or ENDPOINT_PROBE.is_prime_power_tail(fourth_remainder_family)
    )


def load_next_layer_rows(path: Path, scale: int) -> list[dict[str, str]]:
    """Load the next-layer rows for one scale."""
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["scale"]) == int(scale):
                if row["terminal_family"] != "multi_prime_family":
                    raise ValueError(f"non-next-layer terminal family for q={row['q']}")
                if row["grammar_accounted"] != "False":
                    raise ValueError(f"accounted row found in next-layer input for q={row['q']}")
                rows.append(row)
    if not rows:
        raise ValueError(f"no next-layer rows found for scale={scale}")
    return rows


def fourth_strip_row(row: dict[str, str]) -> dict[str, object]:
    """Return one fourth-strip decomposition row."""
    third_remainder = int(row["third_remainder"])
    factors = factorization(third_remainder)
    fourth_factor = factors[0][0]
    fourth_remainder = third_remainder // fourth_factor
    fourth_remainder_factors = factorization(fourth_remainder)
    fourth_remainder_tau = ENDPOINT_PROBE.tau_from_factors(fourth_remainder_factors)
    fourth_remainder_family = ENDPOINT_PROBE.endpoint_family(
        fourth_remainder_factors,
        fourth_remainder_tau,
    )
    terminal = fourth_strip_terminal(fourth_remainder_family)
    accounted = is_fourth_strip_accounted(fourth_remainder_family)
    return {
        "scale": int(row["scale"]),
        "q": int(row["q"]),
        "candidate": int(row["candidate"]),
        "factor_signature": row["factor_signature"],
        "third_factor": int(row["third_factor"]),
        "third_remainder": third_remainder,
        "fourth_factor": fourth_factor,
        "fourth_remainder": fourth_remainder,
        "fourth_remainder_tau": fourth_remainder_tau,
        "fourth_remainder_family": fourth_remainder_family,
        "fourth_remainder_signature": ENDPOINT_PROBE.factor_signature(fourth_remainder_factors),
        "fourth_strip_terminal": terminal,
        "fourth_strip_accounted": accounted,
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
    """Return summary metrics for fourth-strip pressure."""
    accounted = [row for row in rows if bool(row["fourth_strip_accounted"])]
    fifth_layer = [row for row in rows if not bool(row["fourth_strip_accounted"])]
    low_complexity = [
        row
        for row in rows
        if row["fourth_remainder_family"] in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES
    ]
    prime_power_tail = [
        row
        for row in rows
        if ENDPOINT_PROBE.is_prime_power_tail(str(row["fourth_remainder_family"]))
    ]
    return {
        "scale": int(rows[0]["scale"]),
        "input_next_layer_count": len(rows),
        "fourth_strip_low_complexity_count": len(low_complexity),
        "fourth_strip_prime_power_tail_count": len(prime_power_tail),
        "fourth_strip_accounted_count": len(accounted),
        "fifth_layer_count": len(fifth_layer),
        "fourth_strip_compression_rate": len(accounted) / len(rows),
        "fourth_remainder_family_distribution": count_by(rows, "fourth_remainder_family"),
        "fourth_strip_terminal_distribution": count_by(rows, "fourth_strip_terminal"),
        "fifth_layer_family_distribution": count_by(fifth_layer, "fourth_remainder_family"),
        "grammar_disposition": "CLOSED" if not fifth_layer else "FIFTH_LAYER_FOUND",
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the focused fourth-strip probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_rows = load_next_layer_rows(args.input, args.scale)
    rows = [fourth_strip_row(row) for row in source_rows]
    summary = summarize(rows)
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "third_factor",
        "third_remainder",
        "fourth_factor",
        "fourth_remainder",
        "fourth_remainder_tau",
        "fourth_remainder_family",
        "fourth_remainder_signature",
        "fourth_strip_terminal",
        "fourth_strip_accounted",
    ]
    fifth_layer_rows = [row for row in rows if not bool(row["fourth_strip_accounted"])]
    write_csv(args.output_dir / "fourth_strip_rows.csv", rows, fields)
    write_csv(args.output_dir / "fifth_layer_rows.csv", fifth_layer_rows, fields)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
