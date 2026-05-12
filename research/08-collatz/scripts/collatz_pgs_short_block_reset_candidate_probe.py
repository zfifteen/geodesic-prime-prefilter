"""Extract the exact short-block Collatz reset theorem candidate."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import (
    median,
    percentile,
    rate,
    read_jsonl,
    write_json,
    write_jsonl,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_first_descent_probe" / "block_rows.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_short_block_reset_candidate_probe"
TARGET_FINAL_V2 = (4, 8)

CLASS_BELOW = "below_minimizer_terminal"
CLASS_ABOVE = "above_minimizer_terminal"
CLASS_NO_WITNESS = "no_witness_contact"
CLASS_NONTERMINAL = "nonterminal_witness_contact"
CLASS_OTHER_TERMINAL = "other_terminal_minimizer_contact"


def v2(value: int) -> int:
    """Return the exponent of 2 in one positive integer."""
    return (value & -value).bit_length() - 1


def accelerated_odd_transition(source: int) -> tuple[int, int]:
    """Return the accelerated odd target and divided power of 2."""
    value = 3 * source + 1
    exponent = v2(value)
    return value >> exponent, exponent


def transition_exponents(seed: int, count: int) -> tuple[list[int], list[int], list[int]]:
    """Return sources, targets, and exponents for a fixed number of odd steps."""
    sources: list[int] = []
    targets: list[int] = []
    exponents: list[int] = []
    current = seed
    for _ in range(count):
        target, exponent = accelerated_odd_transition(current)
        sources.append(current)
        targets.append(target)
        exponents.append(exponent)
        current = target
    return sources, targets, exponents


def inverse_seed_from_terminal(terminal_source: int, middle_v2: int) -> int | None:
    """Return the exact 3-step seed with first v2=1 and given middle v2."""
    middle_numerator = (1 << middle_v2) * terminal_source - 1
    if middle_numerator % 3 != 0:
        return None
    middle_source = middle_numerator // 3
    seed_numerator = 2 * middle_source - 1
    if seed_numerator % 3 != 0:
        return None
    return seed_numerator // 3


def asymptotic_reset_strength(final_v2: int, middle_v2: int) -> float:
    """Return the large-terminal-source limit for exact 3-step reset strength."""
    return (1 << (final_v2 + middle_v2 + 1)) / 27.0


def exact_reset_formula(terminal_source: int, final_v2: int, middle_v2: int) -> float:
    """Return the exact reset strength forced by a 3-step inverse branch."""
    seed = inverse_seed_from_terminal(terminal_source, middle_v2)
    if seed is None:
        return 0.0
    terminal_target = (3 * terminal_source + 1) >> final_v2
    return seed / terminal_target


def below_residue_exact(witness: int, final_v2: int) -> bool:
    """Return whether w satisfies exact below-minimizer final-v2 residue."""
    return v2(3 * witness - 2) == final_v2


def terminal_class(row: dict[str, object]) -> str:
    """Return the terminal/minimizer contact class for one block row."""
    final_source = int(row["final_source"])
    witness = int(row["final_witness"])
    if (
        not bool(row["final_is_prime"])
        and bool(row["final_odd_projected_witness_hit"])
        and final_source == witness - 1
    ):
        return CLASS_BELOW
    if (
        not bool(row["final_is_prime"])
        and bool(row["final_odd_projected_witness_hit"])
        and final_source == witness + 1
    ):
        return CLASS_ABOVE
    if int(row["source_interior_odd_projected_witness_hit_count"]) == 0:
        return CLASS_NO_WITNESS
    if bool(row["final_odd_projected_witness_hit"]):
        return CLASS_OTHER_TERMINAL
    return CLASS_NONTERMINAL


def compact_counter(counter: Counter[int] | Counter[str]) -> dict[str, int]:
    """Return a sorted JSON-ready counter."""
    return {str(key): counter[key] for key in sorted(counter)}


def bin_gap_width(width: int) -> str:
    """Return a compact gap-width bin."""
    if width <= 16:
        return str(width)
    if width <= 32:
        return "18-32"
    if width <= 64:
        return "34-64"
    return ">=66"


def row_record(row: dict[str, object]) -> dict[str, object] | None:
    """Return a theorem-candidate row or None for rows outside the target."""
    if int(row["odd_steps_to_first_descent"]) != 3:
        return None
    final_v2 = int(row["final_v2"])
    if final_v2 not in TARGET_FINAL_V2:
        return None

    seed = int(row["seed"])
    sources, targets, exponents = transition_exponents(seed, 3)
    terminal_source = int(row["final_source"])
    terminal_target = int(row["terminal_below_seed"])
    if sources[-1] != terminal_source or targets[-1] != terminal_target:
        raise ValueError(f"row transition mismatch for seed {seed}")

    first_v2, middle_v2, recomputed_final_v2 = exponents
    if recomputed_final_v2 != final_v2:
        raise ValueError(f"final v2 mismatch for seed {seed}")

    witness = int(row["final_witness"])
    reset_strength = seed / terminal_target
    formula_seed = inverse_seed_from_terminal(terminal_source, middle_v2)
    formula_reset = exact_reset_formula(terminal_source, final_v2, middle_v2)
    class_label = terminal_class(row)
    asymptote = asymptotic_reset_strength(final_v2, middle_v2)

    return {
        "seed": seed,
        "first_v2": first_v2,
        "middle_v2": middle_v2,
        "final_v2": final_v2,
        "final_source": terminal_source,
        "terminal_target": terminal_target,
        "final_witness": witness,
        "terminal_class": class_label,
        "reset_strength": reset_strength,
        "branch_asymptotic_reset_strength": asymptote,
        "reset_gap_to_asymptote": asymptote - reset_strength,
        "formula_seed": formula_seed,
        "formula_seed_ok": formula_seed == seed,
        "formula_reset_strength": formula_reset,
        "formula_reset_ok": abs(formula_reset - reset_strength) < 1.0e-12,
        "first_two_sources_not_below_seed": targets[0] >= seed and targets[1] >= seed,
        "terminal_target_below_seed": terminal_target < seed,
        "final_gap_width": int(row["final_gap_width"]),
        "gap_width_bin": bin_gap_width(int(row["final_gap_width"])),
        "final_prev_prime": int(row["final_prev_prime"]),
        "final_next_prime": int(row["final_next_prime"]),
        "witness_mod9": witness % 9,
        "witness_even": witness % 2 == 0,
        "below_residue_exact_for_final_v2": below_residue_exact(witness, final_v2),
        "source_witness_hit_count": int(
            row["source_interior_odd_projected_witness_hit_count"],
        ),
    }


class VectorStats:
    """Collect reset statistics for a record group."""

    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []

    def add(self, record: dict[str, object]) -> None:
        """Add one target record."""
        self.records.append(record)

    def summary(self) -> dict[str, object]:
        """Return JSON-ready group statistics."""
        resets = [float(record["reset_strength"]) for record in self.records]
        gaps = [int(record["final_gap_width"]) for record in self.records]
        first_v2 = Counter(int(record["first_v2"]) for record in self.records)
        middle_v2 = Counter(int(record["middle_v2"]) for record in self.records)
        witness_mod9 = Counter(int(record["witness_mod9"]) for record in self.records)
        return {
            "count": len(self.records),
            "median_reset_strength": median(resets),
            "p90_reset_strength": percentile(resets, 0.90),
            "p99_reset_strength": percentile(resets, 0.99),
            "min_reset_strength": min(resets) if resets else 0.0,
            "max_reset_strength": max(resets) if resets else 0.0,
            "median_gap_width": median(gaps),
            "first_v2_distribution": compact_counter(first_v2),
            "middle_v2_distribution": compact_counter(middle_v2),
            "witness_mod9_distribution": compact_counter(witness_mod9),
            "formula_seed_ok_rate": rate(
                sum(bool(record["formula_seed_ok"]) for record in self.records),
                len(self.records),
            ),
            "formula_reset_ok_rate": rate(
                sum(bool(record["formula_reset_ok"]) for record in self.records),
                len(self.records),
            ),
        }


def grouped_rows(
    records: list[dict[str, object]],
    key_names: tuple[str, ...],
) -> list[dict[str, object]]:
    """Return summaries grouped by selected record fields."""
    groups: dict[tuple[object, ...], VectorStats] = defaultdict(VectorStats)
    for record in records:
        groups[tuple(record[key] for key in key_names)].add(record)

    rows: list[dict[str, object]] = []
    for key in sorted(groups):
        summary = groups[key].summary()
        for index, key_name in enumerate(key_names):
            summary[key_name] = key[index]
        rows.append(summary)
    return rows


def median_comparison(
    records: list[dict[str, object]],
    left_class: str,
    right_class: str,
    final_v2: int,
    middle_v2: int | None,
) -> dict[str, object]:
    """Return one median reset comparison."""
    left = [
        float(record["reset_strength"])
        for record in records
        if record["terminal_class"] == left_class
        and int(record["final_v2"]) == final_v2
        and (middle_v2 is None or int(record["middle_v2"]) == middle_v2)
    ]
    right = [
        float(record["reset_strength"])
        for record in records
        if record["terminal_class"] == right_class
        and int(record["final_v2"]) == final_v2
        and (middle_v2 is None or int(record["middle_v2"]) == middle_v2)
    ]
    left_median = median(left)
    right_median = median(right)
    return {
        "left_class": left_class,
        "right_class": right_class,
        "final_v2": final_v2,
        "middle_v2": middle_v2 if middle_v2 is not None else "all",
        "left_count": len(left),
        "right_count": len(right),
        "left_median_reset_strength": left_median,
        "right_median_reset_strength": right_median,
        "median_reset_strength_delta": left_median - right_median,
        "median_reset_strength_ratio": left_median / right_median
        if right_median
        else 0.0,
    }


def unique_gap_records(input_path: Path) -> list[dict[str, object]]:
    """Return unique final-source prime gaps from the block table."""
    gaps: dict[tuple[int, int], dict[str, object]] = {}
    for row in read_jsonl(input_path):
        width = int(row["final_gap_width"])
        if width == 0:
            continue
        key = (int(row["final_prev_prime"]), int(row["final_next_prime"]))
        if key in gaps:
            continue
        witness = int(row["final_witness"])
        record = {
            "final_prev_prime": key[0],
            "final_next_prime": key[1],
            "gap_width": width,
            "gap_width_bin": bin_gap_width(width),
            "witness": witness,
            "witness_mod9": witness % 9,
            "witness_even": witness % 2 == 0,
        }
        for final_v2 in TARGET_FINAL_V2:
            record[f"below_residue_exact_v2_{final_v2}"] = below_residue_exact(
                witness,
                final_v2,
            )
        gaps[key] = record
    return list(gaps.values())


def residue_bias_summary(gaps: list[dict[str, object]]) -> dict[str, object]:
    """Return independent residue rates for unique visited prime gaps."""
    even_count = sum(bool(gap["witness_even"]) for gap in gaps)
    by_k: dict[str, object] = {}
    for final_v2 in TARGET_FINAL_V2:
        field = f"below_residue_exact_v2_{final_v2}"
        exact_count = sum(bool(gap[field]) for gap in gaps)
        exact_even_count = sum(
            bool(gap[field]) and bool(gap["witness_even"]) for gap in gaps
        )
        by_k[str(final_v2)] = {
            "exact_residue_gap_count": exact_count,
            "exact_residue_gap_rate": rate(exact_count, len(gaps)),
            "exact_residue_even_minimizer_count": exact_even_count,
            "exact_residue_rate_among_even_minimizers": rate(
                exact_even_count,
                even_count,
            ),
        }
    return {
        "unique_gap_count": len(gaps),
        "even_minimizer_count": even_count,
        "even_minimizer_rate": rate(even_count, len(gaps)),
        "by_final_v2": by_k,
    }


def residue_gap_width_rows(gaps: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return residue rates by gap-width bin."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for gap in gaps:
        groups[str(gap["gap_width_bin"])].append(gap)

    rows: list[dict[str, object]] = []
    for gap_bin in sorted(groups):
        group = groups[gap_bin]
        record: dict[str, object] = {
            "gap_width_bin": gap_bin,
            "unique_gap_count": len(group),
            "even_minimizer_rate": rate(
                sum(bool(gap["witness_even"]) for gap in group),
                len(group),
            ),
        }
        for final_v2 in TARGET_FINAL_V2:
            field = f"below_residue_exact_v2_{final_v2}"
            record[f"exact_residue_v2_{final_v2}_rate"] = rate(
                sum(bool(gap[field]) for gap in group),
                len(group),
            )
            record[f"exact_residue_v2_{final_v2}_count"] = sum(
                bool(gap[field]) for gap in group
            )
        rows.append(record)
    return rows


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the short-block reset theorem-candidate probe."""
    records = [
        record
        for row in read_jsonl(input_path)
        if (record := row_record(row)) is not None
    ]
    gaps = unique_gap_records(input_path)
    class_rows = grouped_rows(records, ("final_v2", "terminal_class"))
    branch_rows = grouped_rows(records, ("final_v2", "middle_v2", "terminal_class"))
    gap_width_rows = grouped_rows(
        records,
        ("final_v2", "gap_width_bin", "terminal_class"),
    )
    residue_width_rows = residue_gap_width_rows(gaps)
    below_records = [
        record for record in records if record["terminal_class"] == CLASS_BELOW
    ]
    comparisons = [
        median_comparison(records, CLASS_BELOW, CLASS_NO_WITNESS, final_v2, None)
        for final_v2 in TARGET_FINAL_V2
    ]
    comparisons.extend(
        median_comparison(records, CLASS_BELOW, CLASS_NO_WITNESS, final_v2, 2)
        for final_v2 in TARGET_FINAL_V2
    )

    first_v2_distribution = Counter(int(record["first_v2"]) for record in records)
    middle_v2_distribution = Counter(int(record["middle_v2"]) for record in records)
    below_witness_mod9 = Counter(int(record["witness_mod9"]) for record in below_records)
    below_middle_v2 = Counter(int(record["middle_v2"]) for record in below_records)
    formula_seed_failures = [
        record["seed"] for record in records if not bool(record["formula_seed_ok"])
    ]
    formula_reset_failures = [
        record["seed"] for record in records if not bool(record["formula_reset_ok"])
    ]

    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "target_odd_steps_to_first_descent": 3,
        "target_final_v2": list(TARGET_FINAL_V2),
        "target_row_count": len(records),
        "exponent_law": {
            "first_v2_distribution": compact_counter(first_v2_distribution),
            "middle_v2_distribution": compact_counter(middle_v2_distribution),
            "first_v2_all_one": set(first_v2_distribution) == {1},
            "middle_v2_only_one_or_two": set(middle_v2_distribution).issubset({1, 2}),
            "formula_seed_failure_count": len(formula_seed_failures),
            "formula_reset_failure_count": len(formula_reset_failures),
            "formula_seed_failure_examples": formula_seed_failures[:10],
            "formula_reset_failure_examples": formula_reset_failures[:10],
        },
        "below_minimizer_target": {
            "count": len(below_records),
            "final_v2_distribution": compact_counter(
                Counter(int(record["final_v2"]) for record in below_records),
            ),
            "middle_v2_distribution": compact_counter(below_middle_v2),
            "witness_mod9_distribution": compact_counter(below_witness_mod9),
            "exact_residue_rate": rate(
                sum(
                    bool(record["below_residue_exact_for_final_v2"])
                    for record in below_records
                ),
                len(below_records),
            ),
            "all_observed_below_rows_are_middle_v2_2": set(below_middle_v2) == {2},
            "all_observed_below_rows_have_witness_mod9_5": set(below_witness_mod9)
            == {5},
        },
        "median_comparisons": comparisons,
        "class_summary": class_rows,
        "branch_summary": branch_rows,
        "gap_width_summary": gap_width_rows,
        "independent_residue_bias": residue_bias_summary(gaps),
        "theorem_candidate": {
            "branch_1_condition": "witness_mod9 == 0 gives middle_v2 == 1",
            "branch_1_seed": "s=(4*w-9)/9 for below-minimizer terminal source n=w-1",
            "branch_1_reset": "R=2^k*(4*w-9)/(9*(3*w-2))",
            "branch_1_asymptote": "2^(k+2)/27",
            "branch_2_condition": "witness_mod9 == 5 gives middle_v2 == 2",
            "branch_2_seed": "s=(8*w-13)/9 for below-minimizer terminal source n=w-1",
            "branch_2_reset": "R=2^k*(8*w-13)/(9*(3*w-2))",
            "branch_2_asymptote": "2^(k+3)/27",
            "current_positive_carrier": (
                "At final_v2 4 and 8, every observed below-minimizer exact "
                "3-step row is branch 2."
            ),
            "current_obstruction": (
                "Inside fixed final_v2 and fixed middle_v2, the reset formula "
                "is the ordinary exact 3-step Collatz formula; the measured "
                "advantage is branch selection before it is a new within-branch "
                "reset law."
            ),
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(records, output_dir / "target_rows.jsonl")
    write_jsonl(class_rows, output_dir / "class_rows.jsonl")
    write_jsonl(branch_rows, output_dir / "branch_rows.jsonl")
    write_jsonl(gap_width_rows, output_dir / "gap_width_rows.jsonl")
    write_jsonl(residue_width_rows, output_dir / "residue_gap_width_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Extract exact 3-step final-v2 4/8 reset branches for the "
            "below-minimizer terminal Collatz family."
        ),
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    """Run the command-line probe."""
    args = parse_args()
    summary = run_probe(Path(args.input), Path(args.output_dir))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
