#!/usr/bin/env python3
"""Private scale audit for public anchor-confirmed band triangulation."""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from public_anchor_band_scale_runner import public_band_width, public_radius, public_thread_counts, score_distance, write_public_result

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_anchor_band_scale"
CAP_RATIO_SCHEDULE = (Fraction(1, 16), Fraction(1, 8), Fraction(1, 4), Fraction(1, 2), Fraction(1, 1))

CASES: tuple[dict[str, Any], ...] = (
    {"name": "baseline_41bit_1048583x1153441", "p": 1048583, "q": 1153441},
    {"name": "scale_43bit_2097287x2307191", "p": 2097287, "q": 2307191},
    {"name": "scale_45bit_4194433x4614061", "p": 4194433, "q": 4614061},
    {"name": "scale_47bit_8388733x9227791", "p": 8388733, "q": 9227791},
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_factor_hit(rows_path: Path, p_value: int, q_value: int) -> dict[str, Any] | None:
    targets = {p_value: "p", q_value: "q"}
    with gzip.open(rows_path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            which = targets.get(row["distance"])
            if which is None:
                continue
            return {
                "which": which,
                "distance": row["distance"],
                "band": row["band"],
                "band_rank": row["band_rank"],
                "score": row["score"],
                "shared_thread_count": row["shared_thread_count"],
                "union_thread_count": row["union_thread_count"],
            }
    return None


def target_band_rank(n_value: int, distance: int) -> dict[str, Any]:
    radius = public_radius(n_value)
    band_width = public_band_width(radius)
    counts = public_thread_counts(n_value, radius)
    band = (distance - 1) // band_width
    low = band * band_width + 1
    high = min(radius, (band + 1) * band_width)
    target_score = tuple(score_distance(n_value, distance, counts)["score"])
    better_count = 0
    for current in range(low, high + 1):
        if tuple(score_distance(n_value, current, counts)["score"]) > target_score:
            better_count += 1
    return {
        "distance": distance,
        "band": band,
        "band_width": band_width,
        "band_rank": better_count + 1,
        "score": list(target_score),
    }


def audit_case(case: dict[str, Any]) -> dict[str, Any]:
    n_value = case["p"] * case["q"]
    attempts = []
    public = None
    hit = None
    for cap_ratio in CAP_RATIO_SCHEDULE:
        cap_label = f"{cap_ratio.numerator}_over_{cap_ratio.denominator}"
        case_dir = OUT_ROOT / "public_frozen" / case["name"] / f"cap_ratio_{cap_label}"
        write_public_result(n_value, case_dir, cap_ratio)
        public = read_json(case_dir / "public_manifest.json")
        attempt_hit = find_factor_hit(case_dir / "public_band_rows.jsonl.gz", case["p"], case["q"])
        attempts.append({
            "cap_ratio": f"{cap_ratio.numerator}/{cap_ratio.denominator}",
            "top_per_band": public["top_per_band"],
            "hit": attempt_hit,
            "public_cost": public["public_cost"],
            "selected_band_rows": public["selected_band_rows"],
        })
        if attempt_hit:
            hit = attempt_hit
            break
    assert public is not None
    covered = public["radius"] >= min(case["p"], case["q"])
    if hit:
        classification = "one_factor_in_public_band_rows"
    elif covered:
        classification = "covered_but_not_in_public_band_rows"
    else:
        classification = "public_window_insufficient_coverage"
    return {
        "name": case["name"],
        "N": n_value,
        "N_bits": n_value.bit_length(),
        "p": case["p"],
        "q": case["q"],
        "radius": public["radius"],
        "covered": covered,
        "classification": classification,
        "hit": hit,
        "cap_ratio_schedule": [f"{ratio.numerator}/{ratio.denominator}" for ratio in CAP_RATIO_SCHEDULE],
        "attempts": attempts,
        "first_success_top_per_band": attempts[-1]["top_per_band"] if hit else None,
        "first_success_cap_ratio": attempts[-1]["cap_ratio"] if hit else None,
        "posthoc_target_band_ranks": {
            "p": target_band_rank(n_value, case["p"]),
            "q": target_band_rank(n_value, case["q"]),
        },
        "public_cost": public["public_cost"],
        "selected_band_rows": public["selected_band_rows"],
    }


def write_summary(records: list[dict[str, Any]]) -> None:
    success_count = sum(1 for record in records if record["classification"] == "one_factor_in_public_band_rows")
    summary = {
        "status": "success" if success_count == len(records) else "boundary_or_failure",
        "success_count": success_count,
        "case_count": len(records),
        "cases": records,
    }
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Anchor-Confirmed Band Scale Audit",
        "",
        f"Status: `{summary['status']}`",
        "",
        "| case | bits | radius | cap ratio | cap | classification | hit | band rank | p rank | q rank | seconds |",
        "| --- | ---: | ---: | --- | ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        hit = record["hit"]
        if hit:
            hit_label = f"{hit['which']}={hit['distance']}"
            band_rank = str(hit["band_rank"])
        else:
            hit_label = "-"
            band_rank = "-"
        p_rank = record["posthoc_target_band_ranks"]["p"]["band_rank"]
        q_rank = record["posthoc_target_band_ranks"]["q"]["band_rank"]
        seconds = sum(attempt["public_cost"]["elapsed_seconds"] for attempt in record["attempts"])
        first_cap = record["first_success_top_per_band"] or "-"
        first_ratio = record["first_success_cap_ratio"] or "-"
        lines.append(
            f"| {record['name']} | {record['N_bits']} | {record['radius']} | "
            f"{first_ratio} | {first_cap} | {record['classification']} | {hit_label} | {band_rank} | "
            f"{p_rank} | {q_rank} | {seconds:.6f} |"
        )
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    records = []
    for case in CASES:
        record = audit_case(case)
        records.append(record)
        print(f"{record['name']}: {record['classification']} hit={record['hit']}")
    write_summary(records)
    print(f"summary={OUT_ROOT / 'summary.md'}")


if __name__ == "__main__":
    main()
