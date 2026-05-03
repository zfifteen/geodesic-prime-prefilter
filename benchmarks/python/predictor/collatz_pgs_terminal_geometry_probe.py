"""Measure final-source geometry for terminal Collatz-PGS witness contact."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
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
from collatz_pgs_same_gap_scale_probe import PrimeContext, Transition, first_descent_block
from collatz_pgs_terminal_contact_decomposition_probe import (
    CLASS_NO_WITNESS,
    CLASS_NONTERMINAL,
    CLASS_TERMINAL,
    classify_transitions,
    max_source_in_rows,
)


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_terminal_geometry_probe"
HIT_OFFSETS = ("-1", "0", "1")


class GeometryStats:
    """Collect reset and final-source geometry for one block class."""

    def __init__(self) -> None:
        self.reset_strengths: list[float] = []
        self.max_source_over_seed_values: list[float] = []
        self.final_composite_count = 0
        self.final_prime_count = 0
        self.final_witness_hit_count = 0
        self.exact_witness_hit_count = 0
        self.hit_offset_counts: Counter[str] = Counter()
        self.final_gap_widths: list[int] = []
        self.final_endpoint_distances: list[int] = []
        self.final_odd_witness_distances: list[int] = []
        self.final_gap_offset_fractions: list[float] = []

    def add(
        self,
        row: dict[str, object],
        transitions: list[Transition],
        context: PrimeContext,
    ) -> None:
        """Add one first-descent block row."""
        final_state = context.source_state(transitions[-1].source)
        self.reset_strengths.append(float(row["reset_strength"]))
        self.max_source_over_seed_values.append(float(row["max_source_over_seed"]))

        if final_state.is_prime:
            self.final_prime_count += 1
            return

        self.final_composite_count += 1
        self.final_gap_widths.append(final_state.gap_width)
        self.final_endpoint_distances.append(final_state.endpoint_distance)
        self.final_odd_witness_distances.append(final_state.odd_witness_distance)
        self.final_gap_offset_fractions.append(
            final_state.gap_offset / final_state.gap_width
        )
        if not final_state.odd_projected_witness_hit:
            return

        offset = str(final_state.n - final_state.witness)
        self.final_witness_hit_count += 1
        self.hit_offset_counts[offset] += 1
        if final_state.n == final_state.witness:
            self.exact_witness_hit_count += 1

    def record(self) -> dict[str, object]:
        """Return JSON-ready geometry statistics."""
        count = len(self.reset_strengths)
        return {
            "count": count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "median_max_source_over_seed": median(self.max_source_over_seed_values),
            "final_prime_count": self.final_prime_count,
            "final_composite_count": self.final_composite_count,
            "final_composite_rate": rate(self.final_composite_count, count),
            "final_witness_hit_rate": rate(
                self.final_witness_hit_count,
                self.final_composite_count,
            ),
            "exact_witness_hit_rate": rate(
                self.exact_witness_hit_count,
                self.final_witness_hit_count,
            ),
            "adjacent_projected_witness_hit_rate": rate(
                self.final_witness_hit_count - self.exact_witness_hit_count,
                self.final_witness_hit_count,
            ),
            "hit_offset_rates": {
                offset: rate(self.hit_offset_counts[offset], self.final_witness_hit_count)
                for offset in HIT_OFFSETS
            },
            "median_final_gap_width": median(self.final_gap_widths),
            "p90_final_gap_width": percentile(self.final_gap_widths, 0.90),
            "median_final_endpoint_distance": median(self.final_endpoint_distances),
            "median_final_odd_witness_distance": median(
                self.final_odd_witness_distances,
            ),
            "median_final_gap_offset_fraction": median(
                self.final_gap_offset_fractions,
            ),
        }


def load_strata(path: Path, context: PrimeContext):
    """Load rows into exact odd-step and final-v2 terminal-geometry strata."""
    strata = defaultdict(
        lambda: {
            CLASS_TERMINAL: GeometryStats(),
            CLASS_NO_WITNESS: GeometryStats(),
        }
    )
    class_counts = {
        CLASS_TERMINAL: 0,
        CLASS_NONTERMINAL: 0,
        CLASS_NO_WITNESS: 0,
    }
    for row in read_jsonl(path):
        seed = int(row["seed"])
        transitions = first_descent_block(seed)
        odd_steps = int(row["odd_steps_to_first_descent"])
        final_v2 = transitions[-1].v2
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")
        if "final_v2" in row and int(row["final_v2"]) != final_v2:
            raise ValueError(f"seed={seed} final-v2 mismatch")

        block_class = classify_transitions(transitions, context)
        class_counts[block_class] += 1
        if block_class not in (CLASS_TERMINAL, CLASS_NO_WITNESS):
            continue
        strata[(odd_steps, final_v2)][block_class].add(row, transitions, context)
    return strata, class_counts


def comparison(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    """Return one terminal versus no-witness comparison."""
    left_count = int(left["count"])
    right_count = int(right["count"])
    return {
        "has_both_classes": left_count > 0 and right_count > 0,
        "matched_weight": min(left_count, right_count),
        "median_reset_strength_delta": (
            float(left["median_reset_strength"]) - float(right["median_reset_strength"])
        ),
        "median_reset_strength_ratio": ratio(
            float(left["median_reset_strength"]),
            float(right["median_reset_strength"]),
        ),
        "p90_reset_strength_delta": (
            float(left["p90_reset_strength"]) - float(right["p90_reset_strength"])
        ),
        "median_max_source_over_seed_delta": (
            float(left["median_max_source_over_seed"])
            - float(right["median_max_source_over_seed"])
        ),
    }


def stratum_row(key: tuple[int, int], stats: dict[str, GeometryStats]):
    """Return one exact-step and final-v2 terminal-geometry row."""
    terminal = stats[CLASS_TERMINAL].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    return {
        "odd_steps_to_first_descent": key[0],
        "final_v2": key[1],
        CLASS_TERMINAL: terminal,
        CLASS_NO_WITNESS: no_witness,
        "terminal_vs_no_witness": comparison(terminal, no_witness),
    }


def matched_weighted_mean(rows: list[dict[str, object]], field: str) -> float:
    """Return matched-weighted mean for one comparison field."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row[field])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def matched_weighted_nested_mean(
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


