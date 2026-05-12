"""Compare Collatz-PGS reset strength inside matched odd-step strata."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_reset_length_strata_probe"
CLASS_WITNESS = "witness_contact"
CLASS_NO_WITNESS = "no_witness_contact"


class VectorStats:
    """Collect numeric vectors for one block class."""

    def __init__(self) -> None:
        self.reset_strengths: list[float] = []
        self.max_source_over_seed_values: list[float] = []
        self.final_source_witness_hits = 0

    def add(self, row: dict[str, object]) -> None:
        """Add one block row."""
        self.reset_strengths.append(float(row["reset_strength"]))
        self.max_source_over_seed_values.append(float(row["max_source_over_seed"]))
        if bool(row["final_odd_projected_witness_hit"]):
            self.final_source_witness_hits += 1

    def record(self) -> dict[str, object]:
        """Return JSON-ready statistics."""
        count = len(self.reset_strengths)
        return {
            "count": count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "p99_reset_strength": percentile(self.reset_strengths, 0.99),
            "max_reset_strength": max_or_zero(self.reset_strengths),
            "median_max_source_over_seed": median(self.max_source_over_seed_values),
            "p90_max_source_over_seed": percentile(
                self.max_source_over_seed_values,
                0.90,
            ),
            "max_source_over_seed": max_or_zero(self.max_source_over_seed_values),
            "final_source_witness_hit_count": self.final_source_witness_hits,
            "final_source_witness_hit_rate": rate(
                self.final_source_witness_hits,
                count,
            ),
        }


def read_jsonl(path: Path):
    """Yield JSONL rows."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        for line in handle:
            yield json.loads(line)


def write_json(record: dict[str, object], path: Path) -> None:
    """Write LF-terminated JSON."""
    path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(rows: list[dict[str, object]], path: Path) -> None:
    """Write LF-terminated JSONL."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def median(values: list[float] | list[int]) -> float:
    """Return the median value."""
    if not values:
        return 0.0
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[midpoint])
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2.0


def percentile(values: list[float] | list[int], fraction: float) -> float:
    """Return the nearest-rank percentile."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(fraction * len(ordered)) - 1))
    return float(ordered[index])


def max_or_zero(values: list[float] | list[int]) -> float:
    """Return maximum or zero for an empty vector."""
    if not values:
        return 0.0
    return float(max(values))


def rate(numerator: int, denominator: int) -> float:
    """Return a zero-safe rate."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def ratio(left: float, right: float) -> float:
    """Return a zero-safe ratio."""
    if right == 0.0:
        return 0.0
    return left / right


def load_strata(path: Path) -> dict[int, dict[str, VectorStats]]:
    """Load block rows into exact odd-step strata."""
    strata: dict[int, dict[str, VectorStats]] = defaultdict(
        lambda: {
            CLASS_WITNESS: VectorStats(),
            CLASS_NO_WITNESS: VectorStats(),
        }
    )
    for row in read_jsonl(path):
        block_class = str(row["block_class"])
        if block_class not in (CLASS_WITNESS, CLASS_NO_WITNESS):
            raise ValueError(f"unknown block_class={block_class}")
        odd_steps = int(row["odd_steps_to_first_descent"])
        strata[odd_steps][block_class].add(row)
    return strata


def stratum_row(odd_steps: int, stats: dict[str, VectorStats]) -> dict[str, object]:
    """Return one exact odd-step stratum comparison row."""
    witness = stats[CLASS_WITNESS].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    median_delta = (
        float(witness["median_reset_strength"])
        - float(no_witness["median_reset_strength"])
    )
    return {
        "odd_steps_to_first_descent": odd_steps,
        "witness_contact": witness,
        "no_witness_contact": no_witness,
        "has_both_classes": int(witness["count"]) > 0 and int(no_witness["count"]) > 0,
        "matched_weight": min(int(witness["count"]), int(no_witness["count"])),
        "median_reset_strength_delta": median_delta,
        "median_reset_strength_ratio": ratio(
            float(witness["median_reset_strength"]),
            float(no_witness["median_reset_strength"]),
        ),
        "p90_reset_strength_delta": (
            float(witness["p90_reset_strength"])
            - float(no_witness["p90_reset_strength"])
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


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the exact odd-step matched reset comparison."""
    strata = load_strata(input_path)
    rows = [
        stratum_row(odd_steps, strata[odd_steps])
        for odd_steps in sorted(strata)
    ]
    matched_rows = [row for row in rows if bool(row["has_both_classes"])]
    witness_higher = sum(
        1
        for row in matched_rows
        if float(row["median_reset_strength_delta"]) > 0.0
    )
    no_witness_higher = sum(
        1
        for row in matched_rows
        if float(row["median_reset_strength_delta"]) < 0.0
    )
    tied = len(matched_rows) - witness_higher - no_witness_higher
    total_witness = sum(int(row["witness_contact"]["count"]) for row in rows)
    total_no_witness = sum(int(row["no_witness_contact"]["count"]) for row in rows)
    matched_witness = sum(int(row["witness_contact"]["count"]) for row in matched_rows)
    matched_no_witness = sum(
        int(row["no_witness_contact"]["count"]) for row in matched_rows
    )
    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "strata_count": len(rows),
        "matched_strata_count": len(matched_rows),
        "total_witness_contact_blocks": total_witness,
        "total_no_witness_contact_blocks": total_no_witness,
        "matched_witness_contact_blocks": matched_witness,
        "matched_no_witness_contact_blocks": matched_no_witness,
        "matched_weight_total": sum(int(row["matched_weight"]) for row in matched_rows),
        "strata_where_witness_median_reset_is_higher": witness_higher,
        "strata_where_no_witness_median_reset_is_higher": no_witness_higher,
        "strata_where_median_reset_is_tied": tied,
        "matched_weighted_mean_of_stratum_median_reset_delta": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_delta",
        ),
        "matched_weighted_mean_of_stratum_median_reset_ratio": matched_weighted_mean(
            matched_rows,
            "median_reset_strength_ratio",
        ),
        "matched_weighted_mean_of_stratum_p90_reset_delta": matched_weighted_mean(
            matched_rows,
            "p90_reset_strength_delta",
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "strata_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Compare reset strength inside exact odd-step strata.",
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
