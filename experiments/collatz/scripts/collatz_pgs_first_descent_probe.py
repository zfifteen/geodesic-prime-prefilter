"""Probe PGS state inside odd Collatz first-descent blocks."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_first_descent_probe"
DEFAULT_LIMIT = 10_000


@dataclass(frozen=True)
class Transition:
    """One accelerated odd Collatz transition."""

    source: int
    target: int
    v2: int


@dataclass(frozen=True)
class GapState:
    """Prime-gap and selected-witness state for one integer."""

    n: int
    tau: int
    is_prime: bool
    prev_prime: int
    next_prime: int
    gap_width: int
    gap_offset: int
    witness: int
    witness_tau: int
    odd_witness_distance: int
    odd_witness_projected_hit: bool
    endpoint_distance: int
    f_value: float


class ProfileAccumulator:
    """Accumulate prime-endpoint and composite interior PGS rates."""

    def __init__(self) -> None:
        self.count = 0
        self.prime_count = 0
        self.composite_count = 0
        self.projected_hits = 0
        self.exact_witness_hits = 0
        self.near_endpoint = 0
        self.witness_distances: Counter[int] = Counter()
        self.endpoint_distances: Counter[int] = Counter()

    def add(self, state: GapState) -> None:
        """Add one PGS state."""
        self.count += 1
        self.endpoint_distances[state.endpoint_distance] += 1
        if state.endpoint_distance <= 2:
            self.near_endpoint += 1
        if state.is_prime:
            self.prime_count += 1
            return

        self.composite_count += 1
        self.witness_distances[state.odd_witness_distance] += 1
        if state.odd_witness_projected_hit:
            self.projected_hits += 1
        if state.n == state.witness:
            self.exact_witness_hits += 1

    def record(self) -> dict[str, object]:
        """Return a JSON-ready profile."""
        return {
            "count": self.count,
            "prime_count": self.prime_count,
            "prime_rate": rate(self.prime_count, self.count),
            "composite_count": self.composite_count,
            "interior_odd_projected_witness_hit_count": self.projected_hits,
            "interior_odd_projected_witness_hit_rate": rate(
                self.projected_hits,
                self.composite_count,
            ),
            "interior_exact_witness_hit_count": self.exact_witness_hits,
            "interior_exact_witness_hit_rate": rate(
                self.exact_witness_hits,
                self.composite_count,
            ),
            "near_endpoint_count": self.near_endpoint,
            "near_endpoint_rate": rate(self.near_endpoint, self.count),
            "median_interior_odd_witness_distance": counter_median(
                self.witness_distances,
            ),
            "median_endpoint_distance": counter_median(self.endpoint_distances),
        }

    def distance_histogram(self, cap: int = 10) -> dict[str, int]:
        """Return a capped histogram of composite odd-witness distances."""
        counter: Counter[str] = Counter()
        for distance, count in self.witness_distances.items():
            key = str(distance) if distance <= cap else f">{cap}"
            counter[key] += count
        return ordered_histogram(counter)


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


def v2(value: int) -> int:
    """Return the exponent of 2 in one positive even integer."""
    return (value & -value).bit_length() - 1


def accelerated_odd_transition(n: int) -> Transition:
    """Return one accelerated odd Collatz transition."""
    value = 3 * n + 1
    exponent = v2(value)
    return Transition(source=n, target=value >> exponent, v2=exponent)


def first_descent_block(seed: int) -> list[Transition]:
    """Return odd transitions through the first target below the seed."""
    transitions: list[Transition] = []
    current = seed
    while True:
        transition = accelerated_odd_transition(current)
        transitions.append(transition)
        if transition.target < seed:
            return transitions
        current = transition.target


def smallest_prime_factors(limit: int) -> list[int]:
    """Return the smallest prime factor for every integer up to limit."""
    spf = [0] * (limit + 1)
    if limit >= 1:
        spf[1] = 1
    for number in range(2, limit + 1):
        if spf[number] != 0:
            continue
        spf[number] = number
        if number * number > limit:
            continue
        for composite in range(number * number, limit + 1, number):
            if spf[composite] == 0:
                spf[composite] = number
    return spf


def divisor_counts_from_spf(spf: list[int]) -> list[int]:
    """Return exact divisor counts from a smallest-prime-factor table."""
    limit = len(spf) - 1
    tau = [0] * (limit + 1)
    exponent = [0] * (limit + 1)
    tau[1] = 1
    for number in range(2, limit + 1):
        prime = spf[number]
        quotient = number // prime
        if quotient % prime == 0:
            exponent[number] = exponent[quotient] + 1
            tau[number] = (
                tau[quotient]
                // (exponent[quotient] + 1)
                * (exponent[number] + 1)
            )
        else:
            exponent[number] = 1
            tau[number] = tau[quotient] * 2
    return tau


def odd_projected_witness_distance(n: int, p: int, q: int, witness: int) -> int:
    """Return distance from n to the odd cells nearest the PGS witness."""
    candidates = [
        value
        for value in (witness - 1, witness, witness + 1)
        if p < value < q and value % 2 == 1
    ]
    if not candidates:
        return min(abs(n - p), abs(q - n))
    return min(abs(n - value) for value in candidates)


def build_gap_states(max_lookup: int) -> dict[int, GapState]:
    """Return PGS gap state for odd integers up to max_lookup."""
    sieve_limit = max(8, 2 * max_lookup)
    spf = smallest_prime_factors(sieve_limit)
    tau = divisor_counts_from_spf(spf)
    primes = [number for number in range(2, sieve_limit + 1) if spf[number] == number]
    states: dict[int, GapState] = {}

    for prime in primes:
        if prime > max_lookup:
            break
        if prime % 2 == 1:
            states[prime] = GapState(
                n=prime,
                tau=2,
                is_prime=True,
                prev_prime=prime,
                next_prime=prime,
                gap_width=0,
                gap_offset=0,
                witness=prime,
                witness_tau=2,
                odd_witness_distance=0,
                odd_witness_projected_hit=False,
                endpoint_distance=0,
                f_value=0.0,
            )

    for left, right in zip(primes, primes[1:]):
        if left > max_lookup:
            break
        if right - left <= 1:
            continue
        interior = range(left + 1, right)
        witness = min(interior, key=lambda value: (tau[value], value))
        witness_tau = tau[witness]
        for n in range(left + 1, right):
            if n % 2 == 0:
                continue
            divisor_count = tau[n]
            witness_distance = odd_projected_witness_distance(n, left, right, witness)
            endpoint_distance = min(n - left, right - n)
            states[n] = GapState(
                n=n,
                tau=divisor_count,
                is_prime=False,
                prev_prime=left,
                next_prime=right,
                gap_width=right - left,
                gap_offset=n - left,
                witness=witness,
                witness_tau=witness_tau,
                odd_witness_distance=witness_distance,
                odd_witness_projected_hit=witness_distance == 0,
                endpoint_distance=endpoint_distance,
                f_value=(1.0 - divisor_count / 2.0) * math.log(n),
            )
    return states


def median_int(values: list[int]) -> float:
    """Return a stable numeric median."""
    if not values:
        return 0.0
    return float(statistics.median(values))


def counter_median(counter: Counter[int]) -> float:
    """Return the exact median represented by an integer counter."""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    left_index = (total - 1) // 2
    right_index = total // 2
    left_value = 0
    right_value = 0
    seen = 0
    for value in sorted(counter):
        next_seen = seen + counter[value]
        if seen <= left_index < next_seen:
            left_value = value
        if seen <= right_index < next_seen:
            right_value = value
            break
        seen = next_seen
    return (left_value + right_value) / 2.0


def rate(numerator: int, denominator: int) -> float:
    """Return a zero-safe rate."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def rate_ratio(
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> float:
    """Return a zero-safe ratio of two rates."""
    right = rate(right_numerator, right_denominator)
    if right == 0.0:
        return 0.0
    return rate(left_numerator, left_denominator) / right


