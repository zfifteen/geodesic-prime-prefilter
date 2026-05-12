"""Measure sign and tail stability for below-witness terminal contact."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import (
    median,
    percentile,
    rate,
    ratio,
    read_jsonl,
    write_json,
    write_jsonl,
)
from collatz_pgs_same_gap_scale_probe import PrimeContext, first_descent_block
from collatz_pgs_terminal_adjacent_side_probe import (
    CLASS_ABOVE_WITNESS,
    CLASS_BELOW_WITNESS,
    terminal_side_class,
)
from collatz_pgs_terminal_contact_decomposition_probe import (
    CLASS_NO_WITNESS,
    max_source_in_rows,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_below_witness_stability_probe"
MATCHED_CLASSES = (
    CLASS_BELOW_WITNESS,
    CLASS_ABOVE_WITNESS,
    CLASS_NO_WITNESS,
)


class ResetStats:
    """Collect reset values for one block class."""

    def __init__(self) -> None:
        self.reset_strengths: list[float] = []
        self.max_source_over_seed_values: list[float] = []

    def add(self, row: dict[str, object]) -> None:
        """Add one block row."""
        self.reset_strengths.append(float(row["reset_strength"]))
        self.max_source_over_seed_values.append(float(row["max_source_over_seed"]))

    def record(self) -> dict[str, object]:
        """Return JSON-ready reset statistics."""
        return {
            "count": len(self.reset_strengths),
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "p99_reset_strength": percentile(self.reset_strengths, 0.99),
            "median_max_source_over_seed": median(self.max_source_over_seed_values),
        }


def sign_test_two_sided(positive_count: int, negative_count: int) -> float:
    """Return an exact two-sided sign-test p-value."""
    total = positive_count + negative_count
    if total == 0:
        return 1.0
    cutoff = min(positive_count, negative_count)
    tail = sum(math.comb(total, index) for index in range(cutoff + 1))
    return min(1.0, 2.0 * tail / (2**total))


def load_strata(path: Path, context: PrimeContext):
    """Load rows into exact odd-step and final-v2 strata."""
    strata = defaultdict(lambda: {label: ResetStats() for label in MATCHED_CLASSES})
    class_counts = {label: 0 for label in MATCHED_CLASSES}

    for row in read_jsonl(path):
        seed = int(row["seed"])
        transitions = first_descent_block(seed)
        odd_steps = int(row["odd_steps_to_first_descent"])
        final_v2 = transitions[-1].v2
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")
        if "final_v2" in row and int(row["final_v2"]) != final_v2:
            raise ValueError(f"seed={seed} final-v2 mismatch")

        block_class = terminal_side_class(transitions, context)
        if block_class not in MATCHED_CLASSES:
            continue
        class_counts[block_class] += 1
        strata[(odd_steps, final_v2)][block_class].add(row)

    return strata, class_counts


def comparison(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    """Return one exact-matched two-class comparison."""
    left_count = int(left["count"])
    right_count = int(right["count"])
    median_delta = (
        float(left["median_reset_strength"]) - float(right["median_reset_strength"])
    )
    p90_delta = float(left["p90_reset_strength"]) - float(right["p90_reset_strength"])
    p99_delta = float(left["p99_reset_strength"]) - float(right["p99_reset_strength"])
    return {
        "has_both_classes": left_count > 0 and right_count > 0,
        "matched_weight": min(left_count, right_count),
        "left_count": left_count,
        "right_count": right_count,
        "median_reset_strength_delta": median_delta,
        "median_reset_strength_ratio": ratio(
            float(left["median_reset_strength"]),
            float(right["median_reset_strength"]),
        ),
        "p90_reset_strength_delta": p90_delta,
        "p90_reset_strength_ratio": ratio(
            float(left["p90_reset_strength"]),
            float(right["p90_reset_strength"]),
        ),
        "p99_reset_strength_delta": p99_delta,
        "p99_reset_strength_ratio": ratio(
            float(left["p99_reset_strength"]),
            float(right["p99_reset_strength"]),
        ),
        "median_max_source_over_seed_delta": (
            float(left["median_max_source_over_seed"])
            - float(right["median_max_source_over_seed"])
        ),
    }


def stratum_row(key: tuple[int, int], stats: dict[str, ResetStats]) -> dict[str, object]:
    """Return one exact-step and final-v2 stability row."""
    below = stats[CLASS_BELOW_WITNESS].record()
    above = stats[CLASS_ABOVE_WITNESS].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    return {
        "odd_steps_to_first_descent": key[0],
        "final_v2": key[1],
        CLASS_BELOW_WITNESS: below,
        CLASS_ABOVE_WITNESS: above,
        CLASS_NO_WITNESS: no_witness,
        "below_vs_no_witness": comparison(below, no_witness),
        "below_vs_above": comparison(below, above),
    }


def matched_rows(
    rows: list[dict[str, object]],
    comparison_name: str,
) -> list[dict[str, object]]:
    """Return flattened matched rows for one comparison."""
    flattened: list[dict[str, object]] = []
    for row in rows:
        comparison_row = row[comparison_name]
        if not bool(comparison_row["has_both_classes"]):
            continue
        flattened.append(
            {
                "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
                "final_v2": row["final_v2"],
                **comparison_row,
            }
        )

    total_weight = sum(int(row["matched_weight"]) for row in flattened)
    for row in flattened:
        row["matched_weight_share"] = rate(int(row["matched_weight"]), total_weight)
        row["matched_weighted_mean_of_stratum_median_delta_contribution"] = (
            int(row["matched_weight"])
            * float(row["median_reset_strength_delta"])
            / total_weight
            if total_weight
            else 0.0
        )
    return flattened


def weighted_mean(rows: list[dict[str, object]], field: str) -> float:
    """Return matched-weighted mean for one field."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row[field])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def signed_field_summary(
    rows: list[dict[str, object]],
    field: str,
) -> dict[str, object]:
    """Return sign and matched-weight facts for one delta field."""
    positive_rows = [row for row in rows if float(row[field]) > 0.0]
    negative_rows = [row for row in rows if float(row[field]) < 0.0]
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    positive_weight = sum(int(row["matched_weight"]) for row in positive_rows)
    negative_weight = sum(int(row["matched_weight"]) for row in negative_rows)
    return {
        "positive_strata_count": len(positive_rows),
        "negative_strata_count": len(negative_rows),
        "tied_strata_count": len(rows) - len(positive_rows) - len(negative_rows),
        "positive_matched_weight": positive_weight,
        "negative_matched_weight": negative_weight,
        "positive_matched_weight_share": rate(positive_weight, total_weight),
        "negative_matched_weight_share": rate(negative_weight, total_weight),
        "two_sided_sign_test_p": sign_test_two_sided(
            len(positive_rows),
            len(negative_rows),
        ),
        "weighted_mean_delta": weighted_mean(rows, field),
    }


