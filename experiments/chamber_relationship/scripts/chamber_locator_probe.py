"""Probe whether a modulus chamber localizes factor-predecessor chambers.

The audit labels are known semiprime factors. They are used only after the
modulus-chamber features have been recorded.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

from z_band_prime_rh_bridge.bridge import divisor_counts_up_to


ROOT = Path(__file__).resolve().parents[3]
BASE_OUTPUT_DIR = ROOT / "experiments" / "chamber_relationship" / "output" / "chamber_locator_probe"


@dataclass(frozen=True)
class Chamber:
    left: int
    right: int
    width: int
    selected: int | None
    selected_tau: int | None
    selected_phase: float | None


@dataclass(frozen=True)
class Row:
    row_id: int
    p: int
    q: int
    n: int
    p_index: int
    q_index: int
    n_left: int
    n_right: int
    n_width: int
    n_phase: float
    n_selected_phase: float
    n_selected_tau: int
    n_side: int
    p_selected_phase: float
    q_selected_phase: float
    p_width: int
    q_width: int
    p_target: int
    q_target: int


def primes_from_counts(counts: tuple[int, ...]) -> list[int]:
    """Return every index with exact divisor count two."""
    return [n for n, count in enumerate(counts) if count == 2]


def selected_chamber(left: int, right: int, counts: tuple[int, ...]) -> Chamber:
    """Return the leftmost minimum-divisor interior for one prime chamber."""
    width = right - left
    if width <= 1:
        return Chamber(left, right, width, None, None, None)

    selected = left + 1
    selected_tau = counts[selected]
    for value in range(left + 2, right):
        tau = counts[value]
        if tau < selected_tau:
            selected = value
            selected_tau = tau
    return Chamber(
        left=left,
        right=right,
        width=width,
        selected=selected,
        selected_tau=selected_tau,
        selected_phase=(selected - left) / width,
    )


def enclosing_chamber(value: int, counts: tuple[int, ...]) -> Chamber:
    """Return the prime chamber enclosing one composite value."""
    left = value - 1
    while left >= 2 and counts[left] != 2:
        left -= 1
    if left < 2:
        raise ValueError(f"no left endpoint for value {value}")

    right = value + 1
    while right < len(counts) and counts[right] != 2:
        right += 1
    if right >= len(counts):
        raise ValueError(f"no right endpoint for value {value}")

    return selected_chamber(left, right, counts)


def build_rows(
    p_min: int,
    p_max: int,
    q_min: int,
    q_max: int,
) -> list[Row]:
    """Build the deterministic semiprime chamber surface."""
    limit = (p_max * q_max) + 1000
    counts = divisor_counts_up_to(limit)
    primes = primes_from_counts(counts)
    prime_index = {prime: index for index, prime in enumerate(primes)}

    p_values = [prime for prime in primes if p_min <= prime <= p_max]
    q_values = [prime for prime in primes if q_min <= prime <= q_max]
    rows: list[Row] = []
    row_id = 0

    for p in p_values:
        p_previous = primes[prime_index[p] - 1]
        p_chamber = selected_chamber(p_previous, p, counts)
        if p_chamber.selected_phase is None:
            continue

        for q in q_values:
            q_previous = primes[prime_index[q] - 1]
            q_chamber = selected_chamber(q_previous, q, counts)
            if q_chamber.selected_phase is None:
                continue

            n = p * q
            n_chamber = enclosing_chamber(n, counts)
            if n_chamber.selected is None or n_chamber.selected_phase is None:
                continue

            n_phase = (n - n_chamber.left) / n_chamber.width
            n_side = -1 if n < n_chamber.selected else 1 if n > n_chamber.selected else 0
            rows.append(
                Row(
                    row_id=row_id,
                    p=p,
                    q=q,
                    n=n,
                    p_index=prime_index[p],
                    q_index=prime_index[q],
                    n_left=n_chamber.left,
                    n_right=n_chamber.right,
                    n_width=n_chamber.width,
                    n_phase=n_phase,
                    n_selected_phase=n_chamber.selected_phase,
                    n_selected_tau=int(n_chamber.selected_tau),
                    n_side=n_side,
                    p_selected_phase=float(p_chamber.selected_phase),
                    q_selected_phase=float(q_chamber.selected_phase),
                    p_width=p_chamber.width,
                    q_width=q_chamber.width,
                    p_target=prime_index[p],
                    q_target=prime_index[q],
                )
            )
            row_id += 1

    return rows


def quantile_edges(values: list[float], bin_count: int) -> list[float]:
    """Return deterministic rank edges for bucket construction."""
    sorted_values = sorted(values)
    edges = []
    for index in range(1, bin_count):
        rank = (len(sorted_values) * index) // bin_count
        edges.append(sorted_values[rank])
    return edges


def bucket(value: float, edges: list[float]) -> int:
    """Return the bucket index for one value."""
    for index, edge in enumerate(edges):
        if value < edge:
            return index
    return len(edges)


def median(values: list[float]) -> float:
    """Return the median of a nonempty list."""
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return 0.5 * (ordered[middle - 1] + ordered[middle])


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a nonempty list."""
    return sum(values) / len(values)