def matched_weighted_hit_offset_rates(
    rows: list[dict[str, object]],
) -> dict[str, float]:
    """Return matched-weighted mean of terminal hit-offset rates."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    return {
        offset: (
            sum(
                int(row["matched_weight"])
                * float(row[CLASS_TERMINAL]["hit_offset_rates"][offset])
                for row in rows
            )
            / total_weight
            if total_weight
            else 0.0
        )
        for offset in HIT_OFFSETS
    }


def comparison_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return terminal-vs-no-witness rows with flattened comparison fields."""
    flattened = []
    for row in rows:
        comparison_row = row["terminal_vs_no_witness"]
        if not bool(comparison_row["has_both_classes"]):
            continue
        flattened.append(
            {
                "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
                "final_v2": row["final_v2"],
                CLASS_TERMINAL: row[CLASS_TERMINAL],
                CLASS_NO_WITNESS: row[CLASS_NO_WITNESS],
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


def aggregate_rows(
    rows: list[dict[str, object]],
    total_weight: int,
) -> dict[str, object]:
    """Return matched-weighted geometry facts for one signed row subset."""
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
        "weighted_mean_terminal_exact_witness_hit_rate": matched_weighted_nested_mean(
            rows,
            CLASS_TERMINAL,
            "exact_witness_hit_rate",
        ),
        "weighted_mean_terminal_adjacent_projected_witness_hit_rate": (
            matched_weighted_nested_mean(
                rows,
                CLASS_TERMINAL,
                "adjacent_projected_witness_hit_rate",
            )
        ),
        "weighted_mean_terminal_hit_offset_rates": matched_weighted_hit_offset_rates(
            rows,
        ),
        "weighted_mean_terminal_median_final_gap_width": matched_weighted_nested_mean(
            rows,
            CLASS_TERMINAL,
            "median_final_gap_width",
        ),
        "weighted_mean_terminal_median_final_endpoint_distance": (
            matched_weighted_nested_mean(
                rows,
                CLASS_TERMINAL,
                "median_final_endpoint_distance",
            )
        ),
        "weighted_mean_terminal_median_final_gap_offset_fraction": (
            matched_weighted_nested_mean(
                rows,
                CLASS_TERMINAL,
                "median_final_gap_offset_fraction",
            )
        ),
        "weighted_mean_no_witness_final_composite_rate": (
            matched_weighted_nested_mean(
                rows,
                CLASS_NO_WITNESS,
                "final_composite_rate",
            )
        ),
        "weighted_mean_no_witness_median_final_odd_witness_distance": (
            matched_weighted_nested_mean(
                rows,
                CLASS_NO_WITNESS,
                "median_final_odd_witness_distance",
            )
        ),
    }


def carrier_summary(row: dict[str, object]) -> dict[str, object]:
    """Return compact fields for a geometry carrier row."""
    terminal = row[CLASS_TERMINAL]
    no_witness = row[CLASS_NO_WITNESS]
    return {
        "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
        "final_v2": row["final_v2"],
        "matched_weight": row["matched_weight"],
        "matched_weight_share": row["matched_weight_share"],
        "median_reset_strength_delta": row["median_reset_strength_delta"],
        "matched_weighted_mean_of_stratum_median_delta_contribution": row[
            "matched_weighted_mean_of_stratum_median_delta_contribution"
        ],
        "terminal_exact_witness_hit_rate": terminal["exact_witness_hit_rate"],
        "terminal_hit_offset_rates": terminal["hit_offset_rates"],
        "terminal_median_final_gap_width": terminal["median_final_gap_width"],
        "terminal_median_final_endpoint_distance": terminal[
            "median_final_endpoint_distance"
        ],
        "terminal_median_final_gap_offset_fraction": terminal[
            "median_final_gap_offset_fraction"
        ],
        "no_witness_final_composite_rate": no_witness["final_composite_rate"],
        "no_witness_median_final_odd_witness_distance": no_witness[
            "median_final_odd_witness_distance"
        ],
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the terminal geometry probe."""
    context = PrimeContext(max_source_in_rows(input_path))
    strata, class_counts = load_strata(input_path, context)
    rows = [stratum_row(key, strata[key]) for key in sorted(strata)]
    matched_rows = comparison_rows(rows)
    positive_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    negative_rows = [
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
        "class_counts": class_counts,
        "matched_strata_count": len(matched_rows),
        "matched_weight_total": total_weight,
        "positive_geometry_summary": aggregate_rows(positive_rows, total_weight),
        "negative_geometry_summary": aggregate_rows(negative_rows, total_weight),
        "net_geometry_summary": aggregate_rows(matched_rows, total_weight),
        "top_positive_geometry_carriers": [
            carrier_summary(row)
            for row in sorted(
                positive_rows,
                key=lambda item: float(
                    item[
                        "matched_weighted_mean_of_stratum_median_delta_contribution"
                    ]
                ),
                reverse=True,
            )[:10]
        ],
        "top_negative_geometry_carriers": [
            carrier_summary(row)
            for row in sorted(
                negative_rows,
                key=lambda item: float(
                    item[
                        "matched_weighted_mean_of_stratum_median_delta_contribution"
                    ]
                ),
            )[:10]
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "geometry_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Measure terminal-contact final-source prime-gap geometry.",
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
