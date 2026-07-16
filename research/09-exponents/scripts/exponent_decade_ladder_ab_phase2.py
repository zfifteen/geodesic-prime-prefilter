#!/usr/bin/env python3
"""Phase 2 A/B: left_prime multi-offset vs residue_return Mersenne inference."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import exponent_decade_ladder_pgs_mechanism as mechanism
import exponent_decade_ladder_validator as validator


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = (
    ROOT / "research" / "09-exponents" / "output" / "exponent_decade_ladder_ab_phase2"
)
DEFAULT_RUNGS = "100,400"
DEFAULT_CANDIDATE_BOUND = 4096
DEFAULT_CANDIDATE_SECONDS_LIMIT = 1.0


def build_parser() -> argparse.ArgumentParser:
    """Build the A/B CLI."""
    parser = argparse.ArgumentParser(description="Phase 2 ladder A/B comparison.")
    parser.add_argument("--rungs", default=DEFAULT_RUNGS)
    parser.add_argument("--candidate-bound", type=int, default=DEFAULT_CANDIDATE_BOUND)
    parser.add_argument(
        "--candidate-seconds-limit",
        type=float,
        default=DEFAULT_CANDIDATE_SECONDS_LIMIT,
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def run_arm(
    *,
    mode: str,
    rungs: list[int],
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Run one inference arm and return measured summary fields."""
    started = time.perf_counter()
    rows = mechanism.collect_rows(
        rungs,
        candidate_bound,
        candidate_seconds_limit,
        mode,
    )
    wall = time.perf_counter() - started
    validation_rows = validator.validate_rows(
        [{key: str(value) for key, value in row.items()} for row in rows]
    )
    validation = validator.summarize(validation_rows)
    pgs = mechanism.summarize(
        rows,
        rungs,
        candidate_bound,
        candidate_seconds_limit,
        mode,
    )
    inferred = sorted(
        int(row["exponent"]) for row in rows if bool(row["mersenne_location_inferred"])
    )
    return {
        "mode": mode,
        "wall_elapsed_seconds": wall,
        "row_count": len(rows),
        "candidate_checks_sum": sum(
            int(row["candidate_checks"])
            for row in rows
            if row["candidate_checks"] != ""
        ),
        "inferred_exponents": inferred,
        "inferred_count": len(inferred),
        "unresolved_count": int(pgs["left_prime_unresolved_count"]),
        "resolved_count": int(pgs["left_prime_resolved_count"]),
        "excluded_count": int(pgs["excluded_exponent_count"]),
        "classical_false_positive_count": int(validation["classical_false_positive_count"]),
        "classical_false_negative_count": int(validation["classical_false_negative_count"]),
        "classical_agreement_count": int(validation["classical_agreement_count"]),
        "validated_row_count": int(validation["validated_row_count"]),
        "pgs_summary": pgs,
        "validation_summary": validation,
        "rows": rows,
        "validation_rows": validation_rows,
    }


def compare(arm_a: dict[str, object], arm_b: dict[str, object]) -> dict[str, object]:
    """Return comparison metrics for left_prime (A) vs residue_return (B)."""
    wall_a = float(arm_a["wall_elapsed_seconds"])
    wall_b = float(arm_b["wall_elapsed_seconds"])
    inferred_a = set(arm_a["inferred_exponents"])
    inferred_b = set(arm_b["inferred_exponents"])
    return {
        "window_rungs": arm_a["pgs_summary"]["rungs"],
        "wall_seconds_left_prime": wall_a,
        "wall_seconds_residue_return": wall_b,
        "wall_speedup_ratio": (wall_a / wall_b) if wall_b > 0 else None,
        "candidate_checks_sum_left_prime": arm_a["candidate_checks_sum"],
        "candidate_checks_sum_residue_return": arm_b["candidate_checks_sum"],
        "inferred_left_prime": sorted(inferred_a),
        "inferred_residue_return": sorted(inferred_b),
        "inferred_intersection": sorted(inferred_a & inferred_b),
        "inferred_only_left_prime": sorted(inferred_a - inferred_b),
        "inferred_only_residue_return": sorted(inferred_b - inferred_a),
        "inferred_sets_equal": inferred_a == inferred_b,
        "false_positives_left_prime": arm_a["classical_false_positive_count"],
        "false_positives_residue_return": arm_b["classical_false_positive_count"],
        "false_negatives_left_prime": arm_a["classical_false_negative_count"],
        "false_negatives_residue_return": arm_b["classical_false_negative_count"],
        "acceptance": {
            "zero_false_positives_residue_return": arm_b["classical_false_positive_count"]
            == 0,
            "inferred_sets_equal": inferred_a == inferred_b,
            "wall_speedup_at_least_3x": bool(wall_b > 0 and (wall_a / wall_b) >= 3.0),
        },
    }


