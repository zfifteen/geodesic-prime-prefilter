#!/usr/bin/env python3
"""Expand high-signal gap-grammar cells with deterministic labeled semiprimes."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
ROOT = THIS_DIR.parents[2]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from modulus_gap_grammar_probe import (  # noqa: E402
    LabeledCase,
    public_row_from_labeled_case,
    target_grammar_row,
    targets_from_labeled_case,
)
from grammar_compatibility_catalog import write_json, write_jsonl  # noqa: E402


RULE_ID = "grammar_cell_expander_v1"
DEFAULT_STARTS = (1_000_000, 10_000_000, 100_000_000, 1_000_000_000)
PAIR_OFFSETS = (1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
TARGET_CELLS = (
    ("H", "o4_d4_odd", "L"),
    ("L", "o6_d4_odd", "L"),
    ("L", "o6_d4_odd", "H"),
    ("L", "o2_d4_odd", "L"),
    ("L", "o2_d4_odd", "H"),
    ("L", "o4_d4_odd", "H"),
    ("L", "o4_d4_odd", "L"),
)
ORIENTATIONS = ("p_outward", "p_inward", "q_inward", "q_outward")


def is_higher(state: str) -> bool:
    """Return whether one reduced grammar state is higher-divisor grammar."""
    return "higher_divisor" in state


def low_high(state: str) -> str:
    """Return the low/higher class for one reduced grammar state."""
    return "H" if is_higher(state) else "L"


def family(state: str) -> str:
    """Return the exact family prefix before the divisor bucket."""
    return state.split("|", 1)[0]


def cell_key(public_row: dict[str, object]) -> tuple[str, str, str]:
    """Return the target grammar-cell key for one public row."""
    return (
        low_high(str(public_row["n_previous_gap_reduced_state"])),
        family(str(public_row["n_containing_gap_reduced_state"])),
        low_high(str(public_row["n_following_gap_reduced_state"])),
    )


def primes_from(start: int, count: int, block: int) -> list[int]:
    """Return PGS-discovered primes at or above one fixed start."""
    primes: list[int] = []
    lo = start
    while len(primes) < count:
        counts = divisor_counts_segment(lo, lo + block)
        for offset, divisor_count in enumerate(counts):
            if int(divisor_count) == 2:
                primes.append(lo + offset)
                if len(primes) == count:
                    break
        lo += block
    return primes


def compatibility_row(
    case: LabeledCase,
    public_row: dict[str, object],
    prime_start: int,
    prime_left_index: int,
    prime_pair_offset: int,
) -> dict[str, object]:
    """Return one normalized compatibility row for a generated evidence case."""
    target_rows = {
        row["target_side"]: row
        for row in (
            target_grammar_row(target, {case.case_id: public_row})
            for target in targets_from_labeled_case(case)
        )
    }
    p_row = target_rows["p"]
    q_row = target_rows["q"]
    row = {
        "rule_id": RULE_ID,
        "source_rule_id": str(public_row["rule_id"]),
        "surface": "deterministic_cell_expansion",
        "case_id": case.case_id,
        "bits": case.bits,
        "prime_start": prime_start,
        "prime_left_index": prime_left_index,
        "prime_pair_offset": prime_pair_offset,
        "prime_pair_offset_group": pair_offset_group(prime_pair_offset),
        "public_status": "exact_closed",
        "n_previous": public_row["n_previous_gap_reduced_state"],
        "n_containing": public_row["n_containing_gap_reduced_state"],
        "n_following": public_row["n_following_gap_reduced_state"],
        "n_previous_exact": public_row["n_previous_gap_exact_type_key"],
        "n_containing_exact": public_row["n_containing_gap_exact_type_key"],
        "n_following_exact": public_row["n_following_gap_exact_type_key"],
        "p_outward": p_row["target_left_gap_reduced_state"],
        "p_inward": p_row["target_right_gap_reduced_state"],
        "q_inward": q_row["target_left_gap_reduced_state"],
        "q_outward": q_row["target_right_gap_reduced_state"],
        "p_outward_exact": p_row["target_left_gap"]["exact_type_key"],
        "p_inward_exact": p_row["target_right_gap"]["exact_type_key"],
        "q_inward_exact": q_row["target_left_gap"]["exact_type_key"],
        "q_outward_exact": q_row["target_right_gap"]["exact_type_key"],
        "unresolved_public_roles": [],
        "cell_key": "|".join(cell_key(public_row)),
    }
    row["n_context_key"] = "|".join(
        [str(row["n_previous"]), str(row["n_containing"]), str(row["n_following"])]
    )
    row["target_orientation_key"] = "|".join(str(row[orientation]) for orientation in ORIENTATIONS)
    return row


def pair_offset_group(pair_offset: int) -> str:
    """Return the fixed separation group for one generated prime-pair offset."""
    if pair_offset <= 5:
        return "small"
    if pair_offset <= 21:
        return "mid"
    return "wide"


def labeled_case(case_id: str, p_value: int, q_value: int) -> LabeledCase:
    """Return one deterministic semiprime evidence label."""
    n_value = p_value * q_value
    return LabeledCase(
        case_id=case_id,
        bits=n_value.bit_length(),
        n=gmpy2.mpz(n_value),
        p=gmpy2.mpz(p_value),
        q=gmpy2.mpz(q_value),
        source=RULE_ID,
        family="deterministic_pgs_prime_pair",
    )


def enough(cell_counts: Counter[tuple[str, str, str]], target_per_cell: int) -> bool:
    """Return whether every target cell has enough rows."""
    return all(cell_counts[cell] >= target_per_cell for cell in TARGET_CELLS)


def expand_cells(
    target_per_cell: int,
    prime_count: int,
    block: int,
    starts: tuple[int, ...],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return expanded grammar-cell rows and a compact summary."""
    rows: list[dict[str, object]] = []
    cell_counts: Counter[tuple[str, str, str]] = Counter()
    candidate_count = 0
    seen_n: set[int] = set()

    prime_sets = [(start, primes_from(start, prime_count, block)) for start in starts]
    for left_index in range(prime_count):
        for pair_offset in PAIR_OFFSETS:
            for start, primes in prime_sets:
                right_index = left_index + pair_offset
                if right_index >= len(primes):
                    continue
                p_value = primes[left_index]
                q_value = primes[right_index]
                if p_value >= q_value:
                    continue
                n_value = p_value * q_value
                if n_value in seen_n:
                    continue
                seen_n.add(n_value)
                candidate_count += 1
                case = labeled_case(
                    f"cell_{n_value.bit_length()}_{start}_{left_index}_{pair_offset}",
                    p_value,
                    q_value,
                )
                public_row = public_row_from_labeled_case(case)
                key = cell_key(public_row)
                if key not in TARGET_CELLS or cell_counts[key] >= target_per_cell:
                    continue
                rows.append(
                    compatibility_row(case, public_row, start, left_index, pair_offset)
                )
                cell_counts[key] += 1
                if enough(cell_counts, target_per_cell):
                    return rows, summary(rows, cell_counts, candidate_count, target_per_cell)
    return rows, summary(rows, cell_counts, candidate_count, target_per_cell)