def comparison_summary(
    rows: list[dict[str, object]],
    comparison_name: str,
) -> dict[str, object]:
    """Return sign and tail stability facts for one comparison."""
    comparison_rows = matched_rows(rows, comparison_name)
    positive_rows = [
        row for row in comparison_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    negative_rows = [
        row for row in comparison_rows if float(row["median_reset_strength_delta"]) < 0.0
    ]
    return {
        "matched_strata_count": len(comparison_rows),
        "matched_weight_total": sum(
            int(row["matched_weight"]) for row in comparison_rows
        ),
        "median_delta_sign": signed_field_summary(
            comparison_rows,
            "median_reset_strength_delta",
        ),
        "p90_delta_sign": signed_field_summary(
            comparison_rows,
            "p90_reset_strength_delta",
        ),
        "p99_delta_sign": signed_field_summary(
            comparison_rows,
            "p99_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_reset_ratio": weighted_mean(
            comparison_rows,
            "median_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_p90_reset_ratio": weighted_mean(
            comparison_rows,
            "p90_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_p99_reset_ratio": weighted_mean(
            comparison_rows,
            "p99_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_median_max_source_over_seed_delta": weighted_mean(
            comparison_rows,
            "median_max_source_over_seed_delta",
        ),
        "top_positive_median_delta_strata": sorted(
            positive_rows,
            key=lambda row: float(
                row["matched_weighted_mean_of_stratum_median_delta_contribution"]
            ),
            reverse=True,
        )[:10],
        "top_negative_median_delta_strata": sorted(
            negative_rows,
            key=lambda row: float(
                row["matched_weighted_mean_of_stratum_median_delta_contribution"]
            ),
        )[:10],
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the below-witness stability probe."""
    context = PrimeContext(max_source_in_rows(input_path))
    strata, class_counts = load_strata(input_path, context)
    rows = [stratum_row(key, strata[key]) for key in sorted(strata)]
    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "strata_count": len(rows),
        "class_counts": class_counts,
        "below_vs_no_witness": comparison_summary(rows, "below_vs_no_witness"),
        "below_vs_above": comparison_summary(rows, "below_vs_above"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "stability_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Measure below-witness terminal sign and tail stability inside "
            "exact odd-step and final-v2 strata."
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
