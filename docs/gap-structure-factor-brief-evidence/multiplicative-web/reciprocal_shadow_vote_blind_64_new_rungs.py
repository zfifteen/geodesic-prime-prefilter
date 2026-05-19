#!/usr/bin/env python3
"""Run the blind reciprocal-shadow restart on the new 56..64-bit rungs."""

from __future__ import annotations

import json
from pathlib import Path

import reciprocal_shadow_vote_blind_restart as blind


BIT_RUNGS = [56, 60, 64]
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "reciprocal_shadow_vote_blind_64_new_rungs"


def write_summary(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Reciprocal Shadow Vote Blind 64-Bit New Rungs",
        "",
        "## Contract",
        "",
        "This run tests only the new rungs above the valid 52-bit blind restart.",
        "It reuses the blind restart contract: candidate streams begin at public",
        "`floor(sqrt(N))`, scan downward in fixed public segments, score every",
        "prime candidate before audit, and use `p` or `q` only after scoring.",
        "",
        "No hidden factor is used as a candidate bound, filter, or scoring input.",
        "",
        "## Results",
        "",
        "| bits | N | hit factor | hit candidate | scored until hit | segments | coherence | rows | threads | direct audit rows |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {bits} | {N} | {hit_factor} | {hit_candidate} | "
            "{scored_candidates_until_hit} | {segments_read} | {hit_coherence:.6f} | "
            "{composite_rows} | {thread_count} | {direct_rows_containing_audit_factor} |".format(**row)
        )
    successes = sum(1 for row in rows if row["one_factor_success"])
    lines.extend(
        [
            "",
            "## Measured Surface",
            "",
            "```text",
            f"new_rungs = {len(rows)}",
            f"one_factor_success = {successes} / {len(rows)}",
            f"max_bits = {max(int(row['bits']) for row in rows)}",
            f"fixed_radius = {blind.FIXED_RADIUS}",
            "candidate_lower_bound = public scan to 2",
            "hidden_factor_candidate_bound = none",
            "```",
            "",
            "## Boundary",
            "",
            "This is a blind new-rung measurement. It still uses candidate",
            "enumeration and exact neighboring-composite factorization, so it is",
            "not a scalable resolver.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> None:
    rows = [blind.run_case(blind.build_case(bits)) for bits in BIT_RUNGS]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUTPUT_DIR / "rungs.jsonl", rows)
    write_summary(OUTPUT_DIR / "summary.md", rows)


if __name__ == "__main__":
    main()
