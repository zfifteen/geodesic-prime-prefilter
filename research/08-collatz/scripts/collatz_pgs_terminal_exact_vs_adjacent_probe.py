"""Compare exact and adjacent terminal Collatz-PGS witness hits."""

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


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_terminal_exact_vs_adjacent_probe"
CLASS_EXACT_TERMINAL = "exact_terminal_witness_hit"
CLASS_ADJACENT_TERMINAL = "adjacent_projected_terminal_witness_hit"
MATCHED_CLASSES = (
    CLASS_EXACT_TERMINAL,
    CLASS_ADJACENT_TERMINAL,
    CLASS_NO_WITNESS,
)
CLASS_COUNTS = (
    CLASS_EXACT_TERMINAL,
    CLASS_ADJACENT_TERMINAL,
    CLASS_NONTERMINAL,
    CLASS_NO_WITNESS,
)
HIT_OFFSETS = ("-1", "0", "1")


class ResetGeometryStats:
    """Collect reset and terminal geometry for one block class."""

    def __init__(self) -> None:
        self.reset_strengths: list[float] = []
        self.max_source_over_seed_values: list[float] = []
        self.final_composite_count = 0
        self.final_prime_count = 0
        self.hit_offset_counts: Counter[str] = Counter()
        self.final_gap_widths: list[int] = []
        self.final_endpoint_distances: list[int] = []
        self.final_gap_offset_fractions: list[float] = []

    def add(
        self,
        row: dict[str, object],
        transitions: list[Transition],
        context: PrimeContext,
    ) -> None:
        """Add one first-descent block."""
        final_state = context.source_state(transitions[-1].source)
        self.reset_strengths.append(float(row["reset_strength"]))
        self.max_source_over_seed_values.append(float(row["max_source_over_seed"]))

        if final_state.is_prime:
            self.final_prime_count += 1
            return

        self.final_composite_count += 1
        self.final_gap_widths.append(final_state.gap_width)
        self.final_endpoint_distances.append(final_state.endpoint_distance)
        self.final_gap_offset_fractions.append(
            final_state.gap_offset / final_state.gap_width
        )
        if final_state.odd_projected_witness_hit:
            self.hit_offset_counts[str(final_state.n - final_state.witness)] += 1

    def record(self) -> dict[str, object]:
        """Return JSON-ready reset and geometry statistics."""
        count = len(self.reset_strengths)
        final_witness_hits = sum(self.hit_offset_counts.values())
        return {
            "count": count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "median_max_source_over_seed": median(self.max_source_over_seed_values),
            "final_prime_count": self.final_prime_count,
            "final_composite_count": self.final_composite_count,
            "final_composite_rate": rate(self.final_composite_count, count),
            "final_witness_hit_rate": rate(
                final_witness_hits,
                self.final_composite_count,
            ),
            "hit_offset_rates": {
                offset: rate(self.hit_offset_counts[offset], final_witness_hits)
                for offset in HIT_OFFSETS
            },
            "median_final_gap_width": median(self.final_gap_widths),
            "median_final_endpoint_distance": median(self.final_endpoint_distances),
            "median_final_gap_offset_fraction": median(
                self.final_gap_offset_fractions,
            ),
        }


def terminal_exactness_class(
    transitions: list[Transition],
    context: PrimeContext,
) -> str:
    """Classify one block by exact or adjacent terminal witness contact."""
    block_class = classify_transitions(transitions, context)
    if block_class != CLASS_TERMINAL:
        return block_class

    final_state = context.source_state(transitions[-1].source)
    if final_state.is_prime or not final_state.odd_projected_witness_hit:
        raise ValueError(f"invalid terminal witness state n={final_state.n}")

    offset = final_state.n - final_state.witness
    if offset == 0:
        return CLASS_EXACT_TERMINAL
    if offset in (-1, 1):
        return CLASS_ADJACENT_TERMINAL
    raise ValueError(f"unexpected terminal witness offset={offset} n={final_state.n}")


