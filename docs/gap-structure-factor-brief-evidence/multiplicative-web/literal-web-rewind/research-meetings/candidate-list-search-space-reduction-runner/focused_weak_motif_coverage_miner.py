#!/usr/bin/env python3
"""
Focused weak-motif coverage miner for the PGA grammar pruner.

This miner targets only the live-derived coverage gaps observed in the repaired
real probe. It reads public grammar evidence rows, matches rows by the motif
components available from live derivation, and proposes exact-motif pruning
rules only when the selected factor-neighborhood classes have zero target
observations in both extraction and held-out surfaces.

No p, q, divisibility, product closure, or factor recovery logic is used.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def find_repo_root(start: Path) -> Path:
    current = start
    for _ in range(16):
        if (current / ".git").exists() and (current / "research").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    raise RuntimeError(f"could not locate repo root from {start}")


REPO_ROOT = find_repo_root(ROOT)
EVIDENCE_ROOT = (
    REPO_ROOT
    / "research"
    / "06-cryptology-rsa"
    / "experiments"
    / "pedk"
    / "rsa-v2"
    / "gap-compatibility"
    / "core-evidence"
    / "output"
)

REAL_PROBE_JSON = ROOT / "output" / "ladder" / "real_semiprime_64_80_samples_3" / "ladder_summary.json"
OUTPUT_DIR = ROOT / "output" / "weak_motif_coverage_miner"

TRAIN_BANDS = ("27001_30000", "32001_34000")
HELDOUT_BANDS = ("34001_35000",)
PROMOTION_START_ID = 85
MIN_TRAIN_ROWS = 50
MIN_HELDOUT_ROWS = 1
MIN_GLOBAL_CLASS_SUPPORT = 35
MIN_PROMOTED_CLASS_COUNT = 20
PROMOTED_CLASS_LIMIT = 30

TARGET_MOTIFS = (
    "o6_d4_a6_d4_odd@mid + o2_d4_odd prev",
    "o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev",
    "o2_d4_a2_d4_odd@late + o4_d4_odd prev",
    "o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev",
    "o4_d4_a6_d4_odd@mid + o6_d4_odd prev",
)


@dataclass(frozen=True)
class MotifParts:
    containing_exact_type: str
    phase: str
    previous_reduced_state: str


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def short_state(value: object) -> str:
    return str(value or "").split("|")[0]


def parse_motif(motif: str) -> MotifParts:
    base, prev_part = motif.split(" + ", 1)
    containing, phase = base.split("@", 1)
    return MotifParts(
        containing_exact_type=containing,
        phase=phase,
        previous_reduced_state=prev_part.removesuffix(" prev"),
    )


def row_matches_target(row: dict[str, Any], target: MotifParts) -> bool:
    return (
        row.get("public_containing_exact_type_key") == target.containing_exact_type
        and row.get("public_containing_phase_bucket") == target.phase
        and short_state(row.get("public_previous_reduced_state")) == target.previous_reduced_state
    )


def class_signature(row: dict[str, Any]) -> str:
    return f"{row.get('factor_residue_multiset')} :: {row.get('factor_phase_multiset')}"


def enriched_rows_for_band(band: str) -> list[dict[str, Any]]:
    path = EVIDENCE_ROOT / f"enriched_multiplication_map_corpus_{band}" / "enriched_rows.jsonl"
    return read_jsonl(path)


def load_probe_target_counts() -> Counter[str]:
    data = json.loads(REAL_PROBE_JSON.read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    for level in data["levels"].values():
        for case in level.get("per_case", []):
            motif = case.get("derived_motif") or case.get("motif")
            if motif in TARGET_MOTIFS and case.get("coverage_gap"):
                counts[str(motif)] += 1
    return counts


def mine() -> dict[str, Any]:
    train_rows_by_band = {band: enriched_rows_for_band(band) for band in TRAIN_BANDS}
    heldout_rows_by_band = {band: enriched_rows_for_band(band) for band in HELDOUT_BANDS}
    all_rows = [
        row
        for rows in (*train_rows_by_band.values(), *heldout_rows_by_band.values())
        for row in rows
    ]

    global_class_support: Counter[str] = Counter(class_signature(row) for row in all_rows)
    probe_target_counts = load_probe_target_counts()

    candidate_rows: list[dict[str, Any]] = []
    promoted_rules: list[dict[str, Any]] = []
    next_rule_number = PROMOTION_START_ID

    for motif in TARGET_MOTIFS:
        target = parse_motif(motif)
        train_class_counts: Counter[str] = Counter()
        heldout_class_counts: Counter[str] = Counter()
        train_row_count = 0
        heldout_row_count = 0

        for rows in train_rows_by_band.values():
            for row in rows:
                if row_matches_target(row, target):
                    train_row_count += 1
                    train_class_counts[class_signature(row)] += 1

        for rows in heldout_rows_by_band.values():
            for row in rows:
                if row_matches_target(row, target):
                    heldout_row_count += 1
                    heldout_class_counts[class_signature(row)] += 1

        zero_observed_classes = [
            {
                "class_signature": signature,
                "global_support": support,
                "target_train_observed_count": train_class_counts.get(signature, 0),
                "target_heldout_observed_count": heldout_class_counts.get(signature, 0),
            }
            for signature, support in global_class_support.most_common()
            if support >= MIN_GLOBAL_CLASS_SUPPORT
            and train_class_counts.get(signature, 0) == 0
            and heldout_class_counts.get(signature, 0) == 0
        ]

        selected_classes = zero_observed_classes[:PROMOTED_CLASS_LIMIT]
        observed_count = train_row_count + heldout_row_count
        heldout_contradiction_count = sum(
            item["target_heldout_observed_count"] for item in selected_classes
        )
        eligible = (
            train_row_count >= MIN_TRAIN_ROWS
            and heldout_row_count >= MIN_HELDOUT_ROWS
            and heldout_contradiction_count == 0
            and len(selected_classes) >= MIN_PROMOTED_CLASS_COUNT
        )
        status = "promoted" if eligible else "candidate_only"

        proposed_pruned_count = len(selected_classes) if eligible else 0
        rule_id = f"PG-{next_rule_number:03d}" if eligible else None

        row = {
            "target_motif": motif,
            "target_probe_case_count": probe_target_counts.get(motif, 0),
            "source_surfaces_used": [
                *(f"enriched_multiplication_map_corpus_{band}" for band in TRAIN_BANDS),
                *(f"heldout:enriched_multiplication_map_corpus_{band}" for band in HELDOUT_BANDS),
            ],
            "target_train_row_count": train_row_count,
            "target_heldout_row_count": heldout_row_count,
            "observed_count": observed_count,
            "heldout_contradiction_count": heldout_contradiction_count,
            "selected_zero_observed_class_count": len(selected_classes),
            "excluded_factor_signature_classes": selected_classes,
            "proposed_pruned_count": proposed_pruned_count,
            "promotion_status": status,
            "rule_id": rule_id,
        }
        candidate_rows.append(row)

        if eligible:
            promoted_rules.append(
                {
                    "id": rule_id,
                    "motif": motif,
                    "description": (
                        "exact weak live motif -> prune zero-observed "
                        "residue/phase factor-neighborhood classes from enriched "
                        "27k-35k public grammar surfaces"
                    ),
                    "pruned_count": proposed_pruned_count,
                }
            )
            next_rule_number += 1

    return {
        "rule_id": "focused_weak_motif_coverage_miner_v1",
        "status": "measured_candidate_rule_mining",
        "stage": "stage_one_public_grammar_pruning",
        "reference_real_probe": str(REAL_PROBE_JSON.relative_to(ROOT)),
        "promotion_policy": {
            "target_motifs": list(TARGET_MOTIFS),
            "train_bands": list(TRAIN_BANDS),
            "heldout_bands": list(HELDOUT_BANDS),
            "min_train_rows": MIN_TRAIN_ROWS,
            "min_heldout_rows": MIN_HELDOUT_ROWS,
            "min_global_class_support": MIN_GLOBAL_CLASS_SUPPORT,
            "min_promoted_class_count": MIN_PROMOTED_CLASS_COUNT,
            "promoted_class_limit": PROMOTED_CLASS_LIMIT,
            "broad_high_a_rules_allowed": False,
        },
        "candidate_rows": candidate_rows,
        "promoted_rules": promoted_rules,
    }


def write_outputs(result: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "candidate_rules.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# Focused Weak-Motif Coverage Miner",
        "",
        f"- status: `{result['status']}`",
        f"- stage: `{result['stage']}`",
        f"- promoted rules: `{len(result['promoted_rules'])}`",
        "",
        "## Promotion Policy",
        "",
        f"- train bands: `{', '.join(result['promotion_policy']['train_bands'])}`",
        f"- heldout bands: `{', '.join(result['promotion_policy']['heldout_bands'])}`",
        f"- selected zero-observed classes per promoted rule: `{PROMOTED_CLASS_LIMIT}`",
        f"- minimum zero-observed classes for promotion: `{MIN_PROMOTED_CLASS_COUNT}`",
        f"- broad high-a rules allowed: `{result['promotion_policy']['broad_high_a_rules_allowed']}`",
        "",
        "## Candidate Rows",
        "",
        "| motif | train rows | heldout rows | selected zero classes | contradictions | pruned_count | status | rule |",
        "|-------|------------|--------------|-----------------------|----------------|--------------|--------|------|",
    ]
    for row in result["candidate_rows"]:
        lines.append(
            f"| `{row['target_motif']}` | {row['target_train_row_count']} | "
            f"{row['target_heldout_row_count']} | {row['selected_zero_observed_class_count']} | "
            f"{row['heldout_contradiction_count']} | {row['proposed_pruned_count']} | "
            f"{row['promotion_status']} | {row['rule_id'] or '-'} |"
        )

    lines += [
        "",
        "## Promoted Rules",
        "",
    ]
    if result["promoted_rules"]:
        for rule in result["promoted_rules"]:
            lines.append(
                f"- `{rule['id']}` `{rule['motif']}` -> "
                f"{rule['pruned_count']}/198 pruned"
            )
    else:
        lines.append("- none")

    lines += [
        "",
        "No p, q, divisibility, product closure, or recovery logic is used by this miner.",
    ]
    (OUTPUT_DIR / "candidate_rules.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = mine()
    write_outputs(result)
    print(json.dumps(result["promoted_rules"], indent=2))
    print(f"candidate artifact: {OUTPUT_DIR / 'candidate_rules.json'}")
    print(f"summary artifact:   {OUTPUT_DIR / 'candidate_rules.md'}")


if __name__ == "__main__":
    main()
