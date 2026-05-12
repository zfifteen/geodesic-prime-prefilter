#!/usr/bin/env python3
"""Find exact cross-regime DNI state bundles from transition detail CSVs."""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path


PREFIX_OFFSETS = tuple(range(1, 13))
FAMILY_COMPONENTS = {
    "unrestricted": (
        "residue_mod30",
        "first_open_offset",
        "current_gap_width",
        "current_dmin",
        "current_peak_offset",
    ),
    "no_residue": (
        "first_open_offset",
        "current_gap_width",
        "current_dmin",
        "current_peak_offset",
    ),
    "no_residue_no_first_open": (
        "current_gap_width",
        "current_dmin",
        "current_peak_offset",
    ),
}


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Find minimal exact DNI bundles across multiple transition CSVs.",
    )
    parser.add_argument(
        "--detail-csv",
        dest="detail_csvs",
        action="append",
        type=Path,
        required=True,
        help="Transition detail CSV emitted by gwr_dni_transition_probe.py. Repeat for multiple regimes.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        required=True,
        help="Summary JSON output path.",
    )
    return parser


def load_rows(detail_csvs: list[Path]) -> list[dict[str, str]]:
    """Load rows from one or more transition detail CSVs."""
    rows: list[dict[str, str]] = []
    for path in detail_csvs:
        with path.open(encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    if not rows:
        raise ValueError("detail_csvs must contain at least one data row")
    return rows


def bundle_is_exact(rows: list[dict[str, str]], keys: tuple[str, ...]) -> bool:
    """Return whether one state bundle determines the next-gap state exactly."""
    support: dict[tuple[str, ...], tuple[str, str]] = {}
    for row in rows:
        signature = tuple(row[key] for key in keys)
        target = (row["next_dmin"], row["next_peak_offset"])
        previous = support.get(signature)
        if previous is None:
            support[signature] = target
            continue
        if previous != target:
            return False
    return True


def analyze_exact_bundle(rows: list[dict[str, str]], keys: tuple[str, ...]) -> dict[str, object]:
    """Return exact-state metrics for one bundle already known to be exact."""
    support: dict[tuple[str, ...], tuple[str, str]] = {}
    for row in rows:
        signature = tuple(row[key] for key in keys)
        support[signature] = (row["next_dmin"], row["next_peak_offset"])
    return {
        "state_keys": list(keys),
        "distinct_state_count": len(support),
        "unique_state_count": len(support),
        "unique_state_rate": 1.0,
        "unique_observation_count": len(rows),
        "unique_observation_share": 1.0,
        "max_target_support_size": 1,
    }


def minimal_exact_bundles(
    rows: list[dict[str, str]],
    component_keys: tuple[str, ...],
) -> dict[str, object] | None:
    """Return all minimal exact bundles in one configured component family."""
    exact_matches: list[dict[str, object]] = []
    best_score: tuple[int, int, int] | None = None

    for cutoff in range(1, len(PREFIX_OFFSETS) + 1):
        prefix_keys = tuple(f"prefix_d_{offset}" for offset in range(1, cutoff + 1))
        for component_count in range(len(component_keys) + 1):
            for combo in combinations(component_keys, component_count):
                keys = combo + prefix_keys
                score = (len(keys), cutoff, component_count)
                if best_score is not None and score > best_score:
                    continue
                if not bundle_is_exact(rows, keys):
                    continue
                bundle = analyze_exact_bundle(rows, keys)
                bundle["prefix_cutoff"] = cutoff
                bundle["component_keys"] = list(combo)
                bundle["total_key_count"] = len(keys)
                if best_score is None:
                    best_score = score
                if score == best_score:
                    exact_matches.append(bundle)
    if best_score is None:
        return None
    return {
        "best_score": {
            "total_key_count": best_score[0],
            "prefix_cutoff": best_score[1],
            "component_count": best_score[2],
        },
        "bundles": exact_matches,
    }


def summarize(detail_csvs: list[Path]) -> dict[str, object]:
    """Summarize exact bundle families across one or more regimes."""
    rows = load_rows(detail_csvs)
    families = {
        family_name: minimal_exact_bundles(rows, component_keys)
        for family_name, component_keys in FAMILY_COMPONENTS.items()
    }
    return {
        "source_paths": [str(path) for path in detail_csvs],
        "row_count": len(rows),
        "family_minima": families,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the cross-regime bundle probe and write a JSON summary."""
    args = build_parser().parse_args(argv)
    summary = summarize(args.detail_csvs)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