def load_strata(path: Path, context: PrimeContext):
    """Load rows into exact odd-step and final-v2 strata."""
    strata = defaultdict(
        lambda: {label: ResetGeometryStats() for label in MATCHED_CLASSES}
    )
    class_counts = {label: 0 for label in CLASS_COUNTS}

    for row in read_jsonl(path):
        seed = int(row["seed"])
        transitions = first_descent_block(seed)
        odd_steps = int(row["odd_steps_to_first_descent"])
        final_v2 = transitions[-1].v2
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")
        if "final_v2" in row and int(row["final_v2"]) != final_v2:
            raise ValueError(f"seed={seed} final-v2 mismatch")

        block_class = terminal_exactness_class(transitions, context)
        class_counts[block_class] += 1
        if block_class in MATCHED_CLASSES:
            strata[(odd_steps, final_v2)][block_class].add(row, transitions, context)

    return strata, class_counts


def comparison(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    """Return one exact-matched two-class comparison."""
    left_count = int(left["count"])
    right_count = int(right["count"])
    return {
        "has_both_classes": left_count > 0 and right_count > 0,
        "matched_weight": min(left_count, right_count),
        "left_count": left_count,
        "right_count": right_count,
        "left_median_reset_strength": left["median_reset_strength"],
        "right_median_reset_strength": right["median_reset_strength"],
        "left_p90_reset_strength": left["p90_reset_strength"],
        "right_p90_reset_strength": right["p90_reset_strength"],
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


def stratum_row(
    key: tuple[int, int],
    stats: dict[str, ResetGeometryStats],
) -> dict[str, object]:
    """Return one exact-step and final-v2 stratum row."""
    exact = stats[CLASS_EXACT_TERMINAL].record()
    adjacent = stats[CLASS_ADJACENT_TERMINAL].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    return {
        "odd_steps_to_first_descent": key[0],
        "final_v2": key[1],
        CLASS_EXACT_TERMINAL: exact,
        CLASS_ADJACENT_TERMINAL: adjacent,
        CLASS_NO_WITNESS: no_witness,
        "exact_vs_adjacent": comparison(exact, adjacent),
        "exact_vs_no_witness": comparison(exact, no_witness),
        "adjacent_vs_no_witness": comparison(adjacent, no_witness),
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


def comparison_rows(
    rows: list[dict[str, object]],
    comparison_name: str,
) -> list[dict[str, object]]:
    """Return flattened rows for one comparison."""
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


def comparison_summary(
    rows: list[dict[str, object]],
    comparison_name: str,
) -> dict[str, object]:
    """Return aggregate facts for one exact-matched comparison."""
    matched_rows = comparison_rows(rows, comparison_name)
    positive_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    negative_rows = [
        row for row in matched_rows if float(row["median_reset_strength_delta"]) < 0.0
    ]
    return {
        "matched_strata_count": len(matched_rows),
        "matched_weight_total": sum(int(row["matched_weight"]) for row in matched_rows),
        "positive_strata_count": len(positive_rows),
        "negative_strata_count": len(negative_rows),
        "tied_strata_count": len(matched_rows) - len(positive_rows) - len(negative_rows),
        "weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_reset_ratio": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_p90_reset_delta": matched_weighted_mean(
            matched_rows,
            "p90_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_max_source_over_seed_delta": (
            matched_weighted_mean(
                matched_rows,
                "median_max_source_over_seed_delta",
            )
        ),
        "top_positive_strata": sorted(
            positive_rows,
            key=lambda row: float(
                row["matched_weighted_mean_of_stratum_median_delta_contribution"]
            ),
            reverse=True,
        )[:10],
        "top_negative_strata": sorted(
            negative_rows,
            key=lambda row: float(
                row["matched_weighted_mean_of_stratum_median_delta_contribution"]
            ),
        )[:10],
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the exact terminal versus adjacent terminal probe."""
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
        "exact_vs_adjacent": comparison_summary(rows, "exact_vs_adjacent"),
        "exact_vs_no_witness": comparison_summary(rows, "exact_vs_no_witness"),
        "adjacent_vs_no_witness": comparison_summary(rows, "adjacent_vs_no_witness"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "strata_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Compare exact and adjacent terminal PGS witness hits inside "
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
