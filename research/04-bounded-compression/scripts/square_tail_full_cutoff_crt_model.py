#!/usr/bin/env python3
"""Build a full-cutoff CRT obstruction model for a representative root."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import gmpy2
from sympy import primerange
from sympy.ntheory.modular import crt
from sympy.ntheory.residue_ntheory import sqrt_mod


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_cover_prime_class_audit import build_prime_class_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=int,
        required=True,
        help="Source root whose first prime CRT representative seeds the model.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def repeat_capable_cover(root: int, limit: int) -> dict[int, list[int]]:
    """Return positions covered by all repeat-capable prime carriers."""
    covered: dict[int, list[int]] = {}
    for factor in primerange(3, limit + 1):
        factor_int = int(factor)
        residue = (root * root * pow(2, -1, factor_int)) % factor_int
        first = residue if residue != 0 else factor_int
        for m in range(first, limit + 1, factor_int):
            covered.setdefault(m, []).append(factor_int)
    return covered


def first_large_carrier(m: int, lower_bound: int, used: set[int], start: int) -> tuple[int, int]:
    """Return the first unused prime at or after start where 2m has a square root."""
    candidate = start
    while True:
        if candidate not in used:
            roots = sqrt_mod(2 * m, candidate, all_roots=True)
            if roots:
                return candidate, int(min(roots))
        candidate = int(gmpy2.next_prime(candidate))


def build_full_cutoff_crt_model(source_root: int) -> dict[str, object]:
    """Return a full-cutoff local CRT obstruction model for the representative."""
    representative_audit = build_prime_class_audit(source_root)
    representative = representative_audit["first_prime_representative"]
    if representative is None:
        raise RuntimeError("prime representative required for full-cutoff CRT model")

    root = int(representative["root"])
    limit = int(representative["dynamic_cutoff"]) // 2
    covered = repeat_capable_cover(root, limit)
    rough_m = [m for m in range(1, limit + 1) if m not in covered]
    small_primes = [int(prime) for prime in primerange(3, limit + 1)]

    moduli = list(small_primes)
    residues = [root % prime for prime in small_primes]
    used = set(small_primes)
    carrier_rows = []
    candidate = int(gmpy2.next_prime(limit))
    for m in rough_m:
        carrier, residue = first_large_carrier(m, limit, used, candidate)
        used.add(carrier)
        moduli.append(carrier)
        residues.append(residue)
        carrier_rows.append(
            {
                "m": m,
                "offset": 2 * m,
                "carrier": carrier,
                "residue": residue,
            }
        )
        candidate = int(gmpy2.next_prime(carrier))

    model_residue, model_modulus = crt(moduli, residues, check=True)
    if model_residue is None or model_modulus is None:
        raise RuntimeError("CRT model is inconsistent")
    model_residue = int(model_residue)
    model_modulus = int(model_modulus)

    small_residue_rows = list(zip(small_primes, residues[: len(small_primes)]))
    small_cover_failures = []
    rough_carrier_failures = []
    for m in range(1, limit + 1):
        small_divisors = [
            prime
            for prime, residue in small_residue_rows
            if (residue * residue - 2 * m) % prime == 0
        ]
        if m in rough_m:
            if small_divisors:
                small_cover_failures.append({"m": m, "small_divisors": small_divisors})
        elif not small_divisors:
            small_cover_failures.append({"m": m, "small_divisors": []})

    for row in carrier_rows:
        m = int(row["m"])
        carrier = int(row["carrier"])
        residue = int(row["residue"])
        if (residue * residue - 2 * m) % carrier != 0:
            rough_carrier_failures.append(row)

    residue_text = str(model_residue)
    modulus_text = str(model_modulus)
    return {
        "source_root": source_root,
        "representative_root": str(root),
        "M": limit,
        "repeat_capable_prime_count": len(small_primes),
        "repeat_capable_covered_count": len(covered),
        "rough_defect_count": len(rough_m),
        "assigned_large_carrier_count": len(carrier_rows),
        "first_rough_offsets": [2 * m for m in rough_m[:20]],
        "last_rough_offsets": [2 * m for m in rough_m[-20:]],
        "first_assigned_carrier": int(carrier_rows[0]["carrier"]) if carrier_rows else None,
        "last_assigned_carrier": int(carrier_rows[-1]["carrier"]) if carrier_rows else None,
        "model_residue_digits": len(residue_text),
        "model_modulus_digits": len(modulus_text),
        "model_residue_sha256": hashlib.sha256(residue_text.encode("ascii")).hexdigest(),
        "model_modulus_sha256": hashlib.sha256(modulus_text.encode("ascii")).hexdigest(),
        "model_residue_coprime_to_modulus": math.gcd(model_residue, model_modulus) == 1,
        "local_model_consistent": (
            not small_cover_failures and not rough_carrier_failures
        ),
        "small_pattern_preserved": not small_cover_failures,
        "rough_carriers_cover_all_defects": not rough_carrier_failures,
        "small_cover_failures": small_cover_failures,
        "rough_carrier_failures": rough_carrier_failures,
        "carrier_rows": carrier_rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the full-cutoff CRT obstruction model."""
    args = build_parser().parse_args(argv)
    payload = build_full_cutoff_crt_model(args.source_root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
