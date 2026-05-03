"""Measure source-position patterns inside Collatz-PGS carrier strata."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import (
    CLASS_NO_WITNESS,
    CLASS_WITNESS,
    median,
    percentile,
    rate,
    ratio,
    read_jsonl,
    write_json,
    write_jsonl,
)
from collatz_pgs_same_gap_scale_probe import (
    V2_BINS,
    PrimeContext,
    first_descent_block,
    v2_bin,
)


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_source_position_carrier_probe"


class PositionStats:
    """Collect source-position values for one exact-step block class."""

    def __init__(self) -> None:
        self.count = 0
        self.total_source_count = 0
        self.total_composite_source_count = 0
        self.blocks_with_composite_count = 0
        self.blocks_with_witness_hit_count = 0
        self.first_source_witness_hit_count = 0
        self.final_source_witness_hit_count = 0
        self.final_closest_source_count = 0
        self.source_witness_hit_count = 0
        self.exact_witness_hit_count = 0
        self.reset_strengths: list[float] = []
        self.composite_source_counts: list[int] = []
        self.min_odd_witness_distances: list[int] = []
        self.closest_index_fractions: list[float] = []
        self.first_hit_indexes: list[int] = []
        self.first_hit_fractions: list[float] = []
        self.last_hit_fractions: list[float] = []
        self.final_v2s: list[int] = []
        self.v2_sums: list[int] = []
        self.hit_source_over_seed_values: list[float] = []
        self.hit_gap_offset_fractions: list[float] = []
        self.hit_index_counts: Counter[str] = Counter()
        self.hit_v2_bin_counts: Counter[str] = Counter()

    def add(self, row: dict[str, object], context: PrimeContext) -> None:
        """Add one first-descent block row."""
        seed = int(row["seed"])
        odd_steps = int(row["odd_steps_to_first_descent"])
        transitions = first_descent_block(seed)
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")

        self.count += 1
        self.total_source_count += len(transitions)
        self.reset_strengths.append(float(row["reset_strength"]))
        self.final_v2s.append(transitions[-1].v2)
        self.v2_sums.append(sum(transition.v2 for transition in transitions))

        composite_count = 0
        min_distance = 0
        closest_index = 0
        hit_indexes: list[int] = []
        for index, transition in enumerate(transitions, start=1):
            state = context.source_state(transition.source)
            if state.is_prime:
                continue

            composite_count += 1
            distance = int(state.odd_witness_distance)
            if closest_index == 0 or distance < min_distance:
                min_distance = distance
                closest_index = index

            if not state.odd_projected_witness_hit:
                continue

            hit_indexes.append(index)
            self.source_witness_hit_count += 1
            self.hit_index_counts[str(index)] += 1
            self.hit_v2_bin_counts[v2_bin(transition.v2)] += 1
            self.hit_source_over_seed_values.append(transition.source / seed)
            self.hit_gap_offset_fractions.append(state.gap_offset / state.gap_width)
            if state.n == state.witness:
                self.exact_witness_hit_count += 1

        self.total_composite_source_count += composite_count
        self.composite_source_counts.append(composite_count)
        if composite_count:
            self.blocks_with_composite_count += 1
            self.min_odd_witness_distances.append(min_distance)
            self.closest_index_fractions.append(closest_index / odd_steps)
            if closest_index == odd_steps:
                self.final_closest_source_count += 1

        if hit_indexes:
            self.blocks_with_witness_hit_count += 1
            first_hit = hit_indexes[0]
            last_hit = hit_indexes[-1]
            self.first_hit_indexes.append(first_hit)
            self.first_hit_fractions.append(first_hit / odd_steps)
            self.last_hit_fractions.append(last_hit / odd_steps)
            if first_hit == 1:
                self.first_source_witness_hit_count += 1
            if last_hit == odd_steps:
                self.final_source_witness_hit_count += 1

    def record(self) -> dict[str, object]:
        """Return JSON-ready source-position statistics."""
        return {
            "count": self.count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "median_final_v2": median(self.final_v2s),
            "final_v2_mode": integer_mode(self.final_v2s),
            "mean_v2_sum": rate(sum(self.v2_sums), self.count),
            "median_composite_source_count": median(self.composite_source_counts),
            "source_composite_rate": rate(
                self.total_composite_source_count,
                self.total_source_count,
            ),
            "blocks_with_composite_rate": rate(
                self.blocks_with_composite_count,
                self.count,
            ),
            "source_witness_hit_rate": rate(
                self.source_witness_hit_count,
                self.total_composite_source_count,
            ),
            "blocks_with_witness_hit_rate": rate(
                self.blocks_with_witness_hit_count,
                self.count,
            ),
            "first_source_witness_hit_rate": rate(
                self.first_source_witness_hit_count,
                self.count,
            ),
            "final_source_witness_hit_rate": rate(
                self.final_source_witness_hit_count,
                self.count,
            ),
            "median_first_hit_index": median(self.first_hit_indexes),
            "median_first_hit_fraction": median(self.first_hit_fractions),
            "median_last_hit_fraction": median(self.last_hit_fractions),
            "median_min_odd_witness_distance": median(
                self.min_odd_witness_distances,
            ),
            "median_closest_index_fraction": median(self.closest_index_fractions),
            "final_closest_source_rate": rate(
                self.final_closest_source_count,
                self.blocks_with_composite_count,
            ),
            "exact_witness_hit_rate": rate(
                self.exact_witness_hit_count,
                self.source_witness_hit_count,
            ),
            "median_hit_source_over_seed": median(self.hit_source_over_seed_values),
            "median_hit_gap_offset_fraction": median(self.hit_gap_offset_fractions),
            "hit_v2_bin_rates": {
                label: rate(self.hit_v2_bin_counts[label], self.source_witness_hit_count)
                for label in V2_BINS
            },
            "hit_index_rates": {
                key: rate(self.hit_index_counts[key], self.source_witness_hit_count)
                for key in sorted(self.hit_index_counts, key=int)
            },
        }


def integer_mode(values: list[int]) -> int:
    """Return the smallest most frequent integer."""
    if not values:
        return 0
    counts = Counter(values)
    top_count = max(counts.values())
    return min(value for value, count in counts.items() if count == top_count)


def max_source_in_rows(path: Path) -> int:
    """Return the maximum source value reported by the block rows."""
    max_source = 3
    for row in read_jsonl(path):
        max_source = max(max_source, int(row["max_source"]))
    return max_source


def load_strata(path: Path, context: PrimeContext) -> dict[int, dict[str, PositionStats]]:
    """Load block rows into exact odd-step source-position strata."""
    strata: dict[int, dict[str, PositionStats]] = defaultdict(
        lambda: {
            CLASS_WITNESS: PositionStats(),
            CLASS_NO_WITNESS: PositionStats(),
        }
    )
    for row in read_jsonl(path):
        block_class = str(row["block_class"])
        if block_class not in (CLASS_WITNESS, CLASS_NO_WITNESS):
            raise ValueError(f"unknown block_class={block_class}")
        odd_steps = int(row["odd_steps_to_first_descent"])
        strata[odd_steps][block_class].add(row, context)
    return strata


def stratum_row(odd_steps: int, stats: dict[str, PositionStats]) -> dict[str, object]:
    """Return one exact-step source-position comparison row."""
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
        "median_final_v2_delta": (
            float(witness["median_final_v2"]) - float(no_witness["median_final_v2"])
        ),
        "final_source_witness_hit_rate_delta": (
            float(witness["final_source_witness_hit_rate"])
            - float(no_witness["final_source_witness_hit_rate"])
        ),
        "first_source_witness_hit_rate_delta": (
            float(witness["first_source_witness_hit_rate"])
            - float(no_witness["first_source_witness_hit_rate"])
        ),
        "median_min_odd_witness_distance_delta": (
            float(witness["median_min_odd_witness_distance"])
            - float(no_witness["median_min_odd_witness_distance"])
        ),
        "final_closest_source_rate_delta": (
            float(witness["final_closest_source_rate"])
            - float(no_witness["final_closest_source_rate"])
        ),
    }


def matched_weighted_mean(rows: list[dict[str, object]], field: str) -> float:
    """Return matched-weighted mean for one stratum field."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row[field])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def matched_weighted_class_mean(
    rows: list[dict[str, object]],
    class_name: str,
    field: str,
) -> float:
    """Return matched-weighted mean for one nested class field."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row[class_name][field])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def add_weight_shares(rows: list[dict[str, object]]) -> None:
    """Attach matched-weight shares to rows."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    for row in rows:
        row["matched_weight_share"] = rate(int(row["matched_weight"]), total_weight)


