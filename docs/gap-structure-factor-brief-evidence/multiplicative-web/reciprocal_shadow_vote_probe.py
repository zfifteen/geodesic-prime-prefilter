#!/usr/bin/env python3
"""Test whether non-direct composite threads rank hidden factors."""

from __future__ import annotations

import json
import math
from pathlib import Path

from plot_multiplicative_web import composite_rows, is_prime


FIXED_RADIUS = 300


CASES = [
    {"p": 23, "q": 31},
    {"p": 43, "q": 59},
    {"p": 61, "q": 83},
    {"p": 89, "q": 113},
    {"p": 101, "q": 137},
    {"p": 131, "q": 167},
    {"p": 173, "q": 211},
    {"p": 229, "q": 277},
    {"p": 307, "q": 367},
    {"p": 401, "q": 503},
    {"p": 557, "q": 661},
    {"p": 701, "q": 887},
    {"p": 1009, "q": 1231},
    {"p": 1601, "q": 2003},
    {"p": 3001, "q": 4001},
    {"p": 5003, "q": 7001},
]


OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "reciprocal_shadow_vote_probe"


def reciprocal_shadow_score(n_value: int, candidate: int, rows: list[dict[str, object]]) -> dict[str, object]:
    """Score a lower-endpoint candidate from non-direct composite threads."""
    partner_estimate = round(n_value / candidate)
    votes = 0
    hits = 0
    skipped = 0
    hit_factors: dict[int, int] = {}

    for row in rows:
        offset = int(row["offset"])
        for factor in row["factors"]:
            r = int(factor)
            if math.gcd(candidate, r) != 1:
                skipped += 1
                continue
            implied_partner_residue = ((-offset) * pow(candidate % r, -1, r)) % r
            votes += 1
            if partner_estimate % r == implied_partner_residue:
                hits += 1
                hit_factors[r] = hit_factors.get(r, 0) + 1

    return {
        "candidate": candidate,
        "partner_estimate": partner_estimate,
        "votes": votes,
        "hits": hits,
        "skipped": skipped,
        "coherence": 0.0 if votes == 0 else hits / votes,
        "hit_factor_count": len(hit_factors),
        "hit_factors": sorted(hit_factors),
    }


def candidate_rows_for_case(p_value: int, q_value: int, radius: int) -> dict[str, object]:
    n_value = p_value * q_value
    rows = composite_rows(n_value, radius)
    heldout_rows = [
        row
        for row in rows
        if p_value not in row["factors"] and q_value not in row["factors"]
    ]
    direct_rows_removed = len(rows) - len(heldout_rows)
    scores = []
    for candidate in range(2, math.isqrt(n_value) + 1):
        if not is_prime(candidate):
            continue
        score = reciprocal_shadow_score(n_value, candidate, heldout_rows)
        score.update(
            {
                "N": n_value,
                "p": p_value,
                "q": q_value,
                "radius": radius,
                "is_audit_p": candidate == p_value,
                "is_audit_q": candidate == q_value,
                "is_audit_factor": candidate in {p_value, q_value},
            }
        )
        scores.append(score)

    scores.sort(
        key=lambda row: (
            -float(row["coherence"]),
            -int(row["hits"]),
            abs(int(row["candidate"]) - math.isqrt(n_value)),
            int(row["candidate"]),
        )
    )
    for rank, row in enumerate(scores, start=1):
        row["rank"] = rank

    p_rank = next(row["rank"] for row in scores if row["candidate"] == p_value)
    p_score = next(row for row in scores if row["candidate"] == p_value)
    rotated_rows = rotated_offset_control_rows(heldout_rows)
    control_scores = []
    for candidate in range(2, math.isqrt(n_value) + 1):
        if not is_prime(candidate):
            continue
        score = reciprocal_shadow_score(n_value, candidate, rotated_rows)
        score.update(
            {
                "N": n_value,
                "p": p_value,
                "q": q_value,
                "radius": radius,
                "is_audit_p": candidate == p_value,
                "is_audit_q": candidate == q_value,
                "is_audit_factor": candidate in {p_value, q_value},
            }
        )
        control_scores.append(score)
    control_scores.sort(
        key=lambda row: (
            -float(row["coherence"]),
            -int(row["hits"]),
            abs(int(row["candidate"]) - math.isqrt(n_value)),
            int(row["candidate"]),
        )
    )
    for rank, row in enumerate(control_scores, start=1):
        row["rank"] = rank
    p_control_rank = next(row["rank"] for row in control_scores if row["candidate"] == p_value)
    p_control_score = next(row for row in control_scores if row["candidate"] == p_value)
    return {
        "N": n_value,
        "p": p_value,
        "q": q_value,
        "radius": radius,
        "composite_rows": len(rows),
        "heldout_rows": len(heldout_rows),
        "direct_rows_removed": direct_rows_removed,
        "candidate_count": len(scores),
        "p_rank": p_rank,
        "p_coherence": p_score["coherence"],
        "p_hits": p_score["hits"],
        "p_votes": p_score["votes"],
        "rotated_control_p_rank": p_control_rank,
        "rotated_control_p_coherence": p_control_score["coherence"],
        "rotated_control_p_hits": p_control_score["hits"],
        "rotated_control_p_votes": p_control_score["votes"],
        "top_candidates": scores[:10],
        "rotated_control_top_candidates": control_scores[:10],
        "all_scores": scores,
        "all_rotated_control_scores": control_scores,
    }


