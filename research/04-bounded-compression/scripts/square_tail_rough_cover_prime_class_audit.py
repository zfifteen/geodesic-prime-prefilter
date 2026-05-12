#!/usr/bin/env python3
"""Audit prime representatives in a rough-cover CRT class."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_cover_model import build_cover_model  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Root used to seed the CRT model.")
    parser.add_argument(
        "--search-limit",
        type=int,
        default=10_000,
        help="Maximum k to scan in R = residue + k * modulus.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def dynamic_cutoff(left_prime: int) -> int:
    """Return C(q)=max(64, ceil(0.5 log(q)^2))."""
    return max(64, math.ceil(0.5 * (math.log(left_prime) ** 2)))


def first_prime_representative(residue: int, modulus: int, search_limit: int) -> tuple[int, int] | None:
    """Return the first prime representative R=residue+k*modulus in the scan."""
    for k in range(search_limit + 1):
        candidate = residue + k * modulus
        if gmpy2.is_prime(candidate):
            return k, candidate
    return None


def build_prime_class_audit(root: int, search_limit: int = 10_000) -> dict[str, object]:
    """Return the prime-representative audit for one CRT rough-cover model."""
    model = build_cover_model(root)
    residue = int(model["model_residue"])
    modulus = int(model["model_modulus"])
    modeled_even_window = 2 * int(model["M"])

    found = first_prime_representative(residue, modulus, search_limit)
    if found is None:
        return {
            "source_root": root,
            "search_limit": search_limit,
            "model_residue": model["model_residue"],
            "model_modulus": model["model_modulus"],
            "model_residue_coprime_to_modulus": model["model_residue_coprime_to_modulus"],
            "prime_representative_found": False,
            "first_prime_representative": None,
        }

    k, representative = found
    square = representative * representative
    previous_prime = int(gmpy2.prev_prime(square))
    previous_root = int(gmpy2.prev_prime(representative))
    previous_prime_offset = square - previous_prime
    cutoff = dynamic_cutoff(previous_prime)
    no_prime_in_modeled_window = all(
        not gmpy2.is_prime(square - offset)
        for offset in range(2, modeled_even_window + 1, 2)
    )

    return {
        "source_root": root,
        "search_limit": search_limit,
        "model_residue": model["model_residue"],
        "model_modulus": model["model_modulus"],
        "model_residue_coprime_to_modulus": model["model_residue_coprime_to_modulus"],
        "prime_representative_found": True,
        "first_prime_representative": {
            "k": k,
            "root": str(representative),
            "root_digits": len(str(representative)),
            "previous_root_gap": representative - previous_root,
            "previous_prime_offset": previous_prime_offset,
            "dynamic_cutoff": cutoff,
            "modeled_even_window": modeled_even_window,
            "no_prime_in_modeled_window": no_prime_in_modeled_window,
            "closed_by_cutoff": previous_prime_offset <= cutoff,
            "selected_square_condition": previous_root * previous_root < previous_prime < square,
        },
    }


def main(argv: list[str] | None = None) -> int:
    """Run the prime-class audit."""
    args = build_parser().parse_args(argv)
    payload = build_prime_class_audit(args.root, args.search_limit)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
