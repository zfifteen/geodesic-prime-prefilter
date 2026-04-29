"""Gather gap divisor count statistics for prime gaps."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from sympy import nextprime, prevprime, primerange


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402


DEFAULT_OUTPUT_DIR = ROOT / "output" / "gap_divisor_count_probe"


def gap_divisor_count(p: int, q: int) -> int:
    """Return total divisor load across the composite interior of one gap."""
    p = int(p)
    q = int(q)
    if q <= p:
        raise ValueError("q must be larger than p")
    return int(sum(int(value) for value in divisor_counts_segment(p + 1, q)))


def low_surface_anchors(limit: int) -> list[int]:
    """Return every prime anchor from 11 through one inclusive limit."""
    return [int(prime) for prime in primerange(11, int(limit) + 1)]


def sampled_anchors_near(scale: int, count: int) -> list[int]:
    """Return deterministic prime anchors immediately below one scale."""
    anchors: list[int] = []
    cursor = int(scale)
    while len(anchors) < int(count):
        anchor = int(prevprime(cursor))
        anchors.append(anchor)
        cursor = anchor
    return anchors


def row_from_pair(
    surface: str,
    scale_exponent: int | None,
    p: int,
    q: int,
    interior_divisor_count: int | None = None,
) -> dict[str, int | str | None]:
    """Return one gap divisor count row from one prime pair."""
    gap = int(q) - int(p)
    return {
        "surface": surface,
        "scale_exponent": scale_exponent,
        "p": int(p),
        "q": int(q),
        "gap": gap,
        "interior_composite_count": gap - 1,
        "gap_divisor_count": (
            gap_divisor_count(p, q)
            if interior_divisor_count is None
            else int(interior_divisor_count)
        ),
    }


def rows_for_anchors(
    surface: str,
    scale_exponent: int | None,
    anchors: list[int],
) -> list[dict[str, int | str | None]]:
    """Return metric rows for deterministic downstream prime-gap truth."""
    pairs = [(int(anchor), int(nextprime(anchor))) for anchor in anchors]
    if not pairs:
        return []

    lo = min(p + 1 for p, _q in pairs)
    hi = max(q for _p, q in pairs)
    counts = [int(value) for value in divisor_counts_segment(lo, hi)]
    rows: list[dict[str, int | str | None]] = []
    for p, q in pairs:
        start = p + 1 - lo
        stop = q - lo
        rows.append(row_from_pair(surface, scale_exponent, p, q, sum(counts[start:stop])))
    return rows


def build_rows(
    low_limit: int,
    min_exponent: int,
    max_exponent: int,
    high_sample_size: int,
) -> list[dict[str, int | str | None]]:
    """Return low-surface and decade-window gap divisor rows."""
    rows = rows_for_anchors("low_full", None, low_surface_anchors(low_limit))
    for exponent in range(int(min_exponent), int(max_exponent) + 1):
        rows.extend(
            rows_for_anchors(
                "decade_window",
                exponent,
                sampled_anchors_near(10**exponent, high_sample_size),
            )
        )
    return rows


def _share(count: int, total: int) -> float:
    return 0.0 if total == 0 else int(count) / int(total)


def gap_frequency_rows(
    rows: list[dict[str, int | str | None]],
) -> list[dict[str, int | float]]:
    """Return global gap-size frequencies."""
    total = len(rows)
    grouped: dict[int, list[int]] = defaultdict(list)
    for row in rows:
        grouped[int(row["gap"])].append(int(row["gap_divisor_count"]))
    return [
        {
            "gap": gap,
            "count": len(values),
            "share": _share(len(values), total),
            "min_gap_divisor_count": min(values),
            "mean_gap_divisor_count": mean(values),
            "max_gap_divisor_count": max(values),
        }
        for gap, values in sorted(grouped.items())
    ]


def divisor_count_frequency_rows(
    rows: list[dict[str, int | str | None]],
) -> list[dict[str, int | float]]:
    """Return global frequencies grouped by gap divisor count."""
    total = len(rows)
    gaps_by_count: dict[int, list[int]] = defaultdict(list)
    for row in rows:
        gaps_by_count[int(row["gap_divisor_count"])].append(int(row["gap"]))
    return [
        {
            "gap_divisor_count": count,
            "count": len(gaps),
            "share": _share(len(gaps), total),
            "min_gap": min(gaps),
            "max_gap": max(gaps),
            "mean_gap": mean(gaps),
        }
        for count, gaps in sorted(gaps_by_count.items())
    ]


def metric_summary(
    rows: list[dict[str, int | str | None]],
) -> dict[str, int | float | list[dict[str, int | float]] | None]:
    """Return aggregate statistics for one row group."""
    if not rows:
        return {
            "total_gap_records": 0,
            "distinct_gap_sizes": 0,
            "distinct_gap_divisor_counts": 0,
            "min_gap": None,
            "mean_gap": None,
            "max_gap": None,
            "min_gap_divisor_count": None,
            "mean_gap_divisor_count": None,
            "max_gap_divisor_count": None,
            "top_gap_sizes_by_count": [],
            "top_gap_divisor_counts_by_count": [],
            "largest_observed_gap": None,
            "largest_observed_gap_divisor_count": None,
            "largest_gap_divisor_count": None,
            "gaps_with_largest_gap_divisor_count": [],
        }

    gaps = [int(row["gap"]) for row in rows]
    divisor_counts = [int(row["gap_divisor_count"]) for row in rows]
    gap_counts = Counter(gaps)
    divisor_count_counts = Counter(divisor_counts)
    largest_gap = max(gaps)
    largest_divisor_count = max(divisor_counts)
    return {
        "total_gap_records": len(rows),
        "distinct_gap_sizes": len(gap_counts),
        "distinct_gap_divisor_counts": len(divisor_count_counts),
        "min_gap": min(gaps),
        "mean_gap": mean(gaps),
        "max_gap": largest_gap,
        "min_gap_divisor_count": min(divisor_counts),
        "mean_gap_divisor_count": mean(divisor_counts),
        "max_gap_divisor_count": largest_divisor_count,
        "top_gap_sizes_by_count": [
            {"gap": gap, "count": count, "share": _share(count, len(rows))}
            for gap, count in gap_counts.most_common(10)
        ],
        "top_gap_divisor_counts_by_count": [
            {
                "gap_divisor_count": count_value,
                "count": count,
                "share": _share(count, len(rows)),
            }
            for count_value, count in divisor_count_counts.most_common(10)
        ],
        "largest_observed_gap": largest_gap,
        "largest_observed_gap_divisor_count": max(
            int(row["gap_divisor_count"]) for row in rows if int(row["gap"]) == largest_gap
        ),
        "largest_gap_divisor_count": largest_divisor_count,
        "gaps_with_largest_gap_divisor_count": sorted(
            {gap for gap, count in zip(gaps, divisor_counts) if count == largest_divisor_count}
        ),
    }


def scale_summary_rows(
    rows: list[dict[str, int | str | None]],
) -> list[dict[str, int | float | str | None]]:
    """Return per-surface and per-scale aggregate rows."""
    grouped: dict[tuple[str, int | None], list[dict[str, int | str | None]]] = (
        defaultdict(list)
    )
    for row in rows:
        grouped[(str(row["surface"]), row["scale_exponent"])].append(row)

    summaries: list[dict[str, int | float | str | None]] = []
    def sort_key(key: tuple[str, int | None]) -> tuple[str, int]:
        surface, scale_exponent = key
        return surface, -1 if scale_exponent is None else int(scale_exponent)

    for surface, scale_exponent in sorted(grouped, key=sort_key):
        summary = metric_summary(grouped[(surface, scale_exponent)])
        summaries.append(
            {
                "surface": surface,
                "scale_exponent": scale_exponent,
                "total_gap_records": summary["total_gap_records"],
                "distinct_gap_sizes": summary["distinct_gap_sizes"],
                "distinct_gap_divisor_counts": summary[
                    "distinct_gap_divisor_counts"
                ],
                "min_gap": summary["min_gap"],
                "mean_gap": summary["mean_gap"],
                "max_gap": summary["max_gap"],
                "min_gap_divisor_count": summary["min_gap_divisor_count"],
                "mean_gap_divisor_count": summary["mean_gap_divisor_count"],
                "max_gap_divisor_count": summary["max_gap_divisor_count"],
                "largest_observed_gap": summary["largest_observed_gap"],
                "largest_observed_gap_divisor_count": summary[
                    "largest_observed_gap_divisor_count"
                ],
                "largest_gap_divisor_count": summary["largest_gap_divisor_count"],
            }
        )
    return summaries


def summary_payload(
    rows: list[dict[str, int | str | None]],
) -> dict[str, object]:
    """Return the headline summary payload."""
    by_surface: dict[str, list[dict[str, int | str | None]]] = defaultdict(list)
    for row in rows:
        by_surface[str(row["surface"])].append(row)
    return {
        "metric": "gap_divisor_count",
        "definition": "sum(d(n) for n in range(p + 1, q)), the total divisor load across the composite interior of the prime gap",
        "total_rows": len(rows),
        "global": metric_summary(rows),
        "by_surface": {
            surface: metric_summary(surface_rows)
            for surface, surface_rows in sorted(by_surface.items())
        },
        "scale_summary": scale_summary_rows(rows),
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON artifact."""
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(
    output_dir: Path,
    rows: list[dict[str, int | str | None]],
) -> None:
    """Write all gap divisor count artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "rows.jsonl", rows)
    write_csv(
        output_dir / "gap_frequency.csv",
        gap_frequency_rows(rows),
        [
            "gap",
            "count",
            "share",
            "min_gap_divisor_count",
            "mean_gap_divisor_count",
            "max_gap_divisor_count",
        ],
    )
    write_csv(
        output_dir / "divisor_count_frequency.csv",
        divisor_count_frequency_rows(rows),
        ["gap_divisor_count", "count", "share", "min_gap", "max_gap", "mean_gap"],
    )
    write_csv(
        output_dir / "scale_summary.csv",
        scale_summary_rows(rows),
        [
            "surface",
            "scale_exponent",
            "total_gap_records",
            "distinct_gap_sizes",
            "distinct_gap_divisor_counts",
            "min_gap",
            "mean_gap",
            "max_gap",
            "min_gap_divisor_count",
            "mean_gap_divisor_count",
            "max_gap_divisor_count",
            "largest_observed_gap",
            "largest_observed_gap_divisor_count",
            "largest_gap_divisor_count",
        ],
    )
    write_json(output_dir / "summary.json", summary_payload(rows))


def build_parser() -> argparse.ArgumentParser:
    """Build the gap divisor count probe CLI."""
    parser = argparse.ArgumentParser(description="Probe prime-gap divisor counts.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--low-limit", type=int, default=1_000_000)
    parser.add_argument("--min-exponent", type=int, default=8)
    parser.add_argument("--max-exponent", type=int, default=18)
    parser.add_argument("--high-sample-size", type=int, default=256)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the gap divisor count probe and write artifacts."""
    args = build_parser().parse_args(argv)
    rows = build_rows(
        args.low_limit,
        args.min_exponent,
        args.max_exponent,
        args.high_sample_size,
    )
    write_artifacts(args.output_dir, rows)
    print(json.dumps(summary_payload(rows)["global"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