def profile(values: list[int], states: dict[int, GapState]) -> dict[str, object]:
    """Return PGS rates for one collection of odd integers."""
    accumulator = ProfileAccumulator()
    for value in values:
        accumulator.add(states[value])
    return accumulator.record()


def ordered_histogram(counter: Counter[str]) -> dict[str, int]:
    """Return a numeric histogram with the capped bucket last."""
    return {
        key: counter[key]
        for key in sorted(
            counter,
            key=lambda item: (
                item.startswith(">"),
                int(item[1:] if item.startswith(">") else item),
            ),
        )
    }


def distance_histogram(
    values: list[int],
    states: dict[int, GapState],
    cap: int = 10,
) -> dict[str, int]:
    """Return a capped histogram of composite odd-witness distances."""
    accumulator = ProfileAccumulator()
    for value in values:
        accumulator.add(states[value])
    return accumulator.distance_histogram(cap)


def compact_v2_histogram(transitions: list[Transition]) -> dict[str, int]:
    """Return a compact v2 histogram."""
    counter: Counter[str] = Counter()
    for transition in transitions:
        key = str(transition.v2) if transition.v2 <= 6 else ">6"
        counter[key] += 1
    return ordered_histogram(counter)


def v2_bin(exponent: int) -> str:
    """Return the v2 stratum used for same-gap witness checks."""
    if exponent <= 2:
        return str(exponent)
    if exponent <= 4:
        return "3-4"
    return ">=5"


