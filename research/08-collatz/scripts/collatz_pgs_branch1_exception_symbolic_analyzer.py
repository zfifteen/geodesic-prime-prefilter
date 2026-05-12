"""Summarize the branch-1 composite-terminal exception normal form."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import write_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "08-collatz" / "output" / "collatz_pgs_branch_occupancy_baseline_probe"
DEFAULT_INPUT = DEFAULT_OUTPUT_DIR / "branch1_composite_exception_rows.jsonl"
DEFAULT_OUTPUT = DEFAULT_OUTPUT_DIR / "branch1_exception_symbolic_summary.json"
EXPECTED_GAP_WIDTHS = {6, 8, 10}
EXPECTED_FINAL_V2 = {4, 8}
EXPECTED_TAU = 12
EXPECTED_GEOMETRY = "composite_below_minimizer"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-terminated JSONL rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for line in handle:
            rows.append(json.loads(line))
    return rows


def is_prime(n: int) -> bool:
    """Return exact primality for positive integers."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = math.isqrt(n)
    factor = 3
    while factor <= limit:
        if n % factor == 0:
            return False
        factor += 2
    return True


def count_rows(rows: list[dict[str, object]], key: str) -> list[dict[str, int]]:
    """Return sorted count rows for one integer key."""
    counter = Counter(int(row[key]) for row in rows)
    return [{key: value, "count": counter[value]} for value in sorted(counter)]


def validate_exception_row(row: dict[str, object]) -> None:
    """Raise if a row is outside the branch-1 exception contract."""
    branch = row.get("branch", 1)
    if int(branch) != 1:
        raise ValueError(f"exception row has non-branch-1 branch: {branch}")
    if str(row["terminal_geometry"]) != EXPECTED_GEOMETRY:
        raise ValueError(f"unexpected terminal geometry: {row['terminal_geometry']}")
    if not bool(row["below_minimizer_hit"]):
        raise ValueError("exception row is not a below-minimizer hit")

    witness = int(row["witness"])
    terminal_source = int(row["terminal_source"])
    prev_prime = int(row["prev_prime"])
    next_prime = int(row["next_prime"])
    final_v2 = int(row["final_v2"])
    gap_width = int(row["gap_width"])
    witness_tau = int(row["witness_tau"])

    if final_v2 not in EXPECTED_FINAL_V2:
        raise ValueError(f"unexpected final exponent: {final_v2}")
    if witness != terminal_source + 1:
        raise ValueError("terminal source is not w-1")
    if gap_width != next_prime - prev_prime:
        raise ValueError("gap width does not match prime endpoints")
    if not (prev_prime < terminal_source < witness < next_prime):
        raise ValueError("terminal source and witness are not inside the prime gap")
    if int(row["terminal_source_gap_offset"]) != terminal_source - prev_prime:
        raise ValueError("terminal-source offset does not match prime endpoint")
    if int(row["witness_gap_offset"]) != witness - prev_prime:
        raise ValueError("witness offset does not match prime endpoint")
    if is_prime(terminal_source):
        raise ValueError("terminal source is prime")
    if witness % 18 != 0:
        raise ValueError("witness is not divisible by 18")
    if not is_prime(witness // 18):
        raise ValueError("witness does not have normal form w=18u with u prime")
    if witness_tau != EXPECTED_TAU:
        raise ValueError(f"unexpected witness divisor count: {witness_tau}")
    if gap_width not in EXPECTED_GAP_WIDTHS:
        raise ValueError(f"unexpected gap width: {gap_width}")


def analyze(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the branch-1 exception symbolic summary."""
    for row in rows:
        validate_exception_row(row)

    return {
        "row_count": len(rows),
        "normal_form": "w = 18u, u prime",
        "all_witness_tau": EXPECTED_TAU,
        "counts_by_final_v2": count_rows(rows, "final_v2"),
        "counts_by_gap_width": count_rows(rows, "gap_width"),
        "counts_by_witness_gap_offset": count_rows(rows, "witness_gap_offset"),
        "counts_by_terminal_source_gap_offset": count_rows(
            rows,
            "terminal_source_gap_offset",
        ),
        "counts_by_witness_tau": count_rows(rows, "witness_tau"),
        "factor_form_rows": [
            {
                "factor_form": "w = 2 * 3^2 * u, u prime",
                "equivalent_form": "w = 18u, u prime",
                "count": len(rows),
            },
        ],
    }


def run_analyzer(input_path: Path, output_path: Path) -> dict[str, object]:
    """Analyze branch-1 exception rows and write the compact summary."""
    rows = read_jsonl(input_path)
    summary = analyze(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_path)
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Summarize branch-1 composite-terminal exception structure.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    """Run the command-line analyzer."""
    args = parse_args()
    summary = run_analyzer(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
