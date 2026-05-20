#!/usr/bin/env python3
"""Run the v02 public ratio runner, then perform canonical membership audit."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "thread_triangulation_v02_ratio_runner.py"
CANONICAL_AUDIT = ROOT.parent / "true-triangulation-iteration-loop" / "canonical_membership_audit.py"

AUDIT_PAIRS = {
    "toy_989": (23, 43),
    "toy_9379": (83, 113),
    "toy_25807": (131, 197),
    "toy_1242079": (1009, 1231),
    "toy_200250077": (10007, 20011),
    "toy_4295229443": (65537, 65539),
    "toy_18902665303": (117151, 161353),
    "toy_1209476905903": (7, 172782415129),
    "toy_77468500194643": (2302891, 33639673),
    "toy_4951764003343009": (641, 7725060847649),
}


def load_cases(path: Path) -> list[dict[str, object]]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                cases.append(json.loads(line))
    return cases


def run_command(command: list[str], log_path: Path | None = None) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if log_path is not None:
        log_path.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def median_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return statistics.median(values)


def summarize(rows: list[dict[str, object]], out_dir: Path) -> None:
    recovered = [row for row in rows if row["status"] == "recovered"]
    missed = [row for row in rows if row["status"] == "missed"]
    summary = {
        "policy": "thread_triangulation_v02_ratio",
        "case_count": len(rows),
        "recovered_count": len(recovered),
        "missed_count": len(missed),
        "hit_rate": f"{len(recovered)}/{len(rows)}",
        "median_emitted_count": median_or_none([float(row["emitted_count"]) for row in rows]),
        "median_candidate_reduction_bits": median_or_none(
            [float(row["candidate_reduction_bits"]) for row in rows if row["candidate_reduction_bits"] is not None]
        ),
        "rows": rows,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# v02 Ratio Toy Corpus Summary",
        "",
        f"- policy: `{summary['policy']}`",
        f"- cases: `{summary['case_count']}`",
        f"- recovered: `{summary['recovered_count']}`",
        f"- missed: `{summary['missed_count']}`",
        f"- hit_rate: `{summary['hit_rate']}`",
        f"- median_emitted_count: `{summary['median_emitted_count']}`",
        f"- median_candidate_reduction_bits: `{summary['median_candidate_reduction_bits']}`",
        "",
        "| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status | recovered |",
        "|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| `{case}` | {N_bits} | {active_thread_count} | {min_depth} | {max_candidates} | "
            "{emitted_count} | {pre_cap_qualified_count} | `{cap_active}` | {candidate_reduction_bits} | "
            "`{status}` | `{recovered_factor}` |".format(**row)
        )
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "cases" / "toy_corpus.jsonl")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "output" / "toy_v02_ratio")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for case in load_cases(args.cases):
        case_name = str(case["case"])
        n_value = int(case["N"])
        p_value, q_value = AUDIT_PAIRS[case_name]
        case_dir = args.out_dir / case_name
        public_dir = case_dir / "public"
        audit_dir = case_dir / "audit"
        run_command(
            [
                sys.executable,
                str(RUNNER),
                "--n",
                str(n_value),
                "--out-dir",
                str(public_dir),
            ],
            case_dir / "public_freeze.log",
        )
        run_command(
            [
                sys.executable,
                str(CANONICAL_AUDIT),
                "--public-output",
                str(public_dir / "public_output.jsonl"),
                "--p",
                str(p_value),
                "--q",
                str(q_value),
                "--status-out",
                str(audit_dir / "status.json"),
            ]
        )
        manifest = load_json(public_dir / "public_manifest.json")
        status = load_json(audit_dir / "status.json")
        rows.append(
            {
                "case": case_name,
                "N_bits": manifest["N_bits"],
                "active_thread_count": manifest["active_thread_count"],
                "min_depth": manifest["min_depth"],
                "max_candidates": manifest["max_candidates"],
                "emitted_count": manifest["emitted_count"],
                "original_space_size": manifest["original_space_size"],
                "candidate_reduction_bits": manifest["candidate_reduction_bits"],
                "candidate_reduction_ratio": manifest["candidate_reduction_ratio"],
                "pre_cap_qualified_count": manifest["pre_cap_qualified_count"],
                "max_observed_triangulation_depth": manifest["max_observed_triangulation_depth"],
                "cap_active": manifest["cap_active"],
                "cutoff_triangulation_depth": manifest["cutoff_triangulation_depth"],
                "pre_cap_to_emitted_ratio": manifest["pre_cap_to_emitted_ratio"],
                "status": status["status"],
                "recovered_factor": status["recovered_factor"],
            }
        )
    rows.sort(key=lambda row: (int(row["N_bits"]), str(row["case"])))
    summarize(rows, args.out_dir)
    print(json.dumps(load_json(args.out_dir / "summary.json"), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
