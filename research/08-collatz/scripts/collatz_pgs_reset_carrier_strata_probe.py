"""Identify exact odd-step strata carrying the Collatz-PGS reset effect."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import (
    CLASS_NO_WITNESS,
    CLASS_WITNESS,
    matched_weighted_mean,
    median,
    percentile,
    rate,
    ratio,
    read_jsonl,
    write_json,
    write_jsonl,
)
from collatz_pgs_same_gap_scale_probe import V2_BINS, first_descent_block, v2_bin


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_reset_carrier_strata_probe"


class CarrierStats:
    """Collect reset and transition-composition values for one block class."""

    def __init__(self) -> None:
        self.reset_strengths: list[float] = []
        self.v2_sums: list[int] = []
        self.final_v2s: list[int] = []
        self.transition_count = 0
        self.v2_bin_counts: Counter[str] = Counter()

    def add(self, row: dict[str, object]) -> None:
        """Add one first-descent block row."""
        seed = int(row["seed"])
        odd_steps = int(row["odd_steps_to_first_descent"])
        transitions = first_descent_block(seed)
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")

        v2_values = [transition.v2 for transition in transitions]
        self.reset_strengths.append(float(row["reset_strength"]))
        self.v2_sums.append(sum(v2_values))
        self.final_v2s.append(v2_values[-1])
        self.transition_count += len(v2_values)
        for exponent in v2_values:
            self.v2_bin_counts[v2_bin(exponent)] += 1

    def record(self) -> dict[str, object]:
        """Return JSON-ready reset and transition-composition statistics."""
        count = len(self.reset_strengths)
        return {
            "count": count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "median_v2_sum": median(self.v2_sums),
            "mean_v2_sum": rate(sum(self.v2_sums), count),
            "median_final_v2": median(self.final_v2s),
            "final_v2_mode": integer_mode(self.final_v2s),
            "v2_bin_rates": {
                label: rate(self.v2_bin_counts[label], self.transition_count)
                for label in V2_BINS
            },
        }


def integer_mode(values: list[int]) -> int:
    """Return the smallest most frequent integer."""
    if not values:
        return 0
    counts = Counter(values)
    return min(value for value, count in counts.items() if count == max(counts.values()))


def load_strata(path: Path) -> dict[int, dict[str, CarrierStats]]:
    """Load block rows into exact odd-step carrier strata."""
    strata: dict[int, dict[str, CarrierStats]] = defaultdict(
        lambda: {
            CLASS_WITNESS: CarrierStats(),
            CLASS_NO_WITNESS: CarrierStats(),
        }
    )
    for row in read_jsonl(path):
        block_class = str(row["block_class"])
        if block_class not in (CLASS_WITNESS, CLASS_NO_WITNESS):
            raise ValueError(f"unknown block_class={block_class}")
        odd_steps = int(row["odd_steps_to_first_descent"])
        strata[odd_steps][block_class].add(row)
    return strata


def stratum_row(odd_steps: int, stats: dict[str, CarrierStats]) -> dict[str, object]:
    """Return one exact odd-step carrier row."""
    witness = stats[CLASS_WITNESS].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    median_reset_delta = (
        float(witness["median_reset_strength"])
        - float(no_witness["median_reset_strength"])
    )
    return {
        "odd_steps_to_first_descent": odd_steps,
        "witness_contact": witness,
        "no_witness_contact": no_witness,
        "has_both_classes": int(witness["count"]) > 0 and int(no_witness["count"]) > 0,
        "matched_weight": min(int(witness["count"]), int(no_witness["count"])),
        "median_reset_strength_delta": median_reset_delta,
        "median_reset_strength_ratio": ratio(
            float(witness["median_reset_strength"]),
            float(no_witness["median_reset_strength"]),
        ),
        "p90_reset_strength_delta": (
            float(witness["p90_reset_strength"])
            - float(no_witness["p90_reset_strength"])
        ),
        "mean_v2_sum_delta": (
            float(witness["mean_v2_sum"]) - float(no_witness["mean_v2_sum"])
        ),
        "v2_bin_rate_delta": {
            label: (
                float(witness["v2_bin_rates"][label])
                - float(no_witness["v2_bin_rates"][label])
            )
            for label in V2_BINS
        },
    }


def add_contributions(rows: list[dict[str, object]]) -> None:
    """Attach matched-weighted contribution fields to matched rows."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    for row in rows:
        weight = int(row["matched_weight"])
        row["matched_weight_share"] = rate(weight, total_weight)
        row["matched_weighted_mean_delta_contribution"] = (
            weight * float(row["median_reset_strength_delta"]) / total_weight
            if total_weight
            else 0.0
        )
        row["matched_weighted_mean_ratio_contribution"] = (
            weight * float(row["median_reset_strength_ratio"]) / total_weight
            if total_weight
            else 0.0
        )


