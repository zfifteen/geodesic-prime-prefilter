#!/usr/bin/env python3
"""Test public quotients against slot-preserving factor residue/phase words."""

from __future__ import annotations

import argparse
import itertools
import json
import re
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from intermediate_projection_surface import gwr_distance_bucket


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_9001_11000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_11001_13000"
DEFAULT_PRIOR_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_13001_15000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_15001_17000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "slot_factor_public_quotient_test_15001_17000"
RULE_ID = "pedk_slot_factor_public_quotient_test_v1"
DEFAULT_MIN_PUBLIC_SUPPORT = 5
DEFAULT_MIN_FACTOR_SUPPORT = 5
FACTOR_SLOT_RE = re.compile(r"p=L=(?P<pL>.*?)\|R=(?P<pR>.*?) \|\| q=L=(?P<qL>.*?)\|R=(?P<qR>.*)$")
PHASE_RE = re.compile(r"@([^@|]+)$")
RESIDUE_RE = re.compile(r"^(o[0-9]+)_")


PUBLIC_MODES = (
    "containing_side",
    "prev_containing_side",
    "containing_next_side",
    "public_word",
    "containing_gwr_bucket",
    "public_word_gwr_side",
)

FACTOR_MODES = (
    "slot_residue_phase",
    "unordered_endpoint_pair_residue_phase",
    "unordered_proximity_endpoint_pair_residue_phase",
    "left_right_boundary_multiset_residue_phase",
    "unordered_endpoint_lr_multiset_residue_phase",
    "slot_residue_phase_multiset",
)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def split_factor_slots(factor_word: str) -> dict[str, str]:
    """Split an oriented factor phase word into four slots."""
    match = FACTOR_SLOT_RE.match(factor_word)
    if not match:
        raise ValueError(f"cannot parse factor word: {factor_word}")
    return {name: match.group(name) for name in ("pL", "pR", "qL", "qR")}


def slot_residue_phase(slot: str) -> str:
    """Return residue and phase for one factor-neighborhood slot."""
    residue_match = RESIDUE_RE.search(slot)
    phase_match = PHASE_RE.search(slot)
    residue = residue_match.group(1) if residue_match else "unknown"
    phase = phase_match.group(1) if phase_match else "unknown"
    return f"{residue}@{phase}"


def factor_projection(row: dict[str, object], mode: str) -> str:
    """Return a factor-side projection."""
    slots = split_factor_slots(str(row["oriented_factor_phase_word"]))
    slot_values = {
        slot_name: slot_residue_phase(slots[slot_name])
        for slot_name in ("pL", "pR", "qL", "qR")
    }
    if mode == "slot_residue_phase":
        return "|".join(
            f"{slot_name}={slot_values[slot_name]}"
            for slot_name in ("pL", "pR", "qL", "qR")
        )
    if mode == "unordered_endpoint_pair_residue_phase":
        pairs = sorted(
            (
                f"L={slot_values['pL']}|R={slot_values['pR']}",
                f"L={slot_values['qL']}|R={slot_values['qR']}",
            )
        )
        return " || ".join(pairs)
    if mode == "unordered_proximity_endpoint_pair_residue_phase":
        # Both pairs use canonical order: distal first, proximal second.
        # p: distal=pL | proximal=pR
        # q: distal=qR | proximal=qL
        # Sorting the two pairs then drops p/q identity.
        p_pair = f"distal={slot_values['pL']}|proximal={slot_values['pR']}"
        q_pair = f"distal={slot_values['qR']}|proximal={slot_values['qL']}"
        pairs = sorted([p_pair, q_pair])
        return " || ".join(pairs)
    if mode == "left_right_boundary_multiset_residue_phase":
        left_counts = Counter((slot_values["pL"], slot_values["qL"]))
        right_counts = Counter((slot_values["pR"], slot_values["qR"]))
        left_value = "|".join(
            f"{value}:{count}" for value, count in sorted(left_counts.items())
        )
        right_value = "|".join(
            f"{value}:{count}" for value, count in sorted(right_counts.items())
        )
        return f"L={left_value} || R={right_value}"
    if mode == "unordered_endpoint_lr_multiset_residue_phase":
        pairs = sorted(
            (
                "|".join(sorted((slot_values["pL"], slot_values["pR"]))),
                "|".join(sorted((slot_values["qL"], slot_values["qR"]))),
            )
        )
        return " || ".join(pairs)
    if mode == "slot_residue_phase_multiset":
        counts = Counter(slot_values.values())
        return "|".join(f"{value}:{count}" for value, count in sorted(counts.items()))
    raise ValueError(f"unknown factor mode: {mode}")


