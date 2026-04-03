#!/usr/bin/env python3
"""Deterministic verifier for structural amplification in RSA prime generation."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[3]
MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import rsa_keygen_benchmark as rsa_benchmark


DEFAULT_OUTPUT_DIR = (
    ROOT / "benchmarks" / "output" / "python" / "prefilter" / "structural_amplification"
)
DEFAULT_NAMESPACE = "cdl-structural-amplification"
DEFAULT_REPETITIONS = 3
DEFAULT_EVALUATION_MIN_RSA_BITS = 2048
DEFAULT_REJECTION_STABILITY_TOLERANCE = 0.02
DEFAULT_SCHEDULE: tuple[tuple[int, int], ...] = (
    (1024, 24),
    (2048, 12),
    (3072, 8),
    (4096, 6),
    (8192, 2),
)

SVG_WIDTH = 1280
SVG_HEIGHT = 760
SVG_MARGIN_LEFT = 96
SVG_MARGIN_RIGHT = 92
SVG_MARGIN_TOP = 96
SVG_MARGIN_BOTTOM = 96

REALIZED_COLOR = "#0b6e4f"
CEILING_COLOR = "#c84c09"
REJECTION_COLOR = "#2b59c3"
BASELINE_COLOR = "#8b1e3f"
PROXY_COLOR = "#0b6e4f"
SURVIVOR_MR_COLOR = "#c84c09"


def parse_schedule_tokens(tokens: Sequence[str]) -> list[tuple[int, int]]:
    """Parse schedule tokens of the form rsa_bits:keypair_count."""
    schedule: list[tuple[int, int]] = []
    for token in tokens:
        rsa_bits_text, separator, keypair_count_text = token.partition(":")
        if separator != ":":
            raise ValueError(
                f"invalid schedule token {token!r}; expected rsa_bits:keypair_count"
            )
        rsa_bits = int(rsa_bits_text)
        keypair_count = int(keypair_count_text)
        if rsa_bits < 4 or rsa_bits % 2 != 0:
            raise ValueError("rsa_bits must be an even integer greater than or equal to 4")
        if keypair_count < 1:
            raise ValueError("keypair_count must be at least 1")
        schedule.append((rsa_bits, keypair_count))
    if len(schedule) < 2:
        raise ValueError("schedule must contain at least two cells")
    if any(schedule[index + 1][0] <= schedule[index][0] for index in range(len(schedule) - 1)):
        raise ValueError("schedule rsa_bits must increase strictly")
    return schedule


def summarize_series(values: Sequence[float]) -> Dict[str, float]:
    """Return median, min, max, and half-range for a numeric series."""
    median_value = statistics.median(values)
    min_value = min(values)
    max_value = max(values)
    return {
        "median": median_value,
        "min": min_value,
        "max": max_value,
        "half_range": (max_value - min_value) / 2.0,
    }


def require_constant_repeat_structure(
    repeat_results: Sequence[Dict[str, object]],
) -> None:
    """Require deterministic counts and keypair identity across timing repeats."""
    first = repeat_results[0]
    first_baseline = first["baseline"]
    first_accelerated = first["accelerated"]
    constant_fields = (
        ("matching_keypairs", first["matching_keypairs"]),
        ("saved_miller_rabin_calls", first["saved_miller_rabin_calls"]),
        ("prime_fixed_points.fixed_point_count", first["prime_fixed_points"]["fixed_point_count"]),
        ("baseline.total_candidates_tested", first_baseline["total_candidates_tested"]),
        ("baseline.total_miller_rabin_calls", first_baseline["total_miller_rabin_calls"]),
        ("accelerated.total_candidates_tested", first_accelerated["total_candidates_tested"]),
        ("accelerated.total_miller_rabin_calls", first_accelerated["total_miller_rabin_calls"]),
        ("accelerated.total_proxy_rejections", first_accelerated["total_proxy_rejections"]),
    )

    for repeat_index, result in enumerate(repeat_results[1:], start=1):
        baseline = result["baseline"]
        accelerated = result["accelerated"]
        current_fields = {
            "matching_keypairs": result["matching_keypairs"],
            "saved_miller_rabin_calls": result["saved_miller_rabin_calls"],
            "prime_fixed_points.fixed_point_count": result["prime_fixed_points"]["fixed_point_count"],
            "baseline.total_candidates_tested": baseline["total_candidates_tested"],
            "baseline.total_miller_rabin_calls": baseline["total_miller_rabin_calls"],
            "accelerated.total_candidates_tested": accelerated["total_candidates_tested"],
            "accelerated.total_miller_rabin_calls": accelerated["total_miller_rabin_calls"],
            "accelerated.total_proxy_rejections": accelerated["total_proxy_rejections"],
        }
        for field_name, expected_value in constant_fields:
            if current_fields[field_name] != expected_value:
                raise ValueError(
                    f"repeat {repeat_index} changed deterministic field {field_name}: "
                    f"{current_fields[field_name]!r} != {expected_value!r}"
                )


def run_cell_repetitions(
    rsa_bits: int,
    keypair_count: int,
    repetitions: int,
    public_exponent: int,
    namespace: str,
) -> Dict[str, object]:
    """Run one deterministic RSA cell several times and summarize timing jitter."""
    repeat_results: list[Dict[str, object]] = []
    cell_namespace = f"{namespace}:{rsa_bits}"

    for _ in range(repetitions):
        repeat_results.append(
            rsa_benchmark.run_rsa_keygen_benchmark(
                rsa_bits=rsa_bits,
                keypair_count=keypair_count,
                public_exponent=public_exponent,
                mr_bases=rsa_benchmark.benchmark.DEFAULT_MR_BASES,
                namespace=cell_namespace,
            )
        )

    require_constant_repeat_structure(repeat_results)
    first = repeat_results[0]
    baseline_first = first["baseline"]
    accelerated_first = first["accelerated"]

    speedup_stats = summarize_series([float(result["speedup"]) for result in repeat_results])
    baseline_time_stats = summarize_series(
        [float(result["baseline"]["mean_time_per_keypair_ms"]) for result in repeat_results]
    )
    accelerated_time_stats = summarize_series(
        [float(result["accelerated"]["mean_time_per_keypair_ms"]) for result in repeat_results]
    )
    baseline_mr_stats = summarize_series(
        [float(result["baseline"]["mean_miller_rabin_time_per_keypair_ms"]) for result in repeat_results]
    )
    proxy_time_stats = summarize_series(
        [float(result["accelerated"]["mean_proxy_time_per_keypair_ms"]) for result in repeat_results]
    )
    survivor_mr_stats = summarize_series(
        [float(result["accelerated"]["mean_miller_rabin_time_per_keypair_ms"]) for result in repeat_results]
    )

    rejection_rate = float(accelerated_first["proxy_rejection_rate"])
    structural_speedup_ceiling = math.inf
    if rejection_rate < 1.0:
        structural_speedup_ceiling = 1.0 / (1.0 - rejection_rate)

    return {
        "rsa_bits": rsa_bits,
        "keypair_count": keypair_count,
        "repeat_count": repetitions,
        "matching_keypairs": int(first["matching_keypairs"]),
        "saved_miller_rabin_calls": int(first["saved_miller_rabin_calls"]),
        "saved_miller_rabin_call_rate": float(first["saved_miller_rabin_call_rate"]),
        "prime_fixed_points": first["prime_fixed_points"],
        "baseline_total_candidates_tested": int(baseline_first["total_candidates_tested"]),
        "accelerated_total_candidates_tested": int(accelerated_first["total_candidates_tested"]),
        "baseline_total_miller_rabin_calls": int(baseline_first["total_miller_rabin_calls"]),
        "accelerated_total_miller_rabin_calls": int(accelerated_first["total_miller_rabin_calls"]),
        "accelerated_total_proxy_rejections": int(accelerated_first["total_proxy_rejections"]),
        "proxy_rejection_rate": rejection_rate,
        "speedup": speedup_stats,
        "baseline_mean_time_per_keypair_ms": baseline_time_stats,
        "accelerated_mean_time_per_keypair_ms": accelerated_time_stats,
        "baseline_mean_miller_rabin_time_per_keypair_ms": baseline_mr_stats,
        "accelerated_mean_proxy_time_per_keypair_ms": proxy_time_stats,
        "accelerated_mean_miller_rabin_time_per_keypair_ms": survivor_mr_stats,
        "baseline_to_proxy_cost_ratio": (
            baseline_time_stats["median"] / proxy_time_stats["median"]
            if proxy_time_stats["median"]
            else math.inf
        ),
        "baseline_miller_rabin_to_proxy_cost_ratio": (
            baseline_mr_stats["median"] / proxy_time_stats["median"]
            if proxy_time_stats["median"]
            else math.inf
        ),
        "structural_speedup_ceiling": structural_speedup_ceiling,
        "realized_ceiling_fraction": (
            speedup_stats["median"] / structural_speedup_ceiling
            if math.isfinite(structural_speedup_ceiling) and structural_speedup_ceiling > 0.0
            else 0.0
        ),
        "repeat_measurements": [
            {
                "speedup": float(result["speedup"]),
                "baseline_mean_time_per_keypair_ms": float(
                    result["baseline"]["mean_time_per_keypair_ms"]
                ),
                "accelerated_mean_time_per_keypair_ms": float(
                    result["accelerated"]["mean_time_per_keypair_ms"]
                ),
                "baseline_mean_miller_rabin_time_per_keypair_ms": float(
                    result["baseline"]["mean_miller_rabin_time_per_keypair_ms"]
                ),
                "accelerated_mean_proxy_time_per_keypair_ms": float(
                    result["accelerated"]["mean_proxy_time_per_keypair_ms"]
                ),
                "accelerated_mean_miller_rabin_time_per_keypair_ms": float(
                    result["accelerated"]["mean_miller_rabin_time_per_keypair_ms"]
                ),
            }
            for result in repeat_results
        ],
    }


def analyze_hypothesis(
    rows: Sequence[Dict[str, object]],
    evaluation_min_rsa_bits: int,
    rejection_stability_tolerance: float,
) -> Dict[str, object]:
    """Apply the predeclared amplification decision rule."""
    evaluation_rows = [row for row in rows if int(row["rsa_bits"]) >= evaluation_min_rsa_bits]
    if len(evaluation_rows) < 2:
        return {
            "evaluation_min_rsa_bits": evaluation_min_rsa_bits,
            "rejection_stability_tolerance": rejection_stability_tolerance,
            "evaluated_rsa_bits": [int(row["rsa_bits"]) for row in evaluation_rows],
            "verdict": "incomplete",
            "reason": "need at least two evaluation cells at or above evaluation_min_rsa_bits",
        }

    rejection_rates = [float(row["proxy_rejection_rate"]) for row in evaluation_rows]
    baseline_costs = [
        float(row["baseline_mean_time_per_keypair_ms"]["median"]) for row in evaluation_rows
    ]
    proxy_costs = [
        float(row["accelerated_mean_proxy_time_per_keypair_ms"]["median"])
        for row in evaluation_rows
    ]
    speedups = [float(row["speedup"]["median"]) for row in evaluation_rows]

    rejection_band_width = max(rejection_rates) - min(rejection_rates)
    rejection_stable = rejection_band_width <= rejection_stability_tolerance
    baseline_cost_rises = all(
        baseline_costs[index + 1] > baseline_costs[index]
        for index in range(len(baseline_costs) - 1)
    )
    proxy_growth_slower_than_baseline = (
        baseline_costs[-1] / baseline_costs[0] > proxy_costs[-1] / proxy_costs[0]
        if baseline_costs[0] > 0.0 and proxy_costs[0] > 0.0
        else False
    )
    speedup_rises = all(
        speedups[index + 1] > speedups[index] for index in range(len(speedups) - 1)
    )
    final_step_delta = speedups[-1] - speedups[-2]
    final_step_noise = float(evaluation_rows[-1]["speedup"]["half_range"]) + float(
        evaluation_rows[-2]["speedup"]["half_range"]
    )
    final_step_exceeds_noise = final_step_delta > final_step_noise

    verdict = "verified"
    failed_checks: list[str] = []
    checks = {
        "rejection_stable": rejection_stable,
        "baseline_cost_rises": baseline_cost_rises,
        "proxy_growth_slower_than_baseline": proxy_growth_slower_than_baseline,
        "speedup_rises": speedup_rises,
        "final_step_exceeds_noise": final_step_exceeds_noise,
    }
    for check_name, passed in checks.items():
        if not passed:
            verdict = "falsified"
            failed_checks.append(check_name)

    return {
        "evaluation_min_rsa_bits": evaluation_min_rsa_bits,
        "rejection_stability_tolerance": rejection_stability_tolerance,
        "evaluated_rsa_bits": [int(row["rsa_bits"]) for row in evaluation_rows],
        "rejection_band_width": rejection_band_width,
        "rejection_stable": rejection_stable,
        "baseline_cost_rises": baseline_cost_rises,
        "proxy_growth_slower_than_baseline": proxy_growth_slower_than_baseline,
        "speedup_rises": speedup_rises,
        "final_step_bits": [
            int(evaluation_rows[-2]["rsa_bits"]),
            int(evaluation_rows[-1]["rsa_bits"]),
        ],
        "final_step_speedup_delta": final_step_delta,
        "final_step_speedup_noise_band": final_step_noise,
        "final_step_exceeds_noise": final_step_exceeds_noise,
        "baseline_growth_factor": (
            baseline_costs[-1] / baseline_costs[0] if baseline_costs[0] else math.inf
        ),
        "proxy_growth_factor": (
            proxy_costs[-1] / proxy_costs[0] if proxy_costs[0] else math.inf
        ),
        "verdict": verdict,
        "failed_checks": failed_checks,
    }


def build_markdown_report(results: Dict[str, object]) -> str:
    """Render the amplification verification report as Markdown."""
    configuration = results["configuration"]
    analysis = results["analysis"]
    rows = results["rows"]

    lines = [
        "# Structural Amplification Verification",
        "",
        "This report tests the fixed-pipeline amplification hypothesis directly on the deterministic RSA key-generation path.",
        "The same prefilter setup is held fixed across the whole size ladder. Each size is rerun on the same deterministic workload, medians are taken across repeats, and the verdict is driven by a predeclared rule.",
        "",
        "## Configuration",
        "",
        f"- `schedule`: {configuration['schedule']}",
        f"- `repetitions`: {configuration['repetitions']}",
        f"- `evaluation_min_rsa_bits`: {configuration['evaluation_min_rsa_bits']}",
        f"- `rejection_stability_tolerance`: {configuration['rejection_stability_tolerance']:.2%}",
        f"- `public_exponent`: {configuration['public_exponent']}",
        "",
        "## Decision Rule",
        "",
        f"1. For RSA sizes at or above `{configuration['evaluation_min_rsa_bits']}`, the proxy rejection rate must stay within a `{configuration['rejection_stability_tolerance']:.2%}` band.",
        "2. Baseline mean time per keypair must rise across the evaluation cells.",
        "3. Proxy mean time per keypair must grow more slowly than baseline mean time per keypair between the first and last evaluation cells.",
        "4. Median realized speedup must rise across the evaluation cells.",
        "5. The final step in speedup must exceed the measured timing-noise band from the last two cells.",
        "",
        "## Verdict",
        "",
        f"- `verdict`: **{analysis['verdict']}**",
    ]

    if analysis["verdict"] == "verified":
        lines.append(
            f"- Across RSA sizes `{analysis['evaluated_rsa_bits']}`, rejection stayed inside a `{analysis['rejection_band_width'] * 100.0:.3f}` percentage-point band while median speedup kept rising."
        )
        lines.append(
            f"- The final speedup step from `{analysis['final_step_bits'][0]}` to `{analysis['final_step_bits'][1]}` was `{analysis['final_step_speedup_delta']:.6f}x` against a measured noise band of `{analysis['final_step_speedup_noise_band']:.6f}x`."
        )
    elif analysis["verdict"] == "falsified":
        lines.append(f"- Failed checks: `{analysis['failed_checks']}`")
        lines.append(
            f"- The final speedup step from `{analysis['final_step_bits'][0]}` to `{analysis['final_step_bits'][1]}` was `{analysis['final_step_speedup_delta']:.6f}x` against a measured noise band of `{analysis['final_step_speedup_noise_band']:.6f}x`."
        )
    else:
        lines.append(f"- {analysis['reason']}")

    lines.extend(
        [
            "",
            "## Verification Table",
            "",
            "| RSA bits | Keypairs | Repeats | Rejection | Baseline mean/keypair (ms) | Proxy mean/keypair (ms) | Survivor MR mean/keypair (ms) | Speedup median | Speedup range | Ceiling | Ceiling share |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for row in rows:
        speedup = row["speedup"]
        baseline = row["baseline_mean_time_per_keypair_ms"]
        proxy = row["accelerated_mean_proxy_time_per_keypair_ms"]
        survivor_mr = row["accelerated_mean_miller_rabin_time_per_keypair_ms"]
        lines.append(
            f"| {int(row['rsa_bits'])} | {int(row['keypair_count'])} | {int(row['repeat_count'])} | "
            f"{float(row['proxy_rejection_rate']):.6%} | "
            f"{float(baseline['median']):.6f} | "
            f"{float(proxy['median']):.6f} | "
            f"{float(survivor_mr['median']):.6f} | "
            f"{float(speedup['median']):.6f}x | "
            f"{float(speedup['min']):.6f}x..{float(speedup['max']):.6f}x | "
            f"{float(row['structural_speedup_ceiling']):.6f}x | "
            f"{float(row['realized_ceiling_fraction']):.6%} |"
        )

    lines.extend(
        [
            "",
            "## Mechanism Check",
            "",
            f"- Baseline mean time growth factor across the evaluation regime: `{analysis.get('baseline_growth_factor', 0.0):.6f}x`.",
            f"- Proxy mean time growth factor across the evaluation regime: `{analysis.get('proxy_growth_factor', 0.0):.6f}x`.",
            "",
            "Artifacts written by this verifier:",
            "",
            "- `structural_amplification_results.json`",
            "- `structural_amplification_results.csv`",
            "- `STRUCTURAL_AMPLIFICATION_REPORT.md`",
            "- `structural_amplification_speedup.svg`",
            "- `structural_amplification_rejection.svg`",
            "- `structural_amplification_costs.svg`",
            "",
            "## Reproduction",
            "",
            "```bash",
            results["reproduction_command"],
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_speedup_svg(results: Dict[str, object]) -> str:
    """Render realized speedup against the structural ceiling."""
    rows = results["rows"]
    bits = [int(row["rsa_bits"]) for row in rows]
    speedups = [float(row["speedup"]["median"]) for row in rows]
    speedup_mins = [float(row["speedup"]["min"]) for row in rows]
    speedup_maxs = [float(row["speedup"]["max"]) for row in rows]
    ceilings = [float(row["structural_speedup_ceiling"]) for row in rows]
    y_max = max(max(speedup_maxs), max(ceilings)) * 1.12

    plot_width = SVG_WIDTH - SVG_MARGIN_LEFT - SVG_MARGIN_RIGHT
    plot_height = SVG_HEIGHT - SVG_MARGIN_TOP - SVG_MARGIN_BOTTOM
    slot_width = plot_width / max(1, len(rows) - 1)

    def x_coord(index: int) -> float:
        if len(rows) == 1:
            return SVG_MARGIN_LEFT + plot_width / 2.0
        return SVG_MARGIN_LEFT + slot_width * index

    def y_coord(value: float) -> float:
        return SVG_MARGIN_TOP + ((y_max - value) / y_max) * plot_height

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        '<rect width="100%" height="100%" fill="#fcfbf7" />',
        '<text x="96" y="48" font-family="Menlo, Monaco, monospace" font-size="26" fill="#1f2933">Structural amplification speedup by RSA size</text>',
        '<text x="96" y="74" font-family="Menlo, Monaco, monospace" font-size="14" fill="#52606d">Median realized speedup versus the fixed-rejection ceiling 1 / (1 - rejection)</text>',
    ]

    for tick_index in range(6):
        tick_value = y_max * tick_index / 5.0
        y = y_coord(tick_value)
        parts.append(
            f'<line x1="{SVG_MARGIN_LEFT}" y1="{y:.2f}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{y:.2f}" stroke="#d9e2ec" stroke-width="1" />'
        )
        parts.append(
            f'<text x="{SVG_MARGIN_LEFT - 14}" y="{y + 5:.2f}" text-anchor="end" font-family="Menlo, Monaco, monospace" font-size="13" fill="#486581">{tick_value:.2f}x</text>'
        )

    axis_bottom = SVG_HEIGHT - SVG_MARGIN_BOTTOM
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{axis_bottom}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{SVG_MARGIN_TOP}" x2="{SVG_MARGIN_LEFT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )

    realized_points = " ".join(
        f"{x_coord(index):.2f},{y_coord(value):.2f}"
        for index, value in enumerate(speedups)
    )
    ceiling_points = " ".join(
        f"{x_coord(index):.2f},{y_coord(value):.2f}"
        for index, value in enumerate(ceilings)
    )
    parts.append(
        f'<polyline fill="none" stroke="{REALIZED_COLOR}" stroke-width="3.5" points="{realized_points}" />'
    )
    parts.append(
        f'<polyline fill="none" stroke="{CEILING_COLOR}" stroke-width="3" stroke-dasharray="8 6" points="{ceiling_points}" />'
    )

    for index, bits_value in enumerate(bits):
        x = x_coord(index)
        low_y = y_coord(speedup_mins[index])
        high_y = y_coord(speedup_maxs[index])
        center_y = y_coord(speedups[index])
        parts.append(
            f'<line x1="{x:.2f}" y1="{low_y:.2f}" x2="{x:.2f}" y2="{high_y:.2f}" stroke="{REALIZED_COLOR}" stroke-width="2" />'
        )
        parts.append(
            f'<line x1="{x - 8:.2f}" y1="{low_y:.2f}" x2="{x + 8:.2f}" y2="{low_y:.2f}" stroke="{REALIZED_COLOR}" stroke-width="2" />'
        )
        parts.append(
            f'<line x1="{x - 8:.2f}" y1="{high_y:.2f}" x2="{x + 8:.2f}" y2="{high_y:.2f}" stroke="{REALIZED_COLOR}" stroke-width="2" />'
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{center_y:.2f}" r="6" fill="{REALIZED_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y_coord(ceilings[index]):.2f}" r="5" fill="{CEILING_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<text x="{x:.2f}" y="{axis_bottom + 28:.2f}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">{bits_value}</text>'
        )
        parts.append(
            f'<text x="{x:.2f}" y="{axis_bottom + 48:.2f}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="12" fill="#52606d">{speedups[index]:.2f}x</text>'
        )

    legend_x = SVG_WIDTH - SVG_MARGIN_RIGHT - 236
    legend_y = SVG_MARGIN_TOP + 18
    parts.append(
        f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 34}" y2="{legend_y}" stroke="{REALIZED_COLOR}" stroke-width="3.5" />'
    )
    parts.append(
        f'<text x="{legend_x + 44}" y="{legend_y + 5}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">median realized speedup</text>'
    )
    parts.append(
        f'<line x1="{legend_x}" y1="{legend_y + 24}" x2="{legend_x + 34}" y2="{legend_y + 24}" stroke="{CEILING_COLOR}" stroke-width="3" stroke-dasharray="8 6" />'
    )
    parts.append(
        f'<text x="{legend_x + 44}" y="{legend_y + 29}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">structural ceiling</text>'
    )

    parts.append(
        f'<text x="{(SVG_MARGIN_LEFT + SVG_WIDTH - SVG_MARGIN_RIGHT) / 2.0:.2f}" y="{SVG_HEIGHT - 28}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">RSA modulus bits</text>'
    )
    parts.append(
        f'<text x="26" y="{(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f}" transform="rotate(-90 26 {(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f})" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">Speedup</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_rejection_svg(results: Dict[str, object]) -> str:
    """Render rejection stability across the size ladder."""
    rows = results["rows"]
    analysis = results["analysis"]
    bits = [int(row["rsa_bits"]) for row in rows]
    rejections = [float(row["proxy_rejection_rate"]) for row in rows]
    y_min = min(rejections) - 0.01
    y_max = max(rejections) + 0.01
    if y_max <= y_min:
        y_max = y_min + 0.02

    plot_width = SVG_WIDTH - SVG_MARGIN_LEFT - SVG_MARGIN_RIGHT
    plot_height = SVG_HEIGHT - SVG_MARGIN_TOP - SVG_MARGIN_BOTTOM
    slot_width = plot_width / max(1, len(rows) - 1)

    def x_coord(index: int) -> float:
        if len(rows) == 1:
            return SVG_MARGIN_LEFT + plot_width / 2.0
        return SVG_MARGIN_LEFT + slot_width * index

    def y_coord(value: float) -> float:
        return SVG_MARGIN_TOP + ((y_max - value) / (y_max - y_min)) * plot_height

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        '<rect width="100%" height="100%" fill="#fcfbf7" />',
        '<text x="96" y="48" font-family="Menlo, Monaco, monospace" font-size="26" fill="#1f2933">Proxy rejection stability by RSA size</text>',
        '<text x="96" y="74" font-family="Menlo, Monaco, monospace" font-size="14" fill="#52606d">The amplification claim needs a high rejection rate that stays inside one narrow band</text>',
    ]

    for tick_index in range(6):
        tick_value = y_min + (y_max - y_min) * tick_index / 5.0
        y = y_coord(tick_value)
        parts.append(
            f'<line x1="{SVG_MARGIN_LEFT}" y1="{y:.2f}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{y:.2f}" stroke="#d9e2ec" stroke-width="1" />'
        )
        parts.append(
            f'<text x="{SVG_MARGIN_LEFT - 14}" y="{y + 5:.2f}" text-anchor="end" font-family="Menlo, Monaco, monospace" font-size="13" fill="#486581">{tick_value * 100.0:.2f}%</text>'
        )

    axis_bottom = SVG_HEIGHT - SVG_MARGIN_BOTTOM
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{axis_bottom}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{SVG_MARGIN_TOP}" x2="{SVG_MARGIN_LEFT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )

    if analysis["verdict"] != "incomplete":
        eval_rows = [row for row in rows if int(row["rsa_bits"]) >= int(analysis["evaluation_min_rsa_bits"])]
        band_low = min(float(row["proxy_rejection_rate"]) for row in eval_rows)
        band_high = max(float(row["proxy_rejection_rate"]) for row in eval_rows)
        band_top = y_coord(band_high)
        band_height = y_coord(band_low) - band_top
        parts.append(
            f'<rect x="{SVG_MARGIN_LEFT}" y="{band_top:.2f}" width="{plot_width:.2f}" height="{band_height:.2f}" fill="#d9f2e6" opacity="0.55" />'
        )

    points = " ".join(
        f"{x_coord(index):.2f},{y_coord(value):.2f}"
        for index, value in enumerate(rejections)
    )
    parts.append(
        f'<polyline fill="none" stroke="{REJECTION_COLOR}" stroke-width="3.5" points="{points}" />'
    )

    for index, bits_value in enumerate(bits):
        x = x_coord(index)
        y = y_coord(rejections[index])
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" fill="{REJECTION_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<text x="{x:.2f}" y="{axis_bottom + 28:.2f}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">{bits_value}</text>'
        )
        parts.append(
            f'<text x="{x:.2f}" y="{axis_bottom + 48:.2f}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="12" fill="#52606d">{rejections[index] * 100.0:.2f}%</text>'
        )

    parts.append(
        f'<text x="{SVG_WIDTH - SVG_MARGIN_RIGHT - 240:.2f}" y="{SVG_MARGIN_TOP + 32:.2f}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">evaluation band width: {float(analysis.get("rejection_band_width", 0.0)) * 100.0:.3f} pp</text>'
    )
    parts.append(
        f'<text x="{(SVG_MARGIN_LEFT + SVG_WIDTH - SVG_MARGIN_RIGHT) / 2.0:.2f}" y="{SVG_HEIGHT - 28}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">RSA modulus bits</text>'
    )
    parts.append(
        f'<text x="26" y="{(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f}" transform="rotate(-90 26 {(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f})" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">Proxy rejection rate</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_costs_svg(results: Dict[str, object]) -> str:
    """Render baseline, proxy, and survivor MR costs on a log scale."""
    rows = results["rows"]
    bits = [int(row["rsa_bits"]) for row in rows]
    baseline_values = [
        float(row["baseline_mean_time_per_keypair_ms"]["median"]) for row in rows
    ]
    proxy_values = [
        float(row["accelerated_mean_proxy_time_per_keypair_ms"]["median"]) for row in rows
    ]
    survivor_mr_values = [
        float(row["accelerated_mean_miller_rabin_time_per_keypair_ms"]["median"])
        for row in rows
    ]
    all_values = baseline_values + proxy_values + survivor_mr_values
    positive_values = [value for value in all_values if value > 0.0]
    y_min = min(positive_values)
    y_max = max(positive_values)
    log_min = math.log10(y_min)
    log_max = math.log10(y_max)
    if log_max <= log_min:
        log_max = log_min + 1.0

    plot_width = SVG_WIDTH - SVG_MARGIN_LEFT - SVG_MARGIN_RIGHT
    plot_height = SVG_HEIGHT - SVG_MARGIN_TOP - SVG_MARGIN_BOTTOM
    slot_width = plot_width / max(1, len(rows) - 1)

    def x_coord(index: int) -> float:
        if len(rows) == 1:
            return SVG_MARGIN_LEFT + plot_width / 2.0
        return SVG_MARGIN_LEFT + slot_width * index

    def y_coord(value: float) -> float:
        log_value = math.log10(value)
        return SVG_MARGIN_TOP + ((log_max - log_value) / (log_max - log_min)) * plot_height

    def render_series(values: Sequence[float], color: str) -> str:
        return " ".join(f"{x_coord(index):.2f},{y_coord(value):.2f}" for index, value in enumerate(values))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        '<rect width="100%" height="100%" fill="#fcfbf7" />',
        '<text x="96" y="48" font-family="Menlo, Monaco, monospace" font-size="26" fill="#1f2933">Cost separation behind structural amplification</text>',
        '<text x="96" y="74" font-family="Menlo, Monaco, monospace" font-size="14" fill="#52606d">Baseline cost, proxy cost, and survivor Miller-Rabin cost per keypair on a log scale</text>',
    ]

    for exponent in range(math.floor(log_min), math.ceil(log_max) + 1):
        tick_value = 10.0**exponent
        y = y_coord(tick_value)
        parts.append(
            f'<line x1="{SVG_MARGIN_LEFT}" y1="{y:.2f}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{y:.2f}" stroke="#d9e2ec" stroke-width="1" />'
        )
        parts.append(
            f'<text x="{SVG_MARGIN_LEFT - 14}" y="{y + 5:.2f}" text-anchor="end" font-family="Menlo, Monaco, monospace" font-size="13" fill="#486581">{tick_value:.3f}</text>'
        )

    axis_bottom = SVG_HEIGHT - SVG_MARGIN_BOTTOM
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{axis_bottom}" x2="{SVG_WIDTH - SVG_MARGIN_RIGHT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )
    parts.append(
        f'<line x1="{SVG_MARGIN_LEFT}" y1="{SVG_MARGIN_TOP}" x2="{SVG_MARGIN_LEFT}" y2="{axis_bottom}" stroke="#243b53" stroke-width="1.5" />'
    )

    parts.append(
        f'<polyline fill="none" stroke="{BASELINE_COLOR}" stroke-width="3.5" points="{render_series(baseline_values, BASELINE_COLOR)}" />'
    )
    parts.append(
        f'<polyline fill="none" stroke="{PROXY_COLOR}" stroke-width="3.5" points="{render_series(proxy_values, PROXY_COLOR)}" />'
    )
    parts.append(
        f'<polyline fill="none" stroke="{SURVIVOR_MR_COLOR}" stroke-width="3.5" stroke-dasharray="8 6" points="{render_series(survivor_mr_values, SURVIVOR_MR_COLOR)}" />'
    )

    for index, bits_value in enumerate(bits):
        x = x_coord(index)
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y_coord(baseline_values[index]):.2f}" r="6" fill="{BASELINE_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y_coord(proxy_values[index]):.2f}" r="6" fill="{PROXY_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y_coord(survivor_mr_values[index]):.2f}" r="5" fill="{SURVIVOR_MR_COLOR}" stroke="#fcfbf7" stroke-width="2" />'
        )
        parts.append(
            f'<text x="{x:.2f}" y="{axis_bottom + 28:.2f}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">{bits_value}</text>'
        )

    legend_x = SVG_WIDTH - SVG_MARGIN_RIGHT - 320
    legend_y = SVG_MARGIN_TOP + 18
    parts.append(
        f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 34}" y2="{legend_y}" stroke="{BASELINE_COLOR}" stroke-width="3.5" />'
    )
    parts.append(
        f'<text x="{legend_x + 44}" y="{legend_y + 5}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">baseline mean time per keypair</text>'
    )
    parts.append(
        f'<line x1="{legend_x}" y1="{legend_y + 24}" x2="{legend_x + 34}" y2="{legend_y + 24}" stroke="{PROXY_COLOR}" stroke-width="3.5" />'
    )
    parts.append(
        f'<text x="{legend_x + 44}" y="{legend_y + 29}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">accelerated proxy mean per keypair</text>'
    )
    parts.append(
        f'<line x1="{legend_x}" y1="{legend_y + 48}" x2="{legend_x + 34}" y2="{legend_y + 48}" stroke="{SURVIVOR_MR_COLOR}" stroke-width="3.5" stroke-dasharray="8 6" />'
    )
    parts.append(
        f'<text x="{legend_x + 44}" y="{legend_y + 53}" font-family="Menlo, Monaco, monospace" font-size="13" fill="#243b53">accelerated survivor MR mean per keypair</text>'
    )

    parts.append(
        f'<text x="{(SVG_MARGIN_LEFT + SVG_WIDTH - SVG_MARGIN_RIGHT) / 2.0:.2f}" y="{SVG_HEIGHT - 28}" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">RSA modulus bits</text>'
    )
    parts.append(
        f'<text x="26" y="{(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f}" transform="rotate(-90 26 {(SVG_MARGIN_TOP + axis_bottom) / 2.0:.2f})" text-anchor="middle" font-family="Menlo, Monaco, monospace" font-size="14" fill="#243b53">Mean time per keypair (ms, log scale)</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def run_verification(
    output_dir: Path,
    schedule: Sequence[tuple[int, int]],
    repetitions: int,
    evaluation_min_rsa_bits: int,
    rejection_stability_tolerance: float,
    public_exponent: int,
    namespace: str,
) -> Dict[str, object]:
    """Run the full amplification verifier and write all artifacts."""
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1")
    if rejection_stability_tolerance <= 0.0:
        raise ValueError("rejection_stability_tolerance must be positive")

    rows = [
        run_cell_repetitions(
            rsa_bits=rsa_bits,
            keypair_count=keypair_count,
            repetitions=repetitions,
            public_exponent=public_exponent,
            namespace=namespace,
        )
        for rsa_bits, keypair_count in schedule
    ]
    analysis = analyze_hypothesis(
        rows=rows,
        evaluation_min_rsa_bits=evaluation_min_rsa_bits,
        rejection_stability_tolerance=rejection_stability_tolerance,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "experiment_date": time.strftime("%Y-%m-%d"),
        "configuration": {
            "schedule": [
                {"rsa_bits": rsa_bits, "keypair_count": keypair_count}
                for rsa_bits, keypair_count in schedule
            ],
            "repetitions": repetitions,
            "evaluation_min_rsa_bits": evaluation_min_rsa_bits,
            "rejection_stability_tolerance": rejection_stability_tolerance,
            "public_exponent": public_exponent,
            "namespace": namespace,
        },
        "rows": rows,
        "analysis": analysis,
        "reproduction_command": (
            "python3 benchmarks/python/prefilter/structural_amplification_verifier.py "
            f"--output-dir {output_dir} "
            f"--schedule {' '.join(f'{rsa_bits}:{keypair_count}' for rsa_bits, keypair_count in schedule)} "
            f"--repetitions {repetitions} "
            f"--evaluation-min-rsa-bits {evaluation_min_rsa_bits} "
            f"--rejection-stability-tolerance {rejection_stability_tolerance} "
            f"--public-exponent {public_exponent} "
            f"--namespace {namespace}"
        ),
    }

    json_path = output_dir / "structural_amplification_results.json"
    csv_path = output_dir / "structural_amplification_results.csv"
    markdown_path = output_dir / "STRUCTURAL_AMPLIFICATION_REPORT.md"
    speedup_svg_path = output_dir / "structural_amplification_speedup.svg"
    rejection_svg_path = output_dir / "structural_amplification_rejection.svg"
    costs_svg_path = output_dir / "structural_amplification_costs.svg"

    json_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    csv_rows = [
        {
            "rsa_bits": int(row["rsa_bits"]),
            "keypair_count": int(row["keypair_count"]),
            "repeat_count": int(row["repeat_count"]),
            "proxy_rejection_rate": f"{float(row['proxy_rejection_rate']):.12f}",
            "baseline_mean_time_per_keypair_ms_median": f"{float(row['baseline_mean_time_per_keypair_ms']['median']):.12f}",
            "accelerated_mean_time_per_keypair_ms_median": f"{float(row['accelerated_mean_time_per_keypair_ms']['median']):.12f}",
            "baseline_mean_miller_rabin_time_per_keypair_ms_median": f"{float(row['baseline_mean_miller_rabin_time_per_keypair_ms']['median']):.12f}",
            "accelerated_mean_proxy_time_per_keypair_ms_median": f"{float(row['accelerated_mean_proxy_time_per_keypair_ms']['median']):.12f}",
            "accelerated_mean_miller_rabin_time_per_keypair_ms_median": f"{float(row['accelerated_mean_miller_rabin_time_per_keypair_ms']['median']):.12f}",
            "speedup_median": f"{float(row['speedup']['median']):.12f}",
            "speedup_min": f"{float(row['speedup']['min']):.12f}",
            "speedup_max": f"{float(row['speedup']['max']):.12f}",
            "structural_speedup_ceiling": f"{float(row['structural_speedup_ceiling']):.12f}",
            "realized_ceiling_fraction": f"{float(row['realized_ceiling_fraction']):.12f}",
            "baseline_to_proxy_cost_ratio": f"{float(row['baseline_to_proxy_cost_ratio']):.12f}",
            "baseline_miller_rabin_to_proxy_cost_ratio": f"{float(row['baseline_miller_rabin_to_proxy_cost_ratio']):.12f}",
        }
        for row in rows
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(csv_rows)
    markdown_path.write_text(build_markdown_report(results), encoding="utf-8")
    speedup_svg_path.write_text(render_speedup_svg(results), encoding="utf-8")
    rejection_svg_path.write_text(render_rejection_svg(results), encoding="utf-8")
    costs_svg_path.write_text(render_costs_svg(results), encoding="utf-8")
    return results


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Deterministic verifier for the structural amplification hypothesis."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for JSON, CSV, Markdown, and SVG artifacts.",
    )
    parser.add_argument(
        "--schedule",
        type=str,
        nargs="+",
        default=[f"{rsa_bits}:{keypair_count}" for rsa_bits, keypair_count in DEFAULT_SCHEDULE],
        help="Deterministic RSA sweep schedule as rsa_bits:keypair_count tokens.",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=DEFAULT_REPETITIONS,
        help=f"Timing repeats per RSA size (default: {DEFAULT_REPETITIONS}).",
    )
    parser.add_argument(
        "--evaluation-min-rsa-bits",
        type=int,
        default=DEFAULT_EVALUATION_MIN_RSA_BITS,
        help=(
            "Smallest RSA size included in the decision rule "
            f"(default: {DEFAULT_EVALUATION_MIN_RSA_BITS})."
        ),
    )
    parser.add_argument(
        "--rejection-stability-tolerance",
        type=float,
        default=DEFAULT_REJECTION_STABILITY_TOLERANCE,
        help=(
            "Maximum allowed rejection-rate band width on the evaluation regime "
            f"(default: {DEFAULT_REJECTION_STABILITY_TOLERANCE})."
        ),
    )
    parser.add_argument(
        "--public-exponent",
        type=int,
        default=rsa_benchmark.DEFAULT_PUBLIC_EXPONENT,
        help=(
            "RSA public exponent used for every cell "
            f"(default: {rsa_benchmark.DEFAULT_PUBLIC_EXPONENT})."
        ),
    )
    parser.add_argument(
        "--namespace",
        type=str,
        default=DEFAULT_NAMESPACE,
        help="Deterministic namespace for the repeated workload.",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    """Run the verifier and print a compact terminal summary."""
    args = parse_args(argv)
    schedule = parse_schedule_tokens(args.schedule)
    results = run_verification(
        output_dir=args.output_dir,
        schedule=schedule,
        repetitions=args.repetitions,
        evaluation_min_rsa_bits=args.evaluation_min_rsa_bits,
        rejection_stability_tolerance=args.rejection_stability_tolerance,
        public_exponent=args.public_exponent,
        namespace=args.namespace,
    )

    print("structural amplification verification complete")
    print("verdict:", results["analysis"]["verdict"])
    for row in results["rows"]:
        print(
            f"rsa {int(row['rsa_bits'])}:",
            f"{float(row['speedup']['median']):.3f}x median speedup,",
            f"{float(row['proxy_rejection_rate']):.2%} rejection,",
            f"{float(row['baseline_mean_time_per_keypair_ms']['median']):.3f} ms baseline/keypair,",
            f"{float(row['accelerated_mean_proxy_time_per_keypair_ms']['median']):.3f} ms proxy/keypair",
        )
    print(f"artifacts: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
