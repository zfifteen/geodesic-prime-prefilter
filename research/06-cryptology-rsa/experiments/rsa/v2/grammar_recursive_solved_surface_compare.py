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
    oriented_gaps,
    recursive_target_row,
    row_direction_class,
    split_rows,
    state_class,
    summary as recursive_summary,
    target_direction_class,
)
from rsa_challenge_exact_grammar_probe import (  # noqa: E402
    gap_grammar as exact_gap_grammar,
    next_prime,
    previous_prime,
)


RULE_ID = "grammar_recursive_solved_surface_compare_v1"
SOLVED_SURFACE = "exact_low_regime"
INT64_MAX = 2**63 - 1


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
    values: dict[tuple[str, str], int] = {}
    for row in target_rows:
        if "target_value" in row:
            values[(str(row["case_id"]), str(row["target_side"]))] = int(row["target_value"])
            continue
        role = str(row.get("role"))
        if role in ("p_left", "q_left"):
            values[(str(row["case_id"]), role[:1])] = int(row["right_endpoint"])
    return values


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


def large_side_gaps(target_value: int) -> dict[str, dict[str, object]]:
    """Return three left and three right exact chamber payloads around one large target."""
    left_1 = previous_prime(target_value - 1)
    left_2 = previous_prime(left_1 - 1)
    left_3 = previous_prime(left_2 - 1)
    right_1 = next_prime(target_value + 1)
    right_2 = next_prime(right_1 + 1)
    right_3 = next_prime(right_2 + 1)
    return {
        "left_lag3": exact_gap_grammar("left_lag3", left_3, left_2),
        "left_lag2": exact_gap_grammar("left_lag2", left_2, left_1),
        "left_lag1": exact_gap_grammar("left_lag1", left_1, target_value),
        "right_lag1": exact_gap_grammar("right_lag1", target_value, right_1),
        "right_lag2": exact_gap_grammar("right_lag2", right_1, right_2),
        "right_lag3": exact_gap_grammar("right_lag3", right_2, right_3),
    }


def recursive_target_row_large(
    source_row: dict[str, object],
    target_side: str,
    target_value: int,
) -> dict[str, object]:
    """Return one recursive target row using the large-coordinate exact backend."""
    oriented = oriented_gaps(target_side, large_side_gaps(target_value))
    states = {key: str(gap["reduced_state"]) for key, gap in oriented.items()}
    exact = {f"{key}_exact": str(gap["exact_type_key"]) for key, gap in oriented.items()}
    widths = {f"{key}_width": int(gap["gap_width"]) for key, gap in oriented.items()}
    row = {
        "rule_id": "grammar_recursive_target_catalog_v1",
        "source_rule_id": str(source_row["rule_id"]),
        "case_id": str(source_row["case_id"]),
        "bits": int(source_row["bits"]),
        "surface": str(source_row["surface"]),
        "target_side": target_side,
        "target_value": str(target_value),
        "cell_key": str(source_row["cell_key"]),
        "n_context_key": str(source_row["n_context_key"]),
        "n_previous": str(source_row["n_previous"]),
        "n_containing": str(source_row["n_containing"]),
        "n_following": str(source_row["n_following"]),
        "prime_start": None,
        "prime_left_index": None,
        "prime_pair_offset": None,
        "prime_pair_offset_group": None,
        "case_direction_class": row_direction_class(source_row),
        "target_direction_class": target_direction_class(source_row, target_side),
        "outward_lag3": states["outward_lag3"],
        "outward_lag2": states["outward_lag2"],
        "outward_lag1": states["outward_lag1"],
        "inward_lag1": states["inward_lag1"],
        "inward_lag2": states["inward_lag2"],
        "inward_lag3": states["inward_lag3"],
        "outward_class_signature": "|".join(
            [state_class(states["outward_lag2"]), state_class(states["outward_lag1"])]
        ),
        "inward_class_signature": "|".join(
            [state_class(states["inward_lag1"]), state_class(states["inward_lag2"])]
        ),
        "lag2_class_signature": "|".join(
            [state_class(states["outward_lag2"]), state_class(states["inward_lag2"])]
        ),
        "lag2_reduced_signature": "|".join(
            [states["outward_lag2"], states["inward_lag2"]]
        ),
        "lag3_class_signature": "|".join(
            [state_class(states["outward_lag3"]), state_class(states["inward_lag3"])]
        ),
        "lag3_reduced_signature": "|".join(
            [states["outward_lag3"], states["inward_lag3"]]
        ),
        "lag23_reduced_signature": "|".join(
            [
                states["outward_lag3"],
                states["outward_lag2"],
                states["inward_lag2"],
                states["inward_lag3"],
            ]
        ),
        "recursive_reduced_signature": "|".join(
            [
                states["outward_lag3"],
                states["outward_lag2"],
                states["outward_lag1"],
                states["inward_lag1"],
                states["inward_lag2"],
                states["inward_lag3"],
            ]
        ),
        "recursive_class_signature": "|".join(
            [
                state_class(states["outward_lag3"]),
                state_class(states["outward_lag2"]),
                state_class(states["outward_lag1"]),
                state_class(states["inward_lag1"]),
                state_class(states["inward_lag2"]),
                state_class(states["inward_lag3"]),
            ]
        ),
    }
    row.update(exact)
    row.update(widths)
    return row


def measured_recursive_target_row(
    row: dict[str, object],
    target_side: str,
    target_value: int,
) -> dict[str, object]:
    """Return one recursive target row with the coordinate-appropriate exact backend."""
    if target_value > INT64_MAX:
        return recursive_target_row_large(row, target_side, target_value)
    return recursive_target_row(row, target_side, target_value)


def solved_rows(
    compatibility_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
    solved_surface: str,
) -> list[dict[str, object]]:
    """Return recursive target rows for the solved compatibility surface."""
    values = target_value_index(target_rows)
    output: list[dict[str, object]] = []
    for row in compatibility_rows:
        if str(row["surface"]) != solved_surface:
            continue
        enriched = with_cell_key(row)
        for target_side in ("p", "q"):
            key = (str(row["case_id"]), target_side)
            if key not in values:
                raise ValueError(f"missing target value for {key}")
            output.append(measured_recursive_target_row(enriched, target_side, values[key]))
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
    solved_surface: str,
) -> dict[str, object]:
    """Return compact solved-vs-expanded recursive comparison summary."""
    payload = recursive_summary(solved, grouped_rows)
    payload["rule_id"] = RULE_ID
    payload["solved_surface"] = solved_surface
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
    parser.add_argument(
        "--solved-surface",
        default=SOLVED_SURFACE,
        help="Compatibility-row surface to treat as solved measurement rows.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run solved-surface recursive grammar comparison."""
    args = parse_args(argv)
    solved = solved_rows(
        read_jsonl(args.compatibility_rows),
        read_jsonl(args.target_rows),
        args.solved_surface,
    )
    expanded = read_jsonl(args.expanded_recursive_rows)
    features = (
        "cell_key+target_side+lag2_reduced_signature",
        "cell_key+target_side+lag2_reduced_signature+lag3_reduced_signature",
        "cell_key+target_side+lag23_reduced_signature",
    )
    grouped_rows = split_rows(solved, features)
    comparison_rows = compare_signatures(solved, expanded)
    payload = comparison_summary(
        solved,
        expanded,
        comparison_rows,
        grouped_rows,
        args.solved_surface,
    )
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