def public_projection(row: dict[str, object], mode: str) -> str:
    """Return one public-side quotient."""
    prev_value = str(row["public_previous_reduced_state"])
    containing_value = (
        f"{row['public_containing_exact_type_key']}@"
        f"{row['public_containing_phase_bucket']}"
    )
    next_value = str(row["public_following_reduced_state"])
    side = str(row["public_gwr_side"])
    if mode == "containing_side":
        return f"containing={containing_value}|{side}"
    if mode == "prev_containing_side":
        return f"prev={prev_value}|containing={containing_value}|{side}"
    if mode == "containing_next_side":
        return f"containing={containing_value}|next={next_value}|{side}"
    if mode == "public_word":
        return str(row["public_word"])
    if mode == "containing_gwr_bucket":
        distance = int(row["public_gwr_signed_distance"])
        return f"containing={containing_value}|{gwr_distance_bucket(distance)}"
    if mode == "public_word_gwr_side":
        return f"{row['public_word']}|{side}"
    raise ValueError(f"unknown public mode: {mode}")


def surface(
    rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
    min_public_support: int,
    min_factor_support: int,
) -> dict[str, object]:
    """Return supported keys and observed cells for a public quotient."""
    public_counts = Counter(public_projection(row, public_mode) for row in rows)
    factor_counts = Counter(factor_projection(row, factor_mode) for row in rows)
    observed_counts = Counter(
        (public_projection(row, public_mode), factor_projection(row, factor_mode))
        for row in rows
    )
    supported_public = {
        key for key, count in public_counts.items() if count >= min_public_support
    }
    supported_factor = {
        key for key, count in factor_counts.items() if count >= min_factor_support
    }
    observed_supported = {
        cell
        for cell in observed_counts
        if cell[0] in supported_public and cell[1] in supported_factor
    }
    return {
        "public_counts": public_counts,
        "factor_counts": factor_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_factor": supported_factor,
        "observed_supported": observed_supported,
    }


