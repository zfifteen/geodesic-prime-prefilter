#!/usr/bin/env python3
"""One-shot multi-lane remainder investigation orchestrator.

Coordinates data pulls across interior R(n,M), endpoint residue masks,
left-prime mod-30 ridge orientation, state-budget residue cells, RSA
backward modulus/remainder search, and GWR Super-Signal epistemic status.

All outputs are measurement-layer artifacts under research/remainders/.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from correlation_analysis import (  # noqa: E402
    compute_intra_gap_repeat_stats,
    compute_residue_histograms,
    feature_correlation_matrix,
    mutual_information,
)

DEFAULT_OUT = ROOT / "research/remainders/correlations/investigation"


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
    for p, grecs in gaps.items():
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
        "gaps_analyzed": len(gaps),
        "gwr_last_rate": gwr_last / len(gaps) if gaps else 0.0,
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


def extract_endpoint_lane_summary() -> dict[str, Any]:
    """Pin endpoint residue-mask rates from the committed hourly frontier doc."""
    return {
        "lane": "endpoint_residue_mask",
        "source": "research/00-index/docs/algorithmic_frontier_hourly.md",
        "regime": "100000 consecutive gaps from q >= 10^13",
        "mask_width": 96,
        "carried_residues_primes_le": 37,
        "gaps_tested": 100000,
        "chain_mismatches": 0,
        "resolved_in_mask_fraction": 1.0,
        "small_prime_mod_checks_baseline": 5145085,
        "small_prime_mod_checks_hybrid": 0,
        "small_prime_mod_reduction_fraction": 0.999846,
        "miller_rabin_calls_unchanged": 444678,
        "wall_time_speedup": 1.0345,
        "repro_note": "Prototype cited in hourly doc; repo script gwr_dni_boundary_state_mask_search.py referenced but not committed.",
    }


def extract_mod30_ridge_lane_summary() -> dict[str, Any]:
    """Read pinned mod-30 ridge orientation JSON."""
    path = ROOT / "research/11-gap-ridge/output/insight_probes/residue_mod30_right_edge_share.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    scale_1e6 = [row for row in data["summary"] if row["scale"] == 1_000_000]
    return {
        "lane": "left_prime_mod30_ridge",
        "source": str(path),
        "scale_1e6": {
            "global_gaps": data["rows"][0]["global"]["gaps"],
            "global_right_share": data["rows"][0]["global"]["right"]
            / data["rows"][0]["global"]["gaps"],
            "by_residue": [
                {
                    "p_mod_30": row["residue"],
                    "gaps": row["gaps"],
                    "right_share": row["right_share"],
                    "right_lift": row["right_lift"],
                }
                for row in scale_1e6
            ],
        },
        "repro_command": "python research/11-gap-ridge/scripts/insight_probes.py (residue_mod30 probe; see findings doc)",
    }


def extract_state_budget_lane_summary() -> dict[str, Any]:
    """Read residue-matched pair summary."""
    path = ROOT / "research/05-state-budget/output/state_budget_residue_matched_pair_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mod30 = next(m for m in data["mode_summaries"] if m["match_mode"] == "mod30")
    square = next(ms for ms in mod30["measure_summaries"] if ms["measure"] == "square_ruler")
    return {
        "lane": "state_budget_residue_matched_cells",
        "source": str(path),
        "power_range": [data["min_power"], data["max_power"]],
        "mod30_decisive_pairs": square["decisive_pairs"],
        "mod30_signed_advantage": square["signed_advantage"],
        "mod30_advantage_share": square["advantage_share"],
        "mod30_verdict": mod30["verdict"],
        "repro_command": "python research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py",
    }


def extract_rsa_lane_summary() -> dict[str, Any]:
    """Read RSA backward invariant closure summary."""
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
        "invariant_laws_tested": list(data["invariant_law_summaries"].keys()),
        "best_factor_reach_recall": max(
            law["factor_reach_recall"] for law in data["invariant_law_summaries"].values()
        ),
        "repro_command": (
            "python research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py "
            "--max-n 5000 --output-dir research/06-cryptology-rsa/output/semiprime_branch"
        ),
    }


def extract_super_signal_status() -> dict[str, Any]:
    """Epistemic status only (no PROOF.md edits)."""
    return {
        "lane": "gwr_super_signal",
        "proof_location": "PROOF.md Twin-Prime Resonance section",
        "theorem_stack_status": "measured · corollary (per PROOF.md theorem stack table)",
        "open_g2_items": [
            "4+ zeros ⟺ w ≡ 0 (mod 30) needs exhaustive case analysis",
            "Step 3 informal language needs explicit lemma",
            "No Lean mirror",
        ],
        "reference": "docs/proof-enhancements/goals.md G2",
    }


def write_lane_table(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    """Write a simple markdown table."""
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
        default=ROOT / "research/remainders/output/1e6/raw_records.jsonl",
        help="Interior remainder JSONL (default: pinned 1e6 surface).",
    )
    parser.add_argument(
        "--tiny-jsonl",
        type=Path,
        default=ROOT / "research/remainders/output/tiny_val/raw_records.jsonl",
        help="Small validation JSONL for fast correlation tables.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUT,
        help="Investigation output directory.",
    )
    parser.add_argument(
        "--max-interior-records",
        type=int,
        default=None,
        help="Optional cap for quick runs (default: full file).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    run_meta = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "interior_jsonl": str(args.interior_jsonl),
        "tiny_jsonl": str(args.tiny_jsonl),
        "output_dir": str(out_dir),
    }

    interior_stats = stream_analyze_interior_jsonl(
        args.interior_jsonl,
        max_records=args.max_interior_records,
    )
    (out_dir / "interior_1e6_placement_stats.json").write_text(
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
    tiny_corr = {
        "records": len(tiny_records),
        "mi_num_zeros_vs_dist": tiny_mi,
        "histogram_groups": len(histograms["groups"]),
    }
    (out_dir / "tiny_val_correlation_stats.json").write_text(
        json.dumps(tiny_corr, indent=2) + "\n",
        encoding="utf-8",
    )

    endpoint = extract_endpoint_lane_summary()
    mod30 = extract_mod30_ridge_lane_summary()
    state_budget = extract_state_budget_lane_summary()
    rsa = extract_rsa_lane_summary()
    super_signal = extract_super_signal_status()

    for name, payload in [
        ("endpoint_lane_summary.json", endpoint),
        ("mod30_ridge_lane_summary.json", mod30),
        ("state_budget_lane_summary.json", state_budget),
        ("rsa_lane_summary.json", rsa),
        ("super_signal_status.json", super_signal),
    ]:
        (out_dir / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    placement_rows = [
        {
            "metric": "gwr_last_rate",
            "regime": "p<=1e6 interior",
            "value": f"{interior_stats['gwr_last_rate']:.4f}",
            "n_gaps": interior_stats["gaps_analyzed"],
        },
        {
            "metric": "mi_num_zeros_vs_dist",
            "regime": "p<=1e6 interior",
            "value": f"{interior_stats['mi_num_zeros_vs_dist_bin']['mi']:.4f}",
            "n_gaps": interior_stats["records_analyzed"],
        },
        {
            "metric": "spearman_entropy_vs_g",
            "regime": "p<=1e6 interior",
            "value": f"{interior_stats['spearman_entropy_vs_g']:.4f}",
            "n_gaps": interior_stats["gaps_analyzed"],
        },
        {
            "metric": "super_signal_at_gwr_rate",
            "regime": "p<=1e6 interior",
            "value": f"{interior_stats['super_signal_at_gwr_rate']:.6f}",
            "n_gaps": interior_stats["gaps_analyzed"],
        },
        {
            "metric": "g2_with_super_signal_gwr",
            "regime": "p<=1e6 interior",
            "value": str(interior_stats["g2_with_super_signal_gwr"]),
            "n_gaps": interior_stats["gaps_analyzed"],
        },
    ]
    write_lane_table(
        out_dir / "placement_correlation_table.md",
        placement_rows,
        ["metric", "regime", "value", "n_gaps"],
    )

    run_meta["interior_gaps"] = interior_stats["gaps_analyzed"]
    run_meta["interior_records"] = interior_stats["records_analyzed"]
    (out_dir / "RUN_LOG.json").write_text(json.dumps(run_meta, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"output_dir": str(out_dir), **run_meta}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())