def block_background_values(seed: int, max_source: int) -> range:
    """Return every odd integer in the block's deterministic background interval."""
    return range(seed, max_source + 1, 2)


def gap_interior_odd_values(state: GapState) -> range:
    """Return every odd interior integer in a state's containing prime gap."""
    if state.is_prime:
        return range(1, 1)
    start = state.prev_prime + 1
    if start % 2 == 0:
        start += 1
    return range(start, state.next_prime, 2)


def run_probe(limit: int, output_dir: Path) -> dict[str, object]:
    """Run the Collatz-PGS first-descent probe."""
    if limit < 3:
        raise ValueError("limit must be at least 3")

    seed_transitions: dict[int, list[Transition]] = {}
    max_seen = 3
    for seed in range(3, limit + 1, 2):
        transitions = first_descent_block(seed)
        seed_transitions[seed] = transitions
        max_seen = max(
            max_seen,
            max(transition.source for transition in transitions),
            transitions[-1].target,
        )

    states = build_gap_states(max_seen)
    block_rows: list[dict[str, object]] = []
    state_rows: list[dict[str, object]] = []
    source_values: list[int] = []
    final_source_values: list[int] = []
    background_accumulator = ProfileAccumulator()
    source_gap_background_accumulator = ProfileAccumulator()
    final_gap_background_accumulator = ProfileAccumulator()
    source_by_v2 = {
        "1": ProfileAccumulator(),
        "2": ProfileAccumulator(),
        "3-4": ProfileAccumulator(),
        ">=5": ProfileAccumulator(),
    }
    source_gap_background_by_v2 = {
        "1": ProfileAccumulator(),
        "2": ProfileAccumulator(),
        "3-4": ProfileAccumulator(),
        ">=5": ProfileAccumulator(),
    }
    all_transitions: list[Transition] = []

    for seed, transitions in seed_transitions.items():
        sources = [transition.source for transition in transitions]
        final_source = transitions[-1].source
        terminal = transitions[-1].target
        background = block_background_values(seed, max(sources))
        source_values.extend(sources)
        final_source_values.append(final_source)
        for value in background:
            background_accumulator.add(states[value])
        all_transitions.extend(transitions)

        for transition in transitions:
            source_state = states[transition.source]
            bin_label = v2_bin(transition.v2)
            source_by_v2[bin_label].add(source_state)
            for value in gap_interior_odd_values(source_state):
                source_gap_background_accumulator.add(states[value])
                source_gap_background_by_v2[bin_label].add(states[value])

        final_state = states[final_source]
        for value in gap_interior_odd_values(final_state):
            final_gap_background_accumulator.add(states[value])

        block_profile = profile(sources, states)
        max_source = max(sources)
        v2_sum = sum(transition.v2 for transition in transitions)
        block_rows.append(
            {
                "seed": seed,
                "odd_steps_to_first_descent": len(transitions),
                "terminal_below_seed": terminal,
                "max_source": max_source,
                "max_source_over_seed": max_source / seed,
                "v2_sum": v2_sum,
                "v2_excess_over_3_growth": v2_sum - len(transitions) * math.log2(3),
                "source_count": block_profile["count"],
                "source_prime_count": block_profile["prime_count"],
                "source_prime_rate": block_profile["prime_rate"],
                "source_composite_count": block_profile["composite_count"],
                "source_interior_odd_projected_witness_hit_count": block_profile[
                    "interior_odd_projected_witness_hit_count"
                ],
                "source_interior_odd_projected_witness_hit_rate": block_profile[
                    "interior_odd_projected_witness_hit_rate"
                ],
                "source_median_interior_odd_witness_distance": block_profile[
                    "median_interior_odd_witness_distance"
                ],
                "final_source": final_source,
                "final_v2": transitions[-1].v2,
                "final_is_prime": final_state.is_prime,
                "final_tau": final_state.tau,
                "final_prev_prime": final_state.prev_prime,
                "final_next_prime": final_state.next_prime,
                "final_gap_width": final_state.gap_width,
                "final_gap_offset": final_state.gap_offset,
                "final_witness": final_state.witness,
                "final_witness_tau": final_state.witness_tau,
                "final_odd_witness_distance": final_state.odd_witness_distance,
                "final_odd_projected_witness_hit": final_state.odd_witness_projected_hit,
                "final_endpoint_distance": final_state.endpoint_distance,
                "background_odd_count": len(background),
            }
        )

        for index, transition in enumerate(transitions):
            state = states[transition.source]
            state_rows.append(
                {
                    "seed": seed,
                    "transition_index": index,
                    "source": transition.source,
                    "target": transition.target,
                    "v2": transition.v2,
                    "is_final_source": index == len(transitions) - 1,
                    "tau": state.tau,
                    "is_prime": state.is_prime,
                    "prev_prime": state.prev_prime,
                    "next_prime": state.next_prime,
                    "gap_width": state.gap_width,
                    "gap_offset": state.gap_offset,
                    "witness": state.witness,
                    "witness_tau": state.witness_tau,
                    "odd_witness_distance": state.odd_witness_distance,
                    "odd_projected_witness_hit": state.odd_witness_projected_hit,
                    "endpoint_distance": state.endpoint_distance,
                    "f_value": state.f_value,
                }
            )

    source_profile = profile(source_values, states)
    final_profile = profile(final_source_values, states)
    background_profile = background_accumulator.record()
    source_gap_background_profile = source_gap_background_accumulator.record()
    final_gap_background_profile = final_gap_background_accumulator.record()
    same_gap_witness_by_v2 = {}
    for bin_label in ("1", "2", "3-4", ">=5"):
        source_bin_profile = source_by_v2[bin_label].record()
        background_bin_profile = source_gap_background_by_v2[bin_label].record()
        same_gap_witness_by_v2[bin_label] = {
            "source_profile": source_bin_profile,
            "source_gap_background_profile": background_bin_profile,
            "source_vs_same_gap_witness_hit_ratio": rate_ratio(
                int(source_bin_profile["interior_odd_projected_witness_hit_count"]),
                int(source_bin_profile["composite_count"]),
                int(background_bin_profile["interior_odd_projected_witness_hit_count"]),
                int(background_bin_profile["composite_count"]),
            ),
        }
    summary = {
        "limit": limit,
        "odd_seed_count": len(seed_transitions),
        "max_seen_in_first_descent_blocks": max_seen,
        "total_source_states": len(source_values),
        "total_background_states": int(background_profile["count"]),
        "max_odd_steps_to_first_descent": max(
            len(transitions) for transitions in seed_transitions.values()
        ),
        "median_odd_steps_to_first_descent": median_int(
            [len(transitions) for transitions in seed_transitions.values()]
        ),
        "max_source_over_seed": max(row["max_source_over_seed"] for row in block_rows),
        "source_profile": source_profile,
        "final_source_profile": final_profile,
        "background_profile": background_profile,
        "source_gap_background_profile": source_gap_background_profile,
        "final_gap_background_profile": final_gap_background_profile,
        "same_gap_witness_by_v2": same_gap_witness_by_v2,
        "source_vs_background_witness_hit_ratio": rate_ratio(
            int(source_profile["interior_odd_projected_witness_hit_count"]),
            int(source_profile["composite_count"]),
            int(background_profile["interior_odd_projected_witness_hit_count"]),
            int(background_profile["composite_count"]),
        ),
        "final_vs_background_witness_hit_ratio": rate_ratio(
            int(final_profile["interior_odd_projected_witness_hit_count"]),
            int(final_profile["composite_count"]),
            int(background_profile["interior_odd_projected_witness_hit_count"]),
            int(background_profile["composite_count"]),
        ),
        "source_vs_background_prime_hit_ratio": rate_ratio(
            int(source_profile["prime_count"]),
            int(source_profile["count"]),
            int(background_profile["prime_count"]),
            int(background_profile["count"]),
        ),
        "final_vs_background_prime_hit_ratio": rate_ratio(
            int(final_profile["prime_count"]),
            int(final_profile["count"]),
            int(background_profile["prime_count"]),
            int(background_profile["count"]),
        ),
        "source_vs_same_gap_witness_hit_ratio": rate_ratio(
            int(source_profile["interior_odd_projected_witness_hit_count"]),
            int(source_profile["composite_count"]),
            int(source_gap_background_profile["interior_odd_projected_witness_hit_count"]),
            int(source_gap_background_profile["composite_count"]),
        ),
        "final_vs_same_gap_witness_hit_ratio": rate_ratio(
            int(final_profile["interior_odd_projected_witness_hit_count"]),
            int(final_profile["composite_count"]),
            int(final_gap_background_profile["interior_odd_projected_witness_hit_count"]),
            int(final_gap_background_profile["composite_count"]),
        ),
        "source_odd_witness_distance_histogram": distance_histogram(source_values, states),
        "final_source_odd_witness_distance_histogram": distance_histogram(
            final_source_values,
            states,
        ),
        "background_odd_witness_distance_histogram": (
            background_accumulator.distance_histogram()
        ),
        "source_gap_background_odd_witness_distance_histogram": (
            source_gap_background_accumulator.distance_histogram()
        ),
        "final_gap_background_odd_witness_distance_histogram": (
            final_gap_background_accumulator.distance_histogram()
        ),
        "v2_histogram": compact_v2_histogram(all_transitions),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(block_rows, output_dir / "block_rows.jsonl")
    write_jsonl(state_rows, output_dir / "state_rows.jsonl")
    return summary


def write_plot(summary: dict[str, object], output_dir: Path) -> Path:
    """Write one comparison plot."""
    import matplotlib.pyplot as plt

    keys = [str(value) for value in range(0, 11)] + [">10"]
    profiles = [
        ("source", summary["source_odd_witness_distance_histogram"]),
        ("final source", summary["final_source_odd_witness_distance_histogram"]),
        ("background", summary["background_odd_witness_distance_histogram"]),
    ]
    x_positions = list(range(len(keys)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(11, 5.8))
    for offset, (label, raw_histogram) in enumerate(profiles):
        histogram = dict(raw_histogram)
        total = sum(int(histogram.get(key, 0)) for key in keys)
        values = [rate(int(histogram.get(key, 0)), total) for key in keys]
        shifted = [position + (offset - 1) * width for position in x_positions]
        ax.bar(shifted, values, width=width, label=label)
    ax.set_title("Collatz first-descent states by odd-projected PGS witness distance")
    ax.set_xlabel("distance to odd cell nearest the PGS witness")
    ax.set_ylabel("share of states")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(keys)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    path = output_dir / "collatz_pgs_first_descent_profile.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Probe PGS state inside odd Collatz first-descent blocks.",
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--plot", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Run the command-line probe."""
    args = parse_args()
    summary = run_probe(int(args.limit), Path(args.output_dir))
    if args.plot:
        plot_path = write_plot(summary, Path(args.output_dir))
        summary["plot"] = str(plot_path.relative_to(ROOT))
        write_json(summary, Path(args.output_dir) / "summary.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