def aggregate_rows(
    rows: list[dict[str, object]],
    total_weight: int,
) -> dict[str, object]:
    """Return matched-weighted source-position aggregate facts."""
    subset_weight = sum(int(row["matched_weight"]) for row in rows)
    return {
        "strata_count": len(rows),
        "matched_weight": subset_weight,
        "matched_weight_share": rate(subset_weight, total_weight),
        "weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            rows,
            "median_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_final_v2_delta": matched_weighted_mean(
            rows,
            "median_final_v2_delta",
        ),
        "weighted_mean_witness_final_source_witness_hit_rate": (
            matched_weighted_class_mean(
                rows,
                CLASS_WITNESS,
                "final_source_witness_hit_rate",
            )
        ),
        "weighted_mean_witness_first_source_witness_hit_rate": (
            matched_weighted_class_mean(
                rows,
                CLASS_WITNESS,
                "first_source_witness_hit_rate",
            )
        ),
        "weighted_mean_witness_median_first_hit_fraction": (
            matched_weighted_class_mean(
                rows,
                CLASS_WITNESS,
                "median_first_hit_fraction",
            )
        ),
        "weighted_mean_witness_median_hit_gap_offset_fraction": (
            matched_weighted_class_mean(
                rows,
                CLASS_WITNESS,
                "median_hit_gap_offset_fraction",
            )
        ),
        "weighted_mean_witness_exact_witness_hit_rate": (
            matched_weighted_class_mean(
                rows,
                CLASS_WITNESS,
                "exact_witness_hit_rate",
            )
        ),
        "weighted_mean_no_witness_median_min_odd_witness_distance": (
            matched_weighted_class_mean(
                rows,
                CLASS_NO_WITNESS,
                "median_min_odd_witness_distance",
            )
        ),
    }


