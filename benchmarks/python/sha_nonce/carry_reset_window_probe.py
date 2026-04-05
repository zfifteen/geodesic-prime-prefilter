#!/usr/bin/env python3
"""Probe whether SHA-256 nonce-window minima lean toward carry-reset boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(
    "benchmarks/output/python/sha_nonce/carry_reset_window_probe"
)
DEFAULT_WINDOW_SIZES = [64, 256, 1024]
DEFAULT_HEADER_COUNT = 4
DEFAULT_WINDOWS_PER_HEADER = 1024
DEFAULT_PREFIX_DENOMINATORS = [2, 4, 8, 16]
BIN_COUNT = 8
ALIGNMENTS = ("aligned", "half_shifted")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Measure whether minimum SHA-256 outputs inside power-of-two nonce "
            "windows cluster near the left carry-reset edge."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for JSON and SVG artifacts.",
    )
    parser.add_argument(
        "--window-sizes",
        type=int,
        nargs="+",
        default=list(DEFAULT_WINDOW_SIZES),
        help="Power-of-two window sizes to probe.",
    )
    parser.add_argument(
        "--headers",
        type=int,
        default=DEFAULT_HEADER_COUNT,
        help="Number of deterministic 76-byte header prefixes to scan.",
    )
    parser.add_argument(
        "--windows-per-header",
        type=int,
        default=DEFAULT_WINDOWS_PER_HEADER,
        help="Contiguous window count to scan for each header prefix.",
    )
    parser.add_argument(
        "--prefix-denominators",
        type=int,
        nargs="+",
        default=list(DEFAULT_PREFIX_DENOMINATORS),
        help="Prefix fractions reported as first 1/d of each window.",
    )
    return parser


def deterministic_header_prefix(index: int) -> bytes:
    """Return one deterministic 76-byte prefix for nonce-line probing."""
    seed = f"prime-gap-structure/sha-nonce-window/{index}".encode("utf-8")
    chunks: list[bytes] = []
    counter = 0
    total = 0
    while total < 76:
        chunk = hashlib.sha256(seed + counter.to_bytes(4, "little")).digest()
        chunks.append(chunk)
        total += len(chunk)
        counter += 1
    return b"".join(chunks)[:76]


def nonce_digest(prefix: bytes, nonce: int) -> bytes:
    """Return the SHA-256 digest for one 80-byte header candidate."""
    return hashlib.sha256(prefix + nonce.to_bytes(4, "little")).digest()


def collect_min_positions(
    window_size: int,
    header_count: int,
    windows_per_header: int,
    nonce_shift: int,
) -> tuple[list[int], list[dict[str, object]]]:
    """Return minimum positions for all windows and per-header summaries."""
    positions: list[int] = []
    header_rows: list[dict[str, object]] = []

    for header_index in range(header_count):
        prefix = deterministic_header_prefix(header_index)
        header_positions: list[int] = []
        base_nonce = header_index * 2 * window_size * windows_per_header + nonce_shift

        for window_index in range(windows_per_header):
            window_start = base_nonce + window_index * window_size
            best_position = 0
            best_digest = nonce_digest(prefix, window_start)

            for offset in range(1, window_size):
                digest = nonce_digest(prefix, window_start + offset)
                if digest < best_digest:
                    best_digest = digest
                    best_position = offset

            positions.append(best_position)
            header_positions.append(best_position)

        header_rows.append(
            {
                "header_index": header_index,
                "window_count": len(header_positions),
                "mean_position": statistics.fmean(header_positions),
                "normalized_mean_position": (
                    statistics.fmean(header_positions) / (window_size - 1)
                    if window_size > 1
                    else 0.0
                ),
                "left_half_share": sum(
                    position < (window_size // 2) for position in header_positions
                )
                / len(header_positions),
                "first_eighth_share": sum(
                    position < max(1, window_size // 8) for position in header_positions
                )
                / len(header_positions),
            }
        )

    return positions, header_rows


def prefix_summary(
    positions: list[int],
    window_size: int,
    prefix_denominators: list[int],
) -> list[dict[str, float | int]]:
    """Return prefix-capture summaries for configured prefix sizes."""
    rows: list[dict[str, float | int]] = []
    total = len(positions)
    for denominator in prefix_denominators:
        prefix_length = max(1, window_size // denominator)
        observed_count = sum(position < prefix_length for position in positions)
        observed_share = observed_count / total if total else 0.0
        expected_share = prefix_length / window_size
        variance = expected_share * (1.0 - expected_share) / total if total else 0.0
        z_score = (
            (observed_share - expected_share) / math.sqrt(variance)
            if variance > 0.0
            else 0.0
        )
        rows.append(
            {
                "denominator": denominator,
                "prefix_length": prefix_length,
                "observed_count": observed_count,
                "observed_share": observed_share,
                "expected_share": expected_share,
                "z_score": z_score,
            }
        )
    return rows


def position_bins(positions: list[int], window_size: int) -> list[dict[str, float | int]]:
    """Return fixed-width normalized position bins."""
    counts = [0] * BIN_COUNT
    for position in positions:
        bucket = min(BIN_COUNT - 1, position * BIN_COUNT // window_size)
        counts[bucket] += 1

    total = len(positions)
    rows: list[dict[str, float | int]] = []
    for index, count in enumerate(counts):
        rows.append(
            {
                "bin_index": index,
                "start": index / BIN_COUNT,
                "end": (index + 1) / BIN_COUNT,
                "count": count,
                "share": (count / total) if total else 0.0,
            }
        )
    return rows


def summarize_window_size(
    window_size: int,
    header_count: int,
    windows_per_header: int,
    prefix_denominators: list[int],
) -> dict[str, object]:
    """Run one window-size probe and return JSON-ready results."""
    alignment_rows = []
    first_eighth_counts: dict[str, int] = {}
    for label in ALIGNMENTS:
        shift = 0 if label == "aligned" else window_size // 2
        positions, header_rows = collect_min_positions(
            window_size=window_size,
            header_count=header_count,
            windows_per_header=windows_per_header,
            nonce_shift=shift,
        )
        mean_position = statistics.fmean(positions)
        median_position = statistics.median(positions)
        left_half_share = sum(
            position < (window_size // 2) for position in positions
        ) / len(positions)
        prefix_summaries = prefix_summary(positions, window_size, prefix_denominators)
        alignment_rows.append(
            {
                "label": label,
                "nonce_shift": shift,
                "total_windows": len(positions),
                "mean_position": mean_position,
                "median_position": median_position,
                "normalized_mean_position": mean_position / (window_size - 1),
                "left_half_share": left_half_share,
                "left_half_expected_share": 0.5,
                "prefix_summaries": prefix_summaries,
                "position_bins": position_bins(positions, window_size),
                "header_rows": header_rows,
            }
        )
        first_eighth_counts[label] = next(
            row["observed_count"] for row in prefix_summaries if row["denominator"] == 8
        )

    total_windows = alignment_rows[0]["total_windows"]
    aligned_share = first_eighth_counts["aligned"] / total_windows
    shifted_share = first_eighth_counts["half_shifted"] / total_windows
    pooled = (
        first_eighth_counts["aligned"] + first_eighth_counts["half_shifted"]
    ) / (2 * total_windows)
    difference_variance = pooled * (1.0 - pooled) * (2.0 / total_windows)
    difference_z = (
        (aligned_share - shifted_share) / math.sqrt(difference_variance)
        if difference_variance > 0.0
        else 0.0
    )
    return {
        "window_size": window_size,
        "header_count": header_count,
        "windows_per_header": windows_per_header,
        "alignments": alignment_rows,
        "first_eighth_difference": {
            "aligned_share": aligned_share,
            "half_shifted_share": shifted_share,
            "delta": aligned_share - shifted_share,
            "z_score": difference_z,
        },
    }


def render_prefix_bias_svg(rows: list[dict[str, object]], output_path: Path) -> None:
    """Render one simple SVG comparing first-eighth share across alignments."""
    width = 900
    height = 420
    margin_left = 80
    margin_right = 40
    margin_top = 50
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    expected_share = 0.125
    max_share = max(
        [expected_share]
        + [
            next(
                row
                for row in next(
                    alignment
                    for alignment in item["alignments"]
                    if alignment["label"] == "aligned"
                )["prefix_summaries"]
                if row["denominator"] == 8
            )["observed_share"]
            for item in rows
        ]
        + [
            next(
                row
                for row in next(
                    alignment
                    for alignment in item["alignments"]
                    if alignment["label"] == "half_shifted"
                )["prefix_summaries"]
                if row["denominator"] == 8
            )["observed_share"]
            for item in rows
        ]
    )
    y_max = max(0.2, max_share * 1.15)

    def x_at(index: int) -> float:
        if len(rows) == 1:
            return margin_left + plot_width / 2
        return margin_left + index * (plot_width / (len(rows) - 1))

    def y_at(share: float) -> float:
        return margin_top + plot_height * (1.0 - share / y_max)

    aligned_polyline = " ".join(
        f"{x_at(index):.1f},{y_at(next(row for row in next(alignment for alignment in item['alignments'] if alignment['label'] == 'aligned')['prefix_summaries'] if row['denominator'] == 8)['observed_share']):.1f}"
        for index, item in enumerate(rows)
    )
    shifted_polyline = " ".join(
        f"{x_at(index):.1f},{y_at(next(row for row in next(alignment for alignment in item['alignments'] if alignment['label'] == 'half_shifted')['prefix_summaries'] if row['denominator'] == 8)['observed_share']):.1f}"
        for index, item in enumerate(rows)
    )

    x_labels = "\n".join(
        f'<text x="{x_at(index):.1f}" y="{height - 30}" text-anchor="middle" '
        f'font-size="12" fill="#1f2937">{item["window_size"]}</text>'
        for index, item in enumerate(rows)
    )
    y_labels = "\n".join(
        f'<text x="{margin_left - 12}" y="{y_at(tick):.1f}" text-anchor="end" '
        f'dominant-baseline="middle" font-size="12" fill="#1f2937">{tick:.3f}</text>'
        for tick in (0.0, y_max / 4, y_max / 2, 3 * y_max / 4, y_max)
    )
    aligned_points = "\n".join(
        f'<circle cx="{x_at(index):.1f}" cy="{y_at(next(row for row in next(alignment for alignment in item["alignments"] if alignment["label"] == "aligned")["prefix_summaries"] if row["denominator"] == 8)["observed_share"]):.1f}" '
        f'r="4" fill="#2563eb" />'
        for index, item in enumerate(rows)
    )
    shifted_points = "\n".join(
        f'<circle cx="{x_at(index):.1f}" cy="{y_at(next(row for row in next(alignment for alignment in item["alignments"] if alignment["label"] == "half_shifted")["prefix_summaries"] if row["denominator"] == 8)["observed_share"]):.1f}" '
        f'r="4" fill="#059669" />'
        for index, item in enumerate(rows)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="{width}" height="{height}" fill="white" />
<text x="{width / 2:.1f}" y="28" text-anchor="middle" font-size="18" fill="#111827">First-eighth capture share by window alignment</text>
<line x1="{margin_left}" y1="{y_at(expected_share):.1f}" x2="{width - margin_right}" y2="{y_at(expected_share):.1f}" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 6" />
<text x="{width - margin_right}" y="{y_at(expected_share) - 8:.1f}" text-anchor="end" font-size="12" fill="#dc2626">uniform expectation = 0.125</text>
<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#111827" stroke-width="1.5" />
<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#111827" stroke-width="1.5" />
<polyline fill="none" stroke="#2563eb" stroke-width="3" points="{aligned_polyline}" />
<polyline fill="none" stroke="#059669" stroke-width="3" points="{shifted_polyline}" />
{aligned_points}
{shifted_points}
{x_labels}
{y_labels}
<rect x="{margin_left + 20}" y="{margin_top + 10}" width="14" height="14" fill="#2563eb" />
<text x="{margin_left + 42}" y="{margin_top + 21}" font-size="12" fill="#1f2937">aligned windows</text>
<rect x="{margin_left + 170}" y="{margin_top + 10}" width="14" height="14" fill="#059669" />
<text x="{margin_left + 192}" y="{margin_top + 21}" font-size="12" fill="#1f2937">half-shifted windows</text>
<text x="{width / 2:.1f}" y="{height - 8}" text-anchor="middle" font-size="12" fill="#1f2937">window size</text>
<text x="20" y="{height / 2:.1f}" text-anchor="middle" font-size="12" fill="#1f2937" transform="rotate(-90 20 {height / 2:.1f})">share of windows whose minimum lands in first 1/8</text>
</svg>
"""
    output_path.write_text(svg + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the carry-reset window probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        summarize_window_size(
            window_size=window_size,
            header_count=args.headers,
            windows_per_header=args.windows_per_header,
            prefix_denominators=args.prefix_denominators,
        )
        for window_size in args.window_sizes
    ]

    payload = {
        "headers": args.headers,
        "windows_per_header": args.windows_per_header,
        "window_sizes": args.window_sizes,
        "rows": rows,
    }

    json_path = args.output_dir / "carry_reset_window_probe.json"
    svg_path = args.output_dir / "carry_reset_window_probe_first_eighth_share.svg"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    render_prefix_bias_svg(rows, svg_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
