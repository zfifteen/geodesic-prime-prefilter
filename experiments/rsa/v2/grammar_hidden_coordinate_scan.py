#!/usr/bin/env python3
"""Scan expanded grammar rows for coordinates that split mixed orientation cells."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "grammar_hidden_coordinate_scan_v1"
ORIENTATIONS = ("p_outward", "p_inward", "q_inward", "q_outward")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from one path."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON document."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    payload = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def is_higher(state: str) -> bool:
    """Return whether one reduced grammar state is higher-divisor grammar."""
    return "higher_divisor" in state


def exact_d(exact_key: object) -> str:
    """Return the exact divisor-count coordinate from one exact grammar key."""
    for part in str(exact_key).split("_"):
        if len(part) > 1 and part.startswith("d") and part[1:].isdigit():
            return part
    return "d_unresolved"


def row_direction_class(row: dict[str, object]) -> str:
    """Return the row-level higher-divisor direction class."""
    outward = int(is_higher(str(row["p_outward"]))) + int(is_higher(str(row["q_outward"])))
    inward = int(is_higher(str(row["p_inward"]))) + int(is_higher(str(row["q_inward"])))
    if outward and inward:
        return "both"
    if outward:
        return "outward_only"
    if inward:
        return "inward_only"
    return "none"


def feature_key(row: dict[str, object], feature: str) -> str:
    """Return one grouping key for a named coordinate split."""
    if feature == "cell_key":
        return str(row["cell_key"])
    if feature == "cell_key+prime_pair_offset_group":
        return f"{row['cell_key']}|offset_group={row['prime_pair_offset_group']}"
    if feature == "cell_key+prime_pair_offset":
        return f"{row['cell_key']}|offset={row['prime_pair_offset']}"
    if feature == "cell_key+bits":
        return f"{row['cell_key']}|bits={row['bits']}"
    if feature == "cell_key+n_previous_exact":
        return f"{row['cell_key']}|n_previous_exact={row['n_previous_exact']}"
    if feature == "cell_key+n_containing_exact":
        return f"{row['cell_key']}|n_containing_exact={row['n_containing_exact']}"
    if feature == "cell_key+n_following_exact":
        return f"{row['cell_key']}|n_following_exact={row['n_following_exact']}"
    if feature == "cell_key+n_previous_d+n_following_d":
        return (
            f"{row['cell_key']}|nprev_d={exact_d(row['n_previous_exact'])}"
            f"|nfol_d={exact_d(row['n_following_exact'])}"
        )
    if feature == "cell_key+n_previous_d+n_containing_d+n_following_d":
        return (
            f"{row['cell_key']}|nprev_d={exact_d(row['n_previous_exact'])}"
            f"|ncont_d={exact_d(row['n_containing_exact'])}"
            f"|nfol_d={exact_d(row['n_following_exact'])}"
        )
    raise ValueError(f"unknown feature: {feature}")


def split_status(outward_higher: int, inward_higher: int) -> str:
    """Return the group-level higher-divisor orientation status."""
    if outward_higher and inward_higher:
        return "both_direction"
    if outward_higher:
        return "outward_only"
    if inward_higher:
        return "inward_only"
    return "no_higher"


def group_rows(rows: list[dict[str, object]], features: tuple[str, ...]) -> list[dict[str, object]]:
    """Return grouped split rows for all requested features."""
    output: list[dict[str, object]] = []
    for feature in features:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in rows:
            grouped[feature_key(row, feature)].append(row)
        for key, group in sorted(grouped.items()):
            orientation_higher = {
                orientation: sum(1 for row in group if is_higher(str(row[orientation])))
                for orientation in ORIENTATIONS
            }
            outward_higher = orientation_higher["p_outward"] + orientation_higher["q_outward"]
            inward_higher = orientation_higher["p_inward"] + orientation_higher["q_inward"]
            direction_classes = Counter(row_direction_class(row) for row in group)
            output.append(
                {
                    "rule_id": RULE_ID,
                    "feature": feature,
                    "key": key,
                    "case_count": len(group),
                    "orientation_higher_counts": orientation_higher,
                    "outward_higher_count": outward_higher,
                    "inward_higher_count": inward_higher,
                    "higher_event_count": outward_higher + inward_higher,
                    "outward_fraction": (
                        None
                        if outward_higher + inward_higher == 0
                        else outward_higher / (outward_higher + inward_higher)
                    ),
                    "split_status": split_status(outward_higher, inward_higher),
                    "row_direction_class_counts": dict(sorted(direction_classes.items())),
                    "case_ids": [str(row["case_id"]) for row in group],
                }
            )
    return output


def feature_summary(grouped_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return per-feature split quality counts."""
    by_feature: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in grouped_rows:
        by_feature[str(row["feature"])].append(row)
    output: list[dict[str, object]] = []
    for feature, rows in sorted(by_feature.items()):
        repeated = [row for row in rows if int(row["case_count"]) > 1]
        repeated_status = Counter(str(row["split_status"]) for row in repeated)
        all_status = Counter(str(row["split_status"]) for row in rows)
        output.append(
            {
                "rule_id": RULE_ID,
                "feature": feature,
                "group_count": len(rows),
                "case_count": sum(int(row["case_count"]) for row in rows),
                "singleton_group_count": sum(1 for row in rows if int(row["case_count"]) == 1),
                "repeated_group_count": len(repeated),
                "repeated_status_counts": dict(sorted(repeated_status.items())),
                "all_status_counts": dict(sorted(all_status.items())),
            }
        )
    return output


def summary(rows: list[dict[str, object]], grouped_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact scan summary."""
    feature_rows = feature_summary(grouped_rows)
    return {
        "rule_id": RULE_ID,
        "source_row_count": len(rows),
        "grouped_row_count": len(grouped_rows),
        "features": [str(row["feature"]) for row in feature_rows],
        "feature_summaries": feature_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Scan hidden grammar coordinates.")
    parser.add_argument(
        "--rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_cell_expansion" / "expanded_compatibility_rows.jsonl",
        help="Expanded compatibility rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_hidden_coordinate_scan",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the hidden-coordinate split scan."""
    args = parse_args(argv)
    rows = read_jsonl(args.rows)
    features = (
        "cell_key",
        "cell_key+prime_pair_offset_group",
        "cell_key+prime_pair_offset",
        "cell_key+bits",
        "cell_key+n_previous_exact",
        "cell_key+n_containing_exact",
        "cell_key+n_following_exact",
        "cell_key+n_previous_d+n_following_d",
        "cell_key+n_previous_d+n_containing_d+n_following_d",
    )
    grouped_rows = group_rows(rows, features)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "split_group_rows.jsonl", grouped_rows)
    write_jsonl(args.output_dir / "feature_summary_rows.jsonl", feature_summary(grouped_rows))
    payload = summary(rows, grouped_rows)
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
