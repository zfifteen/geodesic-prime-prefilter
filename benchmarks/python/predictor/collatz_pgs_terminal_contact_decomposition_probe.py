"""Decompose Collatz reset strength by terminal PGS witness contact."""

from __future__ import annotations

import argparse
import json
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
from collatz_pgs_same_gap_scale_probe import PrimeContext, Transition, first_descent_block


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_terminal_contact_decomposition_probe"
CLASS_TERMINAL = "terminal_witness_contact"
CLASS_NONTERMINAL = "nonterminal_witness_contact"
CLASS_NO_WITNESS = "no_witness_contact"
CLASS_ORDER = (CLASS_TERMINAL, CLASS_NONTERMINAL, CLASS_NO_WITNESS)


class ResetStats:
    """Collect reset values for one terminal-contact class."""

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


def max_source_in_rows(path: Path) -> int:
    """Return the maximum source value reported by the block rows."""
    max_source = 3
    for row in read_jsonl(path):
        max_source = max(max_source, int(row["max_source"]))
    return max_source


def classify_transitions(transitions: list[Transition], context: PrimeContext) -> str:
    """Classify transitions by terminal and nonterminal witness contact."""
    nonterminal_hit = False
    for index, transition in enumerate(transitions, start=1):
        state = context.source_state(transition.source)
        hit = not state.is_prime and state.odd_projected_witness_hit
        if not hit:
            continue
        if index == len(transitions):
            return CLASS_TERMINAL
        nonterminal_hit = True

    if nonterminal_hit:
        return CLASS_NONTERMINAL
    return CLASS_NO_WITNESS


def terminal_contact_class(row: dict[str, object], context: PrimeContext) -> str:
    """Classify one block by terminal and nonterminal witness contact."""
    seed = int(row["seed"])
    odd_steps = int(row["odd_steps_to_first_descent"])
    transitions = first_descent_block(seed)
    if len(transitions) != odd_steps:
        raise ValueError(f"seed={seed} odd-step mismatch")
    if "final_v2" in row and int(row["final_v2"]) != transitions[-1].v2:
        raise ValueError(f"seed={seed} final-v2 mismatch")
    return classify_transitions(transitions, context)


def load_strata(path: Path, context: PrimeContext):
    """Load block rows into exact odd-step and final-v2 strata."""
    strata = defaultdict(lambda: {label: ResetStats() for label in CLASS_ORDER})
    class_counts = {label: 0 for label in CLASS_ORDER}
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
        strata[(odd_steps, final_v2)][block_class].add(row)
    return strata, class_counts


def comparison(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    """Return one two-class comparison."""
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


def stratum_row(key: tuple[int, int], stats: dict[str, ResetStats]) -> dict[str, object]:
    """Return one exact-step and final-v2 stratum row."""
    terminal = stats[CLASS_TERMINAL].record()
    nonterminal = stats[CLASS_NONTERMINAL].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    return {
        "odd_steps_to_first_descent": key[0],
        "final_v2": key[1],
        CLASS_TERMINAL: terminal,
        CLASS_NONTERMINAL: nonterminal,
        CLASS_NO_WITNESS: no_witness,
        "terminal_vs_no_witness": comparison(terminal, no_witness),
        "nonterminal_vs_no_witness": comparison(nonterminal, no_witness),
        "terminal_vs_nonterminal": comparison(terminal, nonterminal),
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


def comparison_summary(
    rows: list[dict[str, object]],
    comparison_name: str,
) -> dict[str, object]:
    """Return aggregate facts for one exact-matched comparison."""
    comparison_rows = [
        {
            "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
            "final_v2": row["final_v2"],
            **row[comparison_name],
        }
        for row in rows
        if bool(row[comparison_name]["has_both_classes"])
    ]
    total_weight = sum(int(row["matched_weight"]) for row in comparison_rows)
    for row in comparison_rows:
        row["matched_weight_share"] = rate(int(row["matched_weight"]), total_weight)
        row["matched_weighted_mean_of_stratum_median_delta_contribution"] = (
            int(row["matched_weight"])
            * float(row["median_reset_strength_delta"])
            / total_weight
            if total_weight
            else 0.0
        )

    positive_rows = [
        row for row in comparison_rows if float(row["median_reset_strength_delta"]) > 0.0
    ]
    negative_rows = [
        row for row in comparison_rows if float(row["median_reset_strength_delta"]) < 0.0
    ]
    return {
        "matched_strata_count": len(comparison_rows),
        "matched_weight_total": total_weight,
        "positive_strata_count": len(positive_rows),
        "negative_strata_count": len(negative_rows),
        "tied_strata_count": len(comparison_rows) - len(positive_rows) - len(negative_rows),
        "weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            comparison_rows,
            "median_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_reset_ratio": matched_weighted_mean(
            comparison_rows,
            "median_reset_strength_ratio",
        ),
        "weighted_mean_of_stratum_p90_reset_delta": matched_weighted_mean(
            comparison_rows,
            "p90_reset_strength_delta",
        ),
        "weighted_mean_of_stratum_median_max_source_over_seed_delta": (
            matched_weighted_mean(
                comparison_rows,
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
    """Run the terminal-contact decomposition probe."""
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
        "terminal_vs_no_witness": comparison_summary(rows, "terminal_vs_no_witness"),
        "nonterminal_vs_no_witness": comparison_summary(
            rows,
            "nonterminal_vs_no_witness",
        ),
        "terminal_vs_nonterminal": comparison_summary(
            rows,
            "terminal_vs_nonterminal",
        ),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "strata_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Decompose reset strength by terminal PGS witness contact.",
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
