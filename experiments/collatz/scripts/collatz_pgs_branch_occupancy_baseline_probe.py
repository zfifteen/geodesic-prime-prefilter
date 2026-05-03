"""Measure divisor-count baseline obstruction for short-block branches."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import median, rate, write_json, write_jsonl
from collatz_pgs_same_gap_scale_probe import PrimeContext
from collatz_pgs_short_block_branch_counterexample_probe import (
    TARGET_FINAL_V2,
    max_witness_for_seed_limit,
    witness_candidates,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIMIT = 10_000_000
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_branch_occupancy_baseline_probe"


def cached_tau(context: PrimeContext, cache: dict[int, int], n: int) -> int:
    """Return exact divisor count.

    The cache parameter keeps the call surface explicit for tests and future
    instrumentation, but this probe does not retain every interior divisor
    count across the full scan. Most gap-interior values are one-shot, and a
    global cache makes the exact full-scale pass memory-bound.
    """
    return context.divisor_count(n)


def divisor_rank(
    context: PrimeContext,
    cache: dict[int, int],
    witness: int,
) -> dict[str, object]:
    """Return divisor-count rank data for witness inside its prime gap."""
    if context.is_prime(witness):
        raise ValueError(f"witness {witness} should be composite")
    prev_prime = context.previous_prime(witness)
    next_prime = context.next_prime(witness)

    witness_tau = cached_tau(context, cache, witness)
    lower_count = 0
    equal_before_count = 0
    equal_total_count = 0
    interior_count = 0
    for value in range(prev_prime + 1, next_prime):
        interior_count += 1
        tau = cached_tau(context, cache, value)
        if tau < witness_tau:
            lower_count += 1
        if tau == witness_tau:
            equal_total_count += 1
            if value < witness:
                equal_before_count += 1

    return {
        "prev_prime": prev_prime,
        "next_prime": next_prime,
        "gap_width": next_prime - prev_prime,
        "interior_count": interior_count,
        "witness_tau": witness_tau,
        "lower_tau_competitor_count": lower_count,
        "equal_tau_before_count": equal_before_count,
        "equal_tau_total_count": equal_total_count,
        "leftmost_minimizer": lower_count == 0 and equal_before_count == 0,
    }


def candidate_record(
    context: PrimeContext,
    cache: dict[int, int],
    witness: int,
    seed: int,
    final_v2: int,
    branch: int,
) -> dict[str, object]:
    """Return one inverse-eligible branch candidate record."""
    rank = divisor_rank(context, cache, witness)
    terminal_source = witness - 1
    terminal_state = context.source_state(terminal_source)
    below_minimizer_hit = (
        not terminal_state.is_prime
        and terminal_state.prev_prime == rank["prev_prime"]
        and terminal_state.next_prime == rank["next_prime"]
        and terminal_state.witness == witness
    )
    return {
        "seed": seed,
        "branch": branch,
        "final_v2": final_v2,
        "witness": witness,
        "terminal_source": terminal_source,
        "terminal_source_is_prime": terminal_state.is_prime,
        "below_minimizer_hit": below_minimizer_hit,
        **rank,
    }


def bin_gap_width(width: int) -> str:
    """Return a compact gap-width bin."""
    if width <= 16:
        return str(width)
    if width <= 32:
        return "18-32"
    if width <= 64:
        return "34-64"
    return ">=66"


def bin_lower_count(count: int) -> str:
    """Return a compact lower-competitor bin."""
    if count <= 4:
        return str(count)
    return ">=5"


class GroupStats:
    """Accumulate candidate and hit statistics for one group."""

    def __init__(self) -> None:
        self.count = 0
        self.hit_count = 0
        self.leftmost_count = 0
        self.taus: list[int] = []
        self.lower_counts: list[int] = []
        self.gap_widths: list[int] = []

    def add(self, record: dict[str, object]) -> None:
        """Add one candidate record."""
        self.count += 1
        self.hit_count += int(bool(record["below_minimizer_hit"]))
        self.leftmost_count += int(bool(record["leftmost_minimizer"]))
        self.taus.append(int(record["witness_tau"]))
        self.lower_counts.append(int(record["lower_tau_competitor_count"]))
        self.gap_widths.append(int(record["gap_width"]))

    def row(self) -> dict[str, object]:
        """Return JSON-ready statistics."""
        return {
            "candidate_count": self.count,
            "below_minimizer_hit_count": self.hit_count,
            "below_minimizer_hit_rate": rate(self.hit_count, self.count),
            "leftmost_minimizer_count": self.leftmost_count,
            "leftmost_minimizer_rate": rate(self.leftmost_count, self.count),
            "below_hit_per_leftmost_minimizer_rate": rate(
                self.hit_count,
                self.leftmost_count,
            ),
            "median_witness_tau": median(self.taus),
            "median_lower_tau_competitor_count": median(self.lower_counts),
            "median_gap_width": median(self.gap_widths),
        }


def grouped_rows(
    records: list[dict[str, object]],
    key_names: tuple[str, ...],
) -> list[dict[str, object]]:
    """Return grouped candidate statistics."""
    groups: dict[tuple[object, ...], GroupStats] = defaultdict(GroupStats)
    for record in records:
        groups[tuple(record[key] for key in key_names)].add(record)

    rows: list[dict[str, object]] = []
    for key in sorted(groups):
        row = groups[key].row()
        for index, key_name in enumerate(key_names):
            row[key_name] = key[index]
        rows.append(row)
    return rows


def run_probe(limit: int, output_dir: Path) -> dict[str, object]:
    """Run the branch occupancy baseline probe."""
    if limit < 3:
        raise ValueError("limit must be at least 3")

    max_witness = max(max_witness_for_seed_limit(limit, branch) for branch in (1, 2))
    context = PrimeContext(max_witness + 1024)
    tau_cache: dict[int, int] = {}
    records: list[dict[str, object]] = []

    for final_v2 in TARGET_FINAL_V2:
        for branch in (1, 2):
            for witness, seed in witness_candidates(limit, final_v2, branch):
                record = candidate_record(context, tau_cache, witness, seed, final_v2, branch)
                record["gap_width_bin"] = bin_gap_width(int(record["gap_width"]))
                record["lower_tau_competitor_bin"] = bin_lower_count(
                    int(record["lower_tau_competitor_count"]),
                )
                records.append(record)

    branch_rows = grouped_rows(records, ("final_v2", "branch"))
    tau_rows = grouped_rows(records, ("final_v2", "branch", "witness_tau"))
    gap_width_rows = grouped_rows(records, ("final_v2", "branch", "gap_width_bin"))
    lower_competitor_rows = grouped_rows(
        records,
        ("final_v2", "branch", "lower_tau_competitor_bin"),
    )
    terminal_source_rows = grouped_rows(
        records,
        ("final_v2", "branch", "terminal_source_is_prime"),
    )
    leftmost_terminal_rows = grouped_rows(
        records,
        ("final_v2", "branch", "leftmost_minimizer", "terminal_source_is_prime"),
    )
    branch_totals = grouped_rows(records, ("branch",))
    hit_counts = Counter(int(record["branch"]) for record in records if record["below_minimizer_hit"])
    candidate_counts = Counter(int(record["branch"]) for record in records)
    summary = {
        "limit": limit,
        "max_witness_checked": max_witness,
        "candidate_count": len(records),
        "tau_cache_size": len(tau_cache),
        "candidate_count_by_branch": {
            str(branch): candidate_counts[branch] for branch in sorted(candidate_counts)
        },
        "below_minimizer_hit_count_by_branch": {
            str(branch): hit_counts[branch] for branch in sorted(candidate_counts)
        },
        "below_minimizer_hit_rate_by_branch": {
            str(branch): rate(hit_counts[branch], candidate_counts[branch])
            for branch in sorted(candidate_counts)
        },
        "branch_rows": branch_rows,
        "branch_totals": branch_totals,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(branch_rows, output_dir / "branch_rows.jsonl")
    write_jsonl(tau_rows, output_dir / "tau_rows.jsonl")
    write_jsonl(gap_width_rows, output_dir / "gap_width_rows.jsonl")
    write_jsonl(lower_competitor_rows, output_dir / "lower_competitor_rows.jsonl")
    write_jsonl(terminal_source_rows, output_dir / "terminal_source_rows.jsonl")
    write_jsonl(leftmost_terminal_rows, output_dir / "leftmost_terminal_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Measure divisor-count baseline obstruction for short-block branches.",
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    """Run the command-line probe."""
    args = parse_args()
    summary = run_probe(int(args.limit), Path(args.output_dir))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