def cell_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return per-cell orientation counts."""
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["cell_key"])].append(row)
    output: list[dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        orientation_higher = {
            orientation: sum(1 for row in group if is_higher(str(row[orientation])))
            for orientation in ORIENTATIONS
        }
        output.append(
            {
                "rule_id": RULE_ID,
                "cell_key": key,
                "case_count": len(group),
                "orientation_higher_counts": orientation_higher,
                "outward_higher_count": (
                    orientation_higher["p_outward"] + orientation_higher["q_outward"]
                ),
                "inward_higher_count": (
                    orientation_higher["p_inward"] + orientation_higher["q_inward"]
                ),
                "case_ids": [str(row["case_id"]) for row in group],
            }
        )
    return output


def summary(
    rows: list[dict[str, object]],
    cell_counts: Counter[tuple[str, str, str]],
    candidate_count: int,
    target_per_cell: int,
) -> dict[str, object]:
    """Return compact expansion summary."""
    orientation_higher = {
        orientation: sum(1 for row in rows if is_higher(str(row[orientation])))
        for orientation in ORIENTATIONS
    }
    outward_higher = orientation_higher["p_outward"] + orientation_higher["q_outward"]
    inward_higher = orientation_higher["p_inward"] + orientation_higher["q_inward"]
    return {
        "rule_id": RULE_ID,
        "generated_case_count": len(rows),
        "candidate_count": candidate_count,
        "target_per_cell": target_per_cell,
        "target_cells": ["|".join(cell) for cell in TARGET_CELLS],
        "cell_counts": {
            "|".join(cell): cell_counts[cell]
            for cell in TARGET_CELLS
        },
        "underfilled_cells": [
            "|".join(cell)
            for cell in TARGET_CELLS
            if cell_counts[cell] < target_per_cell
        ],
        "orientation_higher_counts": orientation_higher,
        "outward_higher_count": outward_higher,
        "inward_higher_count": inward_higher,
        "outward_fraction": (
            None if outward_higher + inward_higher == 0 else outward_higher / (outward_higher + inward_higher)
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Expand high-signal grammar cells.")
    parser.add_argument(
        "--target-per-cell",
        type=int,
        default=10,
        help="Rows to collect per target cell.",
    )
    parser.add_argument(
        "--prime-count",
        type=int,
        default=160,
        help="PGS-discovered prime count per fixed start.",
    )
    parser.add_argument(
        "--block",
        type=int,
        default=8192,
        help="Exact divisor-count scan block.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_cell_expansion",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the target-cell expansion."""
    args = parse_args(argv)
    rows, payload = expand_cells(
        args.target_per_cell,
        args.prime_count,
        args.block,
        DEFAULT_STARTS,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "expanded_compatibility_rows.jsonl", rows)
    write_jsonl(args.output_dir / "cell_summary_rows.jsonl", cell_summary_rows(rows))
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
