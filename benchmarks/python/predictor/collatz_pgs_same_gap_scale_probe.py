"""Scale same-gap PGS witness checks on odd Collatz first-descent blocks."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_same_gap_scale_probe"
DEFAULT_LIMIT = 200_000
V2_BINS = ("1", "2", "3-4", ">=5")
MR_BASES_64 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


@dataclass(frozen=True)
class Transition:
    """One accelerated odd Collatz transition."""

    source: int
    target: int
    v2: int


@dataclass(frozen=True)
class GapProfile:
    """Containing prime-gap witness profile."""

    left_prime: int
    right_prime: int
    witness: int
    witness_tau: int
    odd_interior_count: int
    odd_projected_witness_hit_count: int


@dataclass(frozen=True)
class SourceState:
    """PGS state attached to one Collatz source integer."""

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
    odd_projected_witness_hit: bool
    endpoint_distance: int


class PrimeContext:
    """Exact local prime-gap and divisor-count context."""

    def __init__(self, max_value: int) -> None:
        self.factor_primes = small_primes(math.isqrt(max(4, 2 * max_value)) + 16)
        self.source_cache: dict[int, SourceState] = {}
        self.gap_cache: dict[tuple[int, int], GapProfile] = {}
        self.prime_cache: dict[int, bool] = {}

    def is_prime(self, n: int) -> bool:
        """Return exact primality for one 64-bit integer."""
        cached = self.prime_cache.get(n)
        if cached is not None:
            return cached

        if n < 2:
            result = False
        elif n in MR_BASES_64:
            result = True
        elif n % 2 == 0:
            result = False
        else:
            result = True
            for base in MR_BASES_64:
                if n == base:
                    result = True
                    break
                if n % base == 0:
                    result = False
                    break
            if result:
                result = strong_base_test(n)

        self.prime_cache[n] = result
        return result

    def divisor_count(self, n: int) -> int:
        """Return exact divisor count."""
        remaining = n
        total = 1
        for prime in self.factor_primes:
            if prime * prime > remaining:
                break
            if remaining % prime != 0:
                continue
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            total *= exponent + 1
        if remaining > 1:
            total *= 2
        return total

    def previous_prime(self, n: int) -> int:
        """Return the greatest prime below n."""
        candidate = n - 1
        if candidate % 2 == 0:
            candidate -= 1
        while candidate >= 3:
            if self.is_prime(candidate):
                return candidate
            candidate -= 2
        return 2

    def next_prime(self, n: int) -> int:
        """Return the least prime above n."""
        candidate = n + 1
        if candidate % 2 == 0:
            candidate += 1
        while True:
            if self.is_prime(candidate):
                return candidate
            candidate += 2

    def gap_profile(self, left_prime: int, right_prime: int) -> GapProfile:
        """Return the PGS witness profile for one prime gap."""
        key = (left_prime, right_prime)
        cached = self.gap_cache.get(key)
        if cached is not None:
            return cached

        witness = left_prime + 1
        witness_tau = self.divisor_count(witness)
        for value in range(left_prime + 2, right_prime):
            divisor_count = self.divisor_count(value)
            if divisor_count < witness_tau:
                witness = value
                witness_tau = divisor_count

        odd_start = left_prime + 1
        if odd_start % 2 == 0:
            odd_start += 1
        odd_interior_count = len(range(odd_start, right_prime, 2))
        odd_projected_witness_hit_count = len(
            odd_projected_witness_cells(left_prime, right_prime, witness)
        )
        profile = GapProfile(
            left_prime=left_prime,
            right_prime=right_prime,
            witness=witness,
            witness_tau=witness_tau,
            odd_interior_count=odd_interior_count,
            odd_projected_witness_hit_count=odd_projected_witness_hit_count,
        )
        self.gap_cache[key] = profile
        return profile

    def source_state(self, n: int) -> SourceState:
        """Return PGS state for one Collatz source."""
        cached = self.source_cache.get(n)
        if cached is not None:
            return cached

        if self.is_prime(n):
            state = SourceState(
                n=n,
                tau=2,
                is_prime=True,
                prev_prime=n,
                next_prime=n,
                gap_width=0,
                gap_offset=0,
                witness=n,
                witness_tau=2,
                odd_witness_distance=0,
                odd_projected_witness_hit=False,
                endpoint_distance=0,
            )
            self.source_cache[n] = state
            return state

        prev_prime = self.previous_prime(n)
        next_prime = self.next_prime(n)
        gap = self.gap_profile(prev_prime, next_prime)
        witness_distance = odd_projected_witness_distance(
            n,
            prev_prime,
            next_prime,
            gap.witness,
        )
        state = SourceState(
            n=n,
            tau=self.divisor_count(n),
            is_prime=False,
            prev_prime=prev_prime,
            next_prime=next_prime,
            gap_width=next_prime - prev_prime,
            gap_offset=n - prev_prime,
            witness=gap.witness,
            witness_tau=gap.witness_tau,
            odd_witness_distance=witness_distance,
            odd_projected_witness_hit=witness_distance == 0,
            endpoint_distance=min(n - prev_prime, next_prime - n),
        )
        self.source_cache[n] = state
        return state


class SourceAccumulator:
    """Accumulate source-state counts."""

    def __init__(self) -> None:
        self.count = 0
        self.prime_count = 0
        self.composite_count = 0
        self.witness_hit_count = 0
        self.exact_witness_hit_count = 0

    def add(self, state: SourceState) -> None:
        """Add one source state."""
        self.count += 1
        if state.is_prime:
            self.prime_count += 1
            return
        self.composite_count += 1
        if state.odd_projected_witness_hit:
            self.witness_hit_count += 1
        if state.n == state.witness:
            self.exact_witness_hit_count += 1

    def record(self) -> dict[str, object]:
        """Return one JSON-ready source profile."""
        return {
            "count": self.count,
            "prime_count": self.prime_count,
            "prime_rate": rate(self.prime_count, self.count),
            "composite_count": self.composite_count,
            "witness_hit_count": self.witness_hit_count,
            "witness_hit_rate": rate(self.witness_hit_count, self.composite_count),
            "exact_witness_hit_count": self.exact_witness_hit_count,
            "exact_witness_hit_rate": rate(
                self.exact_witness_hit_count,
                self.composite_count,
            ),
        }


class SameGapAccumulator:
    """Accumulate same-gap background counts."""

    def __init__(self) -> None:
        self.composite_count = 0
        self.witness_hit_count = 0

    def add(self, gap: GapProfile) -> None:
        """Add one containing-gap background."""
        self.composite_count += gap.odd_interior_count
        self.witness_hit_count += gap.odd_projected_witness_hit_count

    def record(self) -> dict[str, object]:
        """Return one JSON-ready same-gap profile."""
        return {
            "composite_count": self.composite_count,
            "witness_hit_count": self.witness_hit_count,
            "witness_hit_rate": rate(self.witness_hit_count, self.composite_count),
        }


class BlockAccumulator:
    """Accumulate reset-profile values for one block class."""

    def __init__(self) -> None:
        self.count = 0
        self.final_source_count = 0
        self.final_source_witness_hit_count = 0
        self.reset_strengths: list[float] = []
        self.odd_steps: list[int] = []
        self.max_source_over_seed_values: list[float] = []

    def add(
        self,
        reset_strength: float,
        odd_steps: int,
        max_source_over_seed: float,
        final_source_witness_hit: bool,
    ) -> None:
        """Add one first-descent block."""
        self.count += 1
        self.final_source_count += 1
        if final_source_witness_hit:
            self.final_source_witness_hit_count += 1
        self.reset_strengths.append(reset_strength)
        self.odd_steps.append(odd_steps)
        self.max_source_over_seed_values.append(max_source_over_seed)

    def record(self) -> dict[str, object]:
        """Return one JSON-ready reset profile."""
        return {
            "block_count": self.count,
            "median_reset_strength": median(self.reset_strengths),
            "p90_reset_strength": percentile(self.reset_strengths, 0.90),
            "p99_reset_strength": percentile(self.reset_strengths, 0.99),
            "max_reset_strength": max_or_zero(self.reset_strengths),
            "median_odd_steps_to_first_descent": median(self.odd_steps),
            "p90_odd_steps_to_first_descent": percentile(self.odd_steps, 0.90),
            "max_odd_steps_to_first_descent": max_or_zero(self.odd_steps),
            "median_max_source_over_seed": median(self.max_source_over_seed_values),
            "p90_max_source_over_seed": percentile(
                self.max_source_over_seed_values,
                0.90,
            ),
            "max_source_over_seed": max_or_zero(self.max_source_over_seed_values),
            "final_source_witness_hit_count": self.final_source_witness_hit_count,
            "final_source_witness_hit_rate": rate(
                self.final_source_witness_hit_count,
                self.final_source_count,
            ),
        }


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


def small_primes(limit: int) -> list[int]:
    """Return every prime up to limit."""
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for value in range(2, math.isqrt(limit) + 1):
        if not sieve[value]:
            continue
        start = value * value
        sieve[start : limit + 1 : value] = b"\x00" * (((limit - start) // value) + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


def strong_base_test(n: int) -> bool:
    """Return exact deterministic primality result for n below 2^64."""
    odd_part = n - 1
    shifts = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shifts += 1

    for base in MR_BASES_64:
        if base >= n:
            continue
        value = pow(base, odd_part, n)
        if value == 1 or value == n - 1:
            continue
        passed = False
        for _ in range(shifts - 1):
            value = (value * value) % n
            if value == n - 1:
                passed = True
                break
        if not passed:
            return False
    return True


def v2(value: int) -> int:
    """Return the exponent of 2 in one positive even integer."""
    return (value & -value).bit_length() - 1


def accelerated_odd_transition(n: int) -> Transition:
    """Return one accelerated odd Collatz transition."""
    value = 3 * n + 1
    exponent = v2(value)
    return Transition(source=n, target=value >> exponent, v2=exponent)


def first_descent_block(seed: int) -> list[Transition]:
    """Return odd transitions through the first target below seed."""
    transitions: list[Transition] = []
    current = seed
    while True:
        transition = accelerated_odd_transition(current)
        transitions.append(transition)
        if transition.target < seed:
            return transitions
        current = transition.target


def odd_projected_witness_cells(
    left_prime: int,
    right_prime: int,
    witness: int,
) -> tuple[int, ...]:
    """Return odd interior cells nearest the PGS witness."""
    return tuple(
        value
        for value in (witness - 1, witness, witness + 1)
        if left_prime < value < right_prime and value % 2 == 1
    )


def odd_projected_witness_distance(
    n: int,
    left_prime: int,
    right_prime: int,
    witness: int,
) -> int:
    """Return distance from n to the odd cells nearest the PGS witness."""
    cells = odd_projected_witness_cells(left_prime, right_prime, witness)
    return min(abs(n - value) for value in cells)


def v2_bin(exponent: int) -> str:
    """Return the v2 stratum."""
    if exponent <= 2:
        return str(exponent)
    if exponent <= 4:
        return "3-4"
    return ">=5"


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
    """Return a zero-safe ratio of rates."""
    right = rate(right_numerator, right_denominator)
    if right == 0.0:
        return 0.0
    return rate(left_numerator, left_denominator) / right


def median(values: list[float] | list[int]) -> float:
    """Return the median value."""
    if not values:
        return 0.0
    ordered = sorted(values)
    count = len(ordered)
    midpoint = count // 2
    if count % 2 == 1:
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


def compact_counter(counter: Counter[str]) -> dict[str, int]:
    """Return a sorted JSON-ready counter."""
    return {key: counter[key] for key in sorted(counter)}


def classify_block(transitions: list[Transition], context: PrimeContext) -> str:
    """Classify one block by composite PGS witness contact."""
    for transition in transitions:
        state = context.source_state(transition.source)
        if not state.is_prime and state.odd_projected_witness_hit:
            return "witness_contact"
    return "no_witness_contact"


def add_same_gap_background(
    accumulator: SameGapAccumulator,
    state: SourceState,
    context: PrimeContext,
) -> None:
    """Add same-gap background for one composite source."""
    if state.is_prime:
        return
    accumulator.add(context.gap_profile(state.prev_prime, state.next_prime))


def first_pass_max_seen(limit: int) -> dict[str, object]:
    """Return first-pass range facts."""
    max_seen = 3
    max_steps = 0
    total_source_states = 0
    for seed in range(3, limit + 1, 2):
        transitions = first_descent_block(seed)
        max_seen = max(
            max_seen,
            max(transition.source for transition in transitions),
            transitions[-1].target,
        )
        max_steps = max(max_steps, len(transitions))
        total_source_states += len(transitions)
    return {
        "max_seen": max_seen,
        "max_steps": max_steps,
        "total_source_states": total_source_states,
    }


def run_probe(limit: int, output_dir: Path) -> dict[str, object]:
    """Run the same-gap Collatz-PGS scale probe."""
    if limit < 3:
        raise ValueError("limit must be at least 3")

    first_pass = first_pass_max_seen(limit)
    context = PrimeContext(int(first_pass["max_seen"]))
    source_profile = SourceAccumulator()
    same_gap_profile = SameGapAccumulator()
    source_by_v2 = {label: SourceAccumulator() for label in V2_BINS}
    same_gap_by_v2 = {label: SameGapAccumulator() for label in V2_BINS}
    block_profiles = {
        "witness_contact": BlockAccumulator(),
        "no_witness_contact": BlockAccumulator(),
    }
    block_class_counts: Counter[str] = Counter()
    v2_counts: Counter[str] = Counter()
    block_rows: list[dict[str, object]] = []

    max_source_over_seed = 0.0
    for seed in range(3, limit + 1, 2):
        transitions = first_descent_block(seed)
        block_class = classify_block(transitions, context)
        block_class_counts[block_class] += 1

        terminal = transitions[-1].target
        reset_strength = seed / terminal
        max_source = max(transition.source for transition in transitions)
        local_max_source_over_seed = max_source / seed
        max_source_over_seed = max(max_source_over_seed, local_max_source_over_seed)
        source_count = 0
        prime_count = 0
        composite_count = 0
        witness_hit_count = 0

        for transition in transitions:
            state = context.source_state(transition.source)
            bin_label = v2_bin(transition.v2)
            v2_counts[bin_label] += 1
            source_profile.add(state)
            source_by_v2[bin_label].add(state)
            add_same_gap_background(same_gap_profile, state, context)
            add_same_gap_background(same_gap_by_v2[bin_label], state, context)
            source_count += 1
            if state.is_prime:
                prime_count += 1
            else:
                composite_count += 1
                if state.odd_projected_witness_hit:
                    witness_hit_count += 1

        final_state = context.source_state(transitions[-1].source)
        final_source_witness_hit = (
            not final_state.is_prime and final_state.odd_projected_witness_hit
        )
        block_profiles[block_class].add(
            reset_strength,
            len(transitions),
            local_max_source_over_seed,
            final_source_witness_hit,
        )
        block_rows.append(
            {
                "seed": seed,
                "block_class": block_class,
                "terminal_below_seed": terminal,
                "reset_strength": reset_strength,
                "odd_steps_to_first_descent": len(transitions),
                "max_source": max_source,
                "max_source_over_seed": local_max_source_over_seed,
                "source_count": source_count,
                "source_prime_count": prime_count,
                "source_composite_count": composite_count,
                "source_witness_hit_count": witness_hit_count,
                "source_witness_hit_rate": rate(witness_hit_count, composite_count),
                "final_source": final_state.n,
                "final_v2": transitions[-1].v2,
                "final_is_prime": final_state.is_prime,
                "final_tau": final_state.tau,
                "final_prev_prime": final_state.prev_prime,
                "final_next_prime": final_state.next_prime,
                "final_witness": final_state.witness,
                "final_odd_projected_witness_hit": final_source_witness_hit,
            }
        )

    source_record = source_profile.record()
    same_gap_record = same_gap_profile.record()
    v2_rows: list[dict[str, object]] = []
    same_gap_witness_by_v2: dict[str, dict[str, object]] = {}
    for label in V2_BINS:
        source_bin = source_by_v2[label].record()
        same_gap_bin = same_gap_by_v2[label].record()
        ratio = rate_ratio(
            int(source_bin["witness_hit_count"]),
            int(source_bin["composite_count"]),
            int(same_gap_bin["witness_hit_count"]),
            int(same_gap_bin["composite_count"]),
        )
        row = {
            "v2_bin": label,
            "source_profile": source_bin,
            "same_gap_background_profile": same_gap_bin,
            "source_vs_same_gap_witness_hit_ratio": ratio,
        }
        v2_rows.append(row)
        same_gap_witness_by_v2[label] = row

    summary = {
        "limit": limit,
        "odd_seed_count": len(range(3, limit + 1, 2)),
        "max_seen_in_first_descent_blocks": int(first_pass["max_seen"]),
        "total_source_states": int(first_pass["total_source_states"]),
        "max_odd_steps_to_first_descent": int(first_pass["max_steps"]),
        "max_source_over_seed": max_source_over_seed,
        "source_profile": source_record,
        "same_gap_background_profile": same_gap_record,
        "source_vs_same_gap_witness_hit_ratio": rate_ratio(
            int(source_record["witness_hit_count"]),
            int(source_record["composite_count"]),
            int(same_gap_record["witness_hit_count"]),
            int(same_gap_record["composite_count"]),
        ),
        "same_gap_witness_by_v2": same_gap_witness_by_v2,
        "prime_endpoint_hit_rate": source_record["prime_rate"],
        "block_class_counts": compact_counter(block_class_counts),
        "block_profiles": {
            label: block_profiles[label].record()
            for label in ("witness_contact", "no_witness_contact")
        },
        "v2_histogram": compact_counter(v2_counts),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(block_rows, output_dir / "block_rows.jsonl")
    write_jsonl(v2_rows, output_dir / "v2_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scale same-gap PGS witness checks on Collatz first-descent blocks.",
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