def circular_distance(a: float, b: float) -> float:
    """Return circular distance on the unit interval."""
    distance = abs(a - b)
    return min(distance, 1.0 - distance)


def echo_errors(rows: list[Row]) -> dict[str, float | int]:
    """Compare true phase errors against deterministic shifted labels."""
    true_p = []
    true_q = []
    shifted_p = []
    shifted_q = []
    count = len(rows)

    for index, row in enumerate(rows):
        shifted = rows[(index + 1) % count]
        phase_delta = (row.n_phase - row.n_selected_phase) % 1.0
        true_p.append(circular_distance(phase_delta, row.p_selected_phase))
        true_q.append(circular_distance(phase_delta, row.q_selected_phase))
        shifted_p.append(circular_distance(phase_delta, shifted.p_selected_phase))
        shifted_q.append(circular_distance(phase_delta, shifted.q_selected_phase))

    return {
        "rows": count,
        "true_p_median": median(true_p),
        "shifted_p_median": median(shifted_p),
        "p_median_gain": median(shifted_p) - median(true_p),
        "true_q_median": median(true_q),
        "shifted_q_median": median(shifted_q),
        "q_median_gain": median(shifted_q) - median(true_q),
    }


def distribution_summary(rows: list[Row]) -> dict[str, object]:
    """Return simple counts for selected modulus-chamber strata."""
    side_counts: dict[str, int] = {"before_floor": 0, "at_floor": 0, "after_floor": 0}
    tau_counts: dict[str, int] = {}
    width_counts: dict[str, int] = {}
    for row in rows:
        if row.n_side < 0:
            side_counts["before_floor"] += 1
        elif row.n_side > 0:
            side_counts["after_floor"] += 1
        else:
            side_counts["at_floor"] += 1
        tau_key = str(row.n_selected_tau)
        tau_counts[tau_key] = tau_counts.get(tau_key, 0) + 1
        width_key = str(row.n_width)
        width_counts[width_key] = width_counts.get(width_key, 0) + 1
    return {
        "n_side_counts": side_counts,
        "n_selected_tau_counts": dict(sorted(tau_counts.items(), key=lambda item: int(item[0]))),
        "n_width_counts": dict(sorted(width_counts.items(), key=lambda item: int(item[0]))),
    }


def model_keys(rows: list[Row]) -> tuple[list[float], list[float], list[float]]:
    """Build shared bucket edges from the full deterministic surface."""
    log_edges = quantile_edges([math.log(row.n) for row in rows], 4)
    phase_edges = quantile_edges([row.n_phase for row in rows], 4)
    selected_edges = quantile_edges([row.n_selected_phase for row in rows], 4)
    return log_edges, phase_edges, selected_edges


def locator_summary(rows: list[Row], target_name: str) -> dict[str, float | int]:
    """Compare scale-only and chamber-bucket localization on odd holdout rows."""
    log_edges, phase_edges, selected_edges = model_keys(rows)
    train = [row for row in rows if row.row_id % 2 == 0]
    test = [row for row in rows if row.row_id % 2 == 1]

    scale_buckets: dict[tuple[int], list[int]] = defaultdict(list)
    chamber_buckets: dict[tuple[int, int, int, int, int], list[int]] = defaultdict(list)

    for row in train:
        target = getattr(row, target_name)
        log_bucket = bucket(math.log(row.n), log_edges)
        phase_bucket = bucket(row.n_phase, phase_edges)
        selected_bucket = bucket(row.n_selected_phase, selected_edges)
        tau_bucket = min(row.n_selected_tau, 12)
        scale_buckets[(log_bucket,)].append(target)
        chamber_buckets[(log_bucket, phase_bucket, selected_bucket, row.n_side, tau_bucket)].append(target)

    scale_errors: list[float] = []
    chamber_errors: list[float] = []
    unresolved = 0
    for row in test:
        target = getattr(row, target_name)
        log_bucket = bucket(math.log(row.n), log_edges)
        phase_bucket = bucket(row.n_phase, phase_edges)
        selected_bucket = bucket(row.n_selected_phase, selected_edges)
        tau_bucket = min(row.n_selected_tau, 12)
        scale_key = (log_bucket,)
        chamber_key = (log_bucket, phase_bucket, selected_bucket, row.n_side, tau_bucket)
        if scale_key not in scale_buckets or chamber_key not in chamber_buckets:
            unresolved += 1
            continue
        scale_prediction = mean([float(value) for value in scale_buckets[scale_key]])
        chamber_prediction = mean([float(value) for value in chamber_buckets[chamber_key]])
        scale_errors.append(abs(target - scale_prediction))
        chamber_errors.append(abs(target - chamber_prediction))

    if not scale_errors:
        raise ValueError(f"no resolved locator rows for {target_name}")

    improvement = median(scale_errors) - median(chamber_errors)
    return {
        "target": target_name,
        "train_rows": len(train),
        "test_rows": len(test),
        "resolved_rows": len(scale_errors),
        "unresolved_rows": unresolved,
        "scale_median_abs_index_error": median(scale_errors),
        "chamber_median_abs_index_error": median(chamber_errors),
        "median_abs_index_error_gain": improvement,
        "scale_mean_abs_index_error": mean(scale_errors),
        "chamber_mean_abs_index_error": mean(chamber_errors),
        "mean_abs_index_error_gain": mean(scale_errors) - mean(chamber_errors),
    }


