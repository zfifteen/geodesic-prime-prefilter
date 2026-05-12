#!/usr/bin/env python3
"""Build a local CRT model for a complete M-rough composite cover."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2
from sympy.ntheory.modular import crt
from sympy.ntheory.residue_ntheory import sqrt_mod
from sympy import primerange


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_defect_audit import build_rough_defect_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Root whose small residues seed the model.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def first_large_carrier(m: int, lower_bound: int, used: set[int]) -> tuple[int, int]:
    """Return the first unused prime above lower_bound where 2m has a square root."""
    candidate = int(gmpy2.next_prime(lower_bound))
    while True:
        if candidate not in used:
            roots = sqrt_mod(2 * m, candidate, all_roots=True)
            if roots:
                return candidate, int(min(roots))
        candidate = int(gmpy2.next_prime(candidate))


def build_cover_model(root: int) -> dict[str, object]:
    """Return a CRT-compatible local complete-cover model for one root."""
    audit = build_rough_defect_audit(root)
    limit = int(audit["full_counterexample_even_count"])
    rough_m = [int(offset) // 2 for offset in audit["rough_defect_offsets"]]
    small_primes = [int(prime) for prime in primerange(3, limit + 1)]

    moduli = []
    residues = []
    for prime in small_primes:
        moduli.append(prime)
        residues.append(root % prime)

    used = set(small_primes)
    carrier_rows = []
    for m in rough_m:
        carrier, residue = first_large_carrier(m, limit, used)
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

    model_residue, model_modulus = crt(moduli, residues, check=True)
    if model_residue is None or model_modulus is None:
        raise RuntimeError("CRT model is inconsistent")
    model_residue = int(model_residue)
    model_modulus = int(model_modulus)

    small_cover_failures = []
    rough_carrier_failures = []
    for m in range(1, limit + 1):
        small_divisors = [
            prime for prime in small_primes if (model_residue * model_residue - 2 * m) % prime == 0
        ]
        if m in rough_m:
            if small_divisors:
                small_cover_failures.append({"m": m, "small_divisors": small_divisors})
        elif not small_divisors:
            small_cover_failures.append({"m": m, "small_divisors": []})

    for row in carrier_rows:
        m = int(row["m"])
        carrier = int(row["carrier"])
        if (model_residue * model_residue - 2 * m) % carrier != 0:
            rough_carrier_failures.append(row)

    return {
        "root": root,
        "M": limit,
        "small_prime_count": len(small_primes),
        "rough_defect_count": len(rough_m),
        "assigned_large_carrier_count": len(carrier_rows),
        "model_residue": str(model_residue),
        "model_modulus": str(model_modulus),
        "model_modulus_digits": len(str(model_modulus)),
        "model_residue_digits": len(str(model_residue)),
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
    """Run the local CRT cover-model builder."""
    args = build_parser().parse_args(argv)
    payload = build_cover_model(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
