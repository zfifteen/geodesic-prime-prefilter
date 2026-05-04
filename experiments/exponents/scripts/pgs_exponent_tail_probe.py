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
DEFAULT_BASE_DECOMPOSITION_INPUT = (
    TWIN_OUTPUT
    / "twin_prime_endpoint_fixed_point_decomposition_probe"
    / "endpoint_decomposition_rows.csv"
)
DEFAULT_DECADE_NEXT_LAYER_INPUT = (
    TWIN_OUTPUT / "twin_prime_decade_ladder_probe" / "next_layer_rows.csv"
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
    parser.add_argument("--base-decomposition-input", type=Path, default=DEFAULT_BASE_DECOMPOSITION_INPUT)
    parser.add_argument("--decade-next-layer-input", type=Path, default=DEFAULT_DECADE_NEXT_LAYER_INPUT)
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


def residue_path_shape(path: str) -> str:
    """Return whether a residue path repeats one residue or mixes residues."""
    parts = path.split("->")
    if len(set(parts)) == 1:
        return f"repeated_{parts[0]}"
    return "mixed"


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


def base_path_pressure_rows(path: Path) -> list[dict[str, object]]:
    """Return denominator rows for the base third-strip higher surface."""
    rows: list[dict[str, object]] = []
    for row in read_csv(path):
        if row["endpoint_class"] != "composite_obstruction":
            continue
        if row["second_strip_family"] != "second_factor_times_higher_remainder":
            continue
        path3 = peeled_factor_residue_path(row["factor_signature"], 3)
        tail = parse_bool(row["third_strip_prime_power_tail"])
        high_tail = False
        tail_pattern = ""
        if tail:
            tail_factors = factorization(int(row["third_remainder"]))
            tail_pattern = exponent_pattern(tail_factors)
            high_tail = max_tail_exponent(tail_factors) > 2
        third_remainder = int(row["third_remainder"])
        third_remainder_factors = factorization(third_remainder)
        third_remainder_exponents = [
            exponent for _prime, exponent in third_remainder_factors if exponent > 1
        ]
        rows.append(
            {
                "scale": BASE_SCALE,
                "q": int(row["q"]),
                "q_mod30": int(row["q"]) % 30,
                "candidate": int(row["candidate"]),
                "candidate_mod30": int(row["candidate"]) % 30,
                "peeled_factor_residue_path": path3,
                "residue_path_shape": residue_path_shape(path3),
                "third_remainder": third_remainder,
                "third_remainder_mod30": third_remainder % 30,
                "third_remainder_family": row["third_remainder_family"],
                "third_remainder_signature": factor_signature(third_remainder_factors),
                "third_remainder_exponent_pattern": (
                    ",".join(str(exponent) for exponent in sorted(third_remainder_exponents))
                    if third_remainder_exponents
                    else ""
                ),
                "third_remainder_max_exponent": max_tail_exponent(third_remainder_factors),
                "third_strip_prime_power_tail": tail,
                "high_exponent_tail": high_tail,
                "tail_exponent_pattern": tail_pattern,
            }
        )
    return rows


def decade_next_layer_pressure_rows(path: Path) -> list[dict[str, object]]:
    """Return third-strip carrier rows from the decade-ladder next layer."""
    rows: list[dict[str, object]] = []
    for row in read_csv(path):
        path3 = peeled_factor_residue_path(row["factor_signature"], 3)
        third_remainder = int(row["third_remainder"])
        third_remainder_factors = factorization(third_remainder)
        rows.append(
            {
                "scale": int(row["scale"]),
                "q": int(row["q"]),
                "q_mod30": int(row["q"]) % 30,
                "candidate": int(row["candidate"]),
                "candidate_mod30": int(row["candidate"]) % 30,
                "peeled_factor_residue_path": path3,
                "residue_path_shape": residue_path_shape(path3),
                "third_remainder": third_remainder,
                "third_remainder_mod30": third_remainder % 30,
                "third_remainder_family": row["third_remainder_family"],
                "third_remainder_signature": factor_signature(third_remainder_factors),
            }
        )
    return rows


def path_pressure_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return tail and high-exponent rates by residue path."""
    path_counts = grouped_counts(rows, ["peeled_factor_residue_path"])
    out = []
    for item in path_counts:
        path = item["peeled_factor_residue_path"]
        path_rows = [row for row in rows if row["peeled_factor_residue_path"] == path]
        tail_rows = [row for row in path_rows if bool(row["third_strip_prime_power_tail"])]
        high_rows = [row for row in path_rows if bool(row["high_exponent_tail"])]
        out.append(
            {
                "peeled_factor_residue_path": path,
                "residue_path_shape": residue_path_shape(str(path)),
                "third_higher_count": len(path_rows),
                "tail_count": len(tail_rows),
                "tail_rate": len(tail_rows) / len(path_rows),
                "high_exponent_tail_count": len(high_rows),
                "high_exponent_tail_rate": len(high_rows) / len(path_rows),
            }
        )
    return out


def path_shape_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return tail and high-exponent rates by path shape."""
    shapes = grouped_counts(rows, ["residue_path_shape"])
    out = []
    for item in shapes:
        shape = item["residue_path_shape"]
        shape_rows = [row for row in rows if row["residue_path_shape"] == shape]
        tail_rows = [row for row in shape_rows if bool(row["third_strip_prime_power_tail"])]
        high_rows = [row for row in shape_rows if bool(row["high_exponent_tail"])]
        out.append(
            {
                "residue_path_shape": shape,
                "third_higher_count": len(shape_rows),
                "tail_count": len(tail_rows),
                "tail_rate": len(tail_rows) / len(shape_rows),
                "high_exponent_tail_count": len(high_rows),
                "high_exponent_tail_rate": len(high_rows) / len(shape_rows),
            }
        )
    return out


def integer_power_base_count(capacity: int, exponent: int) -> int:
    """Return the number of integer bases b >= 2 with b^exponent <= capacity."""
    if capacity < 2:
        return 0
    count = 0
    base = 2
    while base**exponent <= capacity:
        count += 1
        base += 1
    return count


def repeated_carrier_prime(shape: str) -> int | None:
    """Return the repeated carrier prime encoded by a repeated path shape."""
    prefix = "repeated_"
    if not shape.startswith(prefix):
        return None
    return int(shape[len(prefix) :])


def carrier_capacity_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return capacity and tail pressure for repeated least-factor carriers."""
    out = []
    for shape_row in path_shape_summary(rows):
        shape = str(shape_row["residue_path_shape"])
        carrier = repeated_carrier_prime(shape)
        if carrier is None:
            continue
        carrier_rows = [row for row in rows if row["residue_path_shape"] == shape]
        family_counts = {
            str(item["third_remainder_family"]): int(item["count"])
            for item in grouped_counts(carrier_rows, ["third_remainder_family"])
        }
        post_triple_capacity = BASE_SCALE // (carrier**3)
        out.append(
            {
                "residue_path_shape": shape,
                "carrier_prime": carrier,
                "third_higher_count": len(carrier_rows),
                "third_higher_share": len(carrier_rows) / len(rows) if rows else 0.0,
                "post_triple_capacity": post_triple_capacity,
                "integer_cube_base_count": integer_power_base_count(post_triple_capacity, 3),
                "integer_fourth_base_count": integer_power_base_count(post_triple_capacity, 4),
                "tail_count": int(shape_row["tail_count"]),
                "tail_rate": float(shape_row["tail_rate"]),
                "high_exponent_tail_count": int(shape_row["high_exponent_tail_count"]),
                "high_exponent_tail_rate": float(shape_row["high_exponent_tail_rate"]),
                "fixed_point_count": family_counts.get("fixed_point", 0),
                "semiprime_distinct_count": family_counts.get("semiprime_distinct", 0),
                "prime_square_count": family_counts.get("prime_square", 0),
                "prime_cube_count": family_counts.get("prime_cube", 0),
                "prime_power_count": family_counts.get("prime_power", 0),
                "two_prime_power_family_count": family_counts.get("two_prime_power_family", 0),
            }
        )
    return sorted(out, key=lambda row: int(row["carrier_prime"]))


def decade_carrier_capacity_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return repeated-carrier capacity rows by decade scale."""
    scale_counts = Counter(row["scale"] for row in rows)
    counts: Counter[tuple[int, str]] = Counter()
    for row in rows:
        shape = str(row["residue_path_shape"])
        carrier = repeated_carrier_prime(shape)
        if carrier is None:
            continue
        counts[(int(row["scale"]), shape)] += 1
    out = []
    for (scale, shape), count in sorted(
        counts.items(),
        key=lambda item: (item[0][0], repeated_carrier_prime(item[0][1]) or 0),
    ):
        carrier = repeated_carrier_prime(shape)
        if carrier is None:
            raise ValueError(f"non-repeated carrier in decade summary: {shape}")
        post_triple_capacity = scale // (carrier**3)
        out.append(
            {
                "scale": scale,
                "residue_path_shape": shape,
                "carrier_prime": carrier,
                "next_layer_count": count,
                "scale_next_layer_count": scale_counts[scale],
                "scale_next_layer_share": count / scale_counts[scale],
                "post_triple_capacity": post_triple_capacity,
                "integer_cube_base_count": integer_power_base_count(post_triple_capacity, 3),
                "integer_fourth_base_count": integer_power_base_count(post_triple_capacity, 4),
            }
        )
    return out


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


def summarize(
    rows: list[dict[str, object]],
    pressure_rows: list[dict[str, object]],
    decade_rows: list[dict[str, object]],
) -> dict[str, object]:
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
    dominant_pressure_rows = [
        row for row in pressure_rows if row["peeled_factor_residue_path"] == dominant_path
    ]
    dominant_pressure_tail_rows = [
        row for row in dominant_pressure_rows if bool(row["third_strip_prime_power_tail"])
    ]
    dominant_pressure_high_rows = [
        row for row in dominant_pressure_rows if bool(row["high_exponent_tail"])
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
        "base_third_higher_count": len(pressure_rows),
        "decade_next_layer_count": len(decade_rows),
        "dominant_residue_path_base_third_higher_count": len(dominant_pressure_rows),
        "dominant_residue_path_base_tail_count": len(dominant_pressure_tail_rows),
        "dominant_residue_path_base_tail_rate": (
            len(dominant_pressure_tail_rows) / len(dominant_pressure_rows)
            if dominant_pressure_rows
            else 0.0
        ),
        "dominant_residue_path_base_high_exponent_tail_count": len(dominant_pressure_high_rows),
        "dominant_residue_path_base_high_exponent_tail_rate": (
            len(dominant_pressure_high_rows) / len(dominant_pressure_rows)
            if dominant_pressure_rows
            else 0.0
        ),
        "path_pressure_distribution": path_pressure_summary(pressure_rows),
        "path_shape_pressure_distribution": path_shape_summary(pressure_rows),
        "carrier_capacity_distribution": carrier_capacity_summary(pressure_rows),
        "decade_next_layer_path_shape_distribution": grouped_counts(
            decade_rows,
            ["residue_path_shape"],
        ),
        "decade_repeated_carrier_distribution": grouped_counts(
            [
                row
                for row in decade_rows
                if repeated_carrier_prime(str(row["residue_path_shape"])) is not None
            ],
            ["residue_path_shape"],
        ),
        "decade_carrier_capacity_distribution": decade_carrier_capacity_summary(decade_rows),
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
    pressure_rows = base_path_pressure_rows(args.base_decomposition_input)
    decade_rows = decade_next_layer_pressure_rows(args.decade_next_layer_input)
    summary = summarize(rows, pressure_rows, decade_rows)
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
        args.output_dir / "base_path_pressure_rows.csv",
        pressure_rows,
        [
            "scale",
            "q",
            "q_mod30",
            "candidate",
            "candidate_mod30",
            "peeled_factor_residue_path",
            "residue_path_shape",
            "third_remainder",
            "third_remainder_mod30",
            "third_remainder_family",
            "third_remainder_signature",
            "third_remainder_exponent_pattern",
            "third_remainder_max_exponent",
            "third_strip_prime_power_tail",
            "high_exponent_tail",
            "tail_exponent_pattern",
        ],
    )
    write_csv(
        args.output_dir / "path_pressure_rows.csv",
        path_pressure_summary(pressure_rows),
        [
            "peeled_factor_residue_path",
            "residue_path_shape",
            "third_higher_count",
            "tail_count",
            "tail_rate",
            "high_exponent_tail_count",
            "high_exponent_tail_rate",
        ],
    )
    write_csv(
        args.output_dir / "path_shape_pressure_rows.csv",
        path_shape_summary(pressure_rows),
        [
            "residue_path_shape",
            "third_higher_count",
            "tail_count",
            "tail_rate",
            "high_exponent_tail_count",
            "high_exponent_tail_rate",
        ],
    )
    write_csv(
        args.output_dir / "carrier_capacity_rows.csv",
        carrier_capacity_summary(pressure_rows),
        [
            "residue_path_shape",
            "carrier_prime",
            "third_higher_count",
            "third_higher_share",
            "post_triple_capacity",
            "integer_cube_base_count",
            "integer_fourth_base_count",
            "tail_count",
            "tail_rate",
            "high_exponent_tail_count",
            "high_exponent_tail_rate",
            "fixed_point_count",
            "semiprime_distinct_count",
            "prime_square_count",
            "prime_cube_count",
            "prime_power_count",
            "two_prime_power_family_count",
        ],
    )
    write_csv(
        args.output_dir / "decade_next_layer_pressure_rows.csv",
        decade_rows,
        [
            "scale",
            "q",
            "q_mod30",
            "candidate",
            "candidate_mod30",
            "peeled_factor_residue_path",
            "residue_path_shape",
            "third_remainder",
            "third_remainder_mod30",
            "third_remainder_family",
            "third_remainder_signature",
        ],
    )
    write_csv(
        args.output_dir / "decade_carrier_capacity_rows.csv",
        decade_carrier_capacity_summary(decade_rows),
        [
            "scale",
            "residue_path_shape",
            "carrier_prime",
            "next_layer_count",
            "scale_next_layer_count",
            "scale_next_layer_share",
            "post_triple_capacity",
            "integer_cube_base_count",
            "integer_fourth_base_count",
        ],
    )
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