def rotated_offset_control_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Break the true offset-to-factor pairing while preserving factor rows."""
    if not rows:
        return []
    offsets = [int(row["offset"]) for row in rows]
    rotated_offsets = offsets[1:] + offsets[:1]
    out = []
    for row, offset in zip(rows, rotated_offsets, strict=True):
        copied = dict(row)
        copied["offset"] = offset
        out.append(copied)
    return out


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_summary_md(path: Path, case_summaries: list[dict[str, object]]) -> None:
    lines = [
        "# Reciprocal Shadow Vote Probe",
        "",
        "## Contract",
        "",
        "The probe removes every nearby composite row whose factorization contains",
        "the audit factors `p` or `q`. It then scores prime lower-endpoint candidates",
        "using only reciprocal residue shadows cast by the remaining composite",
        "factor threads.",
        "",
        "A run succeeds when it identifies either hidden factor. In these",
        "semiprime cases `p < q`, so the scored lower-endpoint surface tests",
        "one-factor success by asking whether `p` ranks first.",
        "",
        "The score does not call `N % candidate`, does not multiply a candidate pair",
        "as an acceptance test, and does not use the removed direct factor rows.",
        "",
        "## Results",
        "",
        "| N | p | q | radius | heldout rows | direct rows removed | candidates | p rank | p coherence | rotated-control p rank | rotated-control p coherence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for summary in case_summaries:
        lines.append(
            "| {N} | {p} | {q} | {radius} | {heldout_rows} | "
            "{direct_rows_removed} | {candidate_count} | {p_rank} | "
            "{p_coherence:.6f} | {rotated_control_p_rank} | "
            "{rotated_control_p_coherence:.6f} |".format(
                **summary
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a fixed-window scale test of the indirect-web hypothesis.",
            "It shows whether non-direct neighboring composites create a",
            "reciprocal residue field that ranks one hidden factor. It is not a",
            "proof and not a live factor resolver.",
            "",
            "The rotated-control columns keep the same factor rows but rotate offsets",
            "between rows. They test whether the signal depends on the true local",
            "offset-to-factor pairing rather than on the marginal factor multiset.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    case_summaries = []
    all_score_rows = []
    for case in CASES:
        result = candidate_rows_for_case(case["p"], case["q"], FIXED_RADIUS)
        summary = {
            key: value
            for key, value in result.items()
            if key not in {"all_scores", "all_rotated_control_scores"}
        }
        case_summaries.append(summary)
        for row in result["all_scores"]:
            row["surface"] = "true_offset_factor_pairing"
            all_score_rows.append(row)
        for row in result["all_rotated_control_scores"]:
            row["surface"] = "rotated_offset_control"
            all_score_rows.append(row)

    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(case_summaries, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUTPUT_DIR / "candidate_scores.jsonl", all_score_rows)
    write_summary_md(OUTPUT_DIR / "summary.md", case_summaries)


if __name__ == "__main__":
    main()
