#!/usr/bin/env python3
"""Check phase-exclusion preservation under deterministic held-out factor bands."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = THIS_DIR / "output" / "gap_compatibility_search" / "corpus_rows.jsonl"
OUTPUT_DIR = THIS_DIR / "output" / "heldout_phase_exclusion_check"
RULE_ID = "pedk_phase_exclusion_heldout_check_v1"
SOURCE_RULE_ID = "pedk_phase_gap_exclusion_candidate_v1"
MIN_SUPPORT = 50
Q_CEILINGS = (360, 400, 420, 450, 480, 500)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def phase_state(row: dict[str, object]) -> str:
    """Return the public phase state used by the candidate rule."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return the downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


def train_exclusions(
    train_rows: list[dict[str, object]],
) -> tuple[set[tuple[str, str]], Counter[str], dict[str, set[str]], set[str]]:
    """Return candidate exclusions learned from the training band."""
    state_counts = Counter(phase_state(row) for row in train_rows)
    observed_by_state: dict[str, set[str]] = defaultdict(set)
    all_signatures = {factor_signature(row) for row in train_rows}
    for row in train_rows:
        observed_by_state[phase_state(row)].add(factor_signature(row))

    exclusions: set[tuple[str, str]] = set()
    for state, support in state_counts.items():
        if support < MIN_SUPPORT:
            continue
        for signature in all_signatures - observed_by_state[state]:
            exclusions.add((state, signature))
    return exclusions, state_counts, observed_by_state, all_signatures


def split_check(rows: list[dict[str, object]], q_ceiling: int) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    """Return summary, surviving exclusions, and falsified exclusions for one split."""
    train_rows = [row for row in rows if int(str(row["q"])) <= q_ceiling]
    holdout_rows = [row for row in rows if int(str(row["q"])) > q_ceiling]
    exclusions, state_counts, observed_by_state, all_signatures = train_exclusions(train_rows)
    holdout_pairs = {(phase_state(row), factor_signature(row)) for row in holdout_rows}
    falsified_pairs = exclusions & holdout_pairs
    surviving_pairs = exclusions - falsified_pairs

    holdout_rows_by_pair: Counter[tuple[str, str]] = Counter(
        (phase_state(row), factor_signature(row)) for row in holdout_rows
    )
    holdout_rows_by_state: Counter[str] = Counter(phase_state(row) for row in holdout_rows)

    surviving_rows = [
        {
            "rule_id": RULE_ID,
            "q_ceiling": q_ceiling,
            "candidate_status": "survived_this_heldout_split",
            "n_containing_gap_phased_state": state,
            "excluded_factor_neighborhood_signature": signature,
            "train_state_support": state_counts[state],
            "train_observed_signature_count_for_state": len(observed_by_state[state]),
            "train_global_signature_count": len(all_signatures),
            "holdout_state_support": holdout_rows_by_state[state],
        }
        for state, signature in sorted(surviving_pairs)
    ]
    falsified_rows = [
        {
            "rule_id": RULE_ID,
            "q_ceiling": q_ceiling,
            "candidate_status": "falsified_by_heldout_row",
            "n_containing_gap_phased_state": state,
            "excluded_factor_neighborhood_signature": signature,
            "train_state_support": state_counts[state],
            "train_observed_signature_count_for_state": len(observed_by_state[state]),
            "train_global_signature_count": len(all_signatures),
            "holdout_state_support": holdout_rows_by_state[state],
            "falsifying_holdout_row_count": holdout_rows_by_pair[(state, signature)],
        }
        for state, signature in sorted(falsified_pairs)
    ]
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "split_id": f"q_le_{q_ceiling}_vs_q_gt_{q_ceiling}",
        "q_ceiling": q_ceiling,
        "min_support": MIN_SUPPORT,
        "train_row_count": len(train_rows),
        "holdout_row_count": len(holdout_rows),
        "train_global_signature_count": len(all_signatures),
        "train_supported_phase_state_count": sum(
            1 for support in state_counts.values() if support >= MIN_SUPPORT
        ),
        "train_candidate_exclusion_count": len(exclusions),
        "falsified_exclusion_count": len(falsified_pairs),
        "surviving_exclusion_count": len(surviving_pairs),
        "falsifying_holdout_row_count": sum(holdout_rows_by_pair[pair] for pair in falsified_pairs),
    }
    return summary, surviving_rows, falsified_rows


def main() -> int:
    """Run the held-out phase-exclusion check."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"missing required corpus: {INPUT_PATH}")
    rows = read_jsonl(INPUT_PATH)
    split_summaries: list[dict[str, object]] = []
    surviving_rows: list[dict[str, object]] = []
    falsified_rows: list[dict[str, object]] = []

    for q_ceiling in Q_CEILINGS:
        summary, split_survivors, split_falsified = split_check(rows, q_ceiling)
        split_summaries.append(summary)
        surviving_rows.extend(split_survivors)
        falsified_rows.extend(split_falsified)

    trained_splits: dict[tuple[str, str], set[int]] = defaultdict(set)
    survived_splits: dict[tuple[str, str], set[int]] = defaultdict(set)
    falsified_splits: dict[tuple[str, str], set[int]] = defaultdict(set)
    for row in surviving_rows:
        key = (
            str(row["n_containing_gap_phased_state"]),
            str(row["excluded_factor_neighborhood_signature"]),
        )
        q_ceiling = int(str(row["q_ceiling"]))
        trained_splits[key].add(q_ceiling)
        survived_splits[key].add(q_ceiling)
    for row in falsified_rows:
        key = (
            str(row["n_containing_gap_phased_state"]),
            str(row["excluded_factor_neighborhood_signature"]),
        )
        q_ceiling = int(str(row["q_ceiling"]))
        trained_splits[key].add(q_ceiling)
        falsified_splits[key].add(q_ceiling)

    all_split_keys = set(Q_CEILINGS)
    stable_survivors = [
        {
            "rule_id": RULE_ID,
            "candidate_status": "survived_all_deterministic_heldout_splits",
            "n_containing_gap_phased_state": state,
            "excluded_factor_neighborhood_signature": signature,
            "survived_q_ceilings": sorted(survived_splits[(state, signature)]),
        }
        for state, signature in sorted(trained_splits)
        if trained_splits[(state, signature)] == all_split_keys
        and not falsified_splits[(state, signature)]
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "split_summary_rows.jsonl", split_summaries)
    write_jsonl(OUTPUT_DIR / "surviving_exclusion_rows.jsonl", surviving_rows)
    write_jsonl(OUTPUT_DIR / "falsified_exclusion_rows.jsonl", falsified_rows)
    write_jsonl(OUTPUT_DIR / "stable_survivor_rows.jsonl", stable_survivors)
    write_json(
        OUTPUT_DIR / "summary.json",
        {
            "rule_id": RULE_ID,
            "source_rule_id": SOURCE_RULE_ID,
            "status": "measured_heldout_sidecar_check",
            "theorem_status": "hypothesis_not_proved",
            "inference_status": "not_live_pedk_inference",
            "input_corpus": str(INPUT_PATH.relative_to(THIS_DIR)),
            "split_axis": "known_larger_factor_q_for_corpus_partition_only",
            "q_ceilings": list(Q_CEILINGS),
            "min_support": MIN_SUPPORT,
            "corpus_row_count": len(rows),
            "split_count": len(split_summaries),
            "total_surviving_exclusion_rows": len(surviving_rows),
            "total_falsified_exclusion_rows": len(falsified_rows),
            "stable_survivor_count": len(stable_survivors),
            "split_summaries": split_summaries,
        },
    )
    print(json.dumps(split_summaries, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
