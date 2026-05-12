"""Decompose below-witness reset effects by exact carrier family."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import rate, read_jsonl, write_json, write_jsonl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT
    / "output"
    / "collatz_pgs_below_witness_stability_probe"
    / "stability_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_below_witness_family_probe"
COMPARISON_NAME = "below_vs_no_witness"
DELTA_FIELDS = (
    "median_reset_strength_delta",
    "p90_reset_strength_delta",
    "p99_reset_strength_delta",
)


def sign_label(value: float) -> str:
    """Return the sign label for one numeric value."""
    if value > 0.0:
        return "positive"
    if value < 0.0:
        return "negative"
    return "tied"


def sign_pattern(row: dict[str, object]) -> str:
    """Return the median/P90/P99 sign pattern for one family row."""
    return "_".join(sign_label(float(row[field])) for field in DELTA_FIELDS)


def matched_rows(path: Path) -> list[dict[str, object]]:
    """Return exact carrier-family rows for below-vs-no-witness strata."""
    rows: list[dict[str, object]] = []
    for row in read_jsonl(path):
        comparison = row[COMPARISON_NAME]
        if not bool(comparison["has_both_classes"]):
            continue
        flattened = {
            "odd_steps_to_first_descent": int(row["odd_steps_to_first_descent"]),
            "final_v2": int(row["final_v2"]),
            "below_count": int(comparison["left_count"]),
            "no_witness_count": int(comparison["right_count"]),
            "matched_weight": int(comparison["matched_weight"]),
        }
        for field in DELTA_FIELDS:
            flattened[field] = float(comparison[field])
        flattened["median_reset_strength_ratio"] = float(
            comparison["median_reset_strength_ratio"]
        )
        flattened["p90_reset_strength_ratio"] = float(
            comparison["p90_reset_strength_ratio"]
        )
        flattened["p99_reset_strength_ratio"] = float(
            comparison["p99_reset_strength_ratio"]
        )
        flattened["median_max_source_over_seed_delta"] = float(
            comparison["median_max_source_over_seed_delta"]
        )
        flattened["sign_pattern"] = sign_pattern(flattened)
        rows.append(flattened)
    return rows


def add_overall_contributions(rows: list[dict[str, object]]) -> None:
    """Attach matched-weight shares and whole-comparison contributions."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    for row in rows:
        weight = int(row["matched_weight"])
        row["matched_weight_share"] = rate(weight, total_weight)
        for field in DELTA_FIELDS:
            contribution_field = (
                f"overall_{field.replace('_reset_strength_delta', '')}_"
                "delta_contribution"
            )
            row[contribution_field] = (
                weight * float(row[field]) / total_weight if total_weight else 0.0
            )


def weighted_mean(rows: list[dict[str, object]], field: str) -> float:
    """Return matched-weighted mean for one field."""
    numerator = 0.0
    denominator = 0
    for row in rows:
        weight = int(row["matched_weight"])
        numerator += weight * float(row[field])
        denominator += weight
    return numerator / denominator if denominator else 0.0


def sign_counts(rows: list[dict[str, object]], field: str) -> dict[str, object]:
    """Return sign counts and weight shares for one field."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    counts: Counter[str] = Counter()
    weights: Counter[str] = Counter()
    for row in rows:
        label = sign_label(float(row[field]))
        counts[label] += 1
        weights[label] += int(row["matched_weight"])
    return {
        "positive_count": counts["positive"],
        "negative_count": counts["negative"],
        "tied_count": counts["tied"],
        "positive_weight_share": rate(weights["positive"], total_weight),
        "negative_weight_share": rate(weights["negative"], total_weight),
        "tied_weight_share": rate(weights["tied"], total_weight),
    }


def summary_for_rows(
    rows: list[dict[str, object]],
    total_weight: int,
) -> dict[str, object]:
    """Return aggregate facts for a family row subset."""
    subset_weight = sum(int(row["matched_weight"]) for row in rows)
    record: dict[str, object] = {
        "family_count": len(rows),
        "matched_weight": subset_weight,
        "matched_weight_share": rate(subset_weight, total_weight),
        "median_delta_sign": sign_counts(rows, "median_reset_strength_delta"),
        "p90_delta_sign": sign_counts(rows, "p90_reset_strength_delta"),
        "p99_delta_sign": sign_counts(rows, "p99_reset_strength_delta"),
    }
    for field in DELTA_FIELDS:
        short_name = field.replace("_reset_strength_delta", "")
        record[f"weighted_mean_{short_name}_delta"] = weighted_mean(rows, field)
        record[f"overall_{short_name}_delta_contribution"] = (
            sum(int(row["matched_weight"]) * float(row[field]) for row in rows)
            / total_weight
            if total_weight
            else 0.0
        )
    return record


def grouped_summary(
    rows: list[dict[str, object]],
    key_name: str,
) -> list[dict[str, object]]:
    """Return aggregate summaries grouped by one exact family axis."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    groups: dict[int | str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[row[key_name]].append(row)

    records = []
    for key in sorted(groups):
        record = summary_for_rows(groups[key], total_weight)
        record[key_name] = key
        records.append(record)
    return records


