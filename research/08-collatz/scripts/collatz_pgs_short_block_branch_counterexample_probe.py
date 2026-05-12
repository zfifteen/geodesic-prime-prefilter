"""Search exact short-block below-minimizer branches by inverse construction."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import (
    median,
    percentile,
    rate,
    write_json,
    write_jsonl,
)
from collatz_pgs_same_gap_scale_probe import PrimeContext
from collatz_pgs_short_block_reset_candidate_probe import (
    TARGET_FINAL_V2,
    accelerated_odd_transition,
    v2,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIMIT = 10_000_000
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_short_block_branch_probe"
BRANCH_MIDDLE_V2 = {1: 1, 2: 2}
BRANCH_MOD9 = {1: 0, 2: 5}


def seed_from_witness(witness: int, branch: int) -> int:
    """Return the inverse exact 3-step seed for one below-minimizer branch."""
    if branch == 1:
        numerator = 4 * witness - 9
    elif branch == 2:
        numerator = 8 * witness - 13
    else:
        raise ValueError(f"unsupported branch {branch}")
    if numerator % 9 != 0:
        raise ValueError(f"witness {witness} does not close branch {branch}")
    return numerator // 9


def max_witness_for_seed_limit(limit: int, branch: int) -> int:
    """Return the greatest witness whose branch seed can be at most limit."""
    if branch == 1:
        return (9 * limit + 9) // 4
    if branch == 2:
        return (9 * limit + 13) // 8
    raise ValueError(f"unsupported branch {branch}")


def residue_classes(final_v2: int, branch: int) -> list[int]:
    """Return witness residues satisfying exact final-v2 and branch mod 9."""
    period = 9 * (1 << (final_v2 + 1))
    branch_mod9 = BRANCH_MOD9[branch]
    return [
        residue
        for residue in range(period)
        if residue % 9 == branch_mod9 and v2(3 * residue - 2) == final_v2
    ]


def witness_candidates(limit: int, final_v2: int, branch: int):
    """Yield witnesses in the branch/final-v2 residue class."""
    period = 9 * (1 << (final_v2 + 1))
    maximum = max_witness_for_seed_limit(limit, branch)
    for residue in residue_classes(final_v2, branch):
        witness = residue if residue > 0 else period
        while witness <= maximum:
            seed = seed_from_witness(witness, branch)
            if seed >= 3 and seed <= limit and seed % 2 == 1:
                yield witness, seed
            witness += period


def verify_exact_three_step(seed: int, terminal_source: int, final_v2: int) -> bool:
    """Return whether the inverse seed realizes the exact target block."""
    current = seed
    sources = []
    targets = []
    exponents = []
    for _ in range(3):
        target, exponent = accelerated_odd_transition(current)
        sources.append(current)
        targets.append(target)
        exponents.append(exponent)
        current = target
    return (
        sources[-1] == terminal_source
        and exponents == [1, exponents[1], final_v2]
        and exponents[1] in (1, 2)
        and targets[0] >= seed
        and targets[1] >= seed
        and targets[2] < seed
    )


def hit_record(
    context: PrimeContext,
    witness: int,
    seed: int,
    final_v2: int,
    branch: int,
) -> dict[str, object] | None:
    """Return one below-minimizer hit record if the witness is selected."""
    terminal_source = witness - 1
    state = context.source_state(terminal_source)
    if state.is_prime or state.witness != witness:
        return None
    if not verify_exact_three_step(seed, terminal_source, final_v2):
        raise ValueError(f"inverse branch failed for seed {seed}")
    target = (3 * terminal_source + 1) >> final_v2
    return {
        "seed": seed,
        "branch": branch,
        "middle_v2": BRANCH_MIDDLE_V2[branch],
        "final_v2": final_v2,
        "witness": witness,
        "witness_mod9": witness % 9,
        "terminal_source": terminal_source,
        "terminal_target": target,
        "reset_strength": seed / target,
        "prev_prime": state.prev_prime,
        "next_prime": state.next_prime,
        "gap_width": state.gap_width,
        "witness_tau": state.witness_tau,
        "terminal_tau": state.tau,
    }


def run_probe(limit: int, output_dir: Path) -> dict[str, object]:
    """Run the inverse-branch counterexample scan."""
    if limit < 3:
        raise ValueError("limit must be at least 3")

    max_witness = max(max_witness_for_seed_limit(limit, branch) for branch in (1, 2))
    context = PrimeContext(max_witness + 1024)
    hits: list[dict[str, object]] = []
    candidate_counts: Counter[str] = Counter()
    branch_hit_counts: Counter[str] = Counter()
    first_branch1_hit: dict[str, object] | None = None

    for final_v2 in TARGET_FINAL_V2:
        for branch in (1, 2):
            key = f"k{final_v2}_branch{branch}"
            for witness, seed in witness_candidates(limit, final_v2, branch):
                candidate_counts[key] += 1
                record = hit_record(context, witness, seed, final_v2, branch)
                if record is None:
                    continue
                hits.append(record)
                branch_hit_counts[key] += 1
                if branch == 1 and first_branch1_hit is None:
                    first_branch1_hit = record

    summary = {
        "limit": limit,
        "max_witness_checked": max_witness,
        "candidate_counts": {key: candidate_counts[key] for key in sorted(candidate_counts)},
        "below_minimizer_hit_counts": {
            key: branch_hit_counts[key] for key in sorted(candidate_counts)
        },
        "below_minimizer_hit_rate_by_candidate": {
            key: rate(branch_hit_counts[key], candidate_counts[key])
            for key in sorted(candidate_counts)
        },
        "hit_count": len(hits),
        "branch1_counterexample_count": sum(
            int(record["branch"]) == 1 for record in hits
        ),
        "branch2_hit_count": sum(int(record["branch"]) == 2 for record in hits),
        "first_branch1_counterexample": first_branch1_hit,
        "branch_selection_survives": first_branch1_hit is None,
        "hit_summary_by_branch": hit_summary_by_branch(hits),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(hits, output_dir / "hit_rows.jsonl")
    return summary


def compact_counter(counter: Counter[int]) -> dict[str, int]:
    """Return a sorted JSON-ready counter."""
    return {str(key): counter[key] for key in sorted(counter)}


def hit_summary_by_branch(hits: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return hit summaries grouped by final-v2 and branch."""
    groups: dict[tuple[int, int], list[dict[str, object]]] = {}
    for hit in hits:
        key = (int(hit["final_v2"]), int(hit["branch"]))
        groups.setdefault(key, []).append(hit)

    rows: list[dict[str, object]] = []
    for final_v2, branch in sorted(groups):
        group = groups[(final_v2, branch)]
        resets = [float(hit["reset_strength"]) for hit in group]
        seeds = [int(hit["seed"]) for hit in group]
        gap_widths = Counter(int(hit["gap_width"]) for hit in group)
        rows.append(
            {
                "final_v2": final_v2,
                "branch": branch,
                "count": len(group),
                "first_seed": min(seeds),
                "median_reset_strength": median(resets),
                "p90_reset_strength": percentile(resets, 0.90),
                "p99_reset_strength": percentile(resets, 0.99),
                "gap_width_distribution": compact_counter(gap_widths),
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Search inverse exact 3-step below-minimizer branches for "
            "branch-1 counterexamples."
        ),
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
