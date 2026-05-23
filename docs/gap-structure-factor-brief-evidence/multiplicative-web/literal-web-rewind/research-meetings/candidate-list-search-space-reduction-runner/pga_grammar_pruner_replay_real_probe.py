#!/usr/bin/env python3
"""
Replay already-derived real-probe motifs through the current PGA pruner.

This avoids rerunning expensive live public motif derivation. It preserves the
Stage-One measured path boundary by using only the public motifs already emitted
in the audited real probe artifact.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pga_grammar_pruner import REFERENCE_FACTOR_SPACE, prune_factor_space


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "output" / "ladder" / "real_semiprime_64_80_samples_3" / "ladder_summary.json"
DEFAULT_OUTPUT = ROOT / "output" / "ladder" / "real_semiprime_64_80_samples_3_replay"


def replay_case(case: dict[str, Any]) -> dict[str, Any]:
    motif = str(case.get("derived_motif") or case.get("motif"))
    result = prune_factor_space(motif)
    unresolved = result.get("status") == "unresolved"
    reduction_percent = round(float(result.get("reduction_percent", 0.0)), 2)
    return {
        **case,
        "motif": motif,
        "derived_motif": motif,
        "motif_source": case.get("motif_source", "derive_public_motif(N_only)"),
        "construction_method": case.get("construction_method", "deterministic_public_semiprime"),
        "factors_discarded": bool(case.get("factors_discarded", True)),
        "original_search_space_size": REFERENCE_FACTOR_SPACE,
        "rules_fired": result.get("rules_fired", []),
        "pruned": result.get("pruned", 0),
        "pruned_count": result.get("pruned", 0),
        "remaining": result.get("remaining", REFERENCE_FACTOR_SPACE),
        "reduction_percent": reduction_percent,
        "status": "unresolved" if unresolved else "resolved",
        "unresolved_flag": unresolved,
        "coverage_gap": (not unresolved) and reduction_percent < 20,
        "diagnostic_tag": (
            "grammar_pruning_unresolved"
            if unresolved
            else ("low_reduction_coverage_gap" if reduction_percent < 20 else None)
        ),
    }


def aggregate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    resolved = [case for case in cases if not case["unresolved_flag"]]
    unresolved = [case for case in cases if case["unresolved_flag"]]
    reductions = [case["reduction_percent"] for case in cases]
    resolved_reductions = [case["reduction_percent"] for case in resolved]
    top_rules: Counter[str] = Counter()
    coverage_gap_motifs: Counter[str] = Counter()
    motif_breakdown: dict[str, dict[str, Any]] = {}

    for case in cases:
        for rule_id in case["rules_fired"]:
            top_rules[str(rule_id)] += 1
        motif = case["derived_motif"]
        item = motif_breakdown.setdefault(motif, {"frequency": 0, "reductions": []})
        item["frequency"] += 1
        item["reductions"].append(case["reduction_percent"])
        if case["coverage_gap"]:
            coverage_gap_motifs[motif] += 1

    return {
        "total_cases": len(cases),
        "resolved_count": len(resolved),
        "unresolved_count": len(unresolved),
        "average_reduction_over_all_cases": round(sum(reductions) / len(reductions), 2)
        if reductions
        else 0.0,
        "average_reduction_over_resolved_cases_only": round(
            sum(resolved_reductions) / len(resolved_reductions), 2
        )
        if resolved_reductions
        else 0.0,
        "min_reduction": round(min(reductions), 2) if reductions else 0.0,
        "max_reduction": round(max(reductions), 2) if reductions else 0.0,
        "top_rules": top_rules.most_common(10),
        "coverage_gap_motifs": coverage_gap_motifs.most_common(),
        "motif_breakdown": {
            motif: {
                "frequency": data["frequency"],
                "average_reduction": round(
                    sum(data["reductions"]) / len(data["reductions"]), 2
                ),
            }
            for motif, data in sorted(motif_breakdown.items())
        },
    }


def build_replay(input_path: Path) -> dict[str, Any]:
    source = json.loads(input_path.read_text(encoding="utf-8"))
    levels: dict[str, Any] = {}
    all_cases: list[dict[str, Any]] = []

    for bits, level in sorted(source["levels"].items(), key=lambda item: int(item[0])):
        per_case = [replay_case(case) for case in level.get("per_case", [])]
        reductions = [case["reduction_percent"] for case in per_case]
        unresolved_count = sum(1 for case in per_case if case["unresolved_flag"])
        motif_usage = Counter(case["derived_motif"] for case in per_case)
        rule_usage: Counter[str] = Counter()
        for case in per_case:
            for rule_id in case["rules_fired"]:
                rule_usage[str(rule_id)] += 1

        avg = sum(reductions) / len(reductions) if reductions else 0.0
        std = (
            (sum((value - avg) ** 2 for value in reductions) / len(reductions)) ** 0.5
            if len(reductions) > 1
            else 0.0
        )
        levels[str(bits)] = {
            "bit_length": int(bits),
            "samples": len(per_case),
            "average_reduction_percent": round(avg, 2),
            "std_dev": round(std, 2),
            "min_reduction": round(min(reductions), 2) if reductions else 0.0,
            "max_reduction": round(max(reductions), 2) if reductions else 0.0,
            "unresolved_count": unresolved_count,
            "top_motifs": motif_usage.most_common(8),
            "top_rules": rule_usage.most_common(8),
            "per_case": per_case,
        }
        all_cases.extend(per_case)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "real_replay",
        "reference_space": REFERENCE_FACTOR_SPACE,
        "source_probe": str(input_path.relative_to(ROOT)),
        "levels": levels,
        "aggregate": aggregate_cases(all_cases),
    }


def write_reports(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "ladder_summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    aggregate = result["aggregate"]
    lines = [
        "# PGA Grammar Pruner Real-Probe Replay",
        "",
        f"- mode: `{result['mode']}`",
        f"- source_probe: `{result['source_probe']}`",
        f"- reference_space: `{result['reference_space']}`",
        f"- total_cases: `{aggregate['total_cases']}`",
        f"- resolved_cases: `{aggregate['resolved_count']}`",
        f"- unresolved_cases: `{aggregate['unresolved_count']}`",
        f"- average_reduction_over_all_cases: `{aggregate['average_reduction_over_all_cases']}%`",
        f"- average_reduction_over_resolved_cases_only: `{aggregate['average_reduction_over_resolved_cases_only']}%`",
        f"- min_reduction: `{aggregate['min_reduction']}%`",
        f"- max_reduction: `{aggregate['max_reduction']}%`",
        "",
        "## Results By Bit Length",
        "",
        "| bits | avg | min | max | unresolved |",
        "|------|-----|-----|-----|------------|",
    ]
    for bits, level in sorted(result["levels"].items(), key=lambda item: int(item[0])):
        lines.append(
            f"| {bits} | {level['average_reduction_percent']:.2f}% | "
            f"{level['min_reduction']:.2f}% | {level['max_reduction']:.2f}% | "
            f"{level['unresolved_count']} |"
        )

    lines += [
        "",
        "## Motif Breakdown",
        "",
        "| motif | frequency | avg reduction | coverage gap cases |",
        "|-------|-----------|---------------|--------------------|",
    ]
    gap_counts = dict(aggregate["coverage_gap_motifs"])
    for motif, data in aggregate["motif_breakdown"].items():
        lines.append(
            f"| `{motif}` | {data['frequency']} | {data['average_reduction']:.2f}% | "
            f"{gap_counts.get(motif, 0)} |"
        )

    lines += ["", "## Per-Case Replay", ""]
    for bits, level in sorted(result["levels"].items(), key=lambda item: int(item[0])):
        lines += [
            f"### {bits} bits",
            "",
            "| case_id | motif | rules | pruned | remaining | reduction | gap |",
            "|---------|-------|-------|--------|-----------|-----------|-----|",
        ]
        for case in level["per_case"]:
            rules = ",".join(case["rules_fired"]) or "-"
            gap = "yes" if case["coverage_gap"] else "no"
            lines.append(
                f"| {case['case_id']} | `{case['derived_motif']}` | {rules} | "
                f"{case['pruned']} | {case['remaining']} | "
                f"{case['reduction_percent']:.2f}% | {gap} |"
            )
        lines.append("")

    lines.append("Replay uses already-derived public motifs only. It does not rerun motif derivation.")
    (output_dir / "ladder_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay real probe motifs through the current pruner")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = build_replay(args.input)
    write_reports(result, args.out_dir)
    print(json.dumps(result["aggregate"], indent=2))
    print(f"Replay written to: {args.out_dir}")


if __name__ == "__main__":
    main()