def aggregate_rows(
    rows: list[dict[str, object]],
    total_weight: int,
) -> dict[str, object]:
    """Return matched-weighted aggregate facts for one row subset."""
    subset_weight = sum(int(row["matched_weight"]) for row in rows)
    return {
        "strata_count": len(rows),
        "matched_weight": subset_weight,
        "matched_weight_share": rate(subset_weight, total_weight),
        "weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            rows,
            "median_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_reset_ratio": matched_weighted_mean(
            rows,
            "median_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_mean_v2_sum_delta": matched_weighted_mean(
            rows,
            "mean_v2_sum_delta",
        ),
        "weighted_mean_of_stratum_v2_bin_rate_delta": {
            label: matched_weighted_v2_bin_rate_delta(rows, label)
            for label in V2_BINS
        },
    }


def matched_weighted_v2_bin_rate_delta(
    rows: list[dict[str, object]],
    label: str,
) -> float:
    """Return matched-weighted mean of one v2-bin rate delta."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row["v2_bin_rate_delta"][label])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def carrier_summary(row: dict[str, object]) -> dict[str, object]:
    """Return compact row fields for summary carrier lists."""
    return {
        "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
        "matched_weight": row["matched_weight"],
        "matched_weight_share": row["matched_weight_share"],
        "median_reset_strength_delta": row["median_reset_strength_delta"],
        "median_reset_strength_ratio": row["median_reset_strength_ratio"],
        "matched_weighted_mean_delta_contribution": row[
            "matched_weighted_mean_delta_contribution"
        ],
        "witness_mean_v2_sum": row[CLASS_WITNESS]["mean_v2_sum"],
        "no_witness_mean_v2_sum": row[CLASS_NO_WITNESS]["mean_v2_sum"],
        "mean_v2_sum_delta": row["mean_v2_sum_delta"],
        "v2_bin_rate_delta": row["v2_bin_rate_delta"],
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the carrier-strata probe."""
    strata = load_strata(input_path)
    rows = [
        stratum_row(odd_steps, strata[odd_steps])
        for odd_steps in sorted(strata)
    ]
    matched_rows = [row for row in rows if bool(row["has_both_classes"])]
    add_contributions(rows)

    favorable_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    unfavorable_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) < 0.0
    ]
    tied_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) == 0.0
    ]
    total_weight = sum(int(row["matched_weight"]) for row in matched_rows)
    positive_contribution = sum(
        float(row["matched_weighted_mean_delta_contribution"])
        for row in favorable_rows
    )
    negative_contribution = sum(
        float(row["matched_weighted_mean_delta_contribution"])
        for row in unfavorable_rows
    )

    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "strata_count": len(rows),
        "matched_strata_count": len(matched_rows),
        "matched_weight_total": total_weight,
        "favorable_strata_count": len(favorable_rows),
        "unfavorable_strata_count": len(unfavorable_rows),
        "tied_strata_count": len(tied_rows),
        "net_weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_delta",
        ),
        "net_weighted_mean_of_stratum_median_reset_ratio": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_ratio",
        ),
        "positive_delta_contribution_sum": positive_contribution,
        "negative_delta_contribution_sum": negative_contribution,
        "favorable_carrier_summary": aggregate_rows(favorable_rows, total_weight),
        "unfavorable_carrier_summary": aggregate_rows(unfavorable_rows, total_weight),
        "top_positive_delta_carriers": [
            carrier_summary(row)
            for row in sorted(
                favorable_rows,
                key=lambda item: float(item["matched_weighted_mean_delta_contribution"]),
                reverse=True,
            )[:10]
        ],
        "top_negative_delta_carriers": [
            carrier_summary(row)
            for row in sorted(
                unfavorable_rows,
                key=lambda item: float(item["matched_weighted_mean_delta_contribution"]),
            )[:10]
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "carrier_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Identify exact odd-step strata carrying the reset effect.",
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