def pattern_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return aggregate summaries grouped by median/P90/P99 sign pattern."""
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row["sign_pattern"])].append(row)

    records = []
    for key in sorted(groups):
        record = summary_for_rows(groups[key], total_weight)
        record["sign_pattern"] = key
        records.append(record)
    return records


def top_rows(
    rows: list[dict[str, object]],
    contribution_field: str,
    reverse: bool,
) -> list[dict[str, object]]:
    """Return compact top carrier-family rows."""
    selected = sorted(
        rows,
        key=lambda row: float(row[contribution_field]),
        reverse=reverse,
    )[:10]
    return [
        {
            "odd_steps_to_first_descent": row["odd_steps_to_first_descent"],
            "final_v2": row["final_v2"],
            "below_count": row["below_count"],
            "no_witness_count": row["no_witness_count"],
            "matched_weight": row["matched_weight"],
            "matched_weight_share": row["matched_weight_share"],
            "sign_pattern": row["sign_pattern"],
            "median_reset_strength_delta": row["median_reset_strength_delta"],
            "p90_reset_strength_delta": row["p90_reset_strength_delta"],
            "p99_reset_strength_delta": row["p99_reset_strength_delta"],
            contribution_field: row[contribution_field],
        }
        for row in selected
    ]


def top_group_rows(
    rows: list[dict[str, object]],
    contribution_field: str,
    reverse: bool,
) -> list[dict[str, object]]:
    """Return top grouped summary rows."""
    return sorted(
        rows,
        key=lambda row: float(row[contribution_field]),
        reverse=reverse,
    )[:10]


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the below-witness exact carrier-family decomposition."""
    rows = matched_rows(input_path)
    add_overall_contributions(rows)
    total_weight = sum(int(row["matched_weight"]) for row in rows)
    odd_step_rows = grouped_summary(rows, "odd_steps_to_first_descent")
    final_v2_rows = grouped_summary(rows, "final_v2")
    pattern_rows = pattern_summary(rows)
    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "comparison": COMPARISON_NAME,
        "family_count": len(rows),
        "matched_weight_total": total_weight,
        "overall": summary_for_rows(rows, total_weight),
        "sign_pattern_summary": pattern_rows,
        "odd_step_summary": odd_step_rows,
        "final_v2_summary": final_v2_rows,
        "top_positive_median_families": top_rows(
            rows,
            "overall_median_delta_contribution",
            True,
        ),
        "top_negative_median_families": top_rows(
            rows,
            "overall_median_delta_contribution",
            False,
        ),
        "top_positive_p90_families": top_rows(
            rows,
            "overall_p90_delta_contribution",
            True,
        ),
        "top_negative_p90_families": top_rows(
            rows,
            "overall_p90_delta_contribution",
            False,
        ),
        "top_positive_p99_families": top_rows(
            rows,
            "overall_p99_delta_contribution",
            True,
        ),
        "top_negative_p99_families": top_rows(
            rows,
            "overall_p99_delta_contribution",
            False,
        ),
        "top_positive_odd_steps_by_median": top_group_rows(
            odd_step_rows,
            "overall_median_delta_contribution",
            True,
        ),
        "top_negative_odd_steps_by_median": top_group_rows(
            odd_step_rows,
            "overall_median_delta_contribution",
            False,
        ),
        "top_positive_final_v2_by_median": top_group_rows(
            final_v2_rows,
            "overall_median_delta_contribution",
            True,
        ),
        "top_negative_final_v2_by_median": top_group_rows(
            final_v2_rows,
            "overall_median_delta_contribution",
            False,
        ),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "family_rows.jsonl")
    write_jsonl(odd_step_rows, output_dir / "odd_step_rows.jsonl")
    write_jsonl(final_v2_rows, output_dir / "final_v2_rows.jsonl")
    write_jsonl(pattern_rows, output_dir / "sign_pattern_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Decompose below-vs-no-witness reset effects by exact "
            "odd-step and final-v2 carrier families."
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
