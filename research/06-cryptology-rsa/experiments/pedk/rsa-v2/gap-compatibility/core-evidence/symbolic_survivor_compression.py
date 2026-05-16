#!/usr/bin/env python3
"""Summarize symbolic grammar patterns in the current PEDK survivor surface."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = (
    THIS_DIR
    / "output"
    / "public_width_quantile_stability_check"
    / "stable_quantile_survivor_rows.jsonl"
)
OUTPUT_DIR = THIS_DIR / "output" / "symbolic_survivor_compression"
RULE_ID = "pedk_symbolic_survivor_compression_v1"
SOURCE_RULE_ID = "pedk_public_width_quantile_stability_check_v1"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def factor_residues(signature: str) -> tuple[tuple[str, str], tuple[str, str]]:
    """Return factor-side residue pairs from an unordered factor signature."""
    parsed: list[tuple[str, str]] = []
    for part in signature.split(" || "):
        residues = tuple(re.findall(r"[LR]=(o[246])_", part))
        if len(residues) != 2:
            raise ValueError(f"could not parse factor residues from: {part}")
        parsed.append((residues[0], residues[1]))
    if len(parsed) != 2:
        raise ValueError(f"could not parse factor signature: {signature}")
    return (parsed[0], parsed[1])


def residue_multiset(residues: tuple[tuple[str, str], tuple[str, str]]) -> str:
    """Return sorted residue multiset label."""
    return ",".join(sorted(residue for pair in residues for residue in pair))


def main() -> int:
    """Write symbolic compression artifacts."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"missing survivor rows: {INPUT_PATH}")
    rows = read_jsonl(INPUT_PATH)
    symbolic_rows: list[dict[str, object]] = []
    states_by_signature: dict[str, set[str]] = defaultdict(set)
    states_by_multiset: dict[str, set[str]] = defaultdict(set)

    for row in rows:
        state = str(row["n_containing_gap_phased_state"])
        signature = str(row["excluded_factor_neighborhood_signature"])
        residues = factor_residues(signature)
        flat = [residue for pair in residues for residue in pair]
        multiset = residue_multiset(residues)
        o6_count = flat.count("o6")
        has_all_o6_factor = any(pair == ("o6", "o6") for pair in residues)
        both_factors_touch_o6 = all("o6" in pair for pair in residues)
        all_right_residues_o6 = all(pair[1] == "o6" for pair in residues)
        is_all_o6_signature = o6_count == 4
        states_by_signature[signature].add(state)
        states_by_multiset[multiset].add(state)
        symbolic_rows.append(
            {
                "rule_id": RULE_ID,
                "source_rule_id": SOURCE_RULE_ID,
                "n_containing_gap_phased_state": state,
                "excluded_factor_neighborhood_signature": signature,
                "factor_residue_pairs": [list(pair) for pair in residues],
                "factor_residue_multiset": multiset,
                "o6_residue_count": o6_count,
                "has_all_o6_factor_neighborhood": has_all_o6_factor,
                "both_factor_neighborhoods_touch_o6": both_factors_touch_o6,
                "all_right_residues_o6": all_right_residues_o6,
                "is_all_o6_signature": is_all_o6_signature,
            }
        )

    o6_count_distribution = Counter(row["o6_residue_count"] for row in symbolic_rows)
    multiset_distribution = Counter(row["factor_residue_multiset"] for row in symbolic_rows)
    signature_phase_counts = [
        {
            "excluded_factor_neighborhood_signature": signature,
            "public_phase_state_count": len(states),
            "public_phase_states": sorted(states),
        }
        for signature, states in sorted(
            states_by_signature.items(),
            key=lambda item: (-len(item[1]), item[0]),
        )
    ]
    multiset_phase_counts = [
        {
            "factor_residue_multiset": multiset,
            "survivor_count": multiset_distribution[multiset],
            "public_phase_state_count": len(states_by_multiset[multiset]),
            "public_phase_states": sorted(states_by_multiset[multiset]),
        }
        for multiset, _count in multiset_distribution.most_common()
    ]
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "symbolic_compression_sidecar",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "survivor_count": len(rows),
        "minimum_o6_residue_count": min(o6_count_distribution),
        "all_survivors_have_at_least_two_o6_residues": all(
            int(row["o6_residue_count"]) >= 2 for row in symbolic_rows
        ),
        "has_all_o6_factor_neighborhood_count": sum(
            1 for row in symbolic_rows if row["has_all_o6_factor_neighborhood"]
        ),
        "both_factor_neighborhoods_touch_o6_count": sum(
            1 for row in symbolic_rows if row["both_factor_neighborhoods_touch_o6"]
        ),
        "all_right_residues_o6_count": sum(
            1 for row in symbolic_rows if row["all_right_residues_o6"]
        ),
        "all_o6_signature_count": sum(
            1 for row in symbolic_rows if row["is_all_o6_signature"]
        ),
        "o6_count_distribution": {
            str(count): total for count, total in sorted(o6_count_distribution.items())
        },
        "factor_residue_multiset_distribution": dict(multiset_distribution.most_common()),
        "top_signature_phase_counts": signature_phase_counts[:8],
        "multiset_phase_counts": multiset_phase_counts,
        "candidate_symbolic_rule_family": (
            "The current survivor surface is o6-heavy: every surviving excluded "
            "factor-neighborhood signature contains at least two o6 residues, "
            "and the all-o6 factor signature survives across multiple public "
            "phase states."
        ),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "symbolic_survivor_rows.jsonl", symbolic_rows)
    write_jsonl(OUTPUT_DIR / "signature_phase_count_rows.jsonl", signature_phase_counts)
    write_jsonl(OUTPUT_DIR / "multiset_phase_count_rows.jsonl", multiset_phase_counts)
    write_json(OUTPUT_DIR / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
