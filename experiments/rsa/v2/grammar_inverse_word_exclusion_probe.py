#!/usr/bin/env python3
"""Probe inverse recursive grammar as component sharing with ordered-word exclusion."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "grammar_inverse_word_exclusion_probe_v1"
SIGNATURE_KEYS = (
    "lag2_reduced_signature",
    "lag3_reduced_signature",
    "lag23_reduced_signature",
    "recursive_reduced_signature",
    "recursive_class_signature",
)
COMPONENT_KEYS = (
    "lag2_reduced_signature",
    "lag3_reduced_signature",
)


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


def scope_key(row: dict[str, object], scope: str) -> str:
    """Return the comparison scope key for one recursive target row."""
    if scope == "global":
        return "global"
    if scope == "cell":
        return str(row["cell_key"])
    if scope == "cell_side":
        return f"{row['cell_key']}|{row['target_side']}"
    raise ValueError(f"unknown scope: {scope}")


def signature_sets(
    expanded_rows: list[dict[str, object]],
    scopes: tuple[str, ...],
) -> dict[str, dict[str, dict[str, set[str]]]]:
    """Return expanded signature sets by comparison scope."""
    output: dict[str, dict[str, dict[str, set[str]]]] = {
        scope: defaultdict(lambda: {key: set() for key in SIGNATURE_KEYS})
        for scope in scopes
    }
    for row in expanded_rows:
        for scope in scopes:
            scoped = output[scope][scope_key(row, scope)]
            for key in SIGNATURE_KEYS:
                scoped[key].add(str(row[key]))
    return output


def comparison_row(
    solved_row: dict[str, object],
    scope: str,
    expanded_sets: dict[str, set[str]],
) -> dict[str, object]:
    """Return one solved-row comparison against expanded recursive grammar."""
    hits = {
        f"{key}_hit": str(solved_row[key]) in expanded_sets[key]
        for key in SIGNATURE_KEYS
    }
    component_labels = [
        f"{key.removesuffix('_reduced_signature')}:{solved_row[key]}"
        for key in COMPONENT_KEYS
        if hits[f"{key}_hit"]
    ]
    piece_hit = hits["lag2_reduced_signature_hit"] or hits["lag3_reduced_signature_hit"]
    ordered_word_excluded = not hits["lag23_reduced_signature_hit"]
    return {
        "rule_id": RULE_ID,
        "scope": scope,
        "scope_key": scope_key(solved_row, scope),
        "case_id": str(solved_row["case_id"]),
        "target_side": str(solved_row["target_side"]),
        "target_direction_class": str(solved_row["target_direction_class"]),
        "cell_key": str(solved_row["cell_key"]),
        "lag2_reduced_signature": str(solved_row["lag2_reduced_signature"]),
        "lag3_reduced_signature": str(solved_row["lag3_reduced_signature"]),
        "lag23_reduced_signature": str(solved_row["lag23_reduced_signature"]),
        "recursive_reduced_signature": str(solved_row["recursive_reduced_signature"]),
        "recursive_class_signature": str(solved_row["recursive_class_signature"]),
        "combined_lag23_family_label": "|".join(
            [
                f"lag2:{solved_row['lag2_reduced_signature']}",
                f"lag3:{solved_row['lag3_reduced_signature']}",
            ]
        ),
        "shared_component_family_labels": component_labels,
        "shared_component_family_count": len(component_labels),
        "component_piece_hit": piece_hit,
        "ordered_word_excluded": ordered_word_excluded,
        "component_sharing_word_exclusion": piece_hit and ordered_word_excluded,
        "class_sharing_word_exclusion": (
            hits["recursive_class_signature_hit"] and ordered_word_excluded
        ),
    } | hits


def comparison_rows(
    solved_rows: list[dict[str, object]],
    expanded_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return solved-vs-expanded inverse word exclusion comparison rows."""
    scopes = ("global", "cell", "cell_side")
    sets = signature_sets(expanded_rows, scopes)
    output: list[dict[str, object]] = []
    for row in solved_rows:
        for scope in scopes:
            output.append(comparison_row(row, scope, sets[scope][scope_key(row, scope)]))
    return output


