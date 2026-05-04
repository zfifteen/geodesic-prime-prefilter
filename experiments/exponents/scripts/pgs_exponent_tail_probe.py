#!/usr/bin/env python3
"""Extract prime-power exponent tails from PGS obstruction strips."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TWIN_OUTPUT = ROOT / "experiments" / "twin-primes" / "output"
DEFAULT_BASE_INPUT = (
    TWIN_OUTPUT
    / "twin_prime_endpoint_fixed_point_decomposition_probe"
    / "third_strip_higher_rows.csv"
)
DEFAULT_FOURTH_INPUT = TWIN_OUTPUT / "twin_prime_fourth_strip_pressure_probe" / "fourth_strip_rows.csv"
DEFAULT_FIFTH_INPUT = TWIN_OUTPUT / "twin_prime_fifth_strip_pressure_probe" / "fifth_strip_rows.csv"
DEFAULT_SIXTH_INPUT = TWIN_OUTPUT / "twin_prime_sixth_strip_pressure_probe" / "sixth_strip_rows.csv"
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "pgs_exponent_tail_probe"
BASE_SCALE = 1_000_000
PRIME_POWER_TAIL_FAMILIES = frozenset(
    {"prime_square", "prime_cube", "prime_power", "two_prime_power_family"}
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Extract exponent patterns from PGS prime-power tail rows.",
    )
    parser.add_argument("--base-input", type=Path, default=DEFAULT_BASE_INPUT)
    parser.add_argument("--fourth-input", type=Path, default=DEFAULT_FOURTH_INPUT)
    parser.add_argument("--fifth-input", type=Path, default=DEFAULT_FIFTH_INPUT)
    parser.add_argument("--sixth-input", type=Path, default=DEFAULT_SIXTH_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def parse_bool(value: object) -> bool:
    """Parse a CSV boolean field."""
    if value is True:
        return True
    if value is False:
        return False
    if str(value) == "True":
        return True
    if str(value) == "False":
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def parse_factor_signature(signature: str) -> list[tuple[int, int]]:
    """Parse a factor signature such as 7^3*19^2."""
    if not signature:
        raise ValueError("factor signature cannot be empty")
    factors: list[tuple[int, int]] = []
    for part in signature.split("*"):
        if "^" in part:
            prime, exponent = part.split("^", 1)
            factors.append((int(prime), int(exponent)))
        else:
            factors.append((int(part), 1))
    return sorted(factors)


def factorization(n: int) -> list[tuple[int, int]]:
    """Return the exact prime-power factorization of n."""
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


def factor_signature(factors: list[tuple[int, int]]) -> str:
    """Return a stable factor signature."""
    parts = []
    for prime, exponent in sorted(factors):
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def expanded_primes(factors: list[tuple[int, int]]) -> list[int]:
    """Return sorted prime factors with multiplicity."""
    primes: list[int] = []
    for prime, exponent in sorted(factors):
        primes.extend([prime] * exponent)
    return primes


def exponent_pattern(factors: list[tuple[int, int]]) -> str:
    """Return sorted exponents greater than one."""
    exponents = sorted(exponent for _prime, exponent in factors if exponent > 1)
    if not exponents:
        raise ValueError(f"no exponent tail in factors: {factors!r}")
    return ",".join(str(exponent) for exponent in exponents)


def max_tail_exponent(factors: list[tuple[int, int]]) -> int:
    """Return the largest exponent in a tail factorization."""
    return max(exponent for _prime, exponent in factors)


def peeled_factor_residue_path(candidate_signature: str, strip_depth: int) -> str:
    """Return the least-factor residue path through one strip depth."""
    primes = expanded_primes(parse_factor_signature(candidate_signature))
    if len(primes) < strip_depth:
        raise ValueError("candidate signature has fewer factors than strip depth")
    return "->".join(str(prime % 30) for prime in primes[:strip_depth])


def tail_row(
    *,
    source_surface: str,
    scale: int,
    q: int,
    candidate: int,
    candidate_signature: str,
    strip_depth: int,
    tail_family: str,
    tail_remainder: int,
    tail_signature: str,
) -> dict[str, object]:
    """Build one normalized exponent-tail row."""
    if tail_family not in PRIME_POWER_TAIL_FAMILIES:
        raise ValueError(f"unexpected tail family: {tail_family}")
    tail_factors = parse_factor_signature(tail_signature)
    if factor_signature(tail_factors) != tail_signature:
        raise ValueError(f"non-canonical tail signature for q={q}")
    return {
        "source_surface": source_surface,
        "scale": scale,
        "q": q,
        "q_mod30": q % 30,
        "candidate": candidate,
        "candidate_mod30": candidate % 30,
        "strip_depth": strip_depth,
        "tail_family": tail_family,
        "tail_remainder": tail_remainder,
        "tail_remainder_mod30": tail_remainder % 30,
        "tail_signature": tail_signature,
        "tail_exponent_pattern": exponent_pattern(tail_factors),
        "max_tail_exponent": max_tail_exponent(tail_factors),
        "peeled_factor_residue_path": peeled_factor_residue_path(candidate_signature, strip_depth),
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows from a path."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def base_tail_rows(path: Path) -> list[dict[str, object]]:
    """Return base third-strip exponent-tail rows."""
    rows: list[dict[str, object]] = []
    for row in read_csv(path):
        if not parse_bool(row["third_strip_prime_power_tail"]):
            continue
        tail_remainder = int(row["third_remainder"])
        tail_signature = factor_signature(factorization(tail_remainder))
        rows.append(
            tail_row(
                source_surface="base_third_strip",
                scale=BASE_SCALE,
                q=int(row["q"]),
                candidate=int(row["candidate"]),
                candidate_signature=row["factor_signature"],
                strip_depth=3,
                tail_family=row["third_remainder_family"],
                tail_remainder=tail_remainder,
                tail_signature=tail_signature,
            )
        )
    return rows


def strip_tail_rows(
    path: Path,
    *,
    source_surface: str,
    strip_depth: int,
    family_field: str,
    remainder_field: str,
    signature_field: str,
) -> list[dict[str, object]]:
    """Return exponent-tail rows from a focused high-scale strip file."""
    rows: list[dict[str, object]] = []
    for row in read_csv(path):
        tail_family = row[family_field]
        if tail_family not in PRIME_POWER_TAIL_FAMILIES:
            continue
        rows.append(
            tail_row(
                source_surface=source_surface,
                scale=int(row["scale"]),
                q=int(row["q"]),
                candidate=int(row["candidate"]),
                candidate_signature=row["factor_signature"],
                strip_depth=strip_depth,
                tail_family=tail_family,
                tail_remainder=int(row[remainder_field]),
                tail_signature=row[signature_field],
            )
        )
    return rows


def collect_tail_rows(args: argparse.Namespace) -> list[dict[str, object]]:
    """Collect all exponent-tail rows from the configured surfaces."""
    rows: list[dict[str, object]] = []
    rows.extend(base_tail_rows(args.base_input))
    rows.extend(
        strip_tail_rows(
            args.fourth_input,
            source_surface="fourth_strip",
            strip_depth=4,
            family_field="fourth_remainder_family",
            remainder_field="fourth_remainder",
            signature_field="fourth_remainder_signature",
        )
    )
    rows.extend(
        strip_tail_rows(
            args.fifth_input,
            source_surface="fifth_strip",
            strip_depth=5,
            family_field="fifth_remainder_family",
            remainder_field="fifth_remainder",
            signature_field="fifth_remainder_signature",
        )
    )
    rows.extend(
        strip_tail_rows(
            args.sixth_input,
            source_surface="sixth_strip",
            strip_depth=6,
            family_field="sixth_remainder_family",
            remainder_field="sixth_remainder",
            signature_field="sixth_remainder_signature",
        )
    )
    return rows


def grouped_counts(rows: list[dict[str, object]], fields: list[str]) -> list[dict[str, object]]:
    """Return grouped row counts for the selected fields."""
    counts: Counter[tuple[object, ...]] = Counter()
    for row in rows:
        counts[tuple(row[field] for field in fields)] += 1
    grouped = []
    for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        out = {field: value for field, value in zip(fields, key, strict=True)}
        out["count"] = count
        grouped.append(out)
    return grouped


def dominant_residue_path(rows: list[dict[str, object]]) -> str | None:
    """Return the most common peeled residue path."""
    counts = grouped_counts(rows, ["peeled_factor_residue_path"])
    if not counts:
        return None
    return str(counts[0]["peeled_factor_residue_path"])


def high_exponent_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows whose exposed tail has exponent greater than two."""
    return [row for row in rows if int(row["max_tail_exponent"]) > 2]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact exponent-tail summary metrics."""
    depth_exponent_rows = grouped_counts(rows, ["strip_depth", "tail_exponent_pattern"])
    residue_exponent_rows = grouped_counts(
        rows,
        ["peeled_factor_residue_path", "tail_exponent_pattern"],
    )
    dominant_path = dominant_residue_path(rows)
    dominant_path_rows = [
        row for row in rows if row["peeled_factor_residue_path"] == dominant_path
    ]
    high_rows = high_exponent_rows(rows)
    high_rows_on_dominant_path = [
        row for row in high_rows if row["peeled_factor_residue_path"] == dominant_path
    ]
    dominant_depth_exponent_count = depth_exponent_rows[0]["count"] if depth_exponent_rows else 0
    dominant_residue_exponent_count = residue_exponent_rows[0]["count"] if residue_exponent_rows else 0
    total = len(rows)
    return {
        "total_exponent_tail_rows": total,
        "source_surface_distribution": grouped_counts(rows, ["source_surface"]),
        "strip_depth_distribution": grouped_counts(rows, ["strip_depth"]),
        "tail_family_distribution": grouped_counts(rows, ["tail_family"]),
        "tail_exponent_pattern_distribution": grouped_counts(rows, ["tail_exponent_pattern"]),
        "depth_exponent_distribution": depth_exponent_rows,
        "residue_exponent_distribution": residue_exponent_rows,
        "dominant_residue_path": dominant_path,
        "dominant_residue_path_count": len(dominant_path_rows),
        "dominant_residue_path_share": len(dominant_path_rows) / total if total else 0.0,
        "high_exponent_tail_count": len(high_rows),
        "high_exponent_tail_on_dominant_residue_path_count": len(high_rows_on_dominant_path),
        "high_exponent_tail_on_dominant_residue_path_share": (
            len(high_rows_on_dominant_path) / len(high_rows) if high_rows else 0.0
        ),
        "dominant_residue_path_exponent_distribution": grouped_counts(
            dominant_path_rows,
            ["tail_exponent_pattern"],
        ),
        "dominant_residue_path_family_distribution": grouped_counts(
            dominant_path_rows,
            ["tail_family"],
        ),
        "dominant_depth_exponent_share": dominant_depth_exponent_count / total if total else 0.0,
        "dominant_residue_exponent_share": dominant_residue_exponent_count / total if total else 0.0,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the exponent-tail probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = collect_tail_rows(args)
    summary = summarize(rows)
    dominant_path = str(summary["dominant_residue_path"])
    dominant_path_rows = [
        row for row in rows if row["peeled_factor_residue_path"] == dominant_path
    ]
    high_rows = high_exponent_rows(rows)
    tail_fields = [
        "source_surface",
        "scale",
        "q",
        "q_mod30",
        "candidate",
        "candidate_mod30",
        "strip_depth",
        "tail_family",
        "tail_remainder",
        "tail_remainder_mod30",
        "tail_signature",
        "tail_exponent_pattern",
        "max_tail_exponent",
        "peeled_factor_residue_path",
    ]
    write_csv(args.output_dir / "exponent_tail_rows.csv", rows, tail_fields)
    write_csv(args.output_dir / "dominant_residue_path_rows.csv", dominant_path_rows, tail_fields)
    write_csv(args.output_dir / "high_exponent_tail_rows.csv", high_rows, tail_fields)
    write_csv(
        args.output_dir / "depth_exponent_rows.csv",
        grouped_counts(rows, ["strip_depth", "tail_exponent_pattern"]),
        ["strip_depth", "tail_exponent_pattern", "count"],
    )
    write_csv(
        args.output_dir / "residue_exponent_rows.csv",
        grouped_counts(rows, ["peeled_factor_residue_path", "tail_exponent_pattern"]),
        ["peeled_factor_residue_path", "tail_exponent_pattern", "count"],
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