def analyze_mode(
    train_rows: list[dict[str, object]],
    calibration_rows: list[dict[str, object]],
    prior_forward_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
    min_public_support: int,
    min_factor_support: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Analyze one public quotient with fixed slot factor projection."""
    train = surface(
        train_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )
    calibration = surface(
        calibration_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )
    prior_forward = surface(
        prior_forward_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )
    forward = surface(
        forward_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )

    supported_product = set(
        itertools.product(train["supported_public"], train["supported_factor"])
    )
    candidate_cells = (
        supported_product
        - train["observed_supported"]
    )
    for older in (calibration, prior_forward):
        older_product = set(
            itertools.product(older["supported_public"], older["supported_factor"])
        )
        candidate_cells &= older_product
        candidate_cells -= older["observed_supported"]

    forward_product = set(
        itertools.product(forward["supported_public"], forward["supported_factor"])
    )
    testable = candidate_cells & forward_product
    falsified = testable & forward["observed_supported"]
    survived = testable - falsified
    not_testable = candidate_cells - testable

    candidate_rows = []
    for status, cells in (
        ("falsified_forward", falsified),
        ("survived_forward", survived),
        ("not_testable_forward", not_testable),
    ):
        for public_value, factor_value in sorted(cells):
            candidate_rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_mode": public_mode,
                    "factor_mode": factor_mode,
                    "public_key": public_value,
                    "factor_key": factor_value,
                    "train_public_support": train["public_counts"][public_value],
                    "train_factor_support": train["factor_counts"][factor_value],
                    "calibration_public_support": calibration["public_counts"][
                        public_value
                    ],
                    "calibration_factor_support": calibration["factor_counts"][
                        factor_value
                    ],
                    "prior_forward_public_support": prior_forward["public_counts"][
                        public_value
                    ],
                    "prior_forward_factor_support": prior_forward["factor_counts"][
                        factor_value
                    ],
                    "forward_public_support": forward["public_counts"][public_value],
                    "forward_factor_support": forward["factor_counts"][factor_value],
                    "forward_observed_count": forward["observed_counts"][
                        (public_value, factor_value)
                    ],
                    "status": status,
                }
            )

    summary = {
        "rule_id": RULE_ID,
        "public_mode": public_mode,
        "factor_mode": factor_mode,
        "min_public_support": min_public_support,
        "min_factor_support": min_factor_support,
        "train_supported_public_key_count": len(train["supported_public"]),
        "train_supported_factor_key_count": len(train["supported_factor"]),
        "train_observed_supported_cell_count": len(train["observed_supported"]),
        "calibration_observed_supported_cell_count": len(
            calibration["observed_supported"]
        ),
        "prior_forward_observed_supported_cell_count": len(
            prior_forward["observed_supported"]
        ),
        "forward_observed_supported_cell_count": len(forward["observed_supported"]),
        "candidate_clean_absent_cell_count": len(candidate_cells),
        "forward_testable_cell_count": len(testable),
        "survived_forward_cell_count": len(survived),
        "falsified_forward_cell_count": len(falsified),
        "not_testable_forward_cell_count": len(not_testable),
        "strict_falsification_rate_mpermille": (
            len(falsified) * 1000 // len(testable) if testable else None
        ),
    }
    return summary, candidate_rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test public quotients for slot factor words.")
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--prior-forward-dir", type=Path, default=DEFAULT_PRIOR_FORWARD_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--public-mode", action="append", default=[])
    parser.add_argument("--factor-mode", action="append", default=[])
    parser.add_argument("--min-public-support", type=int, default=DEFAULT_MIN_PUBLIC_SUPPORT)
    parser.add_argument("--min-factor-support", type=int, default=DEFAULT_MIN_FACTOR_SUPPORT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run public-quotient test."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(args.prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")

    rows = []
    sample_rows = []
    public_modes = tuple(args.public_mode) if args.public_mode else PUBLIC_MODES
    factor_modes = tuple(args.factor_mode) if args.factor_mode else FACTOR_MODES
    for public_mode in public_modes:
        for factor_mode in factor_modes:
            summary, candidates = analyze_mode(
                train_rows,
                calibration_rows,
                prior_forward_rows,
                forward_rows,
                public_mode,
                factor_mode,
                args.min_public_support,
                args.min_factor_support,
            )
            rows.append(summary)
            sample_rows.extend(candidates[:100])

    rows.sort(
        key=lambda row: (
            row["strict_falsification_rate_mpermille"]
            if row["strict_falsification_rate_mpermille"] is not None
            else 1001,
            -int(row["forward_testable_cell_count"]),
            str(row["public_mode"]),
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_slot_factor_public_quotient_test",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "train_row_count": len(train_rows),
        "calibration_row_count": len(calibration_rows),
        "prior_forward_row_count": len(prior_forward_rows),
        "forward_row_count": len(forward_rows),
        "min_public_support": args.min_public_support,
        "min_factor_support": args.min_factor_support,
        "public_mode_count": len(rows),
        "top_public_modes": rows,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "public_quotient_rows.jsonl", rows)
    write_jsonl(args.output_dir / "public_quotient_sample_cells.jsonl", sample_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