def grouped_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return counts by scope and target direction."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["scope"]), str(row["target_direction_class"]))].append(row)

    output: list[dict[str, object]] = []
    for (scope, direction), group in sorted(grouped.items()):
        output.append(
            {
                "rule_id": RULE_ID,
                "scope": scope,
                "target_direction_class": direction,
                "row_count": len(group),
                "lag2_hit_count": sum(1 for row in group if row["lag2_reduced_signature_hit"]),
                "lag3_hit_count": sum(1 for row in group if row["lag3_reduced_signature_hit"]),
                "lag23_hit_count": sum(1 for row in group if row["lag23_reduced_signature_hit"]),
                "recursive_reduced_hit_count": sum(
                    1 for row in group if row["recursive_reduced_signature_hit"]
                ),
                "recursive_class_hit_count": sum(
                    1 for row in group if row["recursive_class_signature_hit"]
                ),
                "component_sharing_word_exclusion_count": sum(
                    1 for row in group if row["component_sharing_word_exclusion"]
                ),
                "two_component_family_hit_count": sum(
                    1 for row in group if row["shared_component_family_count"] == 2
                ),
                "one_component_family_hit_count": sum(
                    1 for row in group if row["shared_component_family_count"] == 1
                ),
                "class_sharing_word_exclusion_count": sum(
                    1 for row in group if row["class_sharing_word_exclusion"]
                ),
            }
        )
    return output


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact inverse word exclusion summary."""
    by_scope = defaultdict(list)
    for row in rows:
        by_scope[str(row["scope"])].append(row)
    scope_summaries = []
    for scope, group in sorted(by_scope.items()):
        scope_summaries.append(
            {
                "rule_id": RULE_ID,
                "scope": scope,
                "row_count": len(group),
                "lag2_hit_count": sum(1 for row in group if row["lag2_reduced_signature_hit"]),
                "lag3_hit_count": sum(1 for row in group if row["lag3_reduced_signature_hit"]),
                "lag23_hit_count": sum(1 for row in group if row["lag23_reduced_signature_hit"]),
                "recursive_reduced_hit_count": sum(
                    1 for row in group if row["recursive_reduced_signature_hit"]
                ),
                "recursive_class_hit_count": sum(
                    1 for row in group if row["recursive_class_signature_hit"]
                ),
                "component_sharing_word_exclusion_count": sum(
                    1 for row in group if row["component_sharing_word_exclusion"]
                ),
                "two_component_family_hit_count": sum(
                    1 for row in group if row["shared_component_family_count"] == 2
                ),
                "one_component_family_hit_count": sum(
                    1 for row in group if row["shared_component_family_count"] == 1
                ),
                "class_sharing_word_exclusion_count": sum(
                    1 for row in group if row["class_sharing_word_exclusion"]
                ),
            }
        )
    return {
        "rule_id": RULE_ID,
        "comparison_row_count": len(rows),
        "scope_summaries": scope_summaries,
        "direction_summaries": grouped_summary(rows),
        "direction_counts": dict(
            sorted(Counter(str(row["target_direction_class"]) for row in rows).items())
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Probe inverse recursive grammar words.")
    parser.add_argument(
        "--solved-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_solved_surface" / "recursive_target_rows.jsonl",
        help="Solved recursive target rows.",
    )
    parser.add_argument(
        "--expanded-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_target_catalog" / "recursive_target_rows.jsonl",
        help="Expanded recursive target rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_inverse_word_exclusion",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run inverse word exclusion comparison."""
    args = parse_args(argv)
    rows = comparison_rows(
        read_jsonl(args.solved_recursive_rows),
        read_jsonl(args.expanded_recursive_rows),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "inverse_word_rows.jsonl", rows)
    write_jsonl(args.output_dir / "direction_summary_rows.jsonl", grouped_summary(rows))
    payload = summary(rows)
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
