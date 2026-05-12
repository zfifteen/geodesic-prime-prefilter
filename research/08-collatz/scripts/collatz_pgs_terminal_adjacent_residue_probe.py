"""Attach Collatz residue identities to adjacent terminal PGS hits."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import read_jsonl, write_json, write_jsonl
from collatz_pgs_same_gap_scale_probe import median, percentile, rate, v2


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_terminal_adjacent_residue_probe"
SIDE_BELOW = "below_witness_terminal_hit"
SIDE_ABOVE = "above_witness_terminal_hit"


class ResidueStats:
    """Accumulate adjacent terminal residue rows."""

    def __init__(self) -> None:
        self.count = 0
        self.residue_ok_count = 0
        self.exact_v2_residue_ok_count = 0
        self.computed_v2_ok_count = 0
        self.target_match_count = 0
        self.final_v2_counts: Counter[int] = Counter()
        self.reset_strengths: list[float] = []
        self.odd_steps: list[int] = []

    def add(self, row: dict[str, object]) -> None:
        """Add one residue row."""
        self.count += 1
        if bool(row["residue_ok"]):
            self.residue_ok_count += 1
        if bool(row["exact_v2_residue_ok"]):
            self.exact_v2_residue_ok_count += 1
        if bool(row["computed_v2_ok"]):
            self.computed_v2_ok_count += 1
        if bool(row["target_match"]):
            self.target_match_count += 1
        self.final_v2_counts[int(row["final_v2"])] += 1
        self.reset_strengths.append(float(row["reset_strength"]))
        self.odd_steps.append(int(row["odd_steps_to_first_descent"]))

    def record(self) -> dict[str, object]:
        """Return one JSON-ready aggregate record."""
        return {
            "count": self.count,
            "residue_ok_count": self.residue_ok_count,
            "residue_ok_rate": rate(self.residue_ok_count, self.count),
            "exact_v2_residue_ok_count": self.exact_v2_residue_ok_count,
            "exact_v2_residue_ok_rate": rate(
                self.exact_v2_residue_ok_count,
                self.count,
            ),
            "computed_v2_ok_count": self.computed_v2_ok_count,
            "computed_v2_ok_rate": rate(self.computed_v2_ok_count, self.count),
            "target_match_count": self.target_match_count,
            "target_match_rate": rate(self.target_match_count, self.count),
            "final_v2_counts": {
                str(key): self.final_v2_counts[key]
                for key in sorted(self.final_v2_counts)
            },
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "p99_reset_strength": percentile(self.reset_strengths, 0.99),
            "median_odd_steps_to_first_descent": median(self.odd_steps),
            "p90_odd_steps_to_first_descent": percentile(self.odd_steps, 0.90),
        }


def expected_witness_residue(side: str, exponent: int) -> int:
    """Return the witness residue forced by the terminal Collatz exponent."""
    modulus = 1 << exponent
    inverse_three = pow(3, -1, modulus)
    if side == SIDE_BELOW:
        return (2 * inverse_three) % modulus
    if side == SIDE_ABOVE:
        return (-4 * inverse_three) % modulus
    raise ValueError(f"unknown adjacent side={side}")


def adjacent_side(row: dict[str, object]) -> str | None:
    """Return the terminal adjacent witness side for one block row."""
    if bool(row["final_is_prime"]):
        return None
    if not bool(row["final_odd_projected_witness_hit"]):
        return None

    offset = int(row["final_source"]) - int(row["final_witness"])
    if offset == -1:
        return SIDE_BELOW
    if offset == 1:
        return SIDE_ABOVE
    return None


def residue_row(row: dict[str, object], side: str) -> dict[str, object]:
    """Return one adjacent terminal residue record."""
    source = int(row["final_source"])
    witness = int(row["final_witness"])
    exponent = int(row["final_v2"])
    modulus = 1 << exponent
    next_modulus = 1 << (exponent + 1)
    expected = expected_witness_residue(side, exponent)
    next_expected = expected_witness_residue(side, exponent + 1)
    computed_exponent = v2(3 * source + 1)
    computed_target = (3 * source + 1) >> exponent

    return {
        "seed": int(row["seed"]),
        "side": side,
        "final_source": source,
        "final_witness": witness,
        "final_v2": exponent,
        "modulus": modulus,
        "expected_witness_residue": expected,
        "witness_residue": witness % modulus,
        "residue_ok": witness % modulus == expected,
        "next_modulus": next_modulus,
        "next_expected_witness_residue": next_expected,
        "next_witness_residue": witness % next_modulus,
        "exact_v2_residue_ok": witness % next_modulus != next_expected,
        "computed_v2": computed_exponent,
        "computed_v2_ok": computed_exponent == exponent,
        "computed_terminal_below_seed": computed_target,
        "target_match": computed_target == int(row["terminal_below_seed"]),
        "terminal_below_seed": int(row["terminal_below_seed"]),
        "reset_strength": float(row["reset_strength"]),
        "odd_steps_to_first_descent": int(row["odd_steps_to_first_descent"]),
    }


def grouped_rows(
    rows: list[dict[str, object]],
    key_names: tuple[str, ...],
) -> list[dict[str, object]]:
    """Return residue summaries grouped by exact key fields."""
    groups: dict[tuple[object, ...], ResidueStats] = defaultdict(ResidueStats)
    for row in rows:
        key = tuple(row[name] for name in key_names)
        groups[key].add(row)

    records = []
    for key in sorted(groups):
        record = groups[key].record()
        for index, name in enumerate(key_names):
            record[name] = key[index]
        records.append(record)
    return records


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the adjacent terminal residue probe."""
    rows = []
    by_side = {SIDE_BELOW: ResidueStats(), SIDE_ABOVE: ResidueStats()}
    overall = ResidueStats()
    for block_row in read_jsonl(input_path):
        side = adjacent_side(block_row)
        if side is None:
            continue
        row = residue_row(block_row, side)
        rows.append(row)
        by_side[side].add(row)
        overall.add(row)

    side_rows = grouped_rows(rows, ("side",))
    side_v2_rows = grouped_rows(rows, ("side", "final_v2"))
    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "adjacent_terminal_count": len(rows),
        "overall": overall.record(),
        "by_side": {side: by_side[side].record() for side in sorted(by_side)},
        "side_summary": side_rows,
        "side_final_v2_summary": side_v2_rows,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "residue_rows.jsonl")
    write_jsonl(side_rows, output_dir / "side_rows.jsonl")
    write_jsonl(side_v2_rows, output_dir / "side_final_v2_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Attach Collatz residue identities to adjacent terminal PGS hits.",
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