def write_arm_outputs(output_dir: Path, arm: dict[str, object]) -> None:
    """Write one arm's ladder rows and summaries."""
    mode = str(arm["mode"])
    arm_dir = output_dir / mode
    arm_dir.mkdir(parents=True, exist_ok=True)
    mechanism.write_csv(arm_dir / "pgs_ladder_rows.csv", arm["rows"], mechanism.PGS_FIELDNAMES)
    validator.write_outputs(arm_dir, arm["validation_rows"])
    payload = {
        key: value
        for key, value in arm.items()
        if key not in {"rows", "validation_rows", "pgs_summary", "validation_summary"}
    }
    payload["pgs_summary"] = arm["pgs_summary"]
    payload["validation_summary"] = arm["validation_summary"]
    (arm_dir / "arm_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run Phase 2 A/B and write artifacts."""
    args = build_parser().parse_args(argv)
    rungs = mechanism.parse_rungs(args.rungs)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    arm_left = run_arm(
        mode=mechanism.INFERENCE_LEFT_PRIME,
        rungs=rungs,
        candidate_bound=args.candidate_bound,
        candidate_seconds_limit=args.candidate_seconds_limit,
    )
    arm_residue = run_arm(
        mode=mechanism.INFERENCE_RESIDUE_RETURN,
        rungs=rungs,
        candidate_bound=args.candidate_bound,
        candidate_seconds_limit=args.candidate_seconds_limit,
    )
    write_arm_outputs(output_dir, arm_left)
    write_arm_outputs(output_dir, arm_residue)
    comparison = compare(arm_left, arm_residue)
    (output_dir / "ab_comparison.json").write_text(
        json.dumps(comparison, indent=2) + "\n",
        encoding="utf-8",
    )

    # Compact one-row CSV for continuity tables.
    with (output_dir / "ab_comparison_row.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "window_rungs",
                "wall_seconds_left_prime",
                "wall_seconds_residue_return",
                "wall_speedup_ratio",
                "inferred_sets_equal",
                "false_positives_residue_return",
                "false_negatives_residue_return",
                "wall_speedup_at_least_3x",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "window_rungs": ";".join(str(value) for value in comparison["window_rungs"]),
                "wall_seconds_left_prime": comparison["wall_seconds_left_prime"],
                "wall_seconds_residue_return": comparison["wall_seconds_residue_return"],
                "wall_speedup_ratio": comparison["wall_speedup_ratio"],
                "inferred_sets_equal": comparison["inferred_sets_equal"],
                "false_positives_residue_return": comparison[
                    "false_positives_residue_return"
                ],
                "false_negatives_residue_return": comparison[
                    "false_negatives_residue_return"
                ],
                "wall_speedup_at_least_3x": comparison["acceptance"][
                    "wall_speedup_at_least_3x"
                ],
            }
        )

    print(
        "Phase2 A/B: "
        f"left_prime={comparison['wall_seconds_left_prime']:.3f}s, "
        f"residue_return={comparison['wall_seconds_residue_return']:.3f}s, "
        f"speedup={comparison['wall_speedup_ratio']}, "
        f"inferred_equal={comparison['inferred_sets_equal']}, "
        f"fp_B={comparison['false_positives_residue_return']}, "
        f"fn_B={comparison['false_negatives_residue_return']}"
    )
    print(f"Output dir: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
