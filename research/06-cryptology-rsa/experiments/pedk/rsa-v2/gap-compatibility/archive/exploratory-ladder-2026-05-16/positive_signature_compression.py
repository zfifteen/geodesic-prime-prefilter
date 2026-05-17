#!/usr/bin/env python3
"""Compress stable positive PEDK signatures by factor-side residue grammar."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = (
    THIS_DIR
    / "output"
    / "five_state_positive_signature_map"
    / "stable_positive_signature_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "positive_signature_compression"
RULE_ID = "pedk_positive_signature_compression_v1"
SOURCE_RULE_ID = "pedk_five_state_positive_signature_map_v1"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def factor_residues(signature: str) -> tuple[str, ...]:
    """Return the four residue labels in a factor-neighborhood signature."""
    residues = tuple(re.findall(r"[LR]=(o[246])_", signature))
    if len(residues) != 4:
        raise ValueError(f"expected four residues in signature: {signature}")
    return residues


def multiset_key(residues: tuple[str, ...]) -> str:
    """Return residue multiset key."""
    counts = Counter(residues)
    return "|".join(f"{residue}:{counts[residue]}" for residue in ("o2", "o4", "o6"))


def compression_rows(rows: list[dict[str, object]]) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    dict[str, object],
]:
    """Return residue compression rows and summary."""
    global_multisets = Counter()
    state_multisets = Counter()
    presence_counts = Counter()
    state_presence_counts = Counter()
    signatures_by_state: dict[str, set[str]] = {}
    total_counts_by_state_signature: Counter[tuple[str, str]] = Counter()
    annotated_rows: list[dict[str, object]] = []

    for row in rows:
        state = str(row["n_containing_gap_phased_state"])
        signature = str(row["factor_neighborhood_signature"])
        signatures_by_state.setdefault(state, set()).add(signature)
        total_counts_by_state_signature[(state, signature)] += int(str(row["total_observed_count"]))
        residues = factor_residues(signature)
        counts = Counter(residues)
        key = multiset_key(residues)
        global_multisets[key] += 1
        state_multisets[(state, key)] += 1
        for residue in ("o2", "o4", "o6"):
            if counts[residue] > 0:
                presence_counts[residue] += 1
                state_presence_counts[(state, residue)] += 1
        annotated_rows.append(
            {
                "rule_id": RULE_ID,
                "source_rule_id": SOURCE_RULE_ID,
                "n_containing_gap_phased_state": state,
                "factor_neighborhood_signature": signature,
                "total_observed_count": row["total_observed_count"],
                "residue_multiset": key,
                "o2_count": counts["o2"],
                "o4_count": counts["o4"],
                "o6_count": counts["o6"],
                "has_o2": counts["o2"] > 0,
                "has_o4": counts["o4"] > 0,
                "has_o6": counts["o6"] > 0,
            }
        )

    multiset_rows = [
        {
            "rule_id": RULE_ID,
            "residue_multiset": key,
            "stable_positive_signature_count": count,
        }
        for key, count in sorted(
            global_multisets.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]
    state_multiset_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "residue_multiset": key,
            "stable_positive_signature_count": count,
        }
        for (state, key), count in sorted(state_multisets.items())
    ]
    intersection = (
        set.intersection(*signatures_by_state.values())
        if signatures_by_state
        else set()
    )
    intersection_rows = [
        {
            "rule_id": RULE_ID,
            "source_rule_id": SOURCE_RULE_ID,
            "candidate_status": "positive_signature_seen_in_all_five_public_states",
            "factor_neighborhood_signature": signature,
            "residue_multiset": multiset_key(factor_residues(signature)),
            "public_phase_state_count": len(signatures_by_state),
            "total_observed_count": sum(
                total_counts_by_state_signature[(state, signature)]
                for state in signatures_by_state
            ),
            "observed_count_by_state": {
                state: total_counts_by_state_signature[(state, signature)]
                for state in sorted(signatures_by_state)
            },
        }
        for signature in sorted(intersection)
    ]
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_positive_signature_compression",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "stable_positive_signature_count": len(rows),
        "residue_multiset_count": len(global_multisets),
        "all_state_intersection_signature_count": len(intersection_rows),
        "all_o6_positive_signature_count": global_multisets["o2:0|o4:0|o6:4"],
        "all_positive_signatures_have_non_o6_residue": (
            global_multisets["o2:0|o4:0|o6:4"] == 0
        ),
        "signatures_with_o2_count": presence_counts["o2"],
        "signatures_with_o4_count": presence_counts["o4"],
        "signatures_with_o6_count": presence_counts["o6"],
        "state_residue_presence_counts": {
            f"{state}|{residue}": state_presence_counts[(state, residue)]
            for state in sorted({str(row["n_containing_gap_phased_state"]) for row in rows})
            for residue in ("o2", "o4", "o6")
        },
    }
    return annotated_rows, multiset_rows, state_multiset_rows, intersection_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Compress stable positive PEDK signatures by residue grammar."
    )
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run positive signature compression."""
    args = parse_args(argv)
    if not args.input.exists():
        raise FileNotFoundError(f"missing positive signature rows: {args.input}")

    annotated_rows, multiset_rows, state_multiset_rows, intersection_rows, summary = compression_rows(
        read_jsonl(args.input)
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "positive_signature_residue_rows.jsonl", annotated_rows)
    write_jsonl(args.output_dir / "residue_multiset_rows.jsonl", multiset_rows)
    write_jsonl(args.output_dir / "state_residue_multiset_rows.jsonl", state_multiset_rows)
    write_jsonl(args.output_dir / "all_state_intersection_signature_rows.jsonl", intersection_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
