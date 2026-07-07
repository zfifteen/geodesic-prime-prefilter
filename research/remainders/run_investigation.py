#!/usr/bin/env python3
"""Multi-lane remainder investigation orchestrator.

Executes lane collectors (fresh measurements) and streams interior JSONL
for placement-correlation statistics. Writes pinned summaries under
research/remainders/correlations/investigation/.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LANE_DIR = HERE / "lane_collectors"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from correlation_analysis import (  # noqa: E402
    compute_intra_gap_repeat_stats,
    compute_residue_histograms,
    feature_correlation_matrix,
    mutual_information,
)

DEFAULT_OUT = ROOT / "research/remainders/correlations/investigation"
DEFAULT_INTERIOR = ROOT / "research/remainders/output/1.5e6/raw_records.jsonl"


def stream_analyze_interior_jsonl(
    jsonl_path: Path,
    *,
    max_records: int | None = None,
) -> dict[str, Any]:
    """Stream interior records and compute placement-correlation statistics."""
    gaps: dict[int, list[dict[str, Any]]] = defaultdict(list)
    record_count = 0
    residues: list[int] = []
    dist_bins: list[int] = []
    super_signal_gwr = 0
    super_signal_g2 = 0
    gwr_total = 0
    gwr_last = 0

    with jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rec = json.loads(line)
            record_count += 1
            if max_records is not None and record_count > max_records:
                break

            p = int(rec["p"])
            gaps[p].append(rec)

            zeros = sum(1 for v in rec["remainder_vector"] if v == 0)
            dist = int(rec.get("distance_to_next_prime", rec.get("termination_distance", 99)))
            dist_bin = min(dist, 5)
            residues.append(zeros)
            dist_bins.append(dist_bin)

            if rec.get("is_current_min_d") or rec.get("is_gwr_winner"):
                gwr_total += 1
                if zeros >= 4:
                    super_signal_gwr += 1
                if dist == 1:
                    gwr_last += 1

    gap_features: list[dict[str, float]] = []
    for grecs in gaps.values():
        grecs.sort(key=lambda r: int(r.get("k", 0)))
        g = float(grecs[0]["g"])
        counts: dict[tuple[int, ...], int] = defaultdict(int)
        for r in grecs:
            vec = tuple(int(v) for v in r["remainder_vector"][:6])
            counts[vec] += 1
        n = len(grecs)
        entropy = 0.0
        for c in counts.values():
            p_val = c / n
            entropy -= p_val * math.log(p_val)
        gap_features.append({"g": g, "entropy": entropy, "n_unique": float(len(counts))})
        if g == 2.0:
            for r in grecs:
                if r.get("is_current_min_d") and sum(1 for v in r["remainder_vector"] if v == 0) >= 4:
                    super_signal_g2 += 1

    gaps_with_interiors = len(gaps)
    mi = mutual_information(residues, dist_bins)
    feat_list = [{"g": f["g"], "entropy": f["entropy"]} for f in gap_features]
    corr_matrix = feature_correlation_matrix(feat_list, method="spearman")
    spearman_entropy_g = corr_matrix[0][1] if corr_matrix else 0.0

    gwr_distinct_diffs: list[float] = []
    for grecs in gaps.values():
        grecs.sort(key=lambda r: int(r.get("k", 0)))
        avg_zeros = sum(
            sum(1 for v in r["remainder_vector"] if v == 0) for r in grecs
        ) / len(grecs)
        for r in grecs:
            if r.get("is_current_min_d") or r.get("is_gwr_winner"):
                gwr_zeros = sum(1 for v in r["remainder_vector"] if v == 0)
                gwr_distinct_diffs.append(gwr_zeros - avg_zeros)
                break

    avg_gwr_zero_diff = (
        sum(gwr_distinct_diffs) / len(gwr_distinct_diffs) if gwr_distinct_diffs else 0.0
    )

    flat_records = [r for grecs in gaps.values() for r in grecs]
    repeat_stats = compute_intra_gap_repeat_stats(flat_records)

    return {
        "source": str(jsonl_path),
        "records_analyzed": record_count,
        "gaps_with_interiors": gaps_with_interiors,
        "gwr_last_rate": gwr_last / gaps_with_interiors if gaps_with_interiors else 0.0,
        "gwr_last_count": gwr_last,
        "super_signal_at_gwr_count": super_signal_gwr,
        "super_signal_at_gwr_rate": super_signal_gwr / gwr_total if gwr_total else 0.0,
        "g2_with_super_signal_gwr": super_signal_g2,
        "mi_num_zeros_vs_dist_bin": mi,
        "spearman_entropy_vs_g": spearman_entropy_g,
        "avg_gwr_zero_minus_gap_avg": avg_gwr_zero_diff,
        "repeat_stats": repeat_stats,
        "mod2_even_fraction": sum(1 for r in flat_records if r["remainder_vector"][0] == 0)
        / len(flat_records)
        if flat_records
        else 0.0,
    }


def run_subprocess(cmd: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    """Run one lane collector and capture exit metadata."""
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:] if proc.stdout else "",
        "stderr_tail": proc.stderr[-1000:] if proc.stderr else "",
    }


def execute_lane_collectors(out_dir: Path, *, run_slow: bool) -> dict[str, Any]:
    """Execute fresh measurements for non-interior lanes."""
    lane_runs: dict[str, Any] = {}
    py = sys.executable

    endpoint_out = out_dir / "endpoint_residue_probe_fresh.json"
    lane_runs["endpoint"] = run_subprocess(
        [
            py,
            str(LANE_DIR / "endpoint_residue_probe.py"),
            "--start-p",
            "10000000000037",
            "--max-gaps",
            "5000",
            "--output",
            str(endpoint_out),
        ]
    )

    ridge_out = out_dir / "mod30_ridge_probe_fresh.json"
    lane_runs["mod30_ridge"] = run_subprocess(
        [
            py,
            str(LANE_DIR / "mod30_ridge_probe.py"),
            "--max-p",
            "100000" if not run_slow else "200000",
            "--output",
            str(ridge_out),
        ]
    )

    if run_slow:
        lane_runs["state_budget"] = run_subprocess(
            [
                py,
                str(ROOT / "research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py"),
            ]
        )
        lane_runs["rsa"] = run_subprocess(
            [
                py,
                str(
                    ROOT
                    / "research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py"
                ),
                "--max-n",
                "5000",
                "--output-dir",
                str(ROOT / "research/06-cryptology-rsa/output/semiprime_branch"),
            ]
        )

    return lane_runs


def load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def build_endpoint_summary(out_dir: Path) -> dict[str, Any]:
    fresh = load_json_if_exists(out_dir / "endpoint_residue_probe_fresh.json")
    reference = {
        "lane": "endpoint_residue_mask",
        "source": "research/00-index/docs/algorithmic_frontier_hourly.md",
        "regime": "100000 consecutive gaps from q >= 10^13",
        "mask_width": 96,
        "gaps_tested": 100000,
        "chain_mismatches": 0,
        "resolved_in_mask_fraction": 1.0,
        "small_prime_mod_reduction_fraction": 0.999846,
        "wall_time_speedup": 1.0345,
    }
    return {"reference_artifact": reference, "fresh_probe": fresh, "lane_runs": "see RUN_LOG.json"}


def build_mod30_summary(out_dir: Path) -> dict[str, Any]:
    fresh = load_json_if_exists(out_dir / "mod30_ridge_probe_fresh.json")
    pinned_path = ROOT / "research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json"
    pinned = json.loads(pinned_path.read_text(encoding="utf-8")) if pinned_path.exists() else None
    return {"fresh_probe": fresh, "pinned_artifact_path": str(pinned_path), "pinned_scale_1e6": pinned}


def build_state_budget_summary() -> dict[str, Any]:
    path = ROOT / "research/05-state-budget/output/state_budget_residue_matched_pair_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mod30 = next(m for m in data["mode_summaries"] if m["match_mode"] == "mod30")
    square = next(ms for ms in mod30["measure_summaries"] if ms["measure"] == "square_ruler")
    return {
        "lane": "state_budget_residue_matched_cells",
        "source": str(path),
        "mod30_decisive_pairs": square["decisive_pairs"],
        "mod30_signed_advantage": square["signed_advantage"],
        "mod30_advantage_share": square["advantage_share"],
        "mod30_verdict": mod30["verdict"],
        "collector": "state_budget_residue_matched_pair_test.py",
    }


def build_rsa_summary() -> dict[str, Any]:
    path = (
        ROOT
        / "research/06-cryptology-rsa/output/semiprime_branch"
        / "pgs_semiprime_backward_invariant_closure_search_summary.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "lane": "rsa_backward_modulus_remainder",
        "source": str(path),
        "max_n": data["max_n"],
        "case_count": data["case_count"],
        "best_factor_reach_recall": max(
            law["factor_reach_recall"] for law in data["invariant_law_summaries"].values()
        ),
        "collector": "pgs_semiprime_backward_invariant_closure_search.py",
    }


def build_super_signal_status() -> dict[str, Any]:
    return {
        "lane": "gwr_super_signal",
        "theorem_stack_status": "measured · corollary",
        "reference": "docs/proof-enhancements/goals.md G2",
        "open_g2_items": [
            "4+ zeros ⟺ w ≡ 0 (mod 30) needs exhaustive case analysis",
            "Step 3 informal language needs explicit lemma",
            "No Lean mirror",
        ],
    }


def write_lane_table(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in columns) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interior-jsonl",
        type=Path,
        default=DEFAULT_INTERIOR,
        help="Interior remainder JSONL (default: scaled 1.5e6 surface).",
    )
    parser.add_argument(
        "--tiny-jsonl",
        type=Path,
        default=ROOT / "research/remainders/output/tiny_val/raw_records.jsonl",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUT,
    )
    parser.add_argument(
        "--max-interior-records",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--skip-lane-execution",
        action="store_true",
        help="Skip subprocess lane collectors (fast tests only).",
    )
    parser.add_argument(
        "--run-slow-lanes",
        action="store_true",
        help="Also re-run state-budget and RSA collectors.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    lane_runs: dict[str, Any] = {}
    if not args.skip_lane_execution:
        lane_runs = execute_lane_collectors(out_dir, run_slow=args.run_slow_lanes)

    interior_stats = stream_analyze_interior_jsonl(
        args.interior_jsonl,
        max_records=args.max_interior_records,
    )
    (out_dir / "interior_placement_stats.json").write_text(
        json.dumps(interior_stats, indent=2) + "\n",
        encoding="utf-8",
    )

    tiny_records = []
    with args.tiny_jsonl.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                tiny_records.append(json.loads(line))

    tiny_mi = mutual_information(
        [sum(1 for v in r["remainder_vector"] if v == 0) for r in tiny_records],
        [
            min(
                int(r.get("distance_to_next_prime", r.get("termination_distance", 99))),
                5,
            )
            for r in tiny_records
        ],
    )
    histograms = compute_residue_histograms(tiny_records)
    (out_dir / "tiny_val_correlation_stats.json").write_text(
        json.dumps(
            {
                "records": len(tiny_records),
                "mi_num_zeros_vs_dist": tiny_mi,
                "histogram_groups": len(histograms["groups"]),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    regime_label = f"interior {args.interior_jsonl.parent.name}"
    placement_rows = [
        {
            "metric": "gwr_last_rate",
            "regime": regime_label,
            "value": f"{interior_stats['gwr_last_rate']:.4f}",
            "n_gaps": interior_stats["gaps_with_interiors"],
        },
        {
            "metric": "mi_num_zeros_vs_dist",
            "regime": regime_label,
            "value": f"{interior_stats['mi_num_zeros_vs_dist_bin']['mi']:.4f}",
            "n_records": interior_stats["records_analyzed"],
        },
        {
            "metric": "spearman_entropy_vs_g",
            "regime": regime_label,
            "value": f"{interior_stats['spearman_entropy_vs_g']:.4f}",
            "n_gaps": interior_stats["gaps_with_interiors"],
        },
        {
            "metric": "super_signal_at_gwr_rate",
            "regime": regime_label,
            "value": f"{interior_stats['super_signal_at_gwr_rate']:.6f}",
            "n_gaps": interior_stats["gaps_with_interiors"],
        },
        {
            "metric": "g2_with_super_signal_gwr",
            "regime": regime_label,
            "value": str(interior_stats["g2_with_super_signal_gwr"]),
            "n_gaps": interior_stats["gaps_with_interiors"],
        },
    ]
    write_lane_table(
        out_dir / "placement_correlation_table.md",
        placement_rows,
        ["metric", "regime", "value", "n_gaps"],
    )

    summaries = {
        "endpoint_lane_summary.json": build_endpoint_summary(out_dir),
        "mod30_ridge_lane_summary.json": build_mod30_summary(out_dir),
        "state_budget_lane_summary.json": build_state_budget_summary(),
        "rsa_lane_summary.json": build_rsa_summary(),
        "super_signal_status.json": build_super_signal_status(),
    }
    for name, payload in summaries.items():
        (out_dir / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    run_meta = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "interior_jsonl": str(args.interior_jsonl),
        "gaps_with_interiors": interior_stats["gaps_with_interiors"],
        "records_analyzed": interior_stats["records_analyzed"],
        "lane_collector_runs": lane_runs,
    }
    (out_dir / "RUN_LOG.json").write_text(json.dumps(run_meta, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"output_dir": str(out_dir), **run_meta}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())