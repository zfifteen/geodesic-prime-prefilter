#!/usr/bin/env python3
"""Prefix-state L_FCL decisive probe (H_CTC experiment, rev 1)."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_PYTHON = ROOT / "src" / "python"
EXPERIMENT_DIR = Path(__file__).resolve().parent
if str(SRC_PYTHON) not in sys.path:
    sys.path.insert(0, str(SRC_PYTHON))
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

from closure_laws import LAW_IDS, ClosureFire, first_fire_for_law, scan_all_laws  # noqa: E402
from prefix_state import PrefixStateTracker  # noqa: E402
from semantic_audit import static_audit  # noqa: E402

MIN_PRIME = 11
REGIME_LIMITS = {
    "R1": 1_000_000,
    "R2": 1_000_000,
}


def build_tau_table(limit: int) -> list[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            tau[m] += 1
    return tau


def sieve_primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start : limit + 1 : step] = b"\x00" * (
                ((limit - start) // step) + 1
            )
    return [i for i in range(2, limit + 1) if is_prime[i]]


def q_ref_from_tau(p: int, q_true: int, tau: list[int]) -> int:
    for n in range(p + 1, q_true + 1):
        if tau[n] == 2:
            return n
    return q_true


def prefix_bounds_for_gap(gap: int, *, full: bool) -> list[int]:
    if gap < 2:
        return []
    if full or gap <= 256:
        return list(range(1, gap))
    bounds = {1, gap - 1}
    bounds.update(range(4, gap, 4))
    return sorted(bounds)


def d1_metrics(p: int, tau: list[int], gap: int, prefix_bounds: list[int]) -> dict[str, int | None]:
    tracker = PrefixStateTracker(p, tau)
    max_u = 0
    first_eq_1: int | None = None
    first_gt_1: int | None = None
    for bound in prefix_bounds:
        u = tracker.admissible_count(bound)
        if u > max_u:
            max_u = u
        if u == 1 and first_eq_1 is None:
            first_eq_1 = bound
        if u > 1 and first_gt_1 is None:
            first_gt_1 = bound
    return {
        "max_U_before_gap": max_u,
        "first_B_U_eq_1": first_eq_1,
        "first_B_U_gt_1": first_gt_1,
    }


def law_row_fields(
    p: int,
    gap: int,
    q_ref: int,
    fire: ClosureFire | None,
) -> dict[str, object]:
    if fire is None:
        return {
            "B_declare": None,
            "r_declare": None,
            "early_fire": False,
            "match_ref": None,
            "mismatch": False,
        }
    early = fire.B_declare < gap
    match_ref = fire.r_declare == q_ref
    mismatch = not match_ref
    return {
        "B_declare": fire.B_declare,
        "r_declare": fire.r_declare,
        "early_fire": early,
        "match_ref": match_ref if early else None,
        "mismatch": mismatch,
    }


def run_regime(regime: str, output_dir: Path) -> dict[str, object]:
    limit = REGIME_LIMITS[regime]
    tau = build_tau_table(limit + 1)
    primes = sieve_primes(limit)

    audit = static_audit(
        [
            EXPERIMENT_DIR / "closure_laws.py",
            EXPERIMENT_DIR / "prefix_state.py",
        ]
    )

    rows: list[dict[str, object]] = []
    early_fires: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []

    law_counters = {
        law_id: {
            "fire_count": 0,
            "early_fire_count": 0,
            "mismatch_count": 0,
            "early_match_count": 0,
        }
        for law_id in LAW_IDS
    }

    counters = {
        "gaps_total": 0,
        "any_law_mismatch_count": 0,
        "substantive_mismatch_count": 0,
        "any_law_early_support_count": 0,
        "l0_match_count": 0,
        "full_rescan_count": 0,
        "max_U_histogram": {str(i): 0 for i in range(0, 17)},
    }

    started = time.time()
    for index in range(len(primes) - 1):
        p = primes[index]
        q_true = primes[index + 1]
        if p < MIN_PRIME:
            continue

        gap = q_true - p
        counters["gaps_total"] += 1
        q_reference = q_ref_from_tau(p, q_true, tau)

        scan_end = gap - 1 if regime == "R2" else min(gap - 1, 128)
        if scan_end < 1:
            prefix_bounds = []
        else:
            prefix_bounds = prefix_bounds_for_gap(gap, full=False)
            if regime == "R1":
                prefix_bounds = [b for b in prefix_bounds if b <= 128]

        fires = scan_all_laws(p, tau, prefix_bounds) if prefix_bounds else {
            law_id: None for law_id in LAW_IDS
        }

        confirmed: dict[str, ClosureFire | None] = dict(fires)
        needs_full = False
        for law_id, fire in fires.items():
            if fire is None:
                continue
            if fire.r_declare != q_reference:
                needs_full = True
                break

        if needs_full and gap > 256:
            counters["full_rescan_count"] += 1
            full_bounds = prefix_bounds_for_gap(gap, full=True)
            if regime == "R1":
                full_bounds = [b for b in full_bounds if b <= 128]
            confirmed = scan_all_laws(p, tau, full_bounds)

        d1 = (
            d1_metrics(p, tau, gap, prefix_bounds)
            if prefix_bounds
            else {
                "max_U_before_gap": 0,
                "first_B_U_eq_1": None,
                "first_B_U_gt_1": None,
            }
        )
        max_u = int(d1["max_U_before_gap"])
        bucket = str(min(max_u, 16))
        counters["max_U_histogram"][bucket] = counters["max_U_histogram"].get(bucket, 0) + 1

        row: dict[str, object] = {
            "p": p,
            "q_ref": q_reference,
            "gap": gap,
            **d1,
        }

        gap_mismatch = False
        gap_substantive_mismatch = False
        gap_early_support = False
        for law_id in LAW_IDS:
            fire = confirmed[law_id]
            fields = law_row_fields(p, gap, q_reference, fire)
            for key, value in fields.items():
                row[f"{law_id}_{key}"] = value

            if fire is not None:
                law_counters[law_id]["fire_count"] += 1
            if fields["early_fire"]:
                law_counters[law_id]["early_fire_count"] += 1
                early_fires.append(
                    {
                        "p": p,
                        "law_id": law_id,
                        "B_declare": fields["B_declare"],
                        "r_declare": fields["r_declare"],
                        "q_ref": q_reference,
                        "gap": gap,
                        "match_ref": fields["match_ref"],
                    }
                )
            if fields["mismatch"]:
                law_counters[law_id]["mismatch_count"] += 1
                gap_mismatch = True
                if law_id != "L0":
                    gap_substantive_mismatch = True
                    mismatches.append(
                        {
                            "p": p,
                            "law_id": law_id,
                            "B_declare": fields["B_declare"],
                            "r_declare": fields["r_declare"],
                            "q_ref": q_reference,
                            "gap": gap,
                        }
                    )
            if fields["early_fire"] and fields["match_ref"]:
                law_counters[law_id]["early_match_count"] += 1
                gap_early_support = True
            if law_id == "L0" and fire is not None and fire.r_declare == q_reference:
                counters["l0_match_count"] += 1

        if gap_mismatch:
            counters["any_law_mismatch_count"] += 1
        if gap_substantive_mismatch:
            counters["substantive_mismatch_count"] += 1
        if gap_early_support:
            counters["any_law_early_support_count"] += 1

        row["gwr_offset"] = None
        row["threat_offset"] = None
        if prefix_bounds:
            tracker = PrefixStateTracker(p, tau)
            snap = tracker.advance_to(prefix_bounds[-1])
            row["gwr_offset"] = snap.gwr_offset
            row["threat_offset"] = snap.threat_offset

        rows.append(row)

    elapsed = time.time() - started
    total = counters["gaps_total"] or 1

    law_reports: dict[str, dict[str, object]] = {}
    for law_id in LAW_IDS:
        lc = law_counters[law_id]
        early = lc["early_fire_count"]
        law_reports[law_id] = {
            **lc,
            "early_match_rate": (
                lc["early_match_count"] / early if early else None
            ),
            "falsified_as_predictor": lc["early_fire_count"] == 0,
        }

    summary = {
        "regime": regime,
        "prime_limit": limit,
        "min_prime": MIN_PRIME,
        "elapsed_seconds": round(elapsed, 3),
        **counters,
        **audit,
        "l0_match_rate": counters["l0_match_count"] / total,
        "law_reports": law_reports,
        "first_mismatch_row": mismatches[0] if mismatches else None,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "law_reports.json").write_text(
        json.dumps(law_reports, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if rows:
        fieldnames = list(rows[0].keys())
        with (output_dir / "gaps.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    if early_fires:
        fieldnames = list(early_fires[0].keys())
        with (output_dir / "early_fires.csv").open(
            "w", newline="", encoding="utf-8"
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(early_fires)

    if mismatches:
        fieldnames = list(mismatches[0].keys())
        with (output_dir / "mismatches.csv").open(
            "w", newline="", encoding="utf-8"
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mismatches)

    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regime", choices=sorted(REGIME_LIMITS), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    summary = run_regime(args.regime, args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["semantic_audit_pass"]:
        print("HALT: semantic audit failed", file=sys.stderr)
        return 2
    if summary["l0_match_count"]:
        print("HALT: L0 negative control matched q_ref", file=sys.stderr)
        return 3
    if summary["substantive_mismatch_count"]:
        print("FALSIFIED: substantive law mismatch detected", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())