def carrier_summary(row: dict[str, object]) -> dict[str, object]:
    """Return compact source-position fields for summary carrier lists."""
    witness = row[CLASS_WITNESS]
    no_witness = row[CLASS_NO_WITNESS]
    return {
        "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
        "matched_weight": row["matched_weight"],
        "matched_weight_share": row["matched_weight_share"],
        "median_reset_strength_delta": row["median_reset_strength_delta"],
        "median_final_v2_delta": row["median_final_v2_delta"],
        "witness_final_source_witness_hit_rate": witness[
            "final_source_witness_hit_rate"
        ],
        "witness_first_source_witness_hit_rate": witness[
            "first_source_witness_hit_rate"
        ],
        "witness_median_first_hit_fraction": witness["median_first_hit_fraction"],
        "witness_median_last_hit_fraction": witness["median_last_hit_fraction"],
        "witness_median_hit_gap_offset_fraction": witness[
            "median_hit_gap_offset_fraction"
        ],
        "witness_exact_witness_hit_rate": witness["exact_witness_hit_rate"],
        "witness_hit_index_rates": witness["hit_index_rates"],
        "witness_hit_v2_bin_rates": witness["hit_v2_bin_rates"],
        "no_witness_median_min_odd_witness_distance": no_witness[
            "median_min_odd_witness_distance"
        ],
        "no_witness_median_closest_index_fraction": no_witness[
            "median_closest_index_fraction"
        ],
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the source-position carrier probe."""
    context = PrimeContext(max_source_in_rows(input_path))
    strata = load_strata(input_path, context)
    rows = [
        stratum_row(odd_steps, strata[odd_steps])
        for odd_steps in sorted(strata)
    ]
    matched_rows = [row for row in rows if bool(row["has_both_classes"])]
    add_weight_shares(rows)
    favorable_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    unfavorable_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) < 0.0
    ]
    total_weight = sum(int(row["matched_weight"]) for row in matched_rows)

    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "strata_count": len(rows),
        "matched_strata_count": len(matched_rows),
        "matched_weight_total": total_weight,
        "favorable_source_position_summary": aggregate_rows(
            favorable_rows,
            total_weight,
        ),
        "unfavorable_source_position_summary": aggregate_rows(
            unfavorable_rows,
            total_weight,
        ),
        "net_weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_delta",
        ),
        "net_weighted_mean_of_stratum_median_final_v2_delta": matched_weighted_mean(
            matched_rows,
            "median_final_v2_delta",
        ),
        "top_positive_position_carriers": [
            carrier_summary(row)
            for row in sorted(
                favorable_rows,
                key=lambda item: (
                    int(item["matched_weight"])
                    * float(item["median_reset_strength_delta"])
                ),
                reverse=True,
            )[:10]
        ],
        "top_negative_position_carriers": [
            carrier_summary(row)
            for row in sorted(
                unfavorable_rows,
                key=lambda item: (
                    int(item["matched_weight"])
                    * float(item["median_reset_strength_delta"])
                ),
            )[:10]
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "source_position_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Measure source-position patterns inside carrier strata.",
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