def side_split_summary(rows: list[Row], target_name: str) -> list[dict[str, float | int | str]]:
    """Run the locator by modulus position relative to the selected floor."""
    result = []
    for side_label, side in [("before_floor", -1), ("at_floor", 0), ("after_floor", 1)]:
        side_rows = [row for row in rows if row.n_side == side]
        if len(side_rows) < 20:
            continue
        summary = locator_summary(side_rows, target_name)
        summary["side"] = side_label
        result.append(summary)
    return result


def write_rows(rows: list[Row], path: Path) -> None:
    """Write row-level measurements."""
    fields = list(Row.__dataclass_fields__.keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in fields})


def write_echo_plot(rows: list[Row], path: Path) -> None:
    """Plot true versus shifted phase-echo errors."""
    phase_delta = [(row.n_phase - row.n_selected_phase) % 1.0 for row in rows]
    true_p = [circular_distance(delta, row.p_selected_phase) for delta, row in zip(phase_delta, rows)]
    shifted_p = [
        circular_distance(delta, rows[(index + 1) % len(rows)].p_selected_phase)
        for index, delta in enumerate(phase_delta)
    ]
    true_q = [circular_distance(delta, row.q_selected_phase) for delta, row in zip(phase_delta, rows)]
    shifted_q = [
        circular_distance(delta, rows[(index + 1) % len(rows)].q_selected_phase)
        for index, delta in enumerate(phase_delta)
    ]

    plt.figure(figsize=(8, 5))
    bins = [index / 40 for index in range(21)]
    plt.hist(true_p, bins=bins, alpha=0.55, label="true p chamber", density=True)
    plt.hist(shifted_p, bins=bins, alpha=0.55, label="shifted p control", density=True)
    plt.hist(true_q, bins=bins, alpha=0.35, label="true q chamber", density=True)
    plt.hist(shifted_q, bins=bins, alpha=0.35, label="shifted q control", density=True)
    plt.xlabel("phase-echo circular error")
    plt.ylabel("density")
    plt.title("Chamber phase echo error")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def write_locator_plot(summary: dict[str, object], path: Path) -> None:
    """Plot baseline and chamber locator errors."""
    p_summary = summary["locator"]["p_target"]
    q_summary = summary["locator"]["q_target"]
    labels = ["p scale", "p chamber", "q scale", "q chamber"]
    values = [
        p_summary["scale_median_abs_index_error"],
        p_summary["chamber_median_abs_index_error"],
        q_summary["scale_median_abs_index_error"],
        q_summary["chamber_median_abs_index_error"],
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=["#8da0cb", "#66c2a5", "#8da0cb", "#66c2a5"])
    plt.ylabel("median chamber-index error")
    plt.title("Scale-only versus chamber-feature locator")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def run(args: argparse.Namespace) -> dict[str, object]:
    """Run the full deterministic probe."""
    output_dir = BASE_OUTPUT_DIR / args.tag
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows(args.p_min, args.p_max, args.q_min, args.q_max)
    if not rows:
        raise ValueError("empty measurement surface")

    summary: dict[str, object] = {
        "surface": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "q_min": args.q_min,
            "q_max": args.q_max,
            "rows": len(rows),
        },
        "experiments": [
            "phase_echo_true_vs_shifted_control",
            "scale_only_vs_chamber_feature_locator",
            "selected_floor_side_split_locator",
        ],
        "falsification_rule": (
            "The tested chamber relationship is unsupported on this surface if "
            "phase-echo true/control medians are indistinguishable and chamber "
            "features do not reduce resolved holdout chamber-index error beyond "
            "the scale-only baseline."
        ),
        "distribution": distribution_summary(rows),
        "echo": echo_errors(rows),
        "locator": {
            "p_target": locator_summary(rows, "p_target"),
            "q_target": locator_summary(rows, "q_target"),
        },
        "side_split": {
            "p_target": side_split_summary(rows, "p_target"),
            "q_target": side_split_summary(rows, "q_target"),
        },
    }

    write_rows(rows, output_dir / "rows.csv")
    with (output_dir / "summary.json").open("w") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    write_echo_plot(rows, output_dir / "phase_echo_error.png")
    write_locator_plot(summary, output_dir / "locator_error.png")
    return summary


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Run the chamber relationship locator probe.",
    )
    parser.add_argument("--p-min", type=int, default=101)
    parser.add_argument("--p-max", type=int, default=401)
    parser.add_argument("--q-min", type=int, default=1009)
    parser.add_argument("--q-max", type=int, default=2003)
    parser.add_argument("--tag", default="small_surface")
    args = parser.parse_args()
    summary = run(args)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
