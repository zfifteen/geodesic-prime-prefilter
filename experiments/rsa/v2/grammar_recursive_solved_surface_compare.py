#!/usr/bin/env python3
"""Compare solved-surface recursive target grammar with expanded rows."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from grammar_recursive_target_catalog import (  # noqa: E402
    feature_summary,
    recursive_target_row,
    split_rows,
    summary as recursive_summary,
)


RULE_ID = "grammar_recursive_solved_surface_compare_v1"
SOLVED_SURFACE = "exact_low_regime"


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


def target_value_index(target_rows: list[dict[str, object]]) -> dict[tuple[str, str], int]:
    """Return known target coordinate values by case and side."""
    return {
        (str(row["case_id"]), str(row["target_side"])): int(row["target_value"])
        for row in target_rows
    }


def is_higher(state: str) -> bool:
    """Return whether one reduced grammar state is higher-divisor grammar."""
    return "higher_divisor" in state


def low_high(state: str) -> str:
    """Return the low/higher class for one reduced grammar state."""
    return "H" if is_higher(state) else "L"


def family(state: str) -> str:
    """Return the exact family prefix before the divisor bucket."""
    return state.split("|", 1)[0]


def with_cell_key(row: dict[str, object]) -> dict[str, object]:
    """Return a compatibility row with the explicit public cell key attached."""
    if "cell_key" in row:
        return row
    enriched = dict(row)
    enriched["cell_key"] = "|".join(
        [
            low_high(str(row["n_previous"])),
            family(str(row["n_containing"])),
            low_high(str(row["n_following"])),
        ]
    )
    return enriched


def solved_rows(
    compatibility_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return recursive target rows for the solved compatibility surface."""
    values = target_value_index(target_rows)
    output: list[dict[str, object]] = []
    for row in compatibility_rows:
        if str(row["surface"]) != SOLVED_SURFACE:
            continue
        enriched = with_cell_key(row)
        for target_side in ("p", "q"):
            key = (str(row["case_id"]), target_side)
            if key not in values:
                raise ValueError(f"missing target value for {key}")
            output.append(recursive_target_row(enriched, target_side, values[key]))
    return output


def compare_signatures(
    solved: list[dict[str, object]],
    expanded: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return signature-overlap rows between solved and expanded surfaces."""
    expanded_lag23 = {str(row["lag23_reduced_signature"]) for row in expanded}
    expanded_recursive = {str(row["recursive_reduced_signature"]) for row in expanded}
    grouped: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in solved:
        key = (str(row["target_direction_class"]), str(row["lag23_reduced_signature"]))
        grouped.setdefault(key, []).append(row)

    output: list[dict[str, object]] = []
    for (direction, lag23_signature), rows in sorted(grouped.items()):
        recursive_hits = sum(
            1 for row in rows if str(row["recursive_reduced_signature"]) in expanded_recursive
        )
        output.append(
            {
                "rule_id": RULE_ID,
                "target_direction_class": direction,
                "lag23_reduced_signature": lag23_signature,
                "solved_row_count": len(rows),
                "case_ids": [str(row["case_id"]) for row in rows],
                "present_in_expanded_lag23": lag23_signature in expanded_lag23,
                "expanded_recursive_signature_hit_count": recursive_hits,
            }
        )
    return output


def comparison_summary(
    solved: list[dict[str, object]],
    expanded: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
    grouped_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact solved-vs-expanded recursive comparison summary."""
    payload = recursive_summary(solved, grouped_rows)
    payload["rule_id"] = RULE_ID
    payload["solved_surface"] = SOLVED_SURFACE
    payload["expanded_target_row_count"] = len(expanded)
    direction_counts = Counter(str(row["target_direction_class"]) for row in solved)
    payload["solved_target_direction_class_counts"] = dict(sorted(direction_counts.items()))
    outward_rows = [row for row in solved if str(row["target_direction_class"]) == "outward_only"]
    inward_rows = [row for row in solved if str(row["target_direction_class"]) == "inward_only"]
    payload["solved_outward_only_row_count"] = len(outward_rows)
    payload["solved_inward_only_row_count"] = len(inward_rows)
    payload["lag23_signature_count"] = len(comparison_rows)
    payload["lag23_signature_overlap_count"] = sum(
        1 for row in comparison_rows if row["present_in_expanded_lag23"]
    )
    payload["outward_lag23_signature_count"] = sum(
        1 for row in comparison_rows if row["target_direction_class"] == "outward_only"
    )
    payload["outward_lag23_signature_overlap_count"] = sum(
        1
        for row in comparison_rows
        if row["target_direction_class"] == "outward_only" and row["present_in_expanded_lag23"]
    )
    for signature_key in (
        "lag2_reduced_signature",
        "lag3_reduced_signature",
        "lag23_reduced_signature",
        "recursive_reduced_signature",
        "recursive_class_signature",
    ):
        solved_signatures = {str(row[signature_key]) for row in solved}
        expanded_signatures = {str(row[signature_key]) for row in expanded}
        solved_outward = {
            str(row[signature_key])
            for row in solved
            if str(row["target_direction_class"]) == "outward_only"
        }
        expanded_outward = {
            str(row[signature_key])
            for row in expanded
            if str(row["target_direction_class"]) == "outward_only"
        }
        prefix = signature_key.removesuffix("_signature")
        payload[f"{prefix}_solved_signature_count"] = len(solved_signatures)
        payload[f"{prefix}_expanded_signature_count"] = len(expanded_signatures)
        payload[f"{prefix}_signature_overlap_count"] = len(
            solved_signatures & expanded_signatures
        )
        payload[f"{prefix}_solved_outward_signature_count"] = len(solved_outward)
        payload[f"{prefix}_solved_outward_overlap_any_direction_count"] = len(
            solved_outward & expanded_signatures
        )
        payload[f"{prefix}_solved_outward_overlap_outward_count"] = len(
            solved_outward & expanded_outward
        )
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Compare solved recursive grammar.")
    parser.add_argument(
        "--compatibility-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_compatibility" / "compatibility_rows.jsonl",
        help="Compatibility rows with solved surface labels.",
    )
    parser.add_argument(
        "--target-rows",
        type=Path,
        default=THIS_DIR / "output" / "modulus_gap_grammar_catalog" / "target_correlation_rows.jsonl",
        help="Target rows containing known target coordinates.",
    )
    parser.add_argument(
        "--expanded-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_target_catalog" / "recursive_target_rows.jsonl",
        help="Expanded recursive target rows for signature comparison.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_solved_surface",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run solved-surface recursive grammar comparison."""
    args = parse_args(argv)
    solved = solved_rows(read_jsonl(args.compatibility_rows), read_jsonl(args.target_rows))
    expanded = read_jsonl(args.expanded_recursive_rows)
    features = (
        "cell_key+target_side+lag2_reduced_signature",
        "cell_key+target_side+lag2_reduced_signature+lag3_reduced_signature",
        "cell_key+target_side+lag23_reduced_signature",
    )
    grouped_rows = split_rows(solved, features)
    comparison_rows = compare_signatures(solved, expanded)
    payload = comparison_summary(solved, expanded, comparison_rows, grouped_rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "recursive_target_rows.jsonl", solved)
    write_jsonl(args.output_dir / "recursive_split_rows.jsonl", grouped_rows)
    write_jsonl(args.output_dir / "feature_summary_rows.jsonl", feature_summary(grouped_rows))
    write_jsonl(args.output_dir / "signature_comparison_rows.jsonl", comparison_rows)
